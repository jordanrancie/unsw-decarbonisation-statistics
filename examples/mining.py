import pandas as pd
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

import networkx as nx
import math
import random


# Get the data, remove old records
df_mining = pd.read_csv("data/mining.csv")
df_mining['id'] = df_mining.index
df_mining['percent'] = (df_mining['Capital value'] / df_mining['Capital value'].sum())

df_mining_primary = df_mining.dropna(subset=['Company'])
# df_mining_primary['parent'] = None
# df_mining_primary['percent'] = (df_mining_primary['Capital value'] / df_mining_primary['Capital value'].sum())

df_mining_secondary = df_mining[df_mining['Company'].isna()]


# G = nx.random_geometric_graph(len(df_mining.index), 0.1)
G = nx.Graph()

# sample = df_mining.groupby("id", group_keys=False).apply(lambda x: x.sample(weights=x["percent"]))
# choices = sample.reset_index(drop=True, level=0).index
# df_mining["choice"] = df_mining.index.isin(choices)
# print(df_mining_primary.sample(weights=df_mining["percent"]))  
# print(df_mining['percent'].sum())
# print(df_mining_primary)
# First, lets add the primary
for c, row in df_mining_primary.iterrows():
    G.add_node(row['id'], label=row['Company'], Capital_value=row['Capital value'], id=row['id'], )

for c, row in df_mining_secondary.iterrows():
    G.add_node(row['id'], label="", Capital_value=row['Capital value'], id=row['id'])    

for index in range(1, 2):
    for c, row in df_mining_secondary.iterrows():
        sample = df_mining.sample(1, weights=df_mining["percent"])
        sample2 = df_mining.sample(1)
        # index = sample.reset_index(drop=True, level=0)
        # test = df_mining.index.isin(index).astype(int)
        # t = df_mining.iloc[test]
        # print(f"t - id is {t}")
        # print(sample['id'].values[0])
        # print(f"row id is {row['id']}")
        G.add_edge(*(row['id'], sample['id'].values[0]))
        G.add_edge(*(row['id'], sample2['id'].values[0]))
#     df2 = pd.DataFrame({'Company': [row['Company']], 'Capital value':[ row['Capital value']], 'id': [row['id']], 'parent': [index]})
#     df_mining_primary = pd.concat([df_mining_primary, df2], ignore_index=True)
#     df_mining_primary['percent'] = (df_mining_primary['Capital value'] / df_mining_primary['Capital value'].sum())

pos=nx.circular_layout(G)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    marker_size=df_mining["Capital value"],    
    # marker_color=["red", "green", "blue"],
    marker=dict(
        # showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        # colorscale='YlGnBu',
        # reversescale=True,
        color=["red", "green", "blue"],
        sizeref=max(df_mining['Capital value'] )/(300),
        sizemin=5,        
        # size=50,
        # colorbar=dict(
        #     thickness=15,
        #     title='Node Connections',
        #     xanchor='left',
        #     titleside='right'
        # ),
        line_width=2))


node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
# node_trace.marker.size = node_adjacencies * 100
node_trace.text = df_mining['Company']


#######################

edge_trace_d = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_trace_d = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    # marker_size=df_mining["Data"],    
    # marker_color=["red", "green", "blue"],
    marker=dict(
        # showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        # colorscale='YlGnBu',
        # reversescale=True,
        color=["red", "green", "blue"],
        # sizeref=max(df_mining['Data'] )/(100),
        # sizemin=10,        
        size=10,
        # colorbar=dict(
        #     thickness=15,
        #     title='Node Connections',
        #     xanchor='left',
        #     titleside='right'
        # ),
        line_width=2))


node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace_d.marker.color = node_adjacencies
# node_trace.marker.size = node_adjacencies * 100
# node_trace_d.text = df_mining['Data_formatted']