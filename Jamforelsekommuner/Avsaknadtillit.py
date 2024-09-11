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
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Ornskldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Vetlanda"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        #st.write(merged_data)
        merged_dfram['Value_K'] = pd.to_numeric(merged_dfram['Value_K'], errors='coerce').round(0)
        merged_dfram['Value_M'] = pd.to_numeric(merged_dfram['Value_M'], errors='coerce').round(0)
        merged_dfram['Value_T'] = pd.to_numeric(merged_dfram['Value_T'], errors='coerce').round(0)
   check_data = merged_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'], var_name='Type', value_name='Value')     
   type_labels = {'Value_K': 'Kvinnor', 'Value_M': 'Män', 'Value_T': 'Totalt(Kvinnor och män)'}
   check_data['Type'] = check_data['Type'].map(type_labels)      
   selected_kommuner = st.multiselect('Välj kommun(er)', check_data['Kommun'].unique(),default=check_data['Kommun'].unique()[0])
   filtered_data = check_data[check_data['Kommun'].isin(selected_kommuner)]
      
   #selected_kommuner = st.selectbox('Välj kommun(er)', merged_dfram['Kommun'].unique(),index=0)
   #filtered_data = merged_dfram[merged_dfram['Kommun'] == selected_kommuner]
   #numeric_columns = filtered_data.select_dtypes(include='number')
   #st.write(numeric_columns)
   
   if filtered_data is not None and not filtered_data.empty:
       
        #numeric_columns = merged_dfram.select_dtypes(include='number')
        fig = px.line(filtered_data, 
                  x='ar', 
                  y='Value',
                  color='Type',
                  #color=['Value_K', 'Value_M', 'Value_T'],
                  hover_data={'Kommun': True} ,  # Include additional hover data 
                  markers=True, 
                  width=800,
                  #range_y=[10,40],
                  title='Invånare 16-84 år med avsaknad av tillit till andra, andel (%) ',
                  labels={'ar': 'År', 'Value': 'Andel(%)','Type':'typ'},
                  template='plotly_white'
                    )  # You can change the template if you want a different background color

        # Show the plot in Streamlit
        st.plotly_chart(fig)
          

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)
        if not filtered_data.empty:    
           st.download_button(label='Ladda ner excel', data=output, file_name='Tillitlös.xlsx', key='Tillit')
        else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        