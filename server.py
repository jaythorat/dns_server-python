
from core.DNSMessageHandler import DNSMessageHandler
from DB.fetchDNSRecords import FetchDNSRecords
from core.DNSServer import DNSServer

server = DNSServer()
server.start()

while True:
    data,addr = server.getRequest()
    msgHandler = DNSMessageHandler(data)
    msgHandler.createDNSRespMsg()
    response = msgHandler.getDNSRespMsg()
    server.sendResponse(response, addr)
 