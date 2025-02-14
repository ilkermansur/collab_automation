M = {}
function M.inbound_INVITE(msg)
if msg:isInitialInviteRequest() then
local rpid=msg:getHeader("Remote-Party-ID")
local rest=string.match(rpid, "(<.+)")
local pstn= "CCIE Collab"
local final=pstn .. rest
msg:modifyHeader("Remote-Party-ID", final)
end
end
return M
