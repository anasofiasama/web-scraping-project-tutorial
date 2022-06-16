# First i have to install all the packages in the requirments.txt trought the terminal. Then I import some librarys.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import sqlite3

from bs4 import BeautifulSoup

# Download the data using request library

html_data='https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue'
pag=requests.get(html_data)
print(pag) # Prints 200 so it is ok.

# Parse the html data using beautiful_soup

pag_texto=pag.text
text_beau=BeautifulSoup(pag_texto,'html.parser')
tablas=text_beau.findAll('table')
print(len(tablas))

# There is 6 tables

[(i,v) for i,v in enumerate(list(tablas)) if "Tesla Quarterly Revenue" in v.text]

# The table "Tesla Quarterly Revenue" is the element number one of the table list

tab_rev=[v for v in list(tablas) if "Tesla Quarterly Revenue" in v.text][0]
tr_rev=tab_rev.findAll('tr')
td_rev=tab_rev.findAll('td')
print(td_rev)

list_td=[v.findAll('td') for i,v in enumerate(tr_rev)][1:]

# I create a list with the table data filtering the NULL cases and removing the $ and commas.

list_data=[(v[0].text,v[1].text.replace('$','').replace(',','')) for i,v in enumerate(list_td) if (v[1].text is not str()) & (v[0].text is not str())]

# With the list of tuples i create a Data Frame

df_tesla=pd.DataFrame(list_data, columns=['Date','Revenue'])
print(df_tesla)

type(df_tesla)

# Insert the data into sqlite3

records = df_tesla.to_records(index=False)
tuples_rec = list(records)
tuples_rec

# Connect to SQLite
# Conect a connection object
conn=sqlite3.connect('Tesla.db')

# Create a cursor
cur = conn.cursor()

###################
cur.execute('''DROP TABLE revenue''')
conn.commit()
####################

# Create table
cur.execute('''CREATE TABLE revenue
(Date, Revenue)''')



# Insert the values
cur.executemany('INSERT INTO revenue VALUES (?,?)', tuples_rec)

# Save (commit) the changes
conn.commit()

# Retrive information from the db
df_revenue=pd.read_sql('SELECT * FROM revenue',conn)
#print(df_revenue)

conn.close()

# Plot revenue vs date

df_revenue['Revenue']=df_revenue['Revenue'].astype('float64')
df_revenue['Date']=pd.to_datetime(df_revenue['Date'])

df_revenue.dtypes

df_revenue.plot('Date','Revenue')
plt.title('Revenue evolution')
plt.xlabel('Date')
plt.show()