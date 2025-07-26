import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

    # === PLOT MENGGUNAKAN MATPLOTLIB ===
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(global_trend["TIME_PERIOD"], global_trend["OBS_VALUE"], marker='o',
            linewidth=2, color='royalblue', label='Total Subsidi Global')

    # Tambahkan panah naik/turun dan label angka
    for i in range(1, len(global_trend)):
        x_prev = global_trend["TIME_PERIOD"].iloc[i - 1]
        x_curr = global_trend["TIME_PERIOD"].iloc[i]
        y_prev = global_trend["OBS_VALUE"].iloc[i - 1]
        y_curr = global_trend["OBS_VALUE"].iloc[i]

        arrow_color = 'green' if y_curr > y_prev else 'red'
        ax.annotate(
            '',
            xy=(x_curr, y_curr),
            xytext=(x_prev, y_prev),
            arrowprops=dict(facecolor=arrow_color, shrink=0.05, width=2, headwidth=8)
        )

    for i in range(len(global_trend)):
        x = global_trend["TIME_PERIOD"].iloc[i]
        y = global_trend["OBS_VALUE"].iloc[i]
        ax.text(x, y + 20, f"{y:.0f}", ha='center', va='bottom', fontsize=9, color='black')

    # Tambahkan dummy plot untuk legend panah
    ax.plot([], [], color='green', label='Naik')
    ax.plot([], [], color='red', label='Turun')

    # Label dan styling
    ax.set_title('Tren Subsidi Global: Total Implicit & Explicit (dalam Miliar USD)', fontsize=14)
    ax.set_xlabel('Tahun', fontsize=12)
    ax.set_ylabel('Subsidi (Miliar USD)', fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.legend()

    st.pyplot(fig)