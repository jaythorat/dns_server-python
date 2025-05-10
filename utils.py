from dnslib import *
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE,CLASS


class DNSMessageHandler:
    def __init__(self,dnsMsg):
        self.dnsMsg = dnsMsg
        self.parsedMsg = None
        self.dnsResp = None
        self.packedDNSResp = None
        self.dnsRecordTypes = {
            "1": "A",
            "5": "CNAME",
            "16": "TXT",
            "28": "AAAA",
            "15": "MX",
            "255": "ANY"
        }
    
    def dnsReqMsgParse(self) :
        self.parsedMsg =  DNSRecord.parse(self.dnsMsg)
        return self
    
    def getQueryDomain(self):
        # Returns the domain name from the parsed message
        return str(self.parsedMsg.q.qname)
    
    def getQueryType(self):
        # Returns the query type from the parsed message
        return str(self.parsedMsg.q.qtype)
    
    def isQueryTypeValid(self):
        # Check if the query type is valid
        if str(self.parsedMsg.q.qtype) in self.dnsRecordTypes:
            return True
        else:
            return False
        
    def getQueryTypeName(self):
        # Returns the query type name from the parsed message
        return self.dnsRecordTypes.get(str(self.parsedMsg.q.qtype), "Unknown")
    
    
    def createNXDomainRespMsg(self):
        qname = str(self.parsedMsg.q.qname)
        qClass = self.parsedMsg.q.qclass
        ttl = 0
        qType = self.parsedMsg.q.qtype
        self.dnsResp =  DNSRecord(DNSHeader(id = self.parsedMsg.header.id,qr=1,aa=0,ra=1,rcode = RCODE.NXDOMAIN),
                )
        return self



    def createDNSRespMsg(self,value): 
        qname = str(self.parsedMsg.q.qname)
        qClass = self.parsedMsg.q.qclass
        ttl = 0
        qType = self.parsedMsg.q.qtype
        
        if self.getQueryTypeName() == "CNAME":
            rdata = CNAME(value)
        elif self.getQueryTypeName() == "A":
            rdata = A(value)


        self.dnsResp =  DNSRecord(DNSHeader(id = self.parsedMsg.header.id,qr=1,aa=0,ra=1),
                q=DNSQuestion(qname=qname,qtype=qType,qclass=qClass),
                a=RR(str(qname),rtype=qType,rclass=qClass,ttl=ttl,
                    rdata=rdata,))
        return self

    def packDNSRespMsg(self):
        self.packedDNSResp = self.dnsResp.pack()
        return self
    
    def getPackedResponse(self):
        return self.packedDNSResp