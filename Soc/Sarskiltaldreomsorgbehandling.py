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
   api_url = "https://nav.utvecklingfalkenberg.se/items/sarskilt_aldreomsorgbehandling"

   if api_url:
        # Fetch data
        df = fetch_data(api_url)
        melted_data = df.melt(id_vars=['ar','kommun'], value_vars=['sarskiltboende_totalt', 'sarskiltboende_man', 'sarskiltboende_kvinnor'],
                                     var_name='Type', value_name='Value')
        type_labels = {'sarskiltboende_totalt': 'Totalt', 'sarskiltboende_man': 'Män', 'sarskiltboende_kvinnor': 'kvinnor'}
        melted_data['Type'] = melted_data['Type'].map(type_labels) 

        if melted_data is not None and len(melted_data) > 0:
            
            fig = px.bar(melted_data, 
                          x='ar', 
                          y='Value', 
                          title='Brukarbedömning särskilt boende äldreomsorg-bemötande, andel(%)',
                          template= "plotly_white",
                          labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                          custom_data=['kommun','Type'],
                          color='Type',
                          width=800
                          )
            fig.update_layout(
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False))
            )
            fig.update_traces(hovertemplate="<br>".join([
              "År: %{x}",
              "Andel(%): %{y}",
              "Kommun: %{customdata[0]}",
              "Typ: %{customdata[1]}"
            ])) 
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                melted_data.to_excel(writer, sheet_name='Sheet1', index=False)
            st.download_button(label='Ladda ner excel', data=output, file_name='Särskilt boende äldreomsorg-bemötande.xlsx', key='sarskiltaldreomsorgbehandling')
                 
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()
  