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
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Gymnaiseelever_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasielever_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Gymnasieelever_Vetlanda"
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        merged_data.append(df_ar1)
        #st.write(merged_data)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Gymnasieelever_M'] = merged_dfram['Gymnasieelever_M'].round(0)
        merged_dfram['Gymnasieelever_K'] = merged_dfram['Gymnasieelever_K'].round(0)
        merged_dfram['Gymnasieelever_T'] = merged_dfram['Gymnasieelever_T'].round(0)
      
   selected_kommuner = st.multiselect('Välj kommun(er)', merged_dfram['kommun'].unique(),default=merged_dfram['kommun'].unique()[0])
   filtered_data = merged_dfram[merged_dfram['kommun'].isin(selected_kommuner)]
  
   
   if filtered_data is not None and not filtered_data.empty:
       melted_data = filtered_data.melt(id_vars=['ar','kommun'], value_vars=['Gymnasieelever_T', 'Gymnasieelever_M', 'Gymnasieelever_K'],
                                     var_name='Type', value_name='Value')

        # Map column names to more readable labels
       type_labels = {'Gymnasieelever_T': 'Totalt(kvinnor och män)', 'Gymnasieelever_M': 'Män', 'Gymnasieelever_K': 'Kvinnor'}
       melted_data['Type'] = melted_data['Type'].map(type_labels)
       #st.write(melted_data)
    # Create Line Chart
       line_fig = px.line(
             melted_data,
             x='ar',
             y='Value',
             #range_y=[0,100],
             #range_x=[2014,2024],
             width=600,
             color='kommun',
             line_dash='Type',
             labels={'ar': 'År', 'Value': 'Andel (%)', 'kommun': 'Kommun','Tyep':'typ'}
        )
       line_fig.update_layout(
            autosize=True,
            legend_font_size=12,  # Font size for legend items
            xaxis_tickangle=-45,  # Angle X-axis ticks for better readability
            legend=dict(orientation="v", yanchor="bottom", y=1, xanchor="right", x=1),
        )
       line_fig.update_traces(
           mode='lines+markers',  # Display lines with markers
           line=dict(width=2),  # Line width
           marker=dict(size=8)  # Marker size
        )

       st.plotly_chart(line_fig)
       
         
       output = BytesIO()
       with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
           melted_data.to_excel(writer, sheet_name='Sheet1', index=False)
       if not melted_data.empty:    
          st.download_button(label='Ladda ner excel', data=output, file_name='Gymnasieelever med examen.xlsx', key='barn')
       else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        