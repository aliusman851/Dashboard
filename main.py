import streamlit as st
import plotly.express as px
import requests
import pandas as pd
def fetch_data(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from API")
        return None

# This is first streamlit demo
def main():
    st.title("Dashboard with Streamlit")
   
    # Sidebar for user input
    st.sidebar.header("User Input")
    api_url = st.sidebar.text_input("API Endpoint URL")

    if api_url:
        # Fetch data
        data = fetch_data(api_url)

        if data:
            # Convert data to a Pandas DataFrame
            df =pd.DataFrame(data)
            df_ar= pd.json_normalize(df['data'])
            st.subheader("Data from API")
            st.write(df_ar)
            # Create plots using Plotly Express
            st.subheader("Data Visualization")
            fig = px.bar(df_ar, x='ar', y=['utbildade_man', 'utbildade_kvinnor','utbildade_totalt'], title='Plot')
            
            st.plotly_chart(fig)
        else:
            st.warning("No data to display.")

if __name__ == "__main__":
    main()