import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns




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
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Vetlanda",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasielever_Laholm"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Gymnasieelever_M'] = merged_dfram['Gymnasieelever_M'].round(0)
        merged_dfram['Gymnasieelever_K'] = merged_dfram['Gymnasieelever_K'].round(0)
        merged_dfram['Gymnasieelever_T'] = merged_dfram['Gymnasieelever_T'].round(0)
        #merged_df = merged_dfram.sort_values(by='ar')
        st.write(merged_dfram)
   if merged_dfram is not None and len(merged_data) > 0:
        #year_options = merged_dfram['ar'].unique().tolist()
        #year = st.selectbox('select year', year_options,0)
        #merged_dfram = merged_dfram[merged_dfram['ar']==year]
        plt.figure(figsize=(10, 6))
        fig, ax= plt.subplot()
        ax.barplot(data=merged_dfram, x='kommun', y='Gymnasieelever_K', color='skyblue', label='Femlae')
        ax.barplot(data=merged_dfram, x='kommun', y='Gymnasieelever_M', color='orange', label='Male')
        ax.barplot(data=merged_dfram, x='kommun', y='Gymnasieelever_T', color='green', label='Total')
        plt.title('High School Graduates by Municipality')
        plt.xlabel('Municipality')
        plt.ylabel('Number of Graduates')
        plt.legend()
        st.pyplot(fig)
        st.markdown("<h1 style='font-size:15px;'>Barn 1-5 år inskrivna i förskola, andel (%)", unsafe_allow_html=True)
         
         
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