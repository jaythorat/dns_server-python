import json

class FetchDNSRecords:
    def __init__(self, domain):
        self.domain = domain
        self.stripTrailingDot()

    def stripTrailingDot(self):
        if self.domain.endswith('.'):
            self.domain = self.domain[:-1]

    def fetchRecords(self):
        with open('DB/registry.json', 'r') as file:
            data = json.load(file)
            if self.domain in data:
                return data[self.domain]
            else:
                return None
        return None