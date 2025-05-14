from dnslib import *
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE
from DB.fetchDNSRecords import FetchDNSRecords
from config.config import Config
from core.upstreamResolver import UpstreamResolver
from suport.domainParser import DomainParser

upstreamResolver = UpstreamResolver()

class DNSMessageHandler:
    def __init__(self,dnsMsg):
        self.config = Config()
        self.upstreamResolver = UpstreamResolver()
        self.dnsMsg = dnsMsg
        self.parsedMsg = self.dnsReqMsgParse()
        self.dnsResp = None
        self.packedDNSResp = None
        self.DNSRecordTypes = QTYPE.forward   
    
    def dnsReqMsgParse(self) :
        return DNSRecord.parse(self.dnsMsg)
    
    def getQueryDomain(self):
        return str(self.parsedMsg.q.qname)
    
    def getQueryType(self):
        return str(self.parsedMsg.q.qtype)
    
    def getQueryTypeName(self):
        return self.DNSRecordTypes.get(self.parsedMsg.q.qtype)
    
    def isQueryTypeValid(self):
        if str(self.parsedMsg.q.qtype) in self.DNSRecordTypes:
            return True
        else:
            return False
    
    def isAuthoritative(self):
        domain = self.getQueryDomain()
        if domain.endswith("." + self.config.getAuthTLD()) or domain.endswith("." + self.config.getAuthTLD() + "."):
            return True
        else:
            return False


    def fetchDomainDNSRecords(self):
        domain = DomainParser(self.getQueryDomain()).extractDomain()
        return FetchDNSRecords(domain).fetchRecords()
        
    def createResponseDNSRecord(self,rcode,rdata,ttl,atype = None,aa=1): 
        ra = 0 # 1 Recursion Available 0 for not available 
        qname = str(self.parsedMsg.q.qname)
        qclass = self.parsedMsg.q.qclass
        dnsHeader = DNSHeader(id = self.parsedMsg.header.id,qr=1,aa=aa,ra=ra,rcode = rcode)
        dnsQuestion = DNSQuestion(qname=qname,qtype=self.parsedMsg.q.qtype,qclass=qclass)
        dnsAnswer = None
        if rcode == RCODE.NOERROR and rdata is not None and atype is not None:
            dnsAnswer = RR(str(qname),rtype=atype,rclass=qclass,ttl=ttl,
                    rdata=rdata,)
        dnsRecord = DNSRecord(dnsHeader,
                q=dnsQuestion ,
                a=dnsAnswer)
        return dnsRecord
    
    def notImplemented(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOTIMP,None,0)
    
    def nxDomain(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NXDOMAIN,None,0)
    
    def serverFailure(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.SERVFAIL,None,0)
    
    def RR_A(self,value):
        if not value or not isinstance(value, list):
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,None,0)
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,A(value[1]),0,QTYPE.A)
    
    def RR_CNAME(self,value):
        if not value or not isinstance(value, list):
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,None,0)
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,CNAME(value[1]),0,QTYPE.CNAME)


    def dnsRecordValue(self):
        # if req for A -- return a if present or else return c else nxdomain
        # if req for CNAME -- return c if present or else return nxdomi 
        # if req for NS -- return ns if present or else return nxdomain
        pass  

    def getRespUpstream(self):   
        upstreamResp = self.upstreamResolver.sendQuery(self.dnsMsg)
        if not upstreamResp:
            self.serverFailure()
            return None
        self.packedDNSResp = upstreamResp
        self.dnsResp = True  #TODO: Temp bypass fix later
        return True

    def createDNSRespMsg(self):
        print("For :",self.getQueryDomain())
        if not self.isAuthoritative() and not self.getRespUpstream():
                return None
        
        if self.getQueryTypeName() not in self.config.getSupportedRRTypes():         
            self.notImplemented()
            return

        value = self.fetchDomainDNSRecords()
        if not value:
            self.nxDomain()
            return
        
        dp = DomainParser(self.getQueryDomain()).handleFQDN()
        if not dp:
            self.nxDomain()
            return
        value = value.get(dp)
        if self.getQueryTypeName() == "A":
            if value[0] == "A":
                self.RR_A(value)
            elif value[0] == "CNAME":
                print("Technically CNAME")
                self.RR_CNAME(value)
            else:
                self.nxDomain()
            return
        elif self.getQueryTypeName() == "CNAME":
            if value[0] == "CNAME":
                self.RR_CNAME(value)
            else:
                self.nxDomain()
            return
        
    def getDNSRespMsg(self):
        if self.dnsResp is None:
            self.serverFailure()
        elif hasattr(self.dnsResp, "pack"):
            self.packedDNSResp = self.dnsResp.pack()
        return self.packedDNSResp