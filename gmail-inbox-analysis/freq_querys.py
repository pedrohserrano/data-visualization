#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 
from datetime import timedelta, datetime
from dateutil.parser import parse as parse_datetime
import json

# Define la función para obtener las fechas, excluyendo los chats
def get_dates(data):

    datemin=datetime.now() 
    datemax=datetime.fromtimestamp(0/1e6)

    #dias = {}
    #i=0
    all_dates = []
    all_times = []
    for query in data['event']:

        query_text = query['query']['query_text']
        timestamp = int(query['query']['id'][0]['timestamp_usec'])
        dates = datetime.fromtimestamp(timestamp/1e6)
        
        date=str(dates.year)+'-'+str(dates.month)+'-'+str(dates.day)
        time=str(dates.hour)+'-'+str(dates.minute)
        #date= str(parse_datetime(timestamp/1e6)).split(' ')
        all_dates.append(date)
        all_times.append(time)

    return all_dates, all_times


# Toma el archivo
path = 'todas_busquedas.json'

with open(path) as data_file:
    data = json.load(data_file)

#Extrae todas las fechas y las horas
all_dates, all_times = get_dates(data)
date_counts = pd.Series(all_dates).value_counts().sort_index()

date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
index = date_range.map(lambda x: str(x.date()))
date_counts = date_counts.reindex(index, fill_value=0)

date_counts.to_csv('date_counts_querys.csv', encoding='utf-8')

# Ahora se observ por mes
all_months = [x[:-3] for x in all_dates]
month_counts = pd.Series(all_months).value_counts().sort_index()

date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
months_range = date_range.map(lambda x: str(x.date())[:-3])
index = np.unique(months_range)
month_counts = month_counts.reindex(index, fill_value=0)
month_counts = pd.Series(all_months).value_counts().sort_index()

month_counts.to_csv('month_counts_querys.csv', encoding='utf-8')
