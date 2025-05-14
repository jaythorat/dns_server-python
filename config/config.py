class Config:
    def __init__(self):
        self.maxWorkers = 10
        self.host = "0.0.0.0"
        self.port = 53
        self.bufferSize = 512
        self.supporterdRRTypes = ["A","CNAME"]
        self.googleDNShost = "1.1.1.1"
        self.gooogleDNSport = 53
        self.googleUpstreamTimeout = 10
        self.authTLD = "ks"


    def getMaxWorkers(self):
        return self.maxWorkers
    
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
    
    def getGoogleUpstreamTimeout(self):
        return self.googleUpstreamTimeout
    