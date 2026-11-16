from requests import Session
from zeep import Client
from zeep.transports import Transport
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from zeep.cache import SqliteCache
from zeep.plugins import HistoryPlugin
from zeep.exceptions import Fault
from zeep.helpers import serialize_object
from lxml import etree
from requests.auth import HTTPBasicAuth

disable_warnings(InsecureRequestWarning)

username = 'axluser'
password = '1Qaz2Wsx'
fqdn = '198.18.133.3'
address = 'https://{}:8443/axl/'.format(fqdn)
wsdl = 'AXLAPI.wsdl'
binding = "{http://www.cisco.com/AXLAPIService/}AXLAPIBinding"

session = Session()
session.verify = False
session.auth = HTTPBasicAuth(username, password)
transport = Transport(cache=SqliteCache(), session=session, timeout=20)
history = HistoryPlugin()
client = Client(wsdl=wsdl, transport=transport, plugins=[history])
axl = client.create_service(binding, address)


def parse_elements(type_obj, depth=1, max_depth=5, visited=None):
    if visited is None:
        visited = set()

    mandatory = []
    optional = []

    if not hasattr(type_obj, 'elements'):
        return mandatory, optional

    # Prevent infinite recursion on self-referencing types
    type_name = getattr(type_obj, 'name', None)
    if type_name and type_name in visited:
        return mandatory, optional

    new_visited = set(visited)
    if type_name:
        new_visited.add(type_name)

    for name, element in type_obj.elements:
        el_type = element.type
        el_type_name = el_type.name if el_type else 'string'
        is_mandatory = getattr(element, 'min_occurs', 1) >= 1

        # Check whether the element expects a list or a single item
        max_occ = getattr(element, 'max_occurs', 1)
        is_list = (max_occ == 'unbounded') or (isinstance(max_occ, int) and max_occ > 1)
        list_tag = " [LIST -> {...}, {...}]" if is_list else ""

        # XFkType (Foreign Key) fields in CUCM accept a plain string name (hide _value_1 clutter)
        if el_type_name == 'XFkType':
            line = f"{name} (String Name){list_tag}"
            sub_mandatory, sub_optional = [], []
        else:
            line = f"{name} ({el_type_name}){list_tag}"
            if depth < max_depth and hasattr(el_type, 'elements'):
                sub_mandatory, sub_optional = parse_elements(
                    el_type, depth + 1, max_depth, new_visited
                )
            else:
                sub_mandatory, sub_optional = [], []

        record = {
            'header': line,
            'name': name,
            'sub_mandatory': sub_mandatory,
            'sub_optional': sub_optional,
            'is_dict': (el_type_name != 'XFkType' and hasattr(el_type, 'elements'))
        }

        if is_mandatory:
            mandatory.append(record)
        else:
            optional.append(record)

    return mandatory, optional


def print_tree(record_list, indent="  ", mandatory_subfields_only=False):
    for record in record_list:
        print(f"{indent}├── {record['header']}")

        if record['sub_mandatory']:
            print(f"{indent}│   [Mandatory Sub-fields]:")
            print_tree(record['sub_mandatory'], indent + "│     ", mandatory_subfields_only)

        if record['sub_optional'] and not mandatory_subfields_only:
            print(f"{indent}│   [Optional Sub-fields]:")
            print_tree(record['sub_optional'], indent + "│     ", mandatory_subfields_only)


def show_usage(method_name, max_depth=4, show_optional_subfields=True):
    op = axl._binding._operations.get(method_name)

    if not op:
        similar = [m for m in dir(axl) if method_name.lower() in m.lower()]
        print(f"'{method_name}' not found. Similar methods: {similar}")
        return

    print("=" * 65)
    print(f"METHOD: axl.{method_name}()")
    print("=" * 65)

    if not (op.input and op.input.body and op.input.body.type):
        print("Takes no parameters.\nExample:\n  axl." + method_name + "()")
        return

    mandatory, optional = parse_elements(op.input.body.type, max_depth=max_depth)

    # Detect key selection (e.g., userid/uuid or name/uuid) in get*, update*, remove* methods
    choice_group = []
    if method_name.startswith(('get', 'update', 'remove', 'apply', 'reset')):
        remaining_optional = []
        for item in optional:
            if item['name'] in ['uuid', 'userid', 'name', 'pattern']:
                choice_group.append(item)
            else:
                remaining_optional.append(item)
        optional = remaining_optional

    # 1. MANDATORY PARAMETERS SECTION
    print("\n[1] MANDATORY PARAMETERS:")
    if not mandatory and not choice_group:
        print("  (None)")
    if choice_group:
        names = " OR ".join([x['name'] for x in choice_group])
        print(f"  * ONE REQUIRED: {names}")
    if mandatory:
        print_tree(mandatory, indent="  ", mandatory_subfields_only=not show_optional_subfields)

    # 2. OPTIONAL PARAMETERS SECTION
    print("\n[2] OPTIONAL PARAMETERS:")
    if not optional:
        print("  (None)")
    else:
        print_tree(optional, indent="  ", mandatory_subfields_only=not show_optional_subfields)

    # 3. SAMPLE PYTHON CALL TEMPLATE
    print("\n[3] SAMPLE PYTHON CALL TEMPLATE:")
    args = []
    if choice_group:
        args.append(f"    {choice_group[0]['name']}='...'")
    for m in mandatory:
        if m['is_dict']:
            args.append(f"    {m['name']}={{...}}")
        else:
            args.append(f"    {m['name']}='...'")
    if method_name.startswith('list'):
        args.append("    searchCriteria={'...': '%'}")
        args.append("    returnedTags={'...': ''}")

    if args:
        print(f"result = axl.{method_name}(")
        print(",\n".join(args))
        print(")")
    else:
        print(f"result = axl.{method_name}()")
    print("=" * 65 + "\n")


show_usage(method_name='updateUser')
