from flask import Flask, render_template, request
from scrape_data import scrape_airfare_data
from api_integration import generate_insights
import plotly.express as px
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    df = scrape_airfare_data()

    # Clean data
    df.dropna(subset=["route", "year", "passengers", "price"], inplace=True)

    # Handle filters from form
    min_pax_raw = request.form.get("min_passengers", "")
    route_filter = request.form.get("route_keyword", "").lower()
    chart_type = request.form.get("chart_type", "bar")

    try:
        min_pax = int(min_pax_raw)
    except ValueError:
        min_pax = 0

    if min_pax:
        df = df[df["passengers"] >= min_pax]

    if route_filter:
        df = df[df["route"].str.lower().str.contains(route_filter)]

    # Create charts
    if chart_type == "bar":
        bar_df = df.groupby("route", as_index=False).agg({"passengers": "sum"})
        fig = px.bar(bar_df, x="route", y="passengers", title="Total Passengers by Route")
    elif chart_type == "line":
        fig = px.line(df, x="year", y="passengers", color="route", markers=True,
                      title="Passenger Trends Over Years")
    elif chart_type == "pie":
        latest_year = df["year"].max()
        latest_df = df[df["year"] == latest_year]
        fig = px.pie(latest_df, names="route", values="passengers",
                     title=f"Passenger Distribution by Route ({latest_year})")
    else:
        # Default fallback
        bar_df = df.groupby("route", as_index=False).agg({"passengers": "sum"})
        fig = px.bar(bar_df, x="route", y="passengers", title="Total Passengers by Route")

    chart_html = fig.to_html(full_html=False)
    insights = generate_insights(df)

    table_html = df.to_html(classes="table table-striped table-sm table-hover align-left", index=False)

    return render_template("dashboard.html",
                           chart=chart_html,
                           table=table_html,
                           insights=insights,
                           chart_type=chart_type)

if __name__ == "__main__":
    app.run(debug=True)
