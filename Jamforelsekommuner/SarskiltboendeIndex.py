import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO




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
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Vetlanda",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Laholm"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_df = pd.concat(merged_data, ignore_index=True)
        merged_df['Index_Totalt'] = merged_df['Index_Totalt'].round()
        #st.write(merged_df)
   
   if merged_data is not None and len(merged_data) > 0:
     
      fig = px.sunburst(merged_df,
                       #x='ar', 
                       #y='Index_Totalt',
                       values='Index_Totalt',
                       path= ['ar','Kommun','Index_Totalt'],
                       color='Kommun',
                       maxdepth=2,
                       width=1500,
                       height=800,
                       hover_name='Kommun',
                       #hover_data={'Index_Totalt': True},
                       template='plotly_dark',
                       labels={'Index_Totalt': 'Hemtjänst/särskilt boende)Index(%)','id': 'Kommun/År', 'ar': 'År'},
                      
                       
                       
        )
      #fig.update_traces(hoverinfo='ar', selector=dict(type='sunburst', hoverinfo='ar'))
      #fig.update_traces(hovertemplate= 'Index_Totalt')
      st.markdown("<h1 style='font-size:15px;'>Brukarbedömning särskiltboende äldreomsorg-bemötande, förtroende,medelvärde — Kommuner,Index andel(%)", unsafe_allow_html=True)
      fig.update_layout( 
          margin = dict(t=0, l=0, r=750, b=0),
          
          showlegend=True,
        )
      st.plotly_chart(fig)
     
      output = BytesIO()
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        merged_df.to_excel(writer, sheet_name='Sheet1', index=False)
        if not merged_df.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='Boendeindex.xlsx', key='boende')
        else:
            st.warning("No data to display.")
   else:
    st.warning("No data to display.")
    

if __name__ == "__main__":
    show()
       


        
        


       