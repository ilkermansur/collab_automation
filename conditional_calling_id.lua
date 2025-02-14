M = {}
function M.inbound_INVITE(msg)
    if msg:isInitialInviteRequest() then
        local rpid = msg:getHeader("Remote-Party-ID")
        -- Eğer Remote-Party-ID header'ı 5442084497 içeriyorsa:
        if rpid and string.find(rpid, "5442084497") then
            local rest = string.match(rpid, "(<.+)")
            local pstn = "CCIE Collab"
            local final = pstn .. rest
            msg:modifyHeader("Remote-Party-ID", final)
        end
    end
end
return M
