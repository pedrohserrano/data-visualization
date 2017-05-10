import sys
import os
import operator
import mailbox

import io, csv, email

from email import header
from email.utils import getaddresses

from bs4 import BeautifulSoup #required

import chardet #reequired

mbox = mailbox.mbox(sys.argv[1])

def mbox_to_csv(mbox):
    mail = None

    def add_mail():
        if mail:
            msg = email.message_from_string(mail)

            subject = header.make_header(header.decode_header(msg['Subject']))
            body = str(subject)

            body += '\n'

            def parse_payload(message):
                if message.is_multipart():
                    for part in message.get_payload(): 
                        yield from parse_payload(part)
                else:
                    yield message, message.get_payload(decode=True)

            for submsg, part in parse_payload(msg):
                content_type = submsg.get_content_type()
                content = ''
                def decode():
                    charset = submsg.get_content_charset('utf-8')
                    try:
                        return part.decode(charset)
                    except UnicodeDecodeError:
                        charset = chardet.detect(part)['encoding']
                        return part.decode(charset)
                if 'plain' in content_type:
                    content = decode()
                if 'html' in content_type:
                    content = BeautifulSoup(decode()).text
                body += '\n' + content

            senders = getaddresses(msg.get_all('from', []))

            tos = msg.get_all('to', [])
            ccs = msg.get_all('cc', [])
            resent_tos = msg.get_all('resent-to', [])
            resent_ccs = msg.get_all('resent-cc', [])
            all_recipients = getaddresses(tos + ccs + resent_tos + resent_ccs)

    for line in mbox:
        if line.startswith('From '):
            add_mail()
            mail = ''
        if mail is not None: # ignore email without headers
            mail += line
    add_mail()