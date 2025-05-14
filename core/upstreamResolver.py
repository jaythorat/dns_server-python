import socket
from config.config import Config

class UpstreamResolver:

    def __init__(self):
        self.config = Config()
        self.upstreamHost = self.config.getGoogleDNShost()
        self.upstreamPort = self.config.getGoogleDNSport()
        self.upstreamDNS = (self.upstreamHost, self.upstreamPort)
        self.bufferSize = self.config.getBufferSize()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5)

    def sendQuery(self, data):
        self.sock.sendto(data, self.upstreamDNS)
        response_data, _ = self.sock.recvfrom(512)
        return response_data
