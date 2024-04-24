import socket
import dnslib as jay
from dnslib.dns import DNSRecord,DNSHeader,DNSQuestion,RR,CNAME,A




sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = 'localhost'
server_port = 53

server = (server_address, server_port)
sock.bind(server)
print("Listening on " + server_address + ":" + str(server_port))

while True:
	payload, client_address = sock.recvfrom(511)
	print("Echoing data back to " + str(client_address))
	print(payload)
	d = DNSRecord.parse(payload)
	print(d)
	request_id = d.header.id
	print(request_id)
	d1 = DNSRecord(DNSHeader(qr=1,aa=1,ra=1),q=DNSQuestion("jaythorat.in"),a=RR("jaythorat.in",rdata=A("1.23.34.23"),))
	d1.header.id=request_id
	print(str(DNSRecord.parse(d.pack())) == str(d))
	response = d1.pack()
	print(type(response))
	sock.sendto(response, (client_address[0],client_address[1]))
