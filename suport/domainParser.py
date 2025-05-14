import re

class DomainParser():
    def __init__(self, domain):
        self.domain = domain

    def isFQDN(self):
        """
        Check if the domain is a Fully Qualified Domain Name (FQDN).
        An FQDN ends with a dot (.) and contains at least one dot.
        """
        return self.domain.endswith('.') and '.' in self.domain[:-1]
    
    def handleFQDN(self):
        """
        Handles the FQDN by removing the trailing dot if present.
        """
        if self.isFQDN() and self.domain.endswith('.'):
            return self.domain[:-1]
        return self.domain
    
    def extractDomain(self):
        """
        Extracts the domain from the FQDN.
        """
        match = re.search(r'([a-zA-Z0-9-]+\.[a-zA-Z]{2,})$', self.handleFQDN())
        if match:
            return match.group(1)
        return None