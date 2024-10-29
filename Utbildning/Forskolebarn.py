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
   
    api_url = "https://nav.utvecklingfalkenberg.se/items/Forskolebarn"

    if api_url:
        # Fetch data
        df = fetch_data(api_url)
        melted_data = df.melt(id_vars=['ar','kommun'], value_vars='barn',
                                     var_name='Type', value_name='Value')
        type_labels = {'barn': 'Förskolebarn'}
        melted_data['Type'] = melted_data['Type'].map(type_labels)

        if melted_data is not None and len(melted_data) > 0:
            
            fig = px.line(melted_data, 
                          x='ar', 
                          y='Value',
                         #title='Barn i kommunala förskola, andel(%) av inskrivna barn',
                         markers=True,
                         text='Value',
                         labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                         custom_data=['kommun','Type'],
                         color='Type',
                         height=500,
                         template='plotly_white',
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
                margin=dict(l=0, r=0, t=40, b=20),
                legend=dict(orientation="v", yanchor="bottom", y=1.6, xanchor="right", x=1),
                #responsive=True  # Make the graph responsive
            )
            
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            with st.container():
                st.markdown('<div class="download-button">', unsafe_allow_html=True)    
                st.download_button(
                    label='Ladda ner excel', 
                    data=output, 
                    file_name='Barn i kommunala förskola.xlsx', 
                    key='Forskolebarn')
                st.markdown('</div>', unsafe_allow_html=True) 
           

        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()