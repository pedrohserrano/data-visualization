#! /usr/bin/env python3

#__author__ = 'eduardomartinez'


from email.utils import parsedate
import mailbox
import email.errors
import collections

def extract_date(email):
    date = email.get('Date')
    return parsedate(date)


fechas = {}
the_mailbox = mailbox.mbox('mail.mbox')

for key in the_mailbox.iterkeys():
    try:
        message = the_mailbox[key]
    except email.errors.MessageParseError:
        continue  # The message is malformed. Just leave it.

    date = extract_date(message)

    if type(date) is tuple:
        hash = date[0] * 100 + date[1]
        if hash in fechas.keys():
            fechas[hash] = fechas[hash] + 1
        else:
            fechas[hash] = 1




od = collections.OrderedDict(sorted(fechas.items()))
for k, v in od.items(): print(k, v)
the_mailbox.flush()