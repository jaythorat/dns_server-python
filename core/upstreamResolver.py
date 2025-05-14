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
        self.sock.settimeout(self.config.getGoogleUpstreamTimeout())

    def sendQuery(self, data):
        try:
            self.sock.sendto(data, self.upstreamDNS)
            response_data, _ = self.sock.recvfrom(512)
            return response_data
        except socket.timeout:
            print("Upstream DNS query timed out.")
            return None
        except Exception as e:
            print(f"Error occured Upstream Server : {e}")
            return None
