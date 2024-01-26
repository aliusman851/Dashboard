import streamlit as st
import plotly.express as px
import requests
import pandas as pd
from io import BytesIO


def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        res_data = response.json()
        if 'data' in res_data and len(res_data['data']) > 0:
            data = res_data['data']
            # Convert data to a Pandas DataFrame
            df =pd.DataFrame(data)
            #df_ar= pd.json_normalize(df['data'])
            return df
            
        else:
            st.error("Failed to fetch data from API")
            return None
    else:
        st.error("Failed to fetch data from API")
        return None

# This is first streamlit demo
def show():
   api_url = "https://nav.utvecklingfalkenberg.se/items/hemtjanst_aldreomsorgtrygghet"

   if api_url:
        # Fetch data
        df = fetch_data(api_url)

        if df is not None and len(df) > 0:
            
            fig = px.bar( df,
                x= ['hemtjansttrygghet_kvinnor','hemtjansttrygghet_man', 'hemtjansttrygghet_totalt'], 
                y= "ar" ,
                title='Brukarbedömning hemtjänst äldreomsorg-trygghet, andel(%)',
                orientation='h',
                template=("plotly_white"),
            
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,4)",
                xaxis=(dict(showgrid=False))
                  )
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            st.download_button(label='Ladda ner excel', data=output, file_name='Aldreomsorgbehandling.xlsx', key='behandlade')
                 
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()