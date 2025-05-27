import pandas as pd
import plotly.express as px

df = pd.read_csv('data/Air_Quality.csv')
import preswald


df = pd.read_csv("data/Air_Quality.csv", parse_dates=["Start_Date"])
df.dropna(subset=["Data Value"], inplace=True)


preswald.text("# 🌇 Welcome to the NYC Air Quality Explorer")
preswald.text(
    "Explore how air quality varies across neighborhoods and seasons. "
    "This story draws from historical data to highlight urban pollution patterns."
)
preswald.text("## 🏙️ Top 10 Most Polluted Neighborhoods")
top10 = (
    df.groupby("Geo Place Name")["Data Value"]
    .mean()
    .nlargest(10)
    .reset_index(name="Average Pollution")
)
fig1 = px.bar(
    top10,
    x="Average Pollution",
    y="Geo Place Name",
    orientation="h",
    title="Top 10 Most Polluted Neighborhoods (Avg Data Value)",
    color="Average Pollution",
    color_continuous_scale="Reds"
)
fig1.update_layout(yaxis=dict(categoryorder="total ascending"))
preswald.plotly(fig1)

# 📈 Time Trend for NO₂
preswald.text("## 📈 NO₂ Pollution Over Time")
no2_df = df[df["Name"] == "Nitrogen dioxide (NO2)"]
no2_trend = (
    no2_df.groupby("Start_Date")["Data Value"]
    .mean()
    .reset_index(name="NO2_ppb")
)
fig2 = px.line(
    no2_trend,
    x="Start_Date",
    y="NO2_ppb",
    title="Mean NO₂ Levels Over Time",
    markers=True,
    labels={"Start_Date": "Date", "NO2_ppb": "NO₂ (ppb)"}
)
preswald.plotly(fig2)

# 📦 Seasonal Pollution Distribution
preswald.text("## 📦 Seasonal Pollution Patterns")
fig3 = px.box(
    df,
    x="Time Period",
    y="Data Value",
    color="Name",
    title="Pollution Levels by Time Period and Pollutant"
)
fig3.update_layout(xaxis_tickangle=-45)
preswald.plotly(fig3)

# 🧪 Average Levels of All Pollutants
preswald.text("## 🧪 Average Levels Across Pollutants")
avg_pollutants = (
    df.groupby("Name")["Data Value"]
    .mean()
    .sort_values(ascending=False)
    .reset_index(name="Average Level")
)
fig4 = px.bar(
    avg_pollutants,
    x="Average Level",
    y="Name",
    orientation="h",
    title="Average Levels of Each Pollutant",
    color="Average Level",
    color_continuous_scale="Blues"
)
preswald.plotly(fig4)

# 🏘️ Compare Neighborhoods (Flushing vs UWS)
preswald.text("## 🏘️ Compare NO₂ in Two Neighborhoods")
selected = ["Flushing and Whitestone (CD7)", "Upper West Side (CD7)"]
comp_df = no2_df[no2_df["Geo Place Name"].isin(selected)]
fig5 = px.line(
    comp_df,
    x="Start_Date",
    y="Data Value",
    color="Geo Place Name",
    title="NO₂ Levels: Flushing vs. Upper West Side",
    markers=True,
    labels={"Data Value": "NO₂ (ppb)", "Start_Date": "Date"}
)
preswald.plotly(fig5)

# 📋 Raw data table
preswald.text("## 📋 Full Dataset (Explore the Raw Data)")
preswald.table(df)
