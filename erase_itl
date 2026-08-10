import sys
import time
import requests
from requests.auth import HTTPBasicAuth

def main():
    # 1. Komut satırı argümanlarını al
    if len(sys.argv) < 4:
        print("Kullanım: python itldel.py <ip_dosyasi> <kullanici_adi> <sifre>")
        sys.exit(1)

    which_file = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]

    # 2. Telefon modelini ve versiyon bilgisini al
    phone_type = input("Enter Phone Type (69xx, 78xx, 7911, 794x/796x, 797x, 8841/8861, 8831, 8941, 8945, 8961, 99xx): ").strip()

    load = "0"
    if phone_type == '69xx':
        load = input('Phone Load 9.3.3+ (1 for yes, 0 for no)? ').strip()
    elif phone_type == '8945':
        load = input('8945 Phone Load 9.3.4+ (1 for yes, 0 for no)? ').strip()

    # 3. IP listesi dosyasını oku
    try:
        with open(which_file, 'r') as f:
            raw_data = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Dosya açılamadı: {e}")
        sys.exit(1)

    # 4. Modele göre ilgili fonksiyonu çağır
    if phone_type == '69xx':
        print("Deleting ITL from 69xx Phone")
        post_xml_69xx(raw_data, user, password, load)
    elif phone_type == '78xx':
        print("Deleting ITL from 78xx Phone")
        post_xml_78(raw_data, user, password)
    elif phone_type == '7911':
        print("Deleting ITL from 7911 Phone")
        post_xml_7911(raw_data, user, password)
    elif phone_type == '794x/796x':
        print("Deleting ITL from 794x/796x Phone")
        post_xml_796(raw_data, user, password)
    elif phone_type == '797x':
        print("Deleting ITL from 797x Phone")
        post_xml_797(raw_data, user, password)
    elif phone_type == '8841/8861':
        print("Deleting ITL from 8841/8861 Phone")
        post_xml_88xx(raw_data, user, password)
    elif phone_type == '8831':
        print("Deleting ITL from 8831 Phone")
        post_xml_8831(raw_data, user, password)
    elif phone_type == '8941':
        print("Deleting ITL from 8941 Phone")
        post_xml_8941(raw_data, user, password)
    elif phone_type == '8945' and load == '0':
        print("This tool isn't supported on a version lower than 9.3.4-17")
    elif phone_type == '8945' and load == '1':
        print("Deleting ITL from 8945 Phone")
        post_xml_8945_plus(raw_data, user, password)
    elif phone_type in ['8961', '99xx']:
        print(f"Deleting ITL from {phone_type} Phone")
        post_xml_99(raw_data, user, password)
    else:
        print("Geçersiz telefon modeli seçildi.")

def send_xml_command(ip, user, password, key_name, delay=0):
    """Telefona XML komutu gönderen yardımcı fonksiyon"""
    url = f"http://{ip}/CGI/Execute"
    xml_data = f'XML=<CiscoIPPhoneExecute><ExecuteItem URL="{key_name}"/></CiscoIPPhoneExecute>'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    try:
        response = requests.post(
            url, 
            data=xml_data, 
            auth=HTTPBasicAuth(user, password), 
            headers=headers,
            timeout=10
        )
        if response.status_code == 200:
            print(f"Success: {key_name}")
            if delay > 0:
                time.sleep(delay)
            return True
        else:
            print(f"Hata ({response.status_code}): {response.reason}", file=sys.stderr)
            return False
    except Exception as e:
        print(f"Bağlantı hatası [{ip}]: {e}", file=sys.stderr)
        return False

# Model özelindeki fonksiyonlar

def post_xml_78(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Settings", 1)
        send_xml_command(ip, user, password, "Key:KeyPad5", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:Soft4", 1)
        send_xml_command(ip, user, password, "Key:Soft2", 1)
        send_xml_command(ip, user, password, "Key:Soft1", 1)
        send_xml_command(ip, user, password, "Key:Soft1", 1)
        send_xml_command(ip, user, password, "Key:Soft1", 1)
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_88xx(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Applications", 1)
        send_xml_command(ip, user, password, "Key:KeyPad6", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:Soft3", 2)
        send_xml_command(ip, user, password, "Key:Soft1", 0)
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_69xx(raw_data, user, password, load):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Settings", 0)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        if load == '1':
            send_xml_command(ip, user, password, "Key:KeyPad5", 1)
        send_xml_command(ip, user, password, "Key:Soft4", 1)
        send_xml_command(ip, user, password, "Key:Soft2", 1)
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_7911(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Applications")
        send_xml_command(ip, user, password, "Key:KeyPad3")
        send_xml_command(ip, user, password, "Key:KeyPad4")
        send_xml_command(ip, user, password, "Key:KeyPad5")
        send_xml_command(ip, user, password, "Key:KeyPad2")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadPound", 4)
        send_xml_command(ip, user, password, "Key:Soft4", 1)
        send_xml_command(ip, user, password, "Key:Soft2")
        send_xml_command(ip, user, password, "Key:Soft3")
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_796(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Settings")
        send_xml_command(ip, user, password, "Key:KeyPad4")
        send_xml_command(ip, user, password, "Key:KeyPad4")
        send_xml_command(ip, user, password, "Key:KeyPad5")
        send_xml_command(ip, user, password, "Key:KeyPad2")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadPound", 4)
        send_xml_command(ip, user, password, "Key:Soft4", 1)
        send_xml_command(ip, user, password, "Key:Soft2")
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_797(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Settings")
        send_xml_command(ip, user, password, "Key:KeyPad4")
        send_xml_command(ip, user, password, "Key:KeyPad4")
        send_xml_command(ip, user, password, "Key:KeyPad5")
        send_xml_command(ip, user, password, "Key:KeyPad2")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadStar")
        send_xml_command(ip, user, password, "Key:KeyPadPound", 4)
        send_xml_command(ip, user, password, "Key:Soft5")
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_8831(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Soft3", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:Soft4", 1)
        send_xml_command(ip, user, password, "Key:Soft2", 1)
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_8941(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Applications", 1)
        send_xml_command(ip, user, password, "Key:KeyPad3", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:KeyPad3", 1)
        send_xml_command(ip, user, password, "Key:Soft3", 2)
        send_xml_command(ip, user, password, "Key:Soft1")
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_8945_plus(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Applications", 2)
        send_xml_command(ip, user, password, "Key:KeyPad4", 2)
        send_xml_command(ip, user, password, "Key:KeyPad4", 2)
        send_xml_command(ip, user, password, "Key:KeyPad3", 2)
        send_xml_command(ip, user, password, "Key:Soft3", 3)
        send_xml_command(ip, user, password, "Key:Soft1")
        print("\n*************************\nDone. Please verify on the phone!\n")

def post_xml_99(raw_data, user, password):
    for ip in raw_data:
        print(f"\nDeleting ITL file on {ip}")
        send_xml_command(ip, user, password, "Key:Applications", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:KeyPad4", 1)
        send_xml_command(ip, user, password, "Key:Soft3", 2)
        send_xml_command(ip, user, password, "Key:Soft1")
        print("\n*************************\nDone. Please verify on the phone!\n")

if __name__ == '__main__':
    main()
