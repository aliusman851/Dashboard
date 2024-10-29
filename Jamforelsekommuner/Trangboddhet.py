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
   api_urls = [
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Falkenberg",     
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Vetlanda",
   
   
   ]
   merged_data = []
   all_min_value=[]
   all_max_value=[]
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value_K'] = pd.to_numeric(merged_dfram['Value_K'], errors='coerce').round(0)
        merged_dfram['Value_M'] = pd.to_numeric(merged_dfram['Value_M'], errors='coerce').round(0)
        merged_dfram['Value_T'] = pd.to_numeric(merged_dfram['Value_T'], errors='coerce').round(0)
        merged_dfram['ar'] = merged_dfram['ar'].astype(int)  
      
   years = merged_dfram['ar'].unique()
   municipalities = merged_dfram['Kommun'].unique()
   complete_index = pd.MultiIndex.from_product([years, municipalities], names=['ar', 'Kommun'])
   complete_dfram = merged_dfram.set_index(['ar', 'Kommun']).reindex(complete_index).reset_index()
   complete_dfram[['Value_K', 'Value_M', 'Value_T']] = complete_dfram[['Value_K', 'Value_M', 'Value_T']].fillna(0)
   check_data = complete_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'], var_name='Type', value_name='Value')
   type_labels = {'Value_K': 'Kvinnor', 'Value_M': 'Män', 'Value_T': 'Totalt(Kvinnor och män)'}
   check_data['Type'] = check_data['Type'].map(type_labels)
   #st.write(check_data)
   value_type = st.selectbox('Välj Värdetyp', check_data['Type'].unique())
   
   filtered_data = check_data[check_data['Type'] == value_type]
   fig = px.line(filtered_data,
                    x='ar',
                    y='Value',
                    markers='Value',
                    color='Kommun',
                    #line_group= 'Kommun',
                    hover_name='Kommun',
                    labels={'ar': 'År', 'Value': 'Andel(%)'},

                    
                )
   
   fig.update_layout(
            xaxis_title='År',
            yaxis_title='Andel(%)',
            width=500,
            autosize=True,
            xaxis=dict(showgrid=False),  # Smaller font size for axis titles
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins for mobile
            legend=dict(orientation="h", yanchor="bottom", y=1.2, xanchor="right", x=1),
           )  # Adjust gap between bars
                  
   st.write(fig)
   
   output = BytesIO()
   with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)
   if not filtered_data.empty:    
        st.download_button(label='Ladda ner excel', data=output, file_name='Trångboddhet i flerbostadshus.xlsx', key='barn')
   else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()            