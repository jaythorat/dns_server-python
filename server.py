from concurrent.futures import ThreadPoolExecutor
from core.DNSMessageHandler import DNSMessageHandler
from core.DNSServer import DNSServer
from config.config import Config

server = DNSServer()
server.start()


def handleRequest(data, addr, server):
    msgHandler = DNSMessageHandler(data)
    msgHandler.handleQuery()
    response = msgHandler.getResponse()
    server.sendResponse(response, addr)

with ThreadPoolExecutor(max_workers=Config().getMaxWorkers()) as executor:
    while True:
        data, addr = server.getRequest()
        executor.submit(handleRequest, data, addr, server)