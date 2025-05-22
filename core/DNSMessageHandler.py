from DB.fetchDNSRecords import FetchDNSRecords
from config.config import Config
from core.support.domainParser import DomainParser
from core.support.DNSParser import DNSParser
from core.support.DNSRespBuilder import DNSResponseBuilder
        

class DNSMessageHandler:
    def __init__(self,dnsMsg):
        self.config = Config()
        self.respBuilder = DNSResponseBuilder(dnsMsg)
        self.dnsParser = DNSParser(dnsMsg)
        self.domainParser = DomainParser(self.dnsParser.getQueryDomain())
        self.queryDomainName = self.domainParser.handleFQDN().lower()
        self.qtype = self.dnsParser.getQueryTypeName()
        self.extractedDomain = self.domainParser.extractDomain()
        self.dnsMsg = dnsMsg 
    
    def isAuthoritative(self):
        if (self.queryDomainName.endswith(self.config.getAuthTLD()) or 
            self.queryDomainName.endswith("." + self.config.getAuthTLD())):
            return True
        else:
            return False

    def fetchDomainDNSRecords(self):
        return FetchDNSRecords(self.extractedDomain).fetchRecords()

    def __isSupportedRRType__(self):
        if self.dnsParser.getQueryTypeName() not in self.config.getSupportedRRTypes():
            return False
        return True
    
    def generateResponse(self):
        if self.qtype == "NS":
            self.respBuilder.RR_NS()
            return True
        elif self.qtype == "SOA":
            self.respBuilder.RR_SOA()
            return True
        elif self.qtype == "CAA":
            self.respBuilder.RR_CAA()
            return True
        
        domainDetails = FetchDNSRecords.getDomainDetails(self.extractedDomain)
        if not domainDetails or not domainDetails[0]:
            
            if self.extractedDomain in self.config.getRootLevelDomains():
                domainDetails = [{"domainUUID":self.config.getRootLevelDomainUUID()}]
            else:
                self.respBuilder.nxDomain()
                return False
        
            
        allDNSRecords = FetchDNSRecords.fetchAllRecords(domainDetails[0]["domainUUID"])
        if self.qtype == "A":
            self.respBuilder.RR_A(allDNSRecords)
        elif self.qtype == "CNAME":
            self.respBuilder.RR_CNAME(allDNSRecords)
        else:
            return False
        return True


    def handleQuery(self):
        print("Domain:", self.queryDomainName, "Query Type:", self.qtype)
        if not self.isAuthoritative() and not self.respBuilder.upstreamResp():
            print("Not Authoritative and Upstream DNS not responding",self.queryDomainName)
            return None
        
        if not self.__isSupportedRRType__():
            self.respBuilder.notImplemented()      
            return
        
        if not self.generateResponse():
            if not self.respBuilder.dnsResp:
                self.respBuilder.notImplemented()  
            return
        
    def getResponse(self): 
        return self.respBuilder.packResponse()