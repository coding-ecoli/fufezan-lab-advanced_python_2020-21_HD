import pandas as pd
import numpy as np
import plotly.express as px
from pandas_profiling import ProfileReport






arabica_df = pd.read_csv('/Users/huuumath/Git/fufezan-lab-advanced_python_2020-21_HD/data/arabica_data_cleaned.csv')

arabica_df = arabica_df.iloc[:, 1:]

col_to_drop = []

for col, d in zip(arabica_df.columns, arabica_df.dtypes):
    if d == 'object':
        if col not in ["Country.of.Origin", "Producer", "Processing.Method"]:
            col_to_drop.append(col)
arabica_df.drop(columns=col_to_drop, inplace=True)

arabica_df.rename(
    columns={
        "Country.of.Origin": "Country of Origin", 
        "Producer": "Producer", 
        "Processing.Method": "Processing Method"
    },
    inplace=True
)

#profile = ProfileReport(arabica_df)
#profile.to_file(output_file = 'output.html')


def remove_outliers(df):
    '''
    '''
    for col, d in zip(df.columns,df.dtypes):
        
        if d != 'object':

            quantile25 = df[col].quantile(0.25)
            quantile75 = df[col].quantile(0.75)

            iqr = quantile75 - quantile25
            
            lower_limit = quantile25 - 1.5*iqr
            upper_limit = quantile75 + 1.5*iqr

            for pos, value in enumerate(df[col]):
                if (value < lower_limit) or (value > upper_limit):
                    df.loc[pos, col] = df[col].quantile(0.5)

                
remove_outliers(df=arabica_df)


#profile = ProfileReport(arabica_df)
#profile.to_file(output_file = 'output.html')

fig = px.bar(
    data_frame = arabica_df['Country of Origin'].value_counts(),
    title = 'Origin of the Coffee?')
fig.show()

producer = px.bar(
    data_frame=arabica_df['Producer'].value_counts(),
    title = 'Producer with the most entries')
producer.show()

method = px.bar(
    data_frame = arabica_df['Processing Method'].value_counts(),
    title = 'Processing Method')
method.show()