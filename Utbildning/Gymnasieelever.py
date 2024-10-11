from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Gymnasieelever(BaseGraph):
    api_url = "https://nav.utvecklingfalkenberg.se/items/examinerade_gymnasieelev"

    def process_data(self):
        melted_data = self.df.melt(
            id_vars=["ar", "kommun"],
            value_vars="elev",
            var_name="Type",
            value_name="Value",
        )
        type_labels = {"elev": "Elever"}
        melted_data["Type"] = melted_data["Type"].map(type_labels)
        return melted_data

    def plot_data(self, data):
        if data is not None and len(data) > 0:
            fig = px.line(
                data,
                x="ar",
                y="Value",
                title="Gymnasieelever med examen inom 3 år, kommunala skolor, andel(%), avvikelse från modellberäknat värde",
                markers=True,
                template=("plotly_white"),
                labels={"ar": "År", "Value": "Andel(%)", "Type": "Typ"},
                custom_data=["kommun", "Type"],
                color="Type",
                width=700,
                text="Value",
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
    graph = Gymnasieelever()
    graph.show()
