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
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/ArbStud_Vetlanda",
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value_K'] = pd.to_numeric(merged_dfram['Value_K'], errors='coerce').round(0)
        merged_dfram['Value_M'] = pd.to_numeric(merged_dfram['Value_M'], errors='coerce').round(0)
        merged_dfram['Value_T'] = pd.to_numeric(merged_dfram['Value_T'], errors='coerce').round(0)
        #st.write(merged_data)
   selected_kommuner = st.multiselect('Välj kommun(er)', merged_dfram['Kommun'].unique(),default=merged_dfram['Kommun'].unique()[0])
   filtered_data = merged_dfram[merged_dfram['Kommun'].isin(selected_kommuner)]
      
        #merged_dfram['Value'] = merged_dfram['Value'].round(0)
   if filtered_data is not None and not filtered_data.empty:  
       melted_data = filtered_data.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'],
                                     var_name='Type', value_name='Value')

        # Map column names to more readable labels
       type_labels = {'Value_T': 'Totalt', 'Value_M': 'Män', 'Value_K': 'Kvinnor'}
       melted_data['Type'] = melted_data['Type'].map(type_labels)
       
       fig = px.area(melted_data, 
                       x='ar', 
                       y='Value', 
                       color='Type', 
                       markers=True, 
                       height=600,
                       width=800,
                       #title='Invånare 16-24 år som varken arbetar eller studerar, andel (%) ',
                       labels={'ar': 'År', 'Value': 'Andel(%)', 'Type': 'Typ'},
                       template='plotly_dark',
                       custom_data=['Kommun', 'Type']
                    )
       fig.update_layout(
            autosize=True,
            xaxis=dict(showgrid=False),  # Smaller font size for axis titles
            yaxis=dict(showgrid=False),
            margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins for mobile
            legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
           )  # Adjust gap between bars
       fig.update_traces(hovertemplate="<br>".join([
          "År: %{x}",
          "Andel(%): %{y}",
          "Kommun: %{customdata[0]}",
          "Typ: %{customdata[1]}"
        ]))
   
   
# Show figure
       st.plotly_chart(fig)
       output = BytesIO()
       with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         melted_data.to_excel(writer, sheet_name='Sheet1', index=False)
       if not melted_data.empty:    
         st.download_button(label='Ladda ner excel', data=output, file_name='Invånare arbetar eller studerar.xlsx', key='Arbstud')
       else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()            