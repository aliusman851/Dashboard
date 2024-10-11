from BaseGraph import BaseGraph
import streamlit as st
import plotly.express as px


class Yrkesprogrambehoriga(BaseGraph):
    api_url = [
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Falkenberg",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Aneby",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Laholm",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Ljungby",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Nynashamn",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Oskarshamn",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Ornskoldsvik",
        "https://nav.utvecklingfalkenberg.se/items/Yrkesprogram_Vetlanda",
    ]

    def process_data(self):
        self.df["Value_K"] = self.df["Value_K"].round(0)
        self.df["Value_M"] = self.df["Value_M"].round(0)
        self.df["Value_T"] = self.df["Value_T"].round(0)

        # Melt the dataframe
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
            selected_kommun = st.selectbox("Välj kommun", data["Kommun"].unique())
            filtered_data = data[data["Kommun"] == selected_kommun]

            fig = px.bar(
                filtered_data,
                x="ar",
                y="Value",
                color="Type",
                labels={
                    "ar": "År",
                    "Value": "Värde andel(%)",
                    "Type": "Typ",
                    "Kommun": "Kommun",
                },
                barmode="group",
                hover_name="Kommun",
                color_discrete_sequence=px.colors.qualitative.Pastel,
                width=800,
                height=600,
                category_orders={"ar": sorted(filtered_data["ar"].unique())},
            )

            fig.update_layout(
                title="Elever i åk 9 som är behöriga till yrkesprogram, hemkommun, andel (%)",
                showlegend=True,
                xaxis_title="År",
                yaxis_title="Andel(%)",
                bargap=0.2,
                font=dict(family="Arial, sans-serif", size=12),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                hovermode="x",
                hoverlabel=dict(
                    bgcolor="white", font_size=12, font_family="Arial, sans-serif"
                ),
            )

            st.plotly_chart(fig)


def show():
    graph = Yrkesprogrambehoriga()
    graph.show()
