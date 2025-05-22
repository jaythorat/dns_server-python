class Config:
    def __init__(self):
        self.maxWorkers = 10
        self.host = "0.0.0.0"
        self.port = 53
        self.bufferSize = 512
        self.supporterdRRTypes = ["A","CNAME","CAA","NS","SOA"]
        self.googleDNShost = "1.1.1.1"
        self.gooogleDNSport = 53
        self.googleUpstreamTimeout = 10
        self.authTLD = "websculptors.in"
        self.rootLevelDomains = [
            "websculptors.in",
            "ns1.websculptors.in",
            "ns2.websculptors.in",
            "ns3.websculptors.in",
            "ns4.websculptors.in",
            "mx1.websculptors.in",
            "mx2.websculptors.in",
            "mail.websculptors.in",
        ]
        self.rootLevelDomainUUID = "4b946db8-34d7-11f0-bd70-edfd2de8055d"
        self.sqlHost = "65.1.71.40"
        self.sqlPort = "3306"
        self.sqlUser = "root"
        self.sqlPassword = "Qwerty@123"
        self.sqlDatabase = "DomainManager"
        self.connectionPoolSize = 1
        self.nsHosts = [
            "ns3.websculptors.in.",
            "ns4.websculptors.in."
        ]
        self.registrarEmail = "contact.websculptors.in"
        self.registrarName = "Web Sculptors"

    def getRootLevelDomains(self):
        return self.rootLevelDomains
    
    def getRootLevelDomainUUID(self):
        return self.rootLevelDomainUUID

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
    
    def getNSHosts(self):
        return self.nsHosts
    
    def getRegistrarEmail(self):
        return self.registrarEmail
    
    def getRegistrarName(self):
        return self.registrarName
