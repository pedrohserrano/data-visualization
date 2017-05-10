#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 
#import matplotlib.pyplot as plt
#import matplotlib.font_manager as fm
from dateutil.parser import parse as parse_datetime


#family = 'serif'
#title_font = fm.FontProperties(family=family, style='normal', size=20, weight='normal', stretch='normal')
#label_font = fm.FontProperties(family=family, style='normal', size=16, weight='normal', stretch='normal')
#ticks_font = fm.FontProperties(family=family, style='normal', size=12, weight='normal', stretch='normal')

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
mbox = mailbox.mbox(sys.argv[1])
print('There are {:,} messages in the archive.'.format(len(mbox)))

all_dates, all_times = get_dates(mbox)
#print (all_dates[:10], all_times[:10]) funciona la funcioón y regresa las fechas y eso

# Se hace un count por día
date_counts = pd.Series(all_dates).value_counts().sort_index()
print('There are {:,} dates with messages.'.format(len(date_counts)))
#date_counts.head()

# No todas los día debe haber un mensaje, se llenan esos huecos con ceros
#date_range = pd.date_range(start=min(all_dates), end=max(all_dates), freq='D') las funciones min y max no funcionaron
date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
index = date_range.map(lambda x: str(x.date()))
date_counts = date_counts.reindex(index, fill_value=0)
print('There are {:,} dates total in the range, with or without messages.'.format(len(date_counts)))
#date_counts.head()

# create a series of labels for the plot: each new year's day
xlabels = pd.Series([label if '01-01' in label else None for label in date_counts.index])
xlabels = xlabels[pd.notnull(xlabels)]
#xlabels.head()


#aquí en vez de la imagen es hacer un dataframe que coma shiny
# plot the counts per day
#fig = plt.figure(figsize=[15, 5])
#ax = date_counts.plot(kind='line', linewidth=0.5, alpha=0.5, color='g')

#ax.grid(True)
#ax.set_xticks(xlabels.index)
#ax.set_xticklabels(xlabels, rotation=35, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
#ax.set_ylabel('Number of emails', fontproperties=label_font)
#ax.set_title('Sent mails traffic per day', fontproperties=title_font)

#fig.tight_layout()
#fig.savefig('images/gmail-traffic-day-destacados.png', dpi=96)

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

# create a series of labels for the plot: each january
xlabels = pd.Series([label if '-01' in label else None for label in month_counts.index])
xlabels = xlabels[pd.notnull(xlabels)]
#xlabels.head()



# plot the counts per month
#fig = plt.figure(figsize=[15, 5])
#ax = month_counts.plot(kind='line', linewidth=2.5, alpha=0.6, color='g', marker='+', markeredgecolor='g')

#ax.grid(True)
#ax.set_xticks(xlabels.index)
#ax.set_xticklabels(xlabels, rotation=35, rotation_mode='anchor', ha='right', fontproperties=ticks_font)
#ax.set_ylabel('Number of emails', fontproperties=label_font)
#ax.set_title('Sent mail traffic per month', fontproperties=title_font)

#fig.tight_layout()
#fig.savefig('images/gmail-traffic-month.png', dpi=96)
#plt.show()


# Por día de la semana

# get the count per day of the week
day_counts = pd.DataFrame()
day_counts['count'] = date_counts
day_counts['day_of_week'] = date_counts.index.map(lambda x: parse_datetime(x).weekday())
mean_day_counts = day_counts.groupby('day_of_week')['count'].mean()
xlabels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

#print (date_counts)
