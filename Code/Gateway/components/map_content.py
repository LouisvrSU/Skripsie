
from dash import html, dcc
import plotly.express as px
from data import data_func
import pandas as pd
from gpx_converter import Converter

df_map = Converter(input_file='data/map.gpx').gpx_to_dataframe()
# print(df_map)
df_map.head(5)

# Convert GMT to PST and format
# df_map.time = df_map.time.apply(lambda x: x.tz_convert('US/Pacific'))
df_map.time = df_map.time.dt.strftime('%I:%M %p')
df_map.head(5)


# Convert altitude from meters to feet
df_map["alt"] = round(df_map.altitude)
df_map["alt"] = df_map.alt.astype('int')
df_map.head(5)

fig = px.scatter_mapbox(
    df_map, 
    lat="latitude", 
    lon="longitude",
    hover_name="time",
    hover_data={
        "latitude": ":.2f",
        "longitude": ":.2f",
        "alt": ":, m"
    },
    zoom=12, 
    height=500,
    mapbox_style="open-street-map"
)

fig.update_traces(hovertemplate='<b>%{hovertext}</b><br><br>(%{customdata[0]:.2f}, %{customdata[1]:.2f})<br>Elev. %{customdata[2]:} .ft<extra></extra>')

# fig.show()



layout = html.Div([
    
    # df = data_func.read_map()
    dcc.Graph(figure=fig)
])

# @app.callback(
#     Output('datatable-interactivity', 'data'),
#     Input('datatable-interactivity', "page_current"))
# def update_table(page_current):

#     # table_content.page_number = page_current
#     df = data_func.db_update()
    
#     print("update_table_callback")
#     # print(table_content.page_number)
#     lora_func.set_page_number(page_current)
#     print(data)
#     # print(df.index)
#     # table_content.page_number = page_current
#     # print(table_content.page_number)
#     # print(df.iloc[page_current*10:(page_current+ 1)*10].to_dict('records'))
#     # my_data = df.iloc[page_current*10:(page_current+ 1)*10].to_dict('records')
#     my_data = df.to_dict('records')
#     return my_data