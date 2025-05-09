class Config:
    def __init__(self):
        self.host = "localhost"
        self.port = 53
        self.bufferSize = 512

    def getHost(self):
        return self.host
    
    def getPort(self):
        return self.port
    
    def getBufferSize(self):
        return self.bufferSize