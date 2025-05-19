import json

from DB.sql import MysqlConnectionPool

connectionPool = MysqlConnectionPool()

class FetchDNSRecords:
    def __init__(self, domain):
        self.domain = domain
        self.stripTrailingDot()

    def stripTrailingDot(self):
        if self.domain.endswith('.'):
            self.domain = self.domain[:-1]

    def fetchRecords(self):
        data,status = connectionPool.getData("getDataById",["DNSRecordView","domainName",self.domain])
        if status != "SUCCESS":
            return None
        return data 
    
    @classmethod
    def fetchParticularRecord(self,cleanedDomain):
        data= connectionPool.getData("getDataById",["DNSRecordView","recordName",cleanedDomain])
        if data["status"]!= "SUCCESS":
            return None
        return data["data"]
    