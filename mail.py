import dns.resolver
import socket
from socket import gethostbyname, gaierror
import sys
from IPython import embed

def reading(socket):
	rec = socket.recv(512)
	print('[REMOTE]: '+rec)
	return rec
	
def writing(socket,data):
	socket.send(data+'\r\n')
	return
	
def check250(data):
    return data[:3] == '250'
	
		
answers = dns.resolver.query(sys.argv[1], 'MX')
for ans in answers:
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(5)
	try:
		mx_server = ans.exchange.to_text()[:-1]
		print("Connecting to {0} mail server".format(mx_server))
		sock.connect((mx_server,25))
		
		rec = reading(sock)
		if rec[:3] != '220':
			continue
			
		domain = raw_input("Tell the domain of the HELO message: ")
		writing(sock,'HELO '+domain)
		rec = reading(sock)
                if not check250(rec): continue	
		
		email = raw_input("Tell the sender of the email message: ")
		writing(sock,'MAIL FROM: <{0}>'.format(email))
		rec = reading(sock)
                if not check250(rec): continue	
		
		email = raw_input("Tell the receiver of the email message: ")
		writing(sock,'RCPT TO: <{0}>'.format(email))
		rec = reading(sock)
                if not check250(rec): continue	
		
		embed()
	
	except Exception as err:
		print err
		continue
	else:
		break

	
print("Did not find any MX server available")
