import pandas as pd
import plotly.express as px
pd.set_option('display.max_rows',100)

df2 = pd.read_csv("2020GlobalEmissions.csv")
fig = px.icicle(df2, 
title = 'Share of CO2 Emissions per Continent (%)',
path=[px.Constant("World"), 'continent', 'country'], values='share_global_co2')
fig.update_traces(root_color="lightgrey")
fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
fig.show()