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
        self.dnsMsg = dnsMsg   
    
    def isAuthoritative(self):
        domain = self.dnsParser.getQueryDomain()
        if domain.endswith("." + self.config.getAuthTLD()) or domain.endswith("." + self.config.getAuthTLD() + "."):
            return True
        else:
            return False

    def fetchDomainDNSRecords(self):
        domain = self.domainParser.extractDomain()
        return FetchDNSRecords(domain).fetchRecords()
    
    def __handleARecord__(self,dnsRecord):
        if dnsRecord["recordType"] == "A":
            self.respBuilder.RR_A(dnsRecord)
        elif dnsRecord["recordType"] == "CNAME":
            self.respBuilder.RR_CNAME(dnsRecord)
        else:
            self.respBuilder.emptyResponse()

    def __handleCNAMERecord__(self,dnsRecord):
        if dnsRecord["recordType"] == "CNAME":
            self.respBuilder.RR_CNAME(dnsRecord)
        else:
            self.respBuilder.emptyResponse()

    def __isSupportedRRType__(self):
        if self.dnsParser.getQueryTypeName() not in self.config.getSupportedRRTypes():
            return False
        return True

    def handleQuery(self):
        if not self.isAuthoritative() and not self.respBuilder.upstreamResp():
            return None
        if not self.__isSupportedRRType__():         
            self.respBuilder.notImplemented()
            return
        cleanedDomain = self.domainParser.handleFQDN()
        particularDNSRecord = FetchDNSRecords.fetchParticularRecord(cleanedDomain)
        print(particularDNSRecord)
        if not particularDNSRecord or not particularDNSRecord[0]:
            self.respBuilder.emptyResponse()
            return
        if self.dnsParser.getQueryTypeName() == "A":
            self.__handleARecord__(particularDNSRecord[0])
            return
        elif self.dnsParser.getQueryTypeName() == "CNAME":
            self.__handleCNAMERecord__(particularDNSRecord[0])
            return
        
    def getResponse(self): 
        return self.respBuilder.packResponse()