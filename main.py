import streamlit as st

with open('styles.css', 'r') as css_file:
    css_text = css_file.read()
    st.markdown(f'<style>{css_text}</style>', unsafe_allow_html=True)
# Define your list of navigation items
st.sidebar.title("Navigation")
navigation_items = st.sidebar.selectbox('Utbildning',["Behörighet yrkesprogram", "Examinerade gymnasieelev", "Förskolebarn", "Gymnasieutbildad", "Etablerade ungdomar"])

# Apply custom CSS to style the navigation list
st.markdown(f'<h3 class="nav-list">{navigation_items}</h3>', unsafe_allow_html=True)

# Create a list element for each navigation item
navigation_items = st.sidebar.selectbox('Soc',["Hemtjänst äldreomsorg behandling", "Hemtjänst äldreomsorg åsikter", "Hemtjänst äldreomsorg trygghet", "Särskilt Äldreomsorg Behandling", "Särskilt äldreomsorg åsikter", "Särskilt äldreomsorg trygghet"])