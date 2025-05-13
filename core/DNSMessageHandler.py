from dnslib import *
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE
from DB.fetchDNSRecords import FetchDNSRecords
from config import Config


class DNSMessageHandler:
    def __init__(self,dnsMsg):
        self.config = Config()
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

    def fetchDomainDNSRecords(self):
        return FetchDNSRecords(self.getQueryDomain()).fetchRecords()
        
    def createResponseDNSRecord(self,rcode,rdata,ttl,aa=1): 
        ra = 0 # 1 Recursion Available 0 for not available 
        qname = str(self.parsedMsg.q.qname)
        qtype = self.parsedMsg.q.qtype
        qclass = self.parsedMsg.q.qclass
        dnsHeader = DNSHeader(id = self.parsedMsg.header.id,qr=1,aa=aa,ra=ra,rcode = rcode)
        dnsQuestion = DNSQuestion(qname=qname,qtype=qtype,qclass=qclass)
        dnsAnswer = None
        if rcode == RCODE.NOERROR and rdata is not None:
            dnsAnswer = RR(str(qname),rtype=qtype,rclass=qclass,ttl=ttl,
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
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,A(value[1]),0)
    
    def RR_CNAME(self,value):
        if not value or not isinstance(value, list):
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,None,0)
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,CNAME(value[1]),0)

    def createDNSRespMsg(self):
        if self.getQueryTypeName() not in self.config.getSupportedRRTypes():         
            self.notImplemented()
            return

        value = self.fetchDomainDNSRecords()
        if not value:
            self.nxDomain()
            return
        elif self.getQueryTypeName() == "A":
            self.RR_A(value.get("A"))
            return
        elif self.getQueryTypeName() == "CNAME":
            self.RR_CNAME(value.get("CNAME"))
            return
        
    def getDNSRespMsg(self):
        if self.dnsResp is None:
            self.serverFailure()
        self.packedDNSResp = self.dnsResp.pack()
        return self.packedDNSResp
