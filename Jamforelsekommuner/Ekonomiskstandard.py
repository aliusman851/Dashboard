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
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Vetlanda"
   
   
   ]
   merged_data = []
   all_min_value=[]
   all_max_value=[]
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        min_value, max_value = df_ar1['Value_T'].min(), df_ar1['Value_T'].max()
        all_min_value.append(min_value)
        all_max_value.append(max_value)
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value_T'] = merged_dfram['Value_T'].round(0)
       
        #merged_df = merged_dfram.sort_values(by='ar')
        #st.write(merged_dfram)
   if merged_dfram is not None and len(merged_data) > 0:
        #year_options = merged_dfram['ar'].unique().tolist()
        #year = st.selectbox('select year', year_options,0)
        #merged_dfram = merged_dfram[merged_dfram['ar']==year]
         fig  =px.scatter(merged_dfram, 
                 x='ar',
                 y='Value_T',
                 size='Value_T',  # Set bubble size based on 'Value_T'
                 size_max=30,  # Set maximum bubble size
                 color='Kommun',  # Color bubbles by 'Kommun'
                 hover_name='Kommun',  # Display 'Kommun' as hover information
                 labels={'ar': 'Year', 'Value_T': 'Value', 'Kommun': 'Kommun'},  # Label axes and legend
                 #title='Distribution of Value_T Over Time by Kommun',  # Set title
                 template='plotly_dark')  # Dark theme
                  
         fig2  =px.scatter(merged_dfram, 
                  x='Value_T', 
                  y='Kommun',
                  size='Value_T',  # Set size based on the 'Value_T' column
                  animation_frame='ar',  # Set animation frame to 'ar'
                  animation_group='Kommun',  # Set animation group to 'Kommun' for grouping
                  range_x=[min(all_min_value), max(all_max_value)],  # Set range based on minimum and maximum values
                  color='Kommun',  # Set color based on 'Kommun' column
                  labels={'Value_T': 'Andel(%)', 'Kommun': 'Kommun'},
                  title='Invånare med låg ekonomisk standard(0-19år)',
                  color_continuous_scale='agsunset',
                  #width=800,
                  #range_x=[5,40],
                  hover_name='Kommun', 
                  text = merged_dfram['Kommun'],# Display Kommun as hover information
                  size_max=50)  # Set maximum size of bubble    
                     
         st.markdown("<h1 style='font-size:15px;'>Invånare med låg ekonomisk standard(0-19år)", unsafe_allow_html=True)
         fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))

         # Update layout
         fig.update_layout(width=800, height=600)  # Adjust width and height
         fig.update_xaxes(title_text='Year')  # X-axis label
         fig.update_yaxes(title_text='Value_T')  # Y-axis label
         fig.update_coloraxes(colorbar_title='Kommun')
         fig2.update_traces(textposition='top center')
         
         fig2.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))  # Add marker styling

         fig2.update_layout(coloraxis_showscale=False)
         st.plotly_chart(fig)
         st.plotly_chart(fig2)
          

         output = BytesIO()
         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            merged_dfram.to_excel(writer, sheet_name='Sheet1', index=False)
         if not merged_dfram.empty:    
            st.download_button(label='Ladda ner excel', data=output, file_name='ForsskolebarnIndex.xlsx', key='barn')
         else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        