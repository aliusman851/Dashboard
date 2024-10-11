from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Sarskiltaldreomsorgbehandling(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/sarskilt_aldreomsorgbehandling"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=[
                "sarskiltboende_totalt",
                "sarskiltboende_man",
                "sarskiltboende_kvinnor",
            ],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "sarskiltboende_totalt": "Totalt",
            "sarskiltboende_man": "Män",
            "sarskiltboende_kvinnor": "kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.bar(
                data,
                x="ar",
                y="Value",
                title="Brukarbedömning särskilt boende äldreomsorg-bemötande, andel(%)",
                template="plotly_white",
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                custom_data=["kommun", "Type"],
                color="Type",
                width=800,
            )
            fig.update_layout(
                xaxis=dict(tickmode="linear"),
                plot_bgcolor="rgba(0,0,0,0)",
                yaxis=(dict(showgrid=False)),
            )
            fig.update_traces(
                hovertemplate="<br>".join(
                    [
                        "År: %{x}",
                        "Andel(%): %{y}",
                        "Kommun: %{customdata[0]}",
                        "Typ: %{customdata[1]}",
                    ]
                )
            )
            st.plotly_chart(fig)


def show():
    graph = Sarskiltaldreomsorgbehandling()
    graph.show()