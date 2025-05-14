from concurrent.futures import ThreadPoolExecutor
from core.DNSMessageHandler import DNSMessageHandler
from core.DNSServer import DNSServer

def handle_request(data, addr, server):
    msgHandler = DNSMessageHandler(data)
    msgHandler.createDNSRespMsg()
    response = msgHandler.getDNSRespMsg()
    server.sendResponse(response, addr)

server = DNSServer()
server.start()

with ThreadPoolExecutor(max_workers=10000) as executor:
    while True:
        data, addr = server.getRequest()
        executor.submit(handle_request, data, addr, server)