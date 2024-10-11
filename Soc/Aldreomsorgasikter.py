from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Aldreomsorgasikter(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/hemtjanst_aldreomsorgasikter"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars=[
                "hemtjanstasikter_totalt",
                "hemtjanstasikter_man",
                "hemtjanstasikter_kvinnor",
            ],
            var_name="Type",
            value_name="Value",
        )
        type_labels = {
            "hemtjanstasikter_totalt": "Totalt",
            "hemtjanstasikter_man": "Män",
            "hemtjanstasikter_kvinnor": "kvinnor",
        }
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.line(
                data,
                x="ar",
                y="Value",
                color="Type",
                title="Brukarbedömning hemtjänst äldreomsorg-hänsyn till åsikter och önskemål, andel(%)",
                # color="Scenario",
                markers=True,
                width=800,
                custom_data=["kommun", "Type"],
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
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
    graph = Aldreomsorgasikter()
    graph.show()
