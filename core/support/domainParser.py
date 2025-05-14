import re

class DomainParser():
    def __init__(self, domain):
        self.domain = domain

    def isFQDN(self):
        return self.domain.endswith('.') and '.' in self.domain[:-1]
    
    def handleFQDN(self):
        if self.isFQDN() and self.domain.endswith('.'):
            return self.domain[:-1]
        return self.domain
    
    def extractDomain(self):
        match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})$', self.handleFQDN())
        if match:
            return match.group(1)
        return None