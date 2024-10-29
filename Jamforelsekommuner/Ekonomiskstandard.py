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
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/Ekonomiskstandard_Aneby",
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
   check_data = merged_dfram.melt(id_vars=['ar', 'Kommun'], value_vars=['Value_T'], var_name='Type', value_name='Value')     
   type_labels = {'Value_T': 'Totalt(Kvinnor och män)'}
   check_data['Type'] = check_data['Type'].map(type_labels)
   check_data['Kommun_Value'] = check_data.apply(lambda row: f"{row['Kommun']}: {row['Value']}", axis=1)        
   if check_data is not None and len(check_data) > 0:
       
         fig  =px.scatter(check_data, 
                 x='ar',
                 y='Value',
                 size='Value',  # Set bubble size based on 'Value_T'
                 size_max=30,  # Set maximum bubble size
                 color='Kommun',  # Color bubbles by 'Kommun'
                 hover_name='Kommun',  # Display 'Kommun' as hover information
                 labels={'ar': 'År', 'Value': 'Andel(%)', 'Kommun': 'Kommun'},  # Label axes and legend
                 #title='Distribution of Value_T Over Time by Kommun',  # Set title
                 template='plotly_white')  # Dark theme
                  
         fig2  =px.scatter(check_data, 
                  x='Value', 
                  y='Kommun',
                  size='Value',  # Set size based on the 'Value_T' column
                  animation_frame='ar',  # Set animation frame to 'ar'
                  animation_group='Kommun',  # Set animation group to 'Kommun' for grouping
                  range_x=[min(all_min_value), max(all_max_value)],
                  color='Kommun',  # Set color based on 'Kommun' column
                  labels={'Value': 'Andel(%)'},
                  #title='Invånare med låg ekonomisk standard(0-19år)',
                  color_continuous_scale='agsunset',
                  hover_name='Kommun', 
                  text = check_data['Kommun_Value'],# Display Kommun as hover information
                  size_max=40)  # Set maximum size of bubble    
                     
         #st.markdown("<h1 style='font-size:15px;'>Invånare med låg ekonomisk standard(0-19år)", unsafe_allow_html=True)
         fig.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))
         

         # Update layout
         fig.update_layout(
                autosize=True,
                width=500,
                xaxis=dict(showgrid=False, title_font=dict(size=12)),  # Smaller font size for axis titles
                yaxis=dict(showgrid=False, title_font=dict(size=12)),
                margin=dict(l=0, r=0, t=0, b=0),
                
                legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
                
                )  # Adjust width and height
         fig.update_xaxes(title_text='År')  # X-axis label
         fig.update_yaxes(title_text='Andel(%)')  # Y-axis label
         fig.update_coloraxes(colorbar_title='Kommun')
         #fig2.update_traces(textposition='top center')
         #fig2.update_layout(xaxis=dict(range=[all_min_value, all_max_value]))
         #fig2.update_traces(marker=dict(line=dict(width=2, color='DarkSlateGrey')), selector=dict(mode='markers'))  # Add marker styling
         
         fig2.update_layout(
              coloraxis_showscale=False,
              autosize=True,
              height=590,
              margin=dict(l=0, r=0, t=0, b=0),
              xaxis=(dict(showgrid=False)),
              yaxis=dict(showgrid=False),
              legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1)
              

            )
         st.plotly_chart(fig)
         st.plotly_chart(fig2, )
         
         
          

         output = BytesIO()
         with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            check_data.to_excel(writer, sheet_name='Sheet1', index=False)
         if not check_data.empty:
                st.download_button( 
                    label='Ladda ner excel', 
                    data=output, 
                    file_name='Låg ekonomisk standard.xlsx', 
                    key='barn')
                
         else:
            st.warning("No data to display.")
   else:
     st.warning("No data to display.")
    

if __name__ == "__main__":
    show()        