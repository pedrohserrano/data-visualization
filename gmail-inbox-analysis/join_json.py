import os
import json
import subprocess
#import psycopg2
import codecs
import glob

#LOCAL_PATH = '/tmp/'

eventos={'event':[]}
for f in glob.glob("../../google-takeout/Busquedas/*.json"):
    with open(f) as data_file:
                data = json.load(data_file)
                #i=0
                for ev in data['event']:
                        data_event = ev
                        eventos['event'].append(data_event)

with open("todas_busquedas.json", "w") as outfile:
     json.dump(eventos, outfile)