from DB.sql import MysqlConnectionPool

connectionPool = MysqlConnectionPool()

class FetchDNSRecords:
    def __init__(self, domain):
        self.domain = domain
        self.stripTrailingDot()

    def stripTrailingDot(self):
        if self.domain.endswith('.'):
            self.domain = self.domain[:-1]
    
    @classmethod
    def getDomainDetails(self,cleanedDomain):
        data = connectionPool.getData("getDataById",["Domain","domainName",cleanedDomain])
        if data["status"] != "SUCCESS":
            print("Error fetching domain details from database for domain:", self.domain, "Error:", data)
            return None
        return data["data"]
    
    @classmethod
    def checkDomainExists(self,cleanedDomain):
        data = connectionPool.getData("getDataById",["Domain","domainName",cleanedDomain])
        if data["status"] != "SUCCESS":
            return False
        if len(data["data"]) == 0:
            return False
        return True
    
    @classmethod
    def fetchParticularRecord(self,cleanedDomain):
        data= connectionPool.getData("getDataById",["dnsrecordview","recordName",cleanedDomain])
        if data["status"]!= "SUCCESS":
            return None
        return data["data"]
    
    @classmethod
    def fetchAllRecords(cls,domainUUID):
        data = connectionPool.getData("getDataById",["dnsrecordview","domainUUID",domainUUID])
        if data["status"] != "SUCCESS":
            return None
        return data["data"]
    