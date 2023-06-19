import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

import networkx as nx
import math
import random


# Get the data, remove old records
df_mining_world = pd.read_csv("data/mining_world.csv")
df_mining_world['isAus'] = df_mining_world['Country'] == 'Australia'
df_mining_world['percent'] = (df_mining_world['Tonnes'] / df_mining_world['Tonnes'].sum())
