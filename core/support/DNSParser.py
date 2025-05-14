from dnslib.dns import DNSRecord,QTYPE

class DNSParser:
    def __init__(self, dnsMsg):
        self.dnsMsg = dnsMsg
        self.parsedMsg = self.dnsReqMsgParse()
        self.DNSRecordTypes = QTYPE.forward

    def dnsReqMsgParse(self):
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