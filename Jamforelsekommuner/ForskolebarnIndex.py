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
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Vetlanda",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Falkenberg",
   "https://nav.utvecklingfalkenberg.se/items/Forskolebarn_Laholm"
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        
        
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Index_Totalt'] = merged_dfram['Index_Totalt'].round(0)
        #merged_df = merged_dfram.sort_values(by='ar')
        #st.write(merged_dfram)
          
        
   if merged_dfram is not None and len(merged_data) > 0:
        #year_options = merged_dfram['ar'].unique().tolist()
        #year = st.selectbox('select year', year_options,0)
        #merged_dfram = merged_dfram[merged_dfram['ar']==year]
         fig  =px.scatter(merged_dfram, 
                         x='ar', 
                         y='Index_Totalt',
                         size_max=20,
                         size='Index_Totalt',
                         width=1000,
                         template='plotly_dark', 
                         hover_name='Kommun', 
                         color='Kommun',
                         log_x=True,
                         #range_x=[100,10000],
                         range_y=[30,100],
                         
                )
         fig2  =px.scatter(merged_dfram, 
                         x='ar', 
                         y='Index_Totalt',
                         size_max=20,
                         size='Index_Totalt',
                         width=1000,
                         #template='plotly_dark', 
                         hover_name='Kommun', 
                         color='Kommun',
                         title='Barn 1-5 år inskrivna i förskola, andel (%)',
                         log_x=True,
                         range_x=[100,10000],
                         range_y=[25,100],
                         animation_frame='ar',
                         animation_group='Kommun',
                )
         st.markdown("<h1 style='font-size:15px;'>Barn 1-5 år inskrivna i förskola, andel (%)", unsafe_allow_html=True)
         fig.update_traces(textposition='bottom center', marker={"opacity":0.7})
         fig2.update_traces(textposition='bottom center', marker={"opacity":0.7})
         fig.update_layout(
            margin = dict(t=50, l=0, r=200, b=0),
            showlegend=False,
            xaxis_title='År',
            yaxis_title='Index(%)',
            #plot_bgcolor='black',  # Set background color
            
            
         
        )
         fig2.update_layout(
            margin = dict(t=50, l=0, r=200, b=0),
            showlegend=False,
            xaxis_title='År',
            yaxis_title='Index(%)',
            #plot_bgcolor='black',  # Set background color
            xaxis=dict(
                title_font=dict(size=16),  # Adjust size as needed for x-axis title
                tickfont=dict(size=12)  # Adjust size as needed for x-axis tick labels
            ),
                yaxis=dict(
                title_font=dict(size=16),  # Adjust size as needed for y-axis title
                tickfont=dict(size=12)  # Adjust size as needed for y-axis tick labels
            )
            
         
        )
         st.plotly_chart(fig)
         st.write(fig2)
            
        
           
       
        
       




    
        
                      
        
    
    



# Create frames for animation

    
    
   


# Update frames

       
        
   
   
     
         """fig = px.sunburst(merged_df,
                       #x='ar', 
                       #y='Index_Totalt',
                       values='Index_Totalt',
                       path= ['ar','Kommun','Index_Totalt'],
                       color='Kommun',
                       maxdepth=2,
                       width=1500,
                       height=800,
                       hover_name='Kommun',
                       #hover_data={'Index_Totalt': True},
                       #template='plotly_dark',
                       labels={'Index_Totalt': 'Hemtjänst/särskilt boende)Index(%)','id': 'Kommun/År', 'parent': 'År'},
                      
                       
                       
        )
      #fig.update_traces(hoverinfo='ar', selector=dict(type='sunburst', hoverinfo='ar'))
      #fig.update_traces(hovertemplate= 'Index_Totalt')
      st.markdown("<h1 style='font-size:15px;'>Barn 1-5 år inskrivna i förskola, andel (%), förtroende,medelvärde — Kommuner,Index andel(%)", unsafe_allow_html=True)
      fig.update_layout(margin = dict(t=0, l=0, r=750, b=0))
      st.plotly_chart(fig)"""
     
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
       


        
        


       