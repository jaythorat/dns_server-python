from core.upstreamResolver import UpstreamResolver
from core.support.DNSParser import DNSParser
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE,SOA,NS
import time

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
        if not value or not isinstance(value, dict):
            self.emptyResponse()
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,A(value["recordValue"]),0,QTYPE.A)
    
    def RR_CNAME(self,value):
        if not value or not isinstance(value, dict):
            self.emptyResponse()
            return
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR,CNAME(value["recordValue"]),0,QTYPE.CNAME)
    
    def RR_SOA(self):
        soa_record = SOA(
            mname="ns3.websculptors.in.",          # Primary NS
            rname="jay.websculptors.in.",   # Email
            times=(
                int(time.strftime("%Y%m%d%H")),    # Serial
                3600,      # Refresh
                1800,      # Retry
                1209600,   # Expire
                86400      # Minimum
            )
        )

        # DNS Flags
        aa = 1      # Authoritative answer
        ra = 0      # Recursion not available
        rcode = 0   # No error

        qname = str(self.parsedMsg.q.qname)
        qtype = self.parsedMsg.q.qtype
        qclass = self.parsedMsg.q.qclass

        dnsHeader = DNSHeader(
            id=self.parsedMsg.header.id,
            qr=1, aa=aa, ra=ra, rcode=rcode
        )
        dnsQuestion = DNSQuestion(qname=qname, qtype=qtype, qclass=qclass)
        dnsAnswer = RR(
            rname=qname,
            rtype=QTYPE.SOA,
            rclass=qclass,
            ttl=0,
            rdata=soa_record
        )
        dnsRecord = DNSRecord(
            dnsHeader,
            q=dnsQuestion,
            a=dnsAnswer
        )
        self.dnsResp = dnsRecord

    def RR_NS(self):
    # List of your NS hostnames

        ns_hosts = [
            "ns3.websculptors.in.",
            "ns4.websculptors.in."
        ]
        
        qname = str(self.parsedMsg.q.qname)
        qtype = self.parsedMsg.q.qtype
        qclass = self.parsedMsg.q.qclass

        # DNS Flags
        aa = 1      # Authoritative answer
        ra = 0      # Recursion not available
        rcode = 0   # No error

        dnsHeader = DNSHeader(
            id=self.parsedMsg.header.id,
            qr=1, aa=aa, ra=ra, rcode=rcode
        )
        dnsQuestion = DNSQuestion(qname=qname, qtype=qtype, qclass=qclass)
        
        # Create RR for each NS
        ns_answers = [
            RR(
                rname=qname,
                rtype=QTYPE.NS,
                rclass=qclass,
                ttl=300,
                rdata=NS(ns_host)
            )
            for ns_host in ns_hosts
        ]
        
        # Build DNSRecord with all answers
        dnsRecord = DNSRecord(
            dnsHeader,
            q=dnsQuestion,
            a=ns_answers[0] if ns_answers else None,
            # Add the rest as additional answers
            # dnslib supports multiple answers via the 'add_answer' method, so you may need to loop in your handler if not using this directly
        )
        # Add remaining NS answers, if any
        for rr in ns_answers[1:]:
            dnsRecord.add_answer(rr)
        
        self.dnsResp = dnsRecord


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
