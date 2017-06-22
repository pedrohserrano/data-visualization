#! /usr/bin/env python3
__author__ = 'pedrohserrano'

import json
import sys
import operator
from datetime import timedelta, datetime
import pandas as pd

if __name__ == "__main__":

    #datemin=datetime.now() 
    #datemax=datetime.fromtimestamp(0/1e6)

    path = 'todas_busquedas.json'
        
    with open(path) as data_file:
        data = json.load(data_file)


        def get_dates(data):

            datemin=datetime.now() 
            datemax=datetime.fromtimestamp(0/1e6)

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

                    #dias = sorted(dias)

            return dias
                    #for key in sorted(dias):

                     #   print (key, dias[key])

        d = get_dates(data)

                #print(dias)

        output = pd.DataFrame(d)
        output=output.transpose()

        output.to_csv('output.csv', encoding='utf-8', header=False)

        output2 = output.sum(output[[3,6]])

        output2.to_csv('output2.csv', encoding='utf-8', header=False)



"""
    queries = {}
    # QueriesTimeStamps holds a list of every timestamp from every search
    queriesTimeStamps = []

    for query in data['event']:
        query = query['query']
        query_text = query['query_text']
        timestamps = []
        for timestamp in query['id']:
            timestamps.append(timestamp['timestamp_usec'])

            print(timestamps)


        if query_text in queries:
            l = queries[query_text]
            # The list of timestamps might not exist, even if its been added to the dictionary
            if l:
                queries[query_text] = l + timestamps
            else:
                queries[query_text] = timestamps

        else:
            queries[query_text] = timestamps
        queriesTimeStamps = queriesTimeStamps + timestamps

"""

