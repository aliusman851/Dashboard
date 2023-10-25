import streamlit as st
import plotly.express as px
import requests
import pandas as pd
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from API")
        return None

# This is first streamlit demo
def show():
   
    api_url = "https://nav.utvecklingfalkenberg.se/items/examinerade_gymnasieelev"

    if api_url:
        # Fetch data
        data = fetch_data(api_url)

        if data:
            # Convert data to a Pandas DataFrame
            df =pd.DataFrame(data)
            df_ar= pd.json_normalize(df['data'])
            fig = px.line(df_ar, x='ar', y='elev', title='Gymnasieelever med examen inom 3 år, kommunala skolor, avvikelse från modellberäknat värde')
            
            st.plotly_chart(fig)
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()