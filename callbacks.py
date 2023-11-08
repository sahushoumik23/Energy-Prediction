from dash import dcc, Input, Output, callback
import time
import pandas as pd
import plotly.graph_objs as go
import requests

A = 6.4
r = 0.17
PR = 0.75
AC_factor = 0.985
api_key = "b425106dfd1c27aef67eb1be021ed6be"
lat = 12.29
lon = 79.7


def getIrradianceDataframe(date):
    res = requests.get(
        f"https://api.openweathermap.org/energy/1.0/solar/data?lat={lat}&lon={lon}&date={date}&appid={api_key}"
    )
    res_json = res.json()["irradiance"]["hourly"]
    data = [
        {"hour": item["hour"], "ghi": (item["clear_sky"]["ghi"])} for item in res_json
    ]
    df = pd.DataFrame(data)
    df["Energy"] = df.apply(
        lambda row: (A * r * row["ghi"] * PR * AC_factor) / 1000, axis=1
    )
    df["ghi"] = df["ghi"] / 1000
    return df


def get_callbacks(app):
    @app.callback(
        [
            Output("date-output", "children"),
            Output("process-output", "children"),
            Output("energy_output", "figure"),
        ],
        [Input("date-picker", "date")],
    )
    def getDate(date):
        df = getIrradianceDataframe(date)
        total_energy_generated = round(df["Energy"].sum(), 3)
        total_irradiance = round(df["ghi"].sum(), 3)
        fig = go.Figure(
            data=[
                go.Scatter(
                    x=df["hour"],
                    y=df["Energy"],
                    mode="lines+markers",
                    name="Energy Generated",
                ),
                go.Scatter(
                    x=df["hour"], y=df["ghi"], mode="lines+markers", name="Irradiance"
                ),
            ],
            layout={
                "title": "Solar Power Generation",
                "xaxis": {"title": "Hours "},
                "yaxis": {"title": "Energy/Irradiance in kWh/sq.m."},
            },
        )

        return [
            f"Date Selected is {date}",
            f"Energy Generated: {total_energy_generated}kW/sq.m. & Total Irradiance: {total_irradiance} kW/sq.m.",
            fig,
        ]
