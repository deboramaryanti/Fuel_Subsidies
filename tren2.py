import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def tren_chart_2():
    st.subheader("Tren Subsidi Energi (Berdasarkan Jenis)")

    # === LOAD DATA DARI GOOGLE DRIVE ===
    file_id = "15kwCyRwyenxTdiSINSOI7NLqI5LVN1Wz"
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    data = pd.read_csv(download_url)

    df = data[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # dalam miliar USD

    # === PERSIAPAN FILTER ===
    tahun_min = df["TIME_PERIOD"].min()
    tahun_max = df["TIME_PERIOD"].max()
    negara_unik = sorted(df["REF_AREA_NAME"].unique())
    jenis_unik = sorted(df["INDICATOR_NAME"].unique())

    # === SIDEBAR FILTER ===
    with st.sidebar:
        st.markdown("### Filter Data Subsidi")
        negara_opsi = ["Seluruh Dunia"] + negara_unik
        negara_dipilih = st.selectbox("Pilih Negara:", options=negara_opsi)

        jenis_dipilih = st.multiselect(
            "Jenis Subsidi:",
            options=jenis_unik,
            default=[jenis_unik[0]],
            key="jenis_subsidi"
        )

    # === FILTER DATA ===
    df_filtered = df[df["INDICATOR_NAME"].isin(jenis_dipilih)]

    if negara_dipilih != "Seluruh Dunia":
        df_filtered = df_filtered[df_filtered["REF_AREA_NAME"] == negara_dipilih]

    if df_filtered.empty:
        st.warning("Silakan pilih jenis subsidi untuk melihat tren.")
        return

    # === AGREGASI UNTUK GRAFIK ===
    df_agg = df_filtered.groupby(["TIME_PERIOD", "INDICATOR_NAME"])["OBS_VALUE"].sum().reset_index()

    # === GRAFIK TREN LINE ===
    fig = px.line(
        df_agg,
        x="TIME_PERIOD",
        y="OBS_VALUE",
        color="INDICATOR_NAME",
        markers=True,
        title=f"Tren Subsidi Energi - {'Global' if negara_dipilih == 'Seluruh Dunia' else negara_dipilih}",
        labels={
            "TIME_PERIOD": "Tahun",
            "OBS_VALUE": "Subsidi (Miliar USD)",
            "INDICATOR_NAME": "Jenis Subsidi"
        }
    )
    st.plotly_chart(fig, use_container_width=True)

    # === TOTAL TAHUNAN ===
    total_tahunan = df_agg.groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()
    total_tahunan.columns = ["Tahun", "Total Subsidi (Miliar USD)"]

    st.write(f"### Total Subsidi per Tahun - {'Global' if negara_dipilih == 'Seluruh Dunia' else negara_dipilih}")
    st.dataframe(total_tahunan, use_container_width=True)

    # === TOTAL KESELURUHAN ===
    total_semua = total_tahunan["Total Subsidi (Miliar USD)"].sum()

    st.markdown(
        f"""
        <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center; padding: 10px;'>
            <h4 style='color: #007acc;'>Total Keseluruhan: {total_semua:,.2f} miliar USD</h4>
        </div>
        """,
        unsafe_allow_html=True
    )