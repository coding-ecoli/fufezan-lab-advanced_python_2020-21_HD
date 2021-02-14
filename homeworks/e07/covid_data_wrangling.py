import pandas as pd
import numpy as np
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json
import urllib.request
import plotly
import plotly.graph_objs as go
import plotly.express as px
from collections import deque


covid_url = "https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
covid_json_unformated = urllib.request.urlopen(covid_url).read().decode("utf-8")
covid_json = json.loads(covid_json_unformated)
cdf = pd.DataFrame(covid_json['records'])


cdf = cdf.rename(
    columns = {
        'countriesAndTerritories': 'Country',
        'notification_rate_per_100000_population_14-days': '14d-incidence'
}
)


cdf['date_reported'] = pd.to_datetime(cdf['dateRep'], format='%d/%m/%Y', errors='raise')
cdf['14d-incidence'] = pd.to_numeric(cdf['14d-incidence'])

na_mask = cdf['14d-incidence'].notna()
cdf = cdf[na_mask]

cdf['deltaTime_since_start_of_recording'] = cdf['date_reported'] - min(cdf['date_reported'])


# Incosistency - negative values????

cdf['14d-incidence'] = abs(cdf['14d-incidence'])
cdf['cases_weekly'] = abs(cdf['cases_weekly'])
cdf['deaths_weekly'] = abs(cdf['deaths_weekly'])


#from pandas_profiling import ProfileReport

#profile = ProfileReport(cdf, title="Pandas Profiling Report", explorative=True)

#profile.to_widgets()


grp_contintent = cdf[
    [
        'Country',
        'continentExp',
        '14d-incidence',
        'date_reported',
        'deltaTime_since_start_of_recording'
    ]
].sort_values(by = 'date_reported').groupby(
    [
        'continentExp'
    ]
)

grp_countries = cdf[
    [
        'Country',
        'continentExp',
        '14d-incidence',
        'date_reported',
        'deltaTime_since_start_of_recording'
    ]
].sort_values(by = 'date_reported').groupby(
    [
        'Country'
    ]
)


### intuitiv

def plot_14d_incidence_per_continent(grp, continent = 'Europe'):
    '''
    '''
    fig = px.line(
        grp.get_group(continent),
        x='date_reported',
        y='14d-incidence',
        color = 'Country',
        title = f'COVID-19 14 Day Incidence per 100 000 in {continent}'
        )
    fig.show()


continents = cdf['continentExp'].unique()
countries = cdf['Country'].unique()



europe = grp_contintent.get_group('Europe')
europe.sort_values(['Country','deltaTime_since_start_of_recording'], inplace = True)
s_europe = europe['14d-incidence'].rolling(window = 13, center = True).mean()
europe['s_14d-incidence'] = s_europe
fig = px.line(
    europe,
    x = 'date_reported',
    y = 's_14d-incidence',
    color= 'Country',
    title = f'COVID-19 Smoothed (over 3 Months) 14 Day Incidence per 100 000 in Europe'
)
fig.show()




for continent in continents:
    plot_14d_incidence_per_continent(grp_contintent, continent=continent)


for country in countries:
    grp_country = grp_countries.get_group(country)
    for pos, incidence in enumerate(grp_country['14d-incidence']):
        if pos == 0:
            cdf.loc[grp_country.index[pos], 'delta_14d_incidence'] = grp_country.iloc[pos]['14d-incidence']
        else:
            cdf.loc[grp_country.index[pos], 'delta_14d_incidence'] = (grp_country.iloc[pos]['14d-incidence'] - grp_country.iloc[pos-1]['14d-incidence'])


def maximum_rate(df, col = 'delta_14d_incidence'):
    return df.sort_values(col, ascending = False).head(1)

def minimum_rate(df, col = 'delta_14d_incidence'):
    return df.sort_values(col, ascending = True).head(1)

print(cdf[['Country',
        'continentExp',
        '14d-incidence',
        'date_reported',
        'deltaTime_since_start_of_recording',
        'delta_14d_incidence']].groupby(['continentExp']).apply(maximum_rate))
print(cdf[['Country',
        'continentExp',
        '14d-incidence',
        'date_reported',
        'deltaTime_since_start_of_recording',
        'delta_14d_incidence']].groupby(['continentExp']).apply(minimum_rate))




# RADIAL
print(cdf.columns)

rad_cdf = cdf[['Country', 'deaths_weekly', 'popData2019', 'date_reported']]

mask = (rad_cdf['Country'] == 'Germany') | (rad_cdf['Country'] == 'Italy') | (rad_cdf['Country'] == 'Sweden') | (rad_cdf['Country'] == 'Greece')


rad_grp = rad_cdf[mask].groupby('Country')

radial = []
for country, data_frame in rad_grp:
    days = data_frame['date_reported'] - pd.to_datetime(2020, format='%Y')

    radial.append(
            go.Scatterpolar(
                r= (
                    data_frame['deaths_weekly']*100000/data_frame['popData2019']
                    ),
                theta = days.dt.days * 360/365,
                name = country,
        )
        )

layout = {
    'title': {
        'text':'COVID-19 death-rates for Italy, Germany, Sweden and Greece'
    },
    'polar': {
        'angularaxis': {
            'tickmode': 'array',
            'tickvals': [0, 72, 144, 216, 288],
            'ticktext': ['Day 0', 'Day 73', 'Day 146', 'Day 219', 'Day 292']
        },
        'radialaxis': {
            'dtick': 2,
        }
    }
}
fig = go.Figure(data=radial, layout=layout)
fig.show()