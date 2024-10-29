import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
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
   api_url = "https://nav.utvecklingfalkenberg.se/items/sarskilt_aldreomsorgasikter"

   if api_url:
        # Fetch data
        df = fetch_data(api_url)
        melted_data = df.melt(id_vars=['ar','kommun'], value_vars=['sarskiltboende_totalt', 'sarskiltboende_man', 'sarskiltboende_kvinnor'],
                                     var_name='Type', value_name='Value')
        type_labels = {'sarskiltboende_totalt': 'Totalt', 'sarskiltboende_man': 'Män', 'sarskiltboende_kvinnor': 'kvinnor'}
        melted_data['Type'] = melted_data['Type'].map(type_labels) 

        if melted_data is not None and len(melted_data) > 0:
            
            fig = px._chart_types.line(melted_data, 
                                       x='ar', 
                                       y='Value', 
                                       #title='Brukarbedömning särskilt boende äldreomsorg-hänsyn till åsikter och önskemål, andel(%)',
                                       markers=True,
                                       template=("plotly_white"),
                                       labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                                       height=600,
                                       custom_data=['kommun','Type'],
                                       color='Type',
                                       
                                       )
            fig.update_traces(hovertemplate="<br>".join([
              "År: %{y}",
              "Andel(%): %{x}",
              "Kommun: %{customdata[0]}",
              "Typ: %{customdata[1]}"
            ]))
            fig.update_layout(
                autosize=True,
                xaxis=(dict(showgrid=False)),
                yaxis=dict(showgrid=False),
                margin=dict(l=0, r=0, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
                ) 
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                melted_data.to_excel(writer, sheet_name='Sheet1', index=False)
            with st.container():
                st.markdown('<div class="download-button">', unsafe_allow_html=True)    
                st.download_button(
                    label='Ladda ner excel', 
                    data=output, file_name='Särskilt boende äldreomsorg-hänsyn till åsikter.xlsx', 
                    key='sarskiltasikter')
                st.markdown('</div>', unsafe_allow_html=True) 
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()