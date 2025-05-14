import socket
from config.config import Config

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
            return data, addr
        except socket.error as e:
            print("Socket error: " + str(e))
            return None, None
        
    def sendResponse(self, data, addr):
        try:
            self.sock.sendto(data, addr)
        except socket.error as e:
            print("Socket error: " + str(e))