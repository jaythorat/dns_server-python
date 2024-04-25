from dnslib import *
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A


def dns_req_msg_parse(dns_msg: bytes) -> DNSRecord:
    """
    Parse DNS message.
    """
    return DNSRecord.parse(dns_msg)

def create_dns_resp_msg():
    response = DNSRecord()

def pack_dns_res_msg():
    pass