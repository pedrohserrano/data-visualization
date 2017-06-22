#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 

from dateutil.parser import parse as parse_datetime

# Define la función para obtener las fechas, excluyendo los chats
def get_dates(mbox):
	all_dates = []
	all_times = []
	for message in mbox:
	    # it's an email and not a chat if there's no label, or if there's a label but it's not 'chat'
	    if not 'X-Gmail-Labels' in message or ('X-Gmail-Labels' in message and not 'Chat' in message['X-Gmail-Labels']):
	        if 'Date' in message and message['Date'] is not None:
	            try:
	                date, time = str(parse_datetime(message['Date'])).split(' ')
	            except Exception as e:
	                print(e, message['Date'])
	            all_dates.append(date)
	            all_times.append(time)
	        else:
	            # hangouts messages have no Date key, so skip them
	            pass
	return all_times, all_dates


# Toma el archivo
path = '/Users/pedrohserrano/google-takeout/Mail/Destacados.mbox'
mbox = mailbox.mbox(path)
#mbox = mailbox.mbox(sys.argv[1])
print('Hay {:,} mensajes.'.format(len(mbox)))

#Extrae todas las fechas y las horas
all_times, all_dates = get_dates(mbox)
# Se hace un count por día
date_counts = pd.Series(all_dates).value_counts().sort_index()
print('Hay {:,} fechas con mensajes.'.format(len(date_counts)))
#date_counts.head()

# No todas los día debe haber un mensaje, se llenan esos huecos con ceros
#date_range = pd.date_range(start=min(all_dates), end=max(all_dates), freq='D') las funciones min y max no funcionaron
date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
index = date_range.map(lambda x: str(x.date()))
date_counts = date_counts.reindex(index, fill_value=0)
#print('There are {:,} dates total in the range, with or without messages.'.format(len(date_counts)))
#print(date_counts.head())

date_counts.to_csv('date_counts.csv', encoding='utf-8')

# create a series of labels for the plot: each new year's day
xlabels = pd.Series([label if '01-01' in label else None for label in date_counts.index])
xlabels = xlabels[pd.notnull(xlabels)]
print(xlabels.head())

# Ahora se observ por mes
all_months = [x[:-3] for x in all_dates]
month_counts = pd.Series(all_months).value_counts().sort_index()

# not every month necessarily has a message, so fill in missing months in the range with zeros
#date_range = pd.date_range(start=min(all_dates), end=max(all_dates), freq='D') #ya está la variable
date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
months_range = date_range.map(lambda x: str(x.date())[:-3])
index = np.unique(months_range)
month_counts = month_counts.reindex(index, fill_value=0)
month_counts = pd.Series(all_months).value_counts().sort_index()

month_counts.to_csv('month_counts.csv', encoding='utf-8')
# create a series of labels for the plot: each january
xlabels1 = pd.Series([label if '-01' in label else None for label in month_counts.index])
xlabels1 = xlabels[pd.notnull(xlabels)]
print(xlabels1.head())

# Por día de la semana

# get the count per day of the week
day_counts = pd.DataFrame()
day_counts['count'] = date_counts
day_counts['day_of_week'] = date_counts.index.map(lambda x: parse_datetime(x).weekday())
mean_day_counts = day_counts.groupby('day_of_week')['count'].mean()

xlabels2 = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

mean_day_counts.to_csv('mean_day_counts.csv', encoding='utf-8')
