from core.upstreamResolver import UpstreamResolver
from core.support.DNSParser import DNSParser
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE


class DNSResponseBuilder:
    def __init__(self, dnsMsg):
        self.dnsMsg = dnsMsg
        self.upstreamResolver = UpstreamResolver()
        self.parsedMsg = DNSParser(dnsMsg).dnsReqMsgParse()
        self.DNSRecordTypes = QTYPE.forward
        self.dnsResp = None
        self.packedDNSResp = None

    def createResponseDNSRecord(self, rcode, rdata, ttl, atype=None, aa=1):
        ra = 0  # 1 Recursion Available 0 for not available
        qname = str(self.parsedMsg.q.qname)
        qclass = self.parsedMsg.q.qclass
        dnsHeader = DNSHeader(id=self.parsedMsg.header.id, qr=1, aa=aa, ra=ra, rcode=rcode)
        dnsQuestion = DNSQuestion(qname=qname, qtype=self.parsedMsg.q.qtype, qclass=qclass)
        dnsAnswer = None
        if rcode == RCODE.NOERROR and rdata is not None and atype is not None:
            dnsAnswer = RR(str(qname), rtype=atype, rclass=qclass, ttl=ttl,
                           rdata=rdata,)
        dnsRecord = DNSRecord(dnsHeader,
                              q=dnsQuestion,
                              a=dnsAnswer)
        return dnsRecord
    
    def notImplemented(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOTIMP,None,0)
        return self

    def nxDomain(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NXDOMAIN,None,0)
    
    def serverFailure(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.SERVFAIL,None,0)

    def emptyResponse(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,None,0)
    
    def RR_A(self,value):
        if not value or not isinstance(value, list):
            self.emptyResponse()
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,A(value[1]),0,QTYPE.A)
    
    def RR_CNAME(self,value):
        if not value or not isinstance(value, list):
            self.emptyResponse()
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,CNAME(value[1]),0,QTYPE.CNAME)

    def upstreamResp(self):
        upstreamResp = self.upstreamResolver.sendQuery(self.dnsMsg)
        if not upstreamResp:
            self.serverFailure()
            return None
        self.packedDNSResp = upstreamResp
        self.dnsResp = True  #TODO: Temp bypass fix later
    
    def packResponse(self):
        if self.dnsResp is None:
            self.serverFailure()
        elif hasattr(self.dnsResp, "pack"):
            self.packedDNSResp = self.dnsResp.pack()
        return self.packedDNSResp
    