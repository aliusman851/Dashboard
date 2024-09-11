import streamlit as st
import plotly.express as px
import requests
import pandas as pd
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
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Vetlanda"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value_K'] = merged_dfram['Value_K'].round(0)
        merged_dfram['Value_M'] = merged_dfram['Value_M'].round(0)
        merged_dfram['Value_T'] = merged_dfram['Value_T'].round(0)
       

   if merged_dfram is not None and len(merged_data) > 0:
         check_data = merged_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T', 'Value_M', 'Value_K'], var_name='Type', value_name='Value')     
         type_labels = {'Value_K': 'Kvinnor', 'Value_M': 'Män', 'Value_T': 'Totalt(Kvinnor och män)'}
         check_data['Type'] = check_data['Type'].map(type_labels)
         selected_kommun = st.selectbox('Välj kommun', check_data['Kommun'].unique())

         # Update the bar chart based on selected Kommun
         #st.title= 'Elever i åk 9 som är behöriga till yrkesprogram, hemkommun, andel (%)',
         fig = update_bar_chart(selected_kommun, check_data)

         # Show figure
         st.plotly_chart(fig)
         output = BytesIO()
         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
             merged_dfram.to_excel(writer, sheet_name='Sheet1', index=False)
         if not merged_dfram.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='Behöriga till yrkesprogram.xlsx', key='yrkepro')
         else:
            st.warning("No data to display.")
def update_bar_chart(selected_kommun,merged_data):
    filtered_df = merged_data[merged_data['Kommun'] == selected_kommun]
    
    fig = px.bar(filtered_df, 
                 x='ar', 
                 y='Value',
                 color='Type', 
                 labels={'ar': 'År', 'Value': 'Värde andel(%)', 'Type': 'Typ', 'Kommun':'kommun'},
                 barmode='group',  # Grouped bars
                 hover_name='Kommun',
                 #template='plotly_dark',
                 color_discrete_sequence=px.colors.qualitative.Pastel,  # Color palette
                 width=800, height=600,  # Custom width and height
                 category_orders={'ar': sorted(filtered_df['ar'].unique())})   # Dark theme for better contrast
    
    fig.update_layout(title=f'Elever i åk 9 som är behöriga till yrkesprogram, hemkommun, andel (%)',
                      showlegend=True,
                      xaxis_title='År',
                      yaxis_title='Andel(%)',
                      bargap=0.2,  # Adjust gap between bars
                      font=dict(family="Arial, sans-serif", size=12),  # Font style
                      plot_bgcolor='rgba(0,0,0,0)',  # Background color
                      paper_bgcolor='rgba(0,0,0,0)',  # Background color
                      hovermode='x',  # Hover information
                      
                      hoverlabel=dict(bgcolor='white', font_size=12, font_family="Arial, sans-serif"))
    
    return fig      
        
    
  

if __name__ == "__main__":
    show()        