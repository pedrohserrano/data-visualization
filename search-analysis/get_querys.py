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
            querys = []
            i=0
            for query in data['event']:

                    query_text = query['query']['query_text']
                    querys.append(query_text)

            # print("num dias con consultas: {}".format(len(dias)))

        for i in range(len(querys)):
            print(querys[i])
        