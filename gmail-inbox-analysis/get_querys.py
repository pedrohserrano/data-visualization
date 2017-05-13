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

    datemin=datetime.now() 
    datemax=datetime.fromtimestamp(0/1e6)

    path = '../../google-takeout/Busquedas/todas_busquedas.json'
        
    with open(path) as data_file:
        data = json.load(data_file)


    def get_queries(data):
        querys = []
        for query in data['event']:
                query_text = query['query']['query_text']
                querys.append(query_text)

        return querys
        # print("num dias con consultas: {}".format(len(dias)))
    
    output = get_queries(data)

    new_file = open('busquedas.txt','w')
    output = str(output).strip('[]')
    new_file.write(output)
    new_file.close()

    #print(output)
        