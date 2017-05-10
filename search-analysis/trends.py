#!/usr/local/Cellar/python3/3.5.1/bin/python3
__author__ = 'eduardomartinez'
# @param readline es un archivo descargado de google takeout en formato json
# returns imprime en consola el numero de consultas por hora por dia
# ejemplo de salida: 
# 20170202,3,Thursday,0,0,0,0,0,0,0,0,0,1,0,1,6,5,8,11,10,3,0,2,0,0,0,0
# Fecha, NumeroDia, NombreDia, 0-23 horas

from datetime import timedelta, datetime
import json
import sys
import operator

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__ == "__main__":

    while True:
        x = sys.stdin.readline()

        x = x.replace('\n', '')
        if not x:
            break
        # print(x) # mostrar nombre del archivo

        datemin=datetime.now() 
        datemax=datetime.fromtimestamp(0/1e6)
        with open(x) as data_file:
            data = json.load(data_file)

            dias = {}
            i=0
            for query in data['event']:

                    query_text = query['query']['query_text']
                    timestamp = int(query['query']['id'][0]['timestamp_usec'])
                    date = datetime.fromtimestamp(timestamp/1e6)
                    
                    nombredia = date.strftime("%A")
                    diasemana = date.weekday()

                    if date > datemax:
                        datemax=date

                    if date < datemin:
                        datemin=date

                    hash = date.year * 10000 + date.month * 100 + date.day

                    if hash in dias.keys():
                        dias[hash][date.hour+2]+=1
                    else:
                        dias[hash]=[0 for i in range(24)]
                        dias[hash].insert(0,nombredia)
                        dias[hash].insert(0,diasemana)
                        dias[hash][date.hour+2]+=1

            # print("num dias con consultas: {}".format(len(dias)))

        

        for date in daterange(datemin, datemax):
            hash = date.year * 10000 + date.month * 100 + date.day
            if not hash in dias.keys():
                nombredia = date.strftime("%A")
                diasemana = date.weekday()
                dias[hash]=[0 for i in range(24)]
                dias[hash].insert(0,nombredia)
                dias[hash].insert(0,diasemana)
                #print("faltaba: {}".format(hash))

            #print single_date.strftime("%Y-%m-%d")


        sorted_x = sorted(dias.items(), key=operator.itemgetter(0))
        for k, v in enumerate(sorted_x): 
            width = len(v[1])
            for j in range(width):
                if j == 0:
                    print('{},'.format(v[0]), end='')
                if j == width-1:
                    print('{}'.format(v[1][j]))
                else:
                    print('{},'.format(v[1][j]), end='')
        