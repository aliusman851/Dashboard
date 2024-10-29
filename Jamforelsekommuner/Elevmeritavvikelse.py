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
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Falkenberg",    
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Aneby",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Laholm",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Ljungby",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Nynashamn",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Oskarshamn",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Ornskoldsvik",
   "https://nav.utvecklingfalkenberg.se/items/SkolAvikelse_Vetlanda"
   
   
   ]
   merged_data = []
   for api_url in api_urls:
        fetchdata = fetch_data(api_url)
        df_ar1= pd.json_normalize(fetchdata['data'])
        #df1 = pd.DataFrame(merged_data)
        merged_data.append(df_ar1)
        merged_dfram = pd.concat(merged_data, ignore_index=True)
        merged_dfram['Value'] = merged_dfram['Value'].round(0)
   if merged_dfram is not None and not merged_dfram.empty:
       fig = px.histogram(merged_dfram, 
                      x="ar",
                      y="Value", 
                      color="Kommun",
                      width=500,
                      #title='Elever genomsnittligt meritvärde avvikelse, andel (%) ',
                      labels={'ar': 'År', 'Value': 'Andel(%)'},
                      #custom_data='Kommun', 
                      hover_data=merged_dfram.columns)
       fig.update_traces(marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.8) # Adjust marker style'
       fig.update_traces(customdata=merged_dfram[["Kommun"]])
       fig.update_traces(hovertemplate="<br>".join([
          "År: %{x}",
          "Andel(%): %{y}",
          "Kommun: %{customdata[0]}",
          
        ]))
       fig.update_layout(
            bargap=0.2,
            autosize=True,
            xaxis=dict(showgrid=False, title_font=dict(size=12)),  # Smaller font size for axis titles
            yaxis=dict(showgrid=False, title_font=dict(size=12)),
            margin=dict(l=20, r=20, t=30, b=30),  # Adjust margins for mobile
            legend=dict(orientation="v", yanchor="bottom", y=1.2, xanchor="right", x=1),
            font=dict(size=10),
           )  # Adjust gap between bars
       fig.update_xaxes(title_text="År")  # Update x-axis label
       fig.update_yaxes(title_text="Andel(%)")  # Update y-axis label
       #fig.update_layout(title_x=0.5)  # Center title
       fig.update_layout(coloraxis_colorbar=dict(title='Kommun'))  # Update colorbar label
       fig.update_layout(plot_bgcolor='white')  # Set background color

# Show figure
       st.plotly_chart(fig)
       output = BytesIO()
       with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
           merged_dfram.to_excel(writer, sheet_name='Sheet1', index=False)
       if not merged_dfram.empty:    
           st.download_button(label='Ladda ner excel', data=output, file_name='Genomsnittligt meritvärde.xlsx', key='barn')
       else:
             st.warning("No data to display.")

if __name__ == "__main__":
    show()        