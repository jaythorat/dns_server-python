from dnslib import *
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A


class DNSMessageHandler:
    def __init__(self,dnsMsg):
        self.dnsMsg = dnsMsg
        self.parsedMsg = None
        self.dnsResp = None
        self.packedDNSResp = None
    
    def dnsReqMsgParse(self) :
        self.parsedMsg =  DNSRecord.parse(self.dnsMsg)
        return self

    def createDNSRespMsg(self,value): # Keep values here temp.
        # Returns A record only 
        self.dnsResp =  DNSRecord(DNSHeader(id = self.parsedMsg.header.id,qr=1,aa=0,ra=1),
                q=DNSQuestion(str(self.parsedMsg.q.qname)),
                a=RR(str(self.parsedMsg.q.qname),
                    rdata=A(value),))
        return self

    def packDNSRespMsg(self):
        self.packedDNSResp = self.dnsResp.pack()
        return self
    
    def getPackedResponse(self):
        return self.packedDNSResp