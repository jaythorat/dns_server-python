class Config:
    def __init__(self):
        self.host = "localhost"
        self.port = 53
        self.bufferSize = 512
        self.supporterdRRTypes = ["A","CNAME"]
        self.googleDNShost = "8.8.8.8"
        self.gooogleDNSport = 53
        self.authTLD = "ks"

    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getBufferSize(self):
        return self.bufferSize
    
    def getSupportedRRTypes(self):
        return self.supporterdRRTypes
    
    def getGoogleDNShost(self):
        return self.googleDNShost
    
    def getGoogleDNSport(self):
        return self.gooogleDNSport
    
    def getAuthTLD(self):
        return self.authTLD
    