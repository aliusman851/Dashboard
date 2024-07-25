import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO
import plotly.graph_objects as go



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
   "https://nav.utvecklingfalkenberg.se/items/Gymnaiseelever_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasielever_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Vetlanda"
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        merged_data.append(df_ar1)
        #st.write(merged_data)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Gymnasieelever_M'] = merged_dfram['Gymnasieelever_M'].round(0)
        merged_dfram['Gymnasieelever_K'] = merged_dfram['Gymnasieelever_K'].round(0)
        merged_dfram['Gymnasieelever_T'] = merged_dfram['Gymnasieelever_T'].round(0)
      
   
   selected_kommuner = st.selectbox('Välj kommun(er)', merged_dfram['kommun'].unique(),index=0)
   filtered_data = merged_dfram[merged_dfram['kommun'] == selected_kommuner]
   
   if filtered_data is not None and not filtered_data.empty:
    
       fig = px.line(filtered_data, 
                  x='ar', 
                  y=['Gymnasieelever_K', 'Gymnasieelever_M', 'Gymnasieelever_T'], 
                  #color='kommun', 
                  markers=True, 
                  width=800,
                  title='Gymnasieelever med examen inom 4 år, hemkommun, andel (%)',
                  labels={'ar': 'År', 'value': 'Andel(%)', 'kommun': 'Kommun'},
                  template='plotly_white'
                      )  # You can change the template if you want a different background color

        # Show the plot in Streamlit
       st.plotly_chart(fig)
    
         
         
       output = BytesIO()
       with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
           merged_dfram.to_excel(writer, sheet_name='Sheet1', index=False)
       if not merged_dfram.empty:    
          st.download_button(label='Ladda ner excel', data=output, file_name='ForsskolebarnIndex.xlsx', key='barn')
       else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        