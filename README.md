# Simple-email-spoofer
Python based email spoofer. Tested with python 2.7 and 3.7.

> *For educational purposes only. Do not send to or from addresses that you do not own.* 

> Inappropriate usage of this tool could violate of the [CAN-SPAM Act of 2003](https://en.wikipedia.org/wiki/CAN-SPAM_Act_of_2003) and/or the [Computer Fraud and Abuse Act](https://en.wikipedia.org/wiki/Computer_Fraud_and_Abuse_Act). **Use responsibly**.


## Requirements
- [dnspython](http://www.dnspython.org/)
- [argparse](https://pypi.org/project/argparse/)

## Functionalities 
The scripts operates in two modes:
#### 1. weak
In this mode it is required that you own an e-mail account on an e-mail provider.
The tool connects using the account credential to the specifed email exchange server. 
Then, it simply spoofs the 'From:' field not the 'Return-Path:' of the sent email. 
Therefore, if the message is analyzed the original sending address can be quickly retrieved.
Further, some email service providers (e.g., Gmail) automatically replace the forged email
in the 'From:' field with the sending email leaving in the end just the spoofed name. Example:

From: Spoofed name <original@email.com>

Note: It could be required that you allow un-trusted application to send emails from
your acount for this mode to work. Check your email provider account's settings.

#### 2. full
In the full mode the tools tries to connect to the email exchange server of the receiver
email address and send a fully spoofed email. In such a case, the only information avaiable
to track the real sender is the real IP address show in the 'Received' field of the email
header. Nowadays, if the spoofed email domain used as sending adress deploys the DMRAC
security mechanisms the email will be very likely marked as spam or even rejected.

In such a mode, adding the "--tls" command line parameter the tool is using TLS to
communicate with the email exchange server (reccomanded).

# Disclaimer
Made for fun and no profit. Only use this tool for education, research, or in the course of approved social engineering assessments. While email spoofing is a powerful tool in the social engineer's arsenal, it is also trivial to identify the server that sent any email.
