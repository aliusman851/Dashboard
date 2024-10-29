import streamlit as st
import plotly.express as px
import requests # type: ignore
import pandas as pd # type: ignore
from io import BytesIO

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
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Deltagare_Vetlanda",
   
   
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

   melted_data = merged_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'],
                                     var_name='Type', value_name='Value')
   type_labels = {'Value_T': 'Totalt', 'Value_M': 'Män', 'Value_K': 'kvinnor'}
   melted_data['Type'] = melted_data['Type'].map(type_labels) 
   melted_data['Kommun_Type'] = melted_data['Kommun'] + ' - ' + melted_data['Type']
   selected_kommuner = st.multiselect('Välj kommun(er)', melted_data['Kommun'].unique(),default=melted_data['Kommun'].unique()[0])
   filtered_data = melted_data[melted_data['Kommun'].isin(selected_kommuner)]
   selected_typ = st.multiselect('Välj typ', melted_data['Type'].unique(),default=melted_data['Type'].unique()[0])
   #filtered_data = check_data[check_data['Type'].isin(selected_typ)]
   filtered_data = melted_data[
    (melted_data['Kommun'].isin(selected_kommuner)) & 
    (melted_data['Type'].isin(selected_typ))
    ]
   
   if filtered_data is not None and not filtered_data.empty:
       
                                         
        fig = px.scatter(filtered_data, 
                     x='ar', 
                     y='Value', 
                     color='Kommun_Type',
                     size='Value',
                     range_y=[0,50],
                     #markers=True, 
                     width=500,
                     #title='Deltagartillfällen i idrottsföreningar, antal/inv 7–25 år',
                     labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                     template='plotly_white',
                     custom_data=['Kommun', 'Type'])
     
        fig.update_traces(customdata=filtered_data[['Kommun', 'Type']].values)  # Add lines to the scatter plot
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
                #margin=dict(l=0, r=0, t=40, b=20),
                legend=dict(orientation="v", yanchor="bottom", y=1.2, xanchor="right", x=1),
                #responsive=True  # Make the graph responsive
            )
       
       # Show figure
        st.plotly_chart(fig)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
             filtered_data.to_excel(writer, sheet_name='Sheet1', index=False)
        if not filtered_data.empty: 
           with st.container():
                st.markdown('<div class="download-button">', unsafe_allow_html=True)    
                st.download_button(
                    label='Ladda ner excel', 
                    data=output, file_name='Deltagartillfällen i idrottsföreningar.xlsx', 
                    key='Deltagar')
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()            