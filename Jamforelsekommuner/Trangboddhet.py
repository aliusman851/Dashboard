from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Trangboddhet(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Trangboddhet_Vetlanda",
    ]

    def process_data(self):
        self.df["Value_K"] = pd.to_numeric(self.df["Value_K"], errors="coerce").round(0)
        self.df["Value_M"] = pd.to_numeric(self.df["Value_M"], errors="coerce").round(0)
        self.df["Value_T"] = pd.to_numeric(self.df["Value_T"], errors="coerce").round(0)
        self.df["ar"] = self.df["ar"].astype(int)

        years = self.df["ar"].unique()
        municipalities = self.df["Kommun"].unique()
        complete_index = pd.MultiIndex.from_product(
            [years, municipalities], names=["ar", "Kommun"]
        )

        complete_df = (
            self.df.set_index(["ar", "Kommun"]).reindex(complete_index).reset_index()
        )

        complete_df[["Value_K", "Value_M", "Value_T"]] = complete_df[
            ["Value_K", "Value_M", "Value_T"]
        ].fillna(0)

        melted_data = complete_df.melt(
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
            value_type = st.selectbox("Välj Värdetyp", data["Type"].unique())
            filtered_data = data[data["Type"] == value_type]

            fig = px.line(
                filtered_data,
                x="ar",
                y="Value",
                markers="Value",
                color="Kommun",
                hover_name="Kommun",
                labels={"ar": "År", "Value": "Andel(%)"},
            )

            st.plotly_chart(fig)


def show():
    graph = Trangboddhet()
    graph.show()
