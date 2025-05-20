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
        self.authTLD = "websculptors.in"
        self.sqlHost = "65.1.71.40"
        self.sqlPort = "3306"
        self.sqlUser = "root"
        self.sqlPassword = "Qwerty@123"
        self.sqlDatabase = "DomainManager"
        self.connectionPoolSize = 2


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
    
    def getSqlHost(self):
        return self.sqlHost
    def getSqlPort(self):
        return self.sqlPort
    def getSqlUser(self):
        return self.sqlUser
    def getSqlPassword(self):
        return self.sqlPassword
    def getSqlDatabase(self):
        return self.sqlDatabase
    def getConnectionPoolSize(self):
        return self.connectionPoolSize
