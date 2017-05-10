#! /usr/bin/env python3

import sys
import os
import operator
import mailbox

mbox = mailbox.mbox(sys.argv[1])

#subject
#for msg in mbox:
#    print (msg['Subject'])


#body
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
	body=getbody(message)
	print(body)