#!/usr/local/Cellar/python3/3.5.1/bin/python3


import datetime
import time
import json
import sys
import operator
import pandas as pd

if __name__ == "__main__":

    #datemin=datetime.now() 
    #datemax=datetime.fromtimestamp(0/1e6)

    path = '../../google-takeout/Ubicaciones/Historialdeubicaciones.json'

    with open(path, 'r') as fh:
        raw = json.loads(fh.read())

    ld = pd.DataFrame(raw['locations'])

    coords=ld[['latitudeE7','longitudeE7','timestampMs']]
    #coords['timestampMs'] = coords['timestampMs'].apply(pd.to_numeric)

    inicio_s= "01/06/2016"
    final_s="31/12/2016"
    #3 meses
    inicio=1000*time.mktime(datetime.datetime.strptime(inicio_s, "%d/%m/%Y").timetuple())
    final=1000*time.mktime(datetime.datetime.strptime(final_s, "%d/%m/%Y").timetuple())

    #coords3=coords[(coords['timestampMs']>inicio)&(coords['timestampMs']<final)]
    coords3=coords
    coords3.columns = ['lat', 'lon','timestamp']
    coords3['lat']=coords3['lat']/1e7
    coords3['lon']=coords3['lon']/1e7

    cosa=coords3[['lat','lon']]

    f = open('coordenadas.txt','w')

    print(cosa, file=f)


    #output = get_queries(data)

    #new_file = open('busquedas.txt','w')
    #output = str(output).strip('[]')
    #new_file.write(output)
    #new_file.close()

    #print(output)
        