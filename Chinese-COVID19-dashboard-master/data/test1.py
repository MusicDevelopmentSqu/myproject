import pandas as pd
from datetime import datetime, timedelta,date
import math
import plotly.graph_objects as go
import plotly.express as px
import dash
import dash_table
from dash_table.Format import Format
import dash_table.FormatTemplate as FormatTemplate
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


input_list = [
    Input('datatable-interact-location', 'derived_virtual_selected_rows'),
    Input('datatable-interact-location', 'selected_row_ids'),
]


"""
Scraping the data from Johns Hopkins CSSE

"""

# get the date of yesterday and the day before yesterday and convert them to the m-d-Y format
yesterday = (date.today() + timedelta(days = -1)).strftime("%m-%d-%Y")
before_yesterday = (date.today() + timedelta(days = -2)).strftime("%m-%d-%Y")

#the url of global daily reports provided by Johns Hopkins University
address = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/"
url1 = address + yesterday + ".csv"
url2 = address + before_yesterday + ".csv"

# load the csv data into pandas.DataFrame
# and test whether yesterday data has been update yet
try:
    p_td = pd.read_csv(url1)
except:
    p_td = pd.read_csv(url2)
# Only show the data about Australia
# get the summary data for each state in Australia
data_td = p_td[p_td['Country_Region'] == 'Australia']
data_td = data_td.drop(["FIPS", "Admin2"], axis=1)
data_td = data_td.reset_index(drop=True)
data_td.drop(columns=['Combined_Key'], inplace=True)
data_td['Population'] = [412576, 7544000, 211945, 5071000, 1677000, 515000, 6359000, 2589000]
data_td = data_td.astype({'Last_Update': 'datetime64'})
data_td['Death Rate'] = data_td['Deaths'] / data_td['Confirmed']
data_td['Confirmed/100k'] = ((data_td['Confirmed'] / data_td['Population'])*100000).round()
data_td.drop(columns = 'Population', inplace=True)
data_td = data_td[['Province_State', 'Country_Region','Active', 'Confirmed', 'Recovered','Deaths','Death Rate', 'Confirmed/100k','Last_Update', 'Lat', 'Long_']]

# url of the time series data of global confirmed cases
url_hc= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
# url of the time series data of global death cases
url_hd= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
# url of the time series data of global recovered cases
url_hr= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
p_hc = pd.read_csv(url_hc)
p_hd = pd.read_csv(url_hd)
p_hr = pd.read_csv(url_hr)

# Time series data of Australia Confrimed cases
data_hc = p_hc[p_hc['Country/Region'] == 'Australia']
data_hc = data_hc.reset_index(drop=True)
data_hc  = data_hc.drop(columns = ['Country/Region', 'Lat', 'Long'])
df0 = pd.DataFrame(data_hc.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
df1 = pd.DataFrame(data_hc.stack()[1], columns= ['NSW']).drop('Province/State')
df2 = pd.DataFrame(data_hc.stack()[2], columns= ['Northern Territory']).drop('Province/State')
df3 = pd.DataFrame(data_hc.stack()[3], columns= ['Queensland']).drop('Province/State')
df4 = pd.DataFrame(data_hc.stack()[4], columns= ['South Australia']).drop('Province/State')
df5 = pd.DataFrame(data_hc.stack()[5], columns= ['Tasmania']).drop('Province/State')
df6 = pd.DataFrame(data_hc.stack()[6], columns= ['Victoria']).drop('Province/State')
df7 = pd.DataFrame(data_hc.stack()[7], columns= ['Western Australia']).drop('Province/State')
df_confirmed = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
list1 = []
list2 = []
for i in range(len(df_confirmed)):
    list1.append(df_confirmed.index[i])
    list2.append(df_confirmed.iloc[i].sum())
df_confirmed = pd.DataFrame({'Date':list1, 'Total':list2})


# Time series data of Australia Deaths
data_hd = p_hd[p_hd['Country/Region'] == 'Australia']
data_hd = data_hd.reset_index(drop=True)
data_hd  = data_hd.drop(columns = ['Country/Region', 'Lat', 'Long'])
df0 = pd.DataFrame(data_hd.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
df1 = pd.DataFrame(data_hd.stack()[1], columns= ['NSW']).drop('Province/State')
df2 = pd.DataFrame(data_hd.stack()[2], columns= ['Northern Territory']).drop('Province/State')
df3 = pd.DataFrame(data_hd.stack()[3], columns= ['Queensland']).drop('Province/State')
df4 = pd.DataFrame(data_hd.stack()[4], columns= ['South Australia']).drop('Province/State')
df5 = pd.DataFrame(data_hd.stack()[5], columns= ['Tasmania']).drop('Province/State')
df6 = pd.DataFrame(data_hd.stack()[6], columns= ['Victoria']).drop('Province/State')
df7 = pd.DataFrame(data_hd.stack()[7], columns= ['Western Australia']).drop('Province/State')
df_death = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
list1 = []
list2 = []
for i in range(len(df_death)):
    list1.append(df_death.index[i])
    list2.append(df_death.iloc[i].sum())
df_death = pd.DataFrame({'Date':list1, 'Total':list2})

# Times series data of Australia recovered cases
data_hr = p_hr[p_hr['Country/Region'] == 'Australia']
data_hr = data_hr.reset_index(drop=True)
data_hr  = data_hr.drop(columns = ['Country/Region', 'Lat', 'Long'])
df0 = pd.DataFrame(data_hr.stack()[0], columns= ['Australian Capital Territory']).drop('Province/State')
df1 = pd.DataFrame(data_hr.stack()[1], columns= ['NSW']).drop('Province/State')
df2 = pd.DataFrame(data_hr.stack()[2], columns= ['Northern Territory']).drop('Province/State')
df3 = pd.DataFrame(data_hr.stack()[3], columns= ['Queensland']).drop('Province/State')
df4 = pd.DataFrame(data_hr.stack()[4], columns= ['South Australia']).drop('Province/State')
df5 = pd.DataFrame(data_hr.stack()[5], columns= ['Tasmania']).drop('Province/State')
df6 = pd.DataFrame(data_hr.stack()[6], columns= ['Victoria']).drop('Province/State')
df7 = pd.DataFrame(data_hr.stack()[7], columns= ['Western Australia']).drop('Province/State')
df_recovered = pd.concat([df0, df1, df2, df3, df4, df5, df6, df7], axis =1)
list1 = []
list2 = []
for i in range(len(df_recovered)):
    list1.append(df_recovered.index[i])
    list2.append(df_recovered.iloc[i].sum())
df_recovered = pd.DataFrame({'Date':list1, 'Total':list2})