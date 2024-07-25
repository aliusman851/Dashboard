import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO
import numpy as np


cached_data = {}
def fetch_data(api_url):
    if api_url in cached_data:
        return cached_data[api_url]
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from API")
        return None
    

def show():
   api_urls =[ 
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Kvalitetsindex_Vetlanda"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        df_ar1['KvalIndex'] = df_ar1['KvalIndex'].round()
        df_ar1['Change'] = df_ar1.groupby('Kommun')['KvalIndex'].diff().fillna(0)
        #st.write(df_ar1)
        """df_ar1['Percentage_Change'] = df_ar1['KvalIndex'].pct_change() * 100
        df_ar1['Percentage_Change'].fillna(0, inplace=True)
        st.write(df_ar1)
        #sorted_df = merged_dfram.sort_values(by='Percentage_Change')
        #min_change = df_ar1['Percentage_Change'].min()
        df_ar1['Positive_Change'] = df_ar1['Percentage_Change'] - df_ar1['Percentage_Change'].min() + 1
        max_change = df_ar1['Positive_Change'].max()
        #epsilon = 1e-10
        df_ar1['Scaled_Change'] = ((df_ar1['Positive_Change'] / max_change)) * 10
        
        st.write(df_ar1)
        #df1 = pd.DataFrame(merged_data)"""
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        #x_range = [max(merged_dfram['Scaled_Change'].min(), 0.1), min(merged_dfram['Scaled_Change'].max(),20)]  # Adjust the lower bound as needed
        
        #st.write(merged_dfram)
       
   if merged_dfram is not None and len(merged_data) > 0:    
    
        fig = px.scatter(merged_dfram,
                       x='ar', 
                       y='KvalIndex',
                       #animation_frame='ar',
                       width=800,
                       #height=400,
                       color ='Kommun',
                       size_max=35,
                       size='KvalIndex',  # Marker size based on 'KvalIndex' values
                       #opacity=1.0,  # Adjust transparency
                       text='Kommun',
                       template='plotly_dark',
                       #range_x=[10,100],
                       range_y=[0,110],
                       title='Kvalitetsindex LSS, andel(%)',
                       labels={'KvalIndex': 'Kvalitetsindex(%)','Kommun': 'Kommun','ar': 'Year'},
                       
                       )
        fig2  =px.scatter(merged_dfram, 
                         x='ar', 
                         y='Change',
                         size_max=20,
                         size='KvalIndex',
                         width=800,
                         #template='plotly_dark', 
                         hover_name='Kommun', 
                         color='Kommun',
                         #color_continuous_scale='RdBu',
                         title='Kvalitetsindex LSS, andel(%)',
                         log_x=True,
                         #range_x=x_range,
                         #range_y=[0,20],
                         #animation_frame='ar',
                         #animation_group='Percentage_Change',
                         #showlegend=True,
                )
       
        st.plotly_chart(fig)
        st.plotly_chart(fig2)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged_dfram.to_excel(writer, sheet_name='Sheet1', index=False)
        if not merged_dfram.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='Kvalitetsindex LSS.xlsx', key='LSS')
        else:
            st.warning("No data to display.")
   else:
    st.warning("No data to display.")
    

if __name__ == "__main__":
    show()