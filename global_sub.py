import streamlit as st
import pandas as pd
import plotly.express as px

def chart_1():
    st.subheader("Tren Subsidi Energi Global (Total Implicit & Explicit)")

    # === LOAD DATA DARI GOOGLE DRIVE ===
    file_id = "15kwCyRwyenxTdiSINSOI7NLqI5LVN1Wz"
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    df = pd.read_csv(download_url)
    df = df[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

    # === FILTER: Total Implicit & Explicit (seluruh dunia) ===
    df_trend = df[
        (df["INDICATOR_NAME"] == "Fossil Fuel Subsidies - Total Implicit and Explicit")
    ]

    # Agregasi per tahun
    global_trend = df_trend.groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()
    global_trend["OBS_VALUE"] = global_trend["OBS_VALUE"] / 1e9  # Dalam miliar USD

    # === BUAT GRAFIK DENGAN PLOTLY ===
    fig = px.line(
        global_trend,
        x="TIME_PERIOD",
        y="OBS_VALUE",
        markers=True,
        title="Tren Subsidi Global: Total Implicit & Explicit (dalam Miliar USD)",
        labels={
            "TIME_PERIOD": "Tahun",
            "OBS_VALUE": "Subsidi (Miliar USD)"
        }
    )

    # === CUSTOMISASI TRANSPARANSI & GAYA ===
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # transparan
        paper_bgcolor='rgba(0,0,0,0)', # transparan
        font=dict(color="black"),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        margin=dict(t=50, b=40, l=50, r=20),
        height=500
    )

    # Tambahkan nilai teks di atas titik
    fig.update_traces(
        text=global_trend["OBS_VALUE"].round(0).astype(int).astype(str),
        textposition="top center",
        mode="lines+markers+text"
    )

    st.plotly_chart(fig, use_container_width=True)
