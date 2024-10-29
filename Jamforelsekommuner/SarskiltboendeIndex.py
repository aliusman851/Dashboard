import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
from io import BytesIO
import pyarrow as pa




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
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Sarskiltboende_Vetlanda"
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_df = pd.concat(merged_data, ignore_index=True)
        merged_df['Index_Totalt'] = pd.to_numeric(merged_df['Index_Totalt'], errors='coerce').round(0)
        merged_df['datum'] = pd.to_datetime(merged_df['datum'], errors='coerce')
        merged_df.dropna(subset=['Index_Totalt', 'datum','id'], inplace=True)

   if merged_df is not None and len(merged_df) > 0:
     
      fig = px.sunburst(merged_df,
                       values='Index_Totalt',
                       path= ['ar','Kommun','Index_Totalt'],
                       color='Kommun',
                       maxdepth=2,
                       width=600,
                       #height=800,
                       hover_name='Kommun',
                       hover_data={'ar':'År', 'ar': True},
                       #template='plotly_dark',
                       labels={'Index_Totalt': 'Hemtjänst/särskilt boende)Index(%)','id': 'Kommun/År', 'ar': 'År'},
                       branchvalues='total',  # Shows how much of the parent sector is contributed by the children
                       #color_discrete_sequence=px.colors.qualitative.Pastel1
                      
                       
                       
        )
      fig.update_traces(hoverinfo='ar', selector=dict(type='sunburst', hoverinfo='ar'))
      fig.update_traces(hovertemplate= 'Index_Totalt')
      #st.markdown("<h1 style='font-size:15px;'>Brukarbedömning särskiltboende äldreomsorg-bemötande, förtroende,medelvärde — Kommuner,Index andel(%)", unsafe_allow_html=True) 
      fig.update_layout( 
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=20),
        xaxis=(dict(showgrid=False)),
        yaxis=dict(showgrid=False),
        legend=dict(orientation="h", yanchor="bottom", y=0, xanchor="right", x=1),
        )
      #fig.update_traces(textinfo='label+percent entry')
      fig.update_traces(hovertemplate='<b>%{label}</b><br>År: %{customdata[0]}<br>Index(%): %{value:.2f}')
      st.plotly_chart(fig)
     
      output = BytesIO()
      with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
           merged_df.to_excel(writer, sheet_name='Sheet1', index=False)

      if not merged_df.empty:    
           st.download_button(label='Ladda ner excel', data=output, file_name='Hemtjänst/särskilt boende.xlsx', key='boende')
      else:
           st.warning("No data to display.")
   else:
    st.warning("No data to display.")
    

if __name__ == "__main__":
    show()
       


        
        


       