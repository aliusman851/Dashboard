from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Deltagartillfallen(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Ornskldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Tillitslos_Vetlanda",
    ]

    def process_data(self):
        self.df["Value_K"] = pd.to_numeric(self.df["Value_K"], errors="coerce").round(0)
        self.df["Value_M"] = pd.to_numeric(self.df["Value_M"], errors="coerce").round(0)
        self.df["Value_T"] = pd.to_numeric(self.df["Value_T"], errors="coerce").round(0)

        melted_data = self.df.melt(
            id_vars=["ar", "Kommun"],
            value_vars=["Value_T", "Value_M", "Value_K"],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "Value_K": "Kvinnor",
            "Value_M": "Män",
            "Value_T": "Totalt(Kvinnor och män)",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)

        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            selected_kommuner = st.multiselect(
                "Välj kommun(er)",
                data["Kommun"].unique(),
                default=data["Kommun"].unique()[0],
            )
            filtered_data = data[data["Kommun"].isin(selected_kommuner)]

            fig = px.line(
                filtered_data,
                x="ar",
                y="Value",
                color="Type",
                hover_data={"Kommun": True},
                markers=True,
                width=800,
                title="Invånare 16-84 år med avsaknad av tillit till andra, andel (%) ",
                labels={"ar": "År", "Value": "Andel(%)", "Type": "typ"},
                template="plotly_white",
            )

            st.plotly_chart(fig)


def show():
    graph = Deltagartillfallen()
    graph.show()
