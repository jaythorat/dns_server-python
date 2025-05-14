import re

class DomainParser():
    def __init__(self, domain):
        self.domain = domain
        # self.subdomain = None
        # self.sld = None
        # self.tld = None
        # self.parse_domain()

    # def parse_domain(self):
    #     parts = self.domain.split('.')
    #     if len(parts) < 2:
    #         raise ValueError("Invalid domain format")
    #     self.tld = parts[-1]
    #     self.sld = parts[-2]
    #     if len(parts) > 2:
    #         self.subdomain = '.'.join(parts[:-2])
    #     else:
    #         self.subdomain = None

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