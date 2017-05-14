#! /usr/bin/env python3
__author__ = 'pedrohserrano'

import sys
import os
import mailbox
from email import header
#import re
#import base64
import codecs
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

if __name__ == '__main__':

	path = 'todos_mails.mbox'
	mbox = mailbox.mbox(path)
	#mbox = mailbox.mbox(sys.argv[1])

	#get mail elements
	def getstuff(message):
	    ad_from = message['From']
	    ad_cc = message['cc']
	    ad_to = message['to']
	    #subj = message['Subject']
	    #id_msg = message["Message-ID"]
	    #subj = re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", msg['Subject'])
	    subj = header.decode_header(message['Subject'])
	    #subj=subj.encode('utf-8')
	    #decoded = base64.b64decode(msg['Subject'])
	    #decode the utf-8
	    #subj = str(decoded, 'latin-1')
	    stuff=[str(ad_from), str(ad_cc), str(ad_to), str(subj)]
	    stuff = ''.join(stuff)
	    #stuff=subj
	    return stuff

	#get mail body
	def getbody(message): #getting plain text 'email body'
	    body = None
	    if message.is_multipart():
	        for part in message.walk():
	            if part.is_multipart():
	                for subpart in part.walk():
	                    if subpart.get_content_type() == 'text/plain':
	                        body = subpart.get_payload(decode=True)
	            elif part.get_content_type() == 'text/plain':
	                body = part.get_payload(decode=True)
	    elif message.get_content_type() == 'text/plain':
	        body = message.get_payload(decode=True)
	    return body

	def get_mail (mbox):
		mail_stuff = []
		for message in mbox:
			#body=getbody(message)
			stuff=getstuff(message)
			mail_stuff.append(stuff)
		mail_stuff = '\n'.join(mail_stuff)

		return mail_stuff

	output = get_mail(mbox)

	f = open('mbox_messages.txt','w')
	print(output, file=f)
	
	
