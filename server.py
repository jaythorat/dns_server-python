import socket
from utils import DNSMessageHandler
from config import Config



class DNSServer:
    def __init__(self):
        self.config = Config()
        self.host = self.config.getHost()
        self.port = self.config.getPort()
        self.bufferSize = self.config.getBufferSize()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self): 
        server = (self.host, self.port)
        self.sock.bind(server)
        print("Listening on " + self.host + ":" + str(self.port))

    def stop(self):
        self.sock.close()
        print("Server stopped.")

    def getRequest(self):
        try:
            data, addr = self.sock.recvfrom(self.bufferSize)
            print("Received data from " + str(addr))
            return data, addr
        except socket.error as e:
            print("Socket error: " + str(e))
            return None, None
        
    def sendResponse(self, data, addr):
        try:
            self.sock.sendto(data, addr)
            print("Sent response to " + str(addr))
        except socket.error as e:
            print("Socket error: " + str(e))

server = DNSServer()
server.start()


while True:
    data,addr = server.getRequest()
    msgHandler = DNSMessageHandler(data)
    msgHandler.dnsReqMsgParse().createDNSRespMsg("11.11.11.11").packDNSRespMsg()
    response = msgHandler.getPackedResponse()
    server.sendResponse(response, addr)
 
