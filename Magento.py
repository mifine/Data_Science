import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os
import glob

## To call Magento BI API
import json
import requests

%matplotlib inline

path = "c:/Users/XXX"
api_key = "XXXX"
client_id = "XXX"
figure_id = "2038156"


def format_dataframe(daf):
    daf['Region'] = ['EU' if str(x)[:2] == "14" else 'GB' for x in df['increment_id']]
    daf['Date'] = [str(x)[:10] for x in df['created_at']]
    daf['Date'] = pd.to_datetime(daf['Date'], format='%Y-%m-%d')
    daf.fillna(value=0, inplace=True)
    daf['Revenues_USD'] = [ 1.16*x + 1.3*y for x, y in zip(daf['Revenues EUR'], daf['Revenues GBP']) ]
    daf = daf.groupby(["Date", "Region"], as_index=False)['Revenues_USD'].sum()
    #daf = daf.groupby(["Date", "Region"])['Revenues_USD'].sum()
    return daf

#Display the values
def display_graph(daf):
    fig, ax = plt.subplots(figsize=(20,10))    
    matplotlib.style.use('ggplot')
    
    ax.set_title('Revenues USD - EU Gear Store')
    ax.set_ylabel('Revenues USD')
    ax.set_xlabel('Date')
    
    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()
    
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=3))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
    daf.set_index('Date',inplace=True)
    ax.bar(daf.index, daf['Revenues_USD'])
    return daf

   # daf.plot(kind="bar", ax=ax, stacked=True, grid=True)

    #daf.plot.bar(stacked=True)
    
#Main function
def main(daf):
    daf = format_dataframe(daf)
    display_graph(daf)
    return daf

#API Call to rjmetrics API
def retrieve_data():
    h = {'X-RJM-API-Key': api_key}
    url = 'https://api/rjmetrics.com/0.1/figure/' + figure_id + '/export'
    response = requests.get(url, headers=h)
    print("Response Code: " + str(response.status_code))
    

# Display the graph
filename = max(glob.iglob(path + "*.csv"), key=os.path.getmtime)[len(path):]
df = pd.read_csv(filename, skiprows=1)
picture = main(df)
