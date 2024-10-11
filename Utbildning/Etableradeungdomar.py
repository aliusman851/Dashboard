from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class EtableradeUngdom(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/etablerade_ungdom"

    def process_data(self):
        processed_data = self.df["ar"].astype(str) + "_" + self.df["id"].astype(str)
        return processed_data

    def plot_data(self, data):
        st.markdown(
            "<h1 style='font-size:15px;'>Ungdomar som är etablerade på arbetsmarknaden eller studerar 2 år efter slutförd gymnasieutbildning, kommunala skolor, andel(%)</h1>",
            unsafe_allow_html=True,
        )
        selected_columns = [
            "etablerade_kvinnor",
            "etablerade_man",
            "etablerade_totalt",
        ]  # Är detta bearbetad data?
        selected_option = st.selectbox(
            "Välj y-axel värde", options=["Välj alla"] + selected_columns
        )

        if selected_option == "Välj alla":
            fig = px.bar(
                data,
                x="x",
                y=selected_columns,
                animation_frame="ar",
                width=800,
                template="plotly_dark",
            )
        else:
            fig = px.funnel(
                data, x="ar", y=selected_option, color=selected_option, width=800
            )
        st.plotly_chart(fig)


def show():
    graph = EtableradeUngdom()
    graph.show()
