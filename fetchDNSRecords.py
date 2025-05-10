import json

class FetchDNSRecords:
    def __init__(self, domain):
        self.domain = domain
        self.stripTrailingDot()

    def stripTrailingDot(self):
        if self.domain.endswith('.'):
            self.domain = self.domain[:-1]


    def fetchRecords(self):
        with open('registry.json', 'r') as file:
            data = json.load(file)
            if self.domain in data:
                print(f"Records found for domain: {self.domain}")
                return data[self.domain]
            else:
                print(f"No records found for domain: {self.domain}")
                return None
        return None