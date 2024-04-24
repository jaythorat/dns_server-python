import socket
import dnslib as jay
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A
from utils import dns_req_msg_parse




sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = 'localhost'
server_port = 53

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

while True:
	payload, client_address = sock.recvfrom(512)
	print("Echoing data back to " + str(client_address))
	
	parsed_msg = dns_req_msg_parse(payload)
	request_id = parsed_msg.header.id
	print(request_id)
	d1 = DNSRecord(DNSHeader(qr=1,aa=0,ra=1),q=DNSQuestion("jaythorat.in"),a=RR("jaythorat.in",rdata=A("1.23.34.99"),))
	d1.header.id=request_id
	response = d1.pack()
	print(type(response))
	sock.sendto(response, (client_address[0],client_address[1]))
