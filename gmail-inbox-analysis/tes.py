import os, sys

#with open('file.txt', 'w') as f:
#    print('hello world', file=f)

#hace el codigo y lo imprime

#path = 'Destacados.mbox'
mbox_file = open('Destacados.mbox','r')
mbox = mbox_file.read()

#new_path = 'new_mbox.txt'
new_mbox = open('new_mbox.txt','w')

#title = 'Text mbox'
#new_mbox.write(title)
#print(title)

new_mbox.write(mbox)
#print(mbox)

mbox_file.close()
new_mbox.close()