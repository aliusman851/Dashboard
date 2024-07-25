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
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Vetlanda"
   
   
   ]
   merged_data = []
   all_min_value=[]
   all_max_value=[]
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        min_value, max_value = df_ar1['Index_Totalt'].min(), df_ar1['Index_Totalt'].max()
        all_min_value.append(min_value)
        all_max_value.append(max_value)
        
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Index_Totalt'] = merged_dfram['Index_Totalt'].round(0)
    
   selected_kommuner = st.selectbox('Välj kommun(er)', merged_dfram['Kommun'].unique(),index=0)
   filtered_data = merged_dfram[merged_dfram['Kommun'] == selected_kommuner]
        #merged_dfram['Total_percentage'] = 100
        #merged_dfram['percentage'] = (merged_dfram['Index_Totalt'] / merged_dfram['Total_percentage']) * 100
        #merged_df = merged_dfram.sort_values(by='ar')
        #st.write(merged_dfram)
        #st.write(min_value,max_value)
          
        
   if filtered_data is not None and len(filtered_data) > 0:
        #year_options = merged_dfram['ar'].unique().tolist()
        #year = st.selectbox('select year', year_options,0)
        #merged_dfram = merged_dfram[merged_dfram['ar']==year]
         fig  =px.bar(filtered_data, 
                         x='ar', 
                         y='Index_Totalt',
                         #size_max=20,
                         #size='Index_Totalt',
                         width=800,
                         template='plotly_dark', 
                         hover_name='Kommun', 
                         color='Index_Totalt',
                         log_x=True,
                         #range_x=[100,10000],
                         range_y=[30,100],
                         
                )
         fig2  =px.bar(merged_dfram, 
                         x='Index_Totalt', 
                         y='Kommun',
                         height=800,
                         width=800,
                         orientation='h',
                         color='Kommun',
                         labels={'ar': 'År', 'Index_Totalt': 'Barn 1-5 år inskrivna i förskola, andel (%)'},
                         title='Barn 1-5 år inskrivna i förskola, andel (%)',
                         range_x=[10,100],
                         animation_frame='ar',
                         color_continuous_scale='agsunset',
                         text=merged_dfram['Index_Totalt'],
                         
                         
                         
                         #animation_group='Kommun',
                )
         st.markdown("<h1 style='font-size:15px;'>Barn 1-5 år inskrivna i förskola, andel (%)", unsafe_allow_html=True)
         
         #fig.update_traces(textposition='bottom center', marker={"opacity":0.7})
         #fig2.update_traces(textposition='bottom center', marker={"opacity":0.7})
         fig2.update_traces(textposition='outside')
         fig2.update_layout(xaxis=dict(range=[all_min_value, all_max_value]))
         fig2.update_layout(coloraxis_showscale=False)
         fig.update_layout(
            margin = dict(t=50, l=0, r=200, b=0),
            showlegend=True,
            
            xaxis_title='År',
            yaxis_title='Index(%)',
            #plot_bgcolor='black',  # Set background color
            
            
         
        )
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
       


        
        


       