from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Sarskiltaldreomsorgasikter(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/sarskilt_aldreomsorgasikter"

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
            fig = px._chart_types.line(
                data,
                x="ar",
                y="Value",
                title="Brukarbedömning särskilt boende äldreomsorg-hänsyn till åsikter och önskemål, andel(%)",
                markers=True,
                template=("plotly_white"),
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                width=800,
                custom_data=["kommun", "Type"],
                color="Type",
            )
            fig.update_traces(
                hovertemplate="<br>".join(
                    [
                        "År: %{y}",
                        "Andel(%): %{x}",
                        "Kommun: %{customdata[0]}",
                        "Typ: %{customdata[1]}",
                    ]
                )
            )
            st.plotly_chart(fig)


def show():
    graph = Sarskiltaldreomsorgasikter()
    graph.show()