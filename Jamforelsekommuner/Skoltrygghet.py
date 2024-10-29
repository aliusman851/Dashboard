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
   #"https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Ornskldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Vetlanda",
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value_K'] = pd.to_numeric(merged_dfram['Value_K'], errors='coerce').round(0)
        merged_dfram['Value_M'] = pd.to_numeric(merged_dfram['Value_M'], errors='coerce').round(0)
        merged_dfram['Value_T'] = pd.to_numeric(merged_dfram['Value_T'], errors='coerce').round(0)
        merged_dfram['datum'] = pd.to_datetime(merged_dfram['datum'], errors='coerce')
        merged_dfram.dropna(subset=['Value_T','Value_M','Value_K', 'datum','id'], inplace=True)
        #st.write(merged_dfram)
        #st.write(merged_dfram)
      
   check_data = merged_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'], var_name='Type', value_name='Value')     
   type_labels = {'Value_K': 'Kvinnor', 'Value_M': 'Män', 'Value_T': 'Totalt(Kvinnor och män)'}
   check_data['Type'] = check_data['Type'].map(type_labels)
   #filtered_data = check_data[check_data['Type'] == value_type]
   #st.write(check_data)   
   fig = px.bar(check_data, 
                    x="ar",
                    y='Value', 
                    color="Kommun",
                    barmode='group',
                    width=600,
                    #title='Elever i åk 8: Känner du dig trygg i skolan, andel (%) ',
                    #range_x=[2021,2026],
                    #orientation='h',
                    labels={'ar': 'År', 'Value': 'Andel(%)'},
                    hover_data={'Type': True} 
                    #hover_data=check_data.columns
                )
   fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8) # Adjust marker style
   fig.update_layout(
        bargap=0.5,  
        autosize=True,
        xaxis=dict(showgrid=False),  # Smaller font size for axis titles
        yaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=0, b=0),  # Adjust margins for mobile
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1))
     # Adjust gap between bars)  # Adjust gap between bars
   fig.update_xaxes(title_text="År")  # Update x-axis label
   #fig.update_yaxes(title_text="Andel(%)")  # Update y-axis label
   #fig.update_layout(title_x=0.5)  # Center title
   fig.update_layout(coloraxis_colorbar=dict(title='Kommun'))  # Update colorbar label
   fig.update_layout(plot_bgcolor='white')  # Set background color

# Show figure
   st.plotly_chart(fig)
   output = BytesIO()
   with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
         check_data.to_excel(writer, sheet_name='Sheet1', index=False)
   if not check_data.empty:    
        st.download_button(label='Ladda ner excel', data=output, file_name='Elever Känner trygg i skolan.xlsx', key='trygghetiskolan')
   else:
            st.warning("No data to display.")

if __name__ == "__main__":
    show()        