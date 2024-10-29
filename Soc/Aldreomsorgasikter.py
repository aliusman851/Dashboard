import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
from io import BytesIO


def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200 :
        res_data = response.json()
        if 'data' in res_data and len(res_data['data']) > 0:
            data = res_data['data']
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
   api_url = "https://nav.utvecklingfalkenberg.se/items/hemtjanst_aldreomsorgasikter"

   if api_url:
        # Fetch data
        df = fetch_data(api_url)
        #st.write(df)
        melted_data = df.melt(id_vars=['ar','kommun'], value_vars=['hemtjanstasikter_totalt', 'hemtjanstasikter_man', 'hemtjanstasikter_kvinnor'],
                                     var_name='Type', value_name='Value')
        type_labels = {'hemtjanstasikter_totalt': 'Totalt', 'hemtjanstasikter_man': 'Män', 'hemtjanstasikter_kvinnor': 'kvinnor'}
        melted_data['Type'] = melted_data['Type'].map(type_labels) 

        if melted_data is not None and len(melted_data) > 0:
            # Convert data to a Pandas DataFrame
            
            fig = px.line(melted_data,
                           x='ar', 
                           y='Value',
                           color='Type', 
                           #title='Brukarbedömning hemtjänst äldreomsorg-hänsyn till åsikter och önskemål, andel(%)',
                           #color="Scenario",
                           markers=True,
                           height=600,
                           custom_data=['kommun','Type'],
                           labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                           template='plotly_dark',
                           )
            
            fig.update_traces(hovertemplate="<br>".join([
              "År: %{x}",
              "Andel(%): %{y}",
              "Kommun: %{customdata[0]}",
              "Typ: %{customdata[1]}"
            ]))
            fig.update_layout(
                autosize=True,
                xaxis=(dict(showgrid=False)),
                yaxis=dict(showgrid=False),
                legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
                #responsive=True  # Make the graph responsive
            )
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                melted_data.to_excel(writer, sheet_name='Sheet1', index=False)
            with st.container():
                st.markdown('<div class="download-button">', unsafe_allow_html=True)     
                st.download_button(
                    label='Ladda ner excel', 
                    data=output, file_name='Äldreomsorg-hänsyn till åsikter.xlsx', 
                    key='asikter')
                st.markdown('</div>', unsafe_allow_html=True) 
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()