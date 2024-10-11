from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px
import pandas as pd


class Skoltrygghet(BaseGraph):
    api_url = [
        # "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Ornskldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Skoltrygghet_Vetlanda",
    ]

    def process_data(self):
        self.df["Value_K"] = pd.to_numeric(self.df["Value_K"], errors="coerce").round(0)
        self.df["Value_M"] = pd.to_numeric(self.df["Value_M"], errors="coerce").round(0)
        self.df["Value_T"] = pd.to_numeric(self.df["Value_T"], errors="coerce").round(0)
        self.df["datum"] = pd.to_datetime(self.df["datum"], errors="coerce")
        self.df.dropna(
            subset=["Value_T", "Value_M", "Value_K", "datum", "id"], inplace=True
        )

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
            fig = px.bar(
                data,
                x="ar",
                y="Value",
                color="Kommun",
                barmode="group",
                width=800,
                title="Elever i åk 8: Känner du dig trygg i skolan, andel (%)",
                labels={"ar": "År", "Value": "Andel(%)"},
                hover_data={"Type": True},
                opacity=0.8,
                template="plotly_white",
            )

            fig.update_traces(
                marker_line_color="rgb(8,48,107)",
                marker_line_width=1.5,
            )

            fig.update_layout(
                bargap=0.5,
                xaxis_title="År",
                title_x=0.5,
                coloraxis_colorbar=dict(title="Kommun"),
                plot_bgcolor="white",
            )

            st.plotly_chart(fig)


def show():
    graph = Skoltrygghet()
    graph.show()
