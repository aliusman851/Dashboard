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
   
    api_url = "https://nav.utvecklingfalkenberg.se/items/etablerade_ungdom"

    if api_url:
        # Fetch data
        df = fetch_data(api_url)
        #st.write(df)
        #x_axis_val = st.selectbox('Select X-axis value', options=df.columns)
        st.markdown("<h1 style='font-size:15px;'>Ungdomar som är etablerade på arbetsmarknaden eller studerar 2 år efter slutförd gymnasieutbildning, kommunala skolor, andel(%)", unsafe_allow_html=True)
        selected_column = ['etablerade_kvinnor','etablerade_man', 'etablerade_totalt']
        #all_columns = df.columns
        selected_columns_all = ['Select all'] + selected_column
        selected_columns = st.selectbox('Select y-axis value', options=selected_columns_all)
        df['x'] = df['ar'].astype(str) + '_' + df['id'].astype(str)
        
        if df is not None and len(df) > 0:
            if selected_columns == 'Select all':
                fig = px.bar(df,
                                    x='x', 
                                    y=selected_column,
                                    animation_frame='ar',
                                    width=800,
                                    #color='selected_column',
                                    #barmode='group',
                                    #range_y=[100, [selected_column]],
                                    template='plotly_dark',
                                    #color=selected_column,
                                    #title='Ungdomar som är etablerade på arbetsmarknaden eller studerar 2 år efter slutförd gymnasieutbildning, kommunala skolor, andel(%)',
                                    )
            else: 
                fig = px.funnel(df, 
                                    x='ar', 
                                    y=selected_columns,
                                    color=selected_columns,
                                    width=800,
                                    #animation_frame='x',
                                    #title='Ungdomar som är etablerade på arbetsmarknaden eller studerar 2 år efter slutförd gymnasieutbildning, kommunala skolor, andel(%)',
                                    )
           
            st.plotly_chart(fig)
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Sheet1', index=False)
            st.download_button(label='Ladda ner excel', data=output, file_name='Etebleradeungdomar.xlsx', key='Etableradeundomar')
                 
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()