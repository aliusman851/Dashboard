import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
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
   check_data['Kommun_Type'] = check_data['Kommun'] + ' - ' + check_data['Type']     
   selected_kommuner = st.multiselect('Välj kommun(er)', check_data['Kommun'].unique(),default=check_data['Kommun'].unique()[0])
   check_data['ar'] = check_data['ar'].astype(int)
   years = range(check_data['ar'].min(), check_data['ar'].max() + 1)
   check_data['Kommun'] = check_data['Kommun'].astype(str)
   full_index = pd.MultiIndex.from_product([selected_kommuner, years], names=['Kommun', 'ar'])
   full_df = pd.DataFrame(index=full_index).reset_index() 
   merged_dfram_filled = pd.merge(full_df, check_data, on=['Kommun', 'ar'], how='left')
   #filtered_data = check_data[check_data['Kommun'].isin(selected_kommuner)]
   selected_typ = st.multiselect('Välj typ', check_data['Type'].unique(),default=check_data['Type'].unique()[0])
   check_data['Type'] = check_data['Type'].astype(str)
   merged_dfram_filled['Type'] = merged_dfram_filled['Type'].astype(str)
   #filtered_data = check_data[check_data['Type'].isin(selected_typ)]
   filtered_data = merged_dfram_filled[
    (merged_dfram_filled['Kommun'].isin(selected_kommuner)) & 
    (merged_dfram_filled['Type'].isin(selected_typ))
]
   if filtered_data is not None and not filtered_data.empty:
       
        #numeric_columns = merged_dfram.select_dtypes(include='number')
        fig = px.line(filtered_data, 
                  x='ar', 
                  y='Value',
                  color='Kommun_Type',
                  #color=['Value_K', 'Value_M', 'Value_T'],
                  hover_data={'Kommun': True} ,  # Include additional hover data 
                  markers=True, 
                  width=500,
                  #range_y=[10,40],
                  #title='Invånare 16-84 år med avsaknad av tillit till andra, andel (%) ',
                  labels={'ar': 'År', 'Value': 'Andel(%)','Type':'typ'},
                  template='plotly_white'
                    )  # You can change the template if you want a different background color

        # Show the plot in Streamlit
        fig.update_traces(customdata=filtered_data[['Kommun', 'Type']].values) 
        fig.update_layout(
                autosize=True,
                xaxis=(dict(showgrid=False)),
                yaxis=dict(showgrid=False),
                #margin=dict(l=0, r=0, t=40, b=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.2, xanchor="right", x=1),
                #responsive=True  # Make the graph responsive
            )
        st.plotly_chart(fig)
          

        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)
        if not filtered_data.empty:
            with st.container():
                st.markdown('<div class="download-button">', unsafe_allow_html=True)     
                st.download_button(
                    label='Ladda ner excel', 
                    data=output, 
                    file_name='Tillitlös.xlsx', 
                    key='Tillit')
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        