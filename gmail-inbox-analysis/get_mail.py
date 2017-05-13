#! /usr/bin/env python3

import sys
import os
import mailbox
#from email import header
#import re
#import base64
#import codecs
#sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
import subprocess


if __name__ == '__main__':

	subprocess.call['./get_todos_mails.sh']

	mbox = mailbox.mbox(sys.argv[1])

	#get mail elements
	def getstuff(msg):
	    #for msg in mbox:
	    ad_from = msg['From']
	    ad_cc = msg['cc']
	    ad_to = msg['to']
	    subj = msg['Subject']
	    id_msg = msg["Message-ID"]
	    #subj = re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", msg['Subject'])
	    #subj = header.decode_header(msg['Subject'])
	    #subj=subj.encode('utf-8')
	    #decoded = base64.b64decode(msg['Subject'])
	    #decode the utf-8
	    #subj = str(decoded, 'latin-1')

	    return id_msg, ad_from, ad_cc, ad_to, subj
	    #print (ad_from, ad_cc, ad_to, subj)

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


	for message in mbox:
		#body=getbody(message)
		stuff=getstuff(message)
		print(stuff)#, body)

