#! /usr/bin/env python3

import sys
import os
import mailbox


if __name__ == '__main__':

	mbox = mailbox.mbox(sys.argv[1])

	#get mail elements
	def getstuff(msg):
	    #for msg in mbox:
	    ad_from = msg['From']
	    ad_cc = msg['cc']
	    ad_to = msg['to']
	    subj = msg['Subject']
	    return ad_from, ad_cc, ad_to, subj
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

