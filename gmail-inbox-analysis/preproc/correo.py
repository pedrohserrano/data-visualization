#! /usr/bin/env python3

#__author__ = 'eduardomartinez'


from email.utils import parsedate
import mailbox
import email.errors
import collections
import sys

mbox = mailbox.mbox(sys.argv[1])

def extract_date(email):
    date = email.get('Date')
    return parsedate(date)


def pars(mbox):
    fechas = {}
    #the_mailbox = mailbox.mbox(mbox)

    for key in mbox.iterkeys():
        try:
            message = mbox[key]
        except email.errors.MessageParseError:
            continue  # The message is malformed. Just leave it.

        date = extract_date(message)

        if type(date) is tuple:
            hash = date[0] * 100 + date[1]
            if hash in fechas.keys():
                fechas[hash] = fechas[hash] + 1
            else:
                fechas[hash] = 1

    return fechas

print (pars(mbox))



#od = collections.OrderedDict(sorted(fechas.items()))
#for k, v in od.items(): print(k, v)
#the_mailbox.flush()