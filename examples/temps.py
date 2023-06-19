import pandas as pd
import numpy as np
import plotly.express as px
pd.set_option('display.max_rows',100)

# Get the data
df_temp = pd.read_csv("data/GlobalTemperatures.csv")
df_temp = df_temp[df_temp['dt'] >= '1900-01-01'] # .dropna()
df_temp['year'] = pd.DatetimeIndex(df_temp['dt']).year

# Land Only
df_temp_land = df_temp.groupby('year').agg(Average=('LandAverageTemperature', np.mean)).reset_index()
df_temp_land['Measurement'] = 'Land Only'

# Model for 1900 - 1950
df_temp_model1 = df_temp_land[df_temp_land['year'] <= 1950]
m_1,c_1 = np.polyfit(df_temp_model1['year'], df_temp_model1['Average'], 1)

# Model for 1950 - 1990
df_temp_model2 = df_temp_land[(df_temp_land['year'] >= 1900) & (df_temp_land['year'] <= 1970)]
m_2,c_2 = np.polyfit(df_temp_model2['year'], df_temp_model2['Average'], 1)

# Model for 1990 - 2015
df_temp_model3 = df_temp_land[df_temp_land['year'] >= 1960]
m_3,c_3 = np.polyfit(df_temp_model3['year'], df_temp_model3['Average'], 1)

# Add projections
# Model 1
df_temp_land['model1'] =  m_1*df_temp_land['year'] + c_1
# Model 2
# df_temp_land = pd.concat([df_temp_land, pd.DataFrame({'year': range(2016, 2050)})])
df_temp_land['model2'] =  m_2*df_temp_land['year'] + c_2
# Model 3
df_temp_land = pd.concat([df_temp_land, pd.DataFrame({'year': range(2050, 2070)})])
df_temp_model3 = df_temp_land[df_temp_land['year'] >= 1960]
df_temp_model3['model3'] =  m_3*df_temp_model3['year'] + c_3
df_temp_land = df_temp_land.merge(df_temp_model3, how='left')

### Land AND Ocean
df_temp_ocean = df_temp.groupby('year').agg(Average=('LandAndOceanAverageTemperature', np.mean)).reset_index()
df_temp_ocean['Measurement'] = 'Land and Ocean'

# Model for 1900 - 1950
df_temp_model1 = df_temp_ocean[df_temp_ocean['year'] <= 1950]
m_1,c_1 = np.polyfit(df_temp_model1['year'], df_temp_model1['Average'], 1)

# Model for 1950 - 1990
df_temp_model2 = df_temp_ocean[(df_temp_ocean['year'] >= 1900) & (df_temp_ocean['year'] <= 1970)]
m_2,c_2 = np.polyfit(df_temp_model2['year'], df_temp_model2['Average'], 1)

# Model for 1990 - 2015
df_temp_model3 = df_temp_ocean[df_temp_ocean['year'] >= 1960]
m_3,c_3 = np.polyfit(df_temp_model3['year'], df_temp_model3['Average'], 1)

# Add projections
# Model 1
df_temp_ocean['model1'] =  m_1*df_temp_ocean['year'] + c_1
# Model 2
# df_temp_ocean = pd.concat([df_temp_ocean, pd.DataFrame({'year': range(2016, 2050)})])
df_temp_ocean['model2'] =  m_2*df_temp_ocean['year'] + c_2
# Model 3
df_temp_ocean = pd.concat([df_temp_ocean, pd.DataFrame({'year': range(2050, 2070)})])
df_temp_model3 = df_temp_ocean[df_temp_ocean['year'] >= 1960]
df_temp_model3['model3'] =  m_3*df_temp_model3['year'] + c_3
df_temp_ocean = df_temp_ocean.merge(df_temp_model3, how='left')





print(df_temp_land)
# print(pd.DataFrame({'year': range(2016, 2050)}))
# print(m_2, c_2)
# print(m_3, c_3)

# print(df_temp_ocean.info())
# # print(pd.DataFrame({'dt': pd.date_range(start='1/1/2016', end='1/1/2100', freq='MS')}))
