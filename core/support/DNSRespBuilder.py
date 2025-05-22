from core.upstreamResolver import UpstreamResolver
from core.support.DNSParser import DNSParser
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A,RCODE,QTYPE,SOA,NS
import time
from config.config import Config

from core.upstreamResolver import UpstreamResolver
from core.support.DNSParser import DNSParser
from dnslib.dns import DNSRecord, DNSHeader, DNSQuestion, RR, CNAME, A, RCODE, QTYPE, SOA, NS
import time
from config.config import Config

class DNSResponseBuilder:
    def __init__(self, dnsMsg):
        self.config = Config()
        self.dnsMsg = dnsMsg
        self.upstreamResolver = UpstreamResolver()
        self.parsedMsg = DNSParser(dnsMsg).dnsReqMsgParse()
        self.DNSRecordTypes = QTYPE.forward
        self.dnsResp = None
        self.packedDNSResp = None

    def createResponseDNSRecord(self, rcode, answers=None, aa=1):
        """
        Create DNSRecord for response, with a list of answers (RR objects).
        aa = Authoritative Answer flag ; 1 for true, 0 for false
        """
        ra = 0  # Recursion Available flag
        qname = str(self.parsedMsg.q.qname)
        qclass = self.parsedMsg.q.qclass

        dnsHeader = DNSHeader(
            id=self.parsedMsg.header.id,
            qr=1, aa=aa, ra=ra, rcode=rcode
        )
        dnsQuestion = DNSQuestion(
            qname=qname, qtype=self.parsedMsg.q.qtype, qclass=qclass
        )
        dnsRecord = DNSRecord(dnsHeader, q=dnsQuestion)
        if answers:
            for ans in answers:
                dnsRecord.add_answer(ans)
        return dnsRecord

    def notImplemented(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOTIMP)
        return self

    def nxDomain(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NXDOMAIN)

    def serverFailure(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.SERVFAIL)

    def emptyResponse(self):
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR)

    def RR_A(self, records):
        """
        Handle A and CNAME records, supporting multiple answers.
        Expect records to be a list of dicts: [{"recordType": "A", "recordValue": "1.2.3.4", "ttl": 300}, ...]
        """
        if not records or not isinstance(records, list):
            self.emptyResponse()
            return
        answers = []
        qname = str(self.parsedMsg.q.qname)
        print("QNAME:", qname[:-1])
        qclass = self.parsedMsg.q.qclass
        for record in records:
            ttl = record.get("ttl", 300)
            if record["recordType"] == "A" and  qname[:-1] == record["recordName"] :
                answers.append(RR(qname, QTYPE.A, qclass, ttl, A(record["recordValue"])))
            elif record["recordType"] == "CNAME" and qname[:-1] == record["recordName"]:
                answers.append(RR(qname, QTYPE.CNAME, qclass, ttl, CNAME(record["recordValue"])))
        if answers:
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR, answers)
        else:
            self.emptyResponse()

    def RR_CNAME(self, records):
        """
        Handle CNAME records; support multiple (though usually only one CNAME is present per RRset).
        """
        if not records or not isinstance(records, list):
            self.emptyResponse()
            return
        answers = []
        qname = str(self.parsedMsg.q.qname)
        qclass = self.parsedMsg.q.qclass
        for record in records:
            if record["recordType"] == "CNAME" and  qname[:-1] == record["recordName"]:
                ttl = record.get("ttl", 300)
                answers.append(RR(qname, QTYPE.CNAME, qclass, ttl, CNAME(record["recordValue"])))
        if answers:
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR, answers)
        else:
            self.emptyResponse()

    def RR_SOA(self):
        """
        Build SOA answer.
        """
        soa_record = SOA(
            mname=self.config.getNSHosts()[0],
            rname=self.config.getRegistrarEmail(),
            times=(
                int(time.strftime("%Y%m%d%H")),  # Serial
                3600, 1800, 1209600, 86400
            )
        )
        # As we are not allowing user to set NS records,
        # So at the end we will be their source of managing all records
        # So valid SOA will be our main  ws.in's  SOA
        # IF in future we allow user to set NS records, then we need to change this
        qname = self.config.getAuthTLD() 
        qclass = self.parsedMsg.q.qclass
        answer = RR(qname, QTYPE.SOA, qclass, 0, soa_record)
        self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR, [answer])

    def RR_NS(self):
        """
        Build NS answers for all configured NS hosts.
        """
        ns_hosts = self.config.getNSHosts()
        qname = str(self.parsedMsg.q.qname)
        qclass = self.parsedMsg.q.qclass
        answers = [
            RR(qname, QTYPE.NS, qclass, 300, NS(ns_host))
            for ns_host in ns_hosts
        ]
        if answers:
            self.dnsResp = self.createResponseDNSRecord(RCODE.NOERROR, answers)
        else:
            self.emptyResponse()

    def RR_CAA(self):
        """
        Return empty response for CAA queries (no CAA records).
        """
        self.emptyResponse()

    def upstreamResp(self):
        """
        Forward query upstream; set self.packedDNSResp to bytes result.
        """
        upstreamResp = self.upstreamResolver.sendQuery(self.dnsMsg)
        if not upstreamResp:
            self.serverFailure()
            return None
        self.packedDNSResp = upstreamResp
        self.dnsResp = True

    def packResponse(self):
        """
        Get packed DNS response (bytes).
        """
        if self.dnsResp is None:
            self.serverFailure()
        if hasattr(self.dnsResp, "pack"):
            self.packedDNSResp = self.dnsResp.pack()
        return self.packedDNSResp