import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
pd.set_option('display.max_rows',100)

from examples.co2 import df_co2_global, df_co2_latest_by_area, df_co2_latest_global, df_co2_latest_by_country, df_co2_by_sector
from examples.temps import df_temp_ocean, df_temp_land
from examples.mining import edge_trace, node_trace, edge_trace_d, node_trace_d
from examples.mining_world import df_mining_world

app = Dash(__name__)

app.layout = html.Div([
    # html.H4('Animated GDP and population over decades'),
    html.P("Select an animation:"),
    dcc.RadioItems(
        id='animations-x-selection',
        options=[
            "Global CO2 emissions - 1900 to 2020",
            "Temperature forecast (Land Only) - 1900 to 2100",
            "Temperature forecast (Land and Ocean) - 1900 to 2100",
            "CO2 emissions globally (2022)",
            "CO2 emissions by area (2022)",
            "CO2 emissions by country (2022)",
            "CO2 emissions by sector (2022)",
            "CO2 emissions Mining (2022)",
            "CO2 emissions Australia in World (2022)"  ,
            "CO2 emissions Australia (2022)",
            "Mining World (2022)",
            "Mining World Australia (2022)",
            "Mining by size",
            "Mining by data"         
            ],
        value='Mining by data',
    ),
    dcc.Loading(dcc.Graph(id="animations-x-graph", style={'height': '50vh'}), type="cube")
])

@app.callback(
    Output("animations-x-graph", "figure"), 
    Input("animations-x-selection", "value"))
def display_animated_graph(selection):
  
    animations = {
        'Global CO2 emissions - 1900 to 2020': px.line(
            df_co2_global,
            x="year",
            y="co2",
            title='Global CO2 emissions - 1900 to 2050',
                labels = {
                    "co2": "CO₂ (Gigatonnes)"
                },
        ).update_layout(
            font=dict(size=16)
        ),
        'Temperature forecast (Land Only) - 1900 to 2100': px.scatter(
            df_temp_land,
            x="year",
            y="Average",
            # trendline="lowess",
            # # trendline_options=dict(log_y=True),
            # trendline_color_override="gray",
            # log_y=True,
            color_discrete_sequence=['blue'],
            title='Temperature forecast (Land Only) - 1900 to 2100',
                 labels={
                     "Average": "Temperature (C)"
                 },
        # ).update_layout(xaxis_range=[1950,2100]  
        # ).add_trace(
        #     go.Scatter(x=df_temp_land['year'],
        #     y=df_temp_land['model1'], name="slope", line_shape='linear')   
        ).add_trace(
            go.Scatter(x=df_temp_land['year'],
            y=df_temp_land['model2'], name="Best fit (1900-1970)", line_shape='linear', text="test")   
        ).add_trace(
            go.Scatter(x=df_temp_land['year'],
            y=df_temp_land['model3'], name="Best fit (1960-2020)", line_shape='linear') 
        ).update_layout(
            font=dict(size=16),                                           
        ).add_hline(
                y=8.7, line_width=1,
                line_dash="dash", 
                line_color="gray",
                annotation_text="0.0 C",
                annotation_position="bottom", 
        ).add_hline(
                y=9.7, line_width=2,
                line_dash="dash", 
                line_color="gray",
                annotation_text="1.0 C",
                annotation_position="bottom", 
        ).add_hrect(
                y0=10.2,
                y1=11.2, 
                # annotation_text="decline",
                # annotation_position="bottom left",
                fillcolor="red",
                opacity=0.1,
                line_width=0
        ).add_hline(
                y=10.7, line_width=1, 
                line_dash="dash",
                line_color="red",
                annotation_text="2.0C",
                annotation_position="bottom", 
        ).add_hline(
                y=11.2, line_width=2,
                line_dash="dash", 
                line_color="red",    
                annotation_text="Increae by 2.5C",
                annotation_position="bottom",                           
        ),
        'Temperature forecast (Land and Ocean) - 1900 to 2100': px.scatter(
            df_temp_ocean,
            x="year",
            y="Average",
            # trendline="lowess",
            # # # trendline_options=dict(log_y=True),
            # trendline_color_override="gray",
            color_discrete_sequence=['red'],
            title='Temperature forecast (Land and Ocean) - 1950 to 2100',
                 labels={
                     "Average": "Temperature (C)"
                 },            
        # ).update_layout(xaxis_range=['01-01-1950',2100]
        # ).update_layout(xaxis_range=[1950,2100]  
        # ).add_trace(
        #     go.Scatter(x=df_temp_land['year'],
        #     y=df_temp_land['model1'], name="slope", line_shape='linear')   
        ).add_trace(
            go.Scatter(x=df_temp_ocean['year'],
            y=df_temp_ocean['model2'], name="Best fit (1950-1990)", line_shape='linear', text="test")   
        ).add_trace(
            go.Scatter(x=df_temp_ocean['year'],
            y=df_temp_ocean['model3'], name="Best fit (1990-2020)", line_shape='linear')    
        ).update_layout(
            font=dict(size=16),                  
        ).add_hline(
                y=15.35, line_width=1,
                line_dash="dash", 
                line_color="gray",
                annotation_text="0.0 C",
                annotation_position="bottom", 
        ).add_hline(
                y=16.35, line_width=2,
                line_dash="dash", 
                line_color="gray",
                annotation_text="1.0 C",
                annotation_position="bottom", 
        ).add_hrect(
                y0=16.85,
                y1=17.85, 
                # annotation_text="decline",
                # annotation_position="bottom left",
                fillcolor="red",
                opacity=0.1,
                line_width=0
        ).add_hline(
                y=17.35, line_width=1, 
                line_dash="dash",
                line_color="red",
                annotation_text="2.0C",
                annotation_position="bottom",                
        ).add_hline(
                y=17.85, line_width=2,
                line_dash="dash", 
                line_color="red",
                annotation_text="Increae by 2.5C",
                annotation_position="bottom",                     
              
        # ).add_hline(
        #         y=11.2, line_width=2, 
        #         line_color="red",
        #         annotation_text="Increae by 2.5 degrees",
        #         annotation_position="bottom",
        ),   
        'CO2 emissions globally (2022)': go.Figure(
            data=go.Scattergeo(
                locations = df_co2_latest_global['iso_code'],
                mode = 'markers+text',
                # text=df_co2_latest_global['co2'],
                text=['37.12 Billion Tonnes of Co2'],
                textfont={
                        "color": ["White"],
                        # "family": ["Arial, sans-serif", "Balto, sans-serif", "Courier New, monospace",
                        #         "Droid Sans, sans-serif", "Droid Serif, serif",
                        #         "Droid Sans Mono, sans-serif",
                        #         "Gravitas One, cursive", "Old Standard TT, serif",
                        #         "Open Sans, sans-serif",
                        #         "PT Sans Narrow, sans-serif", "Raleway, sans-serif",
                        #         "Times New Roman, Times, serif"],
                        "size": [22]
                    },                
                marker=dict(
                    size=df_co2_latest_global['co2'] ,
                    sizemode='area',
                    color=df_co2_latest_global['colour'],
                    sizeref=2.*max(df_co2_latest_by_area['co2'] )/(12000.**2),
                    sizemin=4,
                    colorbar=dict(
                        title="Tonnes of CO₂ (million)"
                    ),
                    # colorscale= [
                    #     [0, 'rgb(250, 250, 250)'],        #0
                    #     [1./10000, 'rgb(200, 200, 200)'], #10
                    #     [1./1000, 'rgb(150, 150, 150)'],  #100
                    #     [1./100, 'rgb(100, 100, 100)'],   #1000
                    #     [1./10, 'rgb(50, 50, 50)'],       #10000
                    #     [1., 'rgb(0, 0, 0)'],             #100000

                    # ],                    
                    # colorscale="Greys"                      
                ),            
            )), 
        'CO2 emissions by area (2022)': go.Figure(
            data=go.Scattergeo(
                locations = df_co2_latest_by_area['iso_code'],
                mode = 'markers+text',
                text=df_co2_latest_by_area['co2'],
                textfont={
                        "color": ["Green", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White", "White"],
                        # "family": ["Arial, sans-serif", "Balto, sans-serif", "Courier New, monospace",
                        #         "Droid Sans, sans-serif", "Droid Serif, serif",
                        #         "Droid Sans Mono, sans-serif",
                        #         "Gravitas One, cursive", "Old Standard TT, serif",
                        #         "Open Sans, sans-serif",
                        #         "PT Sans Narrow, sans-serif", "Raleway, sans-serif",
                        #         "Times New Roman, Times, serif"],
                        # "size": [22]
                    },                
                marker=dict(
                    size=df_co2_latest_by_area['co2'] ,
                    sizemode='area',
                    color=df_co2_latest_by_area['colour'],
                    sizeref=2.*max(df_co2_latest_by_area['co2'] )/(200.**2),
                    sizemin=4,
                    colorbar=dict(
                        title="Tonnes of CO₂ (million)"
                    ),
                    # colorscale= [
                    #     [0, 'rgb(250, 250, 250)'],        #0
                    #     [1./16, 'rgb(200, 200, 200)'], #10
                    #     [1./8, 'rgb(150, 150, 150)'],  #100
                    #     [1./3, 'rgb(100, 100, 100)'],   #1000
                    #     [1./2, 'rgb(50, 50, 50)'],       #10000
                    #     [1., 'rgb(0, 0, 0)'],             #100000

                    # ],                    
                    colorscale="viridis_r"                      
                ),            
            )),     
        'CO2 emissions by country (2022)': go.Figure(
            data=go.Scattergeo(
                locations = df_co2_latest_by_country['iso_code'],
                mode = 'markers',
                marker=dict(
                    size=df_co2_latest_by_country['co2'] ,
                    sizemode='area',
                    color=df_co2_latest_by_country['sub-region-code'],
                    sizeref=2.*max(df_co2_latest_by_country['co2'] )/(200.**2),
                    sizemin=4,
                    # colorbar=dict(
                    #     title="Tonnes of CO₂ (million)"
                    # ),
                    colorscale = 'viridis'
                    # colorscale= [
                    #     [0, 'rgb(250, 250, 250)'],        #0
                    #     [1./2, 'rgb(200, 200, 200)'], #10
                    #     [1./1.5, 'rgb(150, 150, 150)'],  #100
                    #     [1./1.2, 'rgb(100, 100, 100)'],   #1000
                    #     [1./1.1, 'rgb(50, 50, 50)'],       #10000
                    #     [1., 'rgb(0, 0, 0)'],             #100000

                    # ],                        
                ),            
                marker_color = df_co2_latest_by_country['sub-region-code'],
            )),        
        # 'CO2 emissions by country (2022)': px.scatter_geo(
        #     df_co2_latest_by_country,
        #     locations="iso_code",
        #     color="country",
        #     size="co2"), #.update_traces(marker_sizeref = 2 * max(df_co2_latest_by_country['co2'])),
        'CO2 emissions by sector (2022)': px.sunburst(
            df_co2_by_sector,
            values='Percentage',
            names='Subsector',
            path=['Sector', 'Category', 'Subsector'],
            # color_continuous_scale='RdBu'
            color='Category'
        ).update_traces(textinfo="label+percent parent"),         
        'CO2 emissions Mining (2022)': px.sunburst(
            df_co2_by_sector,
            values='Percentage',
            names='Subsector',
            path=['Sector', 'Category', 'Subsector'],
            # color_continuous_scale='RdBu'
            color='mining'
        ).update_traces(textinfo="label+percent parent"), 
        'CO2 emissions Australia in World (2022)': px.sunburst(
            df_co2_latest_by_country,
            values='co2',
            names='country',
            path=['region', 'sub-region', 'country'],
            # color_continuous_scale='RdBu'
            color='sub-region'
        ).update_traces(textinfo="label+percent parent"),
        'CO2 emissions Australia (2022)': px.sunburst(
            df_co2_latest_by_country,
            values='co2',
            names='country',
            path=['region', 'sub-region', 'country'],
            # color_continuous_scale='RdBu'
            color='isAus'
        ).update_traces(textinfo="label+percent parent"),   
        'Mining World (2022)': px.pie(
            df_mining_world,
            values='Tonnes',
            names='Country',
            # color_continuous_scale='RdBu'
            color='Country'
        ).update_traces(textinfo="label"),  
        'Mining World Australia (2022)': px.pie(
            df_mining_world,
            values='Tonnes',
            names='Country',
            # color_continuous_scale='RdBu'
            color='isAus'
        ).update_traces(textinfo="label"),                  
        "Mining by size": go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Mining network',
                titlefont_size=18,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        ).update_traces(textposition='middle center'
        ).update_layout(
            font=dict(size=20)
        ),     
        "Mining by data": go.Figure(
            data=[edge_trace_d, node_trace_d],
            layout=go.Layout(
                title='Mining network',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
        ).update_traces(textposition='top center'
        ).update_layout(
            font=dict(size=16)
        ),                             
    }
    return animations[selection].update_layout(
        plot_bgcolor='White'
    )  


if __name__ == "__main__":
    app.run_server(debug=True)


