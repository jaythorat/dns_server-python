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
        fqdn = self.handleFQDN()
        parts = fqdn.split('.')
        if len(parts) >= 3:
            return '.'.join(parts[-3:])
        return fqdn