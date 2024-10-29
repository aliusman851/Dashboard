import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
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
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        #x_range = [max(merged_dfram['Scaled_Change'].min(), 0.1), min(merged_dfram['Scaled_Change'].max(),20)]  # Adjust the lower bound as needed
        
        #st.write(merged_dfram)
   selected_kommuner = st.multiselect('Välj kommun(er)', merged_dfram['Kommun'].unique(),default=merged_dfram['Kommun'].unique()[0])
   filtered_data = merged_dfram[merged_dfram['Kommun'].isin(selected_kommuner)]
   #st.write(filtered_data)
     
   if filtered_data is not None and len(filtered_data) > 0:    
    
        fig = px.scatter(filtered_data,
                       x='ar', 
                       y='KvalIndex',
                       width=600,
                       #height=400,
                       color ='Kommun',
                       size_max=35,
                       size='KvalIndex',  # Marker size based on 'KvalIndex' values
                       #opacity=1.0,  # Adjust transparency
                       text='KvalIndex',
                       template='plotly_dark',
                       #range_x=[10,100],
                       range_y=[0,110],
                       #title='Kvalitetsindex LSS, andel(%)',
                       labels={'KvalIndex': 'Kvalitetsindex(%)','Kommun': 'Kommun','ar': 'År'},
                       
            )
        fig.update_layout(
                autosize=True,
                xaxis=(dict(showgrid=False)),
                yaxis=dict(showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1.2, xanchor="right", x=1),
                #responsive=True  # Make the graph responsive
            )
        
        st.plotly_chart(fig)
        #st.plotly_chart(fig2)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)
        if not filtered_data.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='Kvalitetsindex LSS.xlsx', key='LSS')
        else:
            st.warning("No data to display.")
   else:
    st.warning("No data to display.")
    

if __name__ == "__main__":
    show()