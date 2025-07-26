import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def chart_1():
    st.subheader("Tren Subsidi Energi (Berdasarkan Jenis)")

    # Load data
    df = pd.read_csv("IMF_FFS.csv")
    df = df[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # Miliar USD

    tahun_min = df["TIME_PERIOD"].min()
    tahun_max = df["TIME_PERIOD"].max()
    negara_unik = sorted(df["REF_AREA_NAME"].unique())

    # === SIDEBAR ===
    with st.sidebar:
        st.markdown("### Filter")
        # Negara dengan default "Seluruh Dunia"
        negara_opsi = ["Seluruh Dunia"] + negara_unik
        negara_dipilih = st.selectbox("Pilih Negara:", options=negara_opsi)

        # Jenis subsidi
        opsi_jenis = sorted(df["INDICATOR_NAME"].unique())
        jenis_dipilih = st.multiselect(
            "Jenis subsidi:",
            options=opsi_jenis,
            default=[opsi_jenis[0]],
            key="jenis_subsidi"
        )

    # === FILTER ===
    df_pilih = df[df["INDICATOR_NAME"].isin(jenis_dipilih)]
    if negara_dipilih != "Seluruh Dunia":
        df_pilih = df_pilih[df_pilih["REF_AREA_NAME"] == negara_dipilih]

    if not df_pilih.empty:
        # Agregasi untuk grafik
        df_agg = df_pilih.groupby(["TIME_PERIOD", "INDICATOR_NAME"])["OBS_VALUE"].sum().reset_index()

        fig = px.line(
            df_agg,
            x="TIME_PERIOD",
            y="OBS_VALUE",
            color="INDICATOR_NAME",
            markers=True,
            title=f"Tren Subsidi Energi {'Global' if negara_dipilih == 'Seluruh Dunia' else negara_dipilih}",
            labels={
                "TIME_PERIOD": "Tahun",
                "OBS_VALUE": "Subsidi (Miliar USD)",
                "INDICATOR_NAME": "Jenis Subsidi"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        # Total per tahun
        total_global = df_agg.groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()
        total_global.columns = ["Tahun", "Total Subsidi (Miliar USD)"]
        st.write(f"### Total Subsidi per Tahun - {'Global' if negara_dipilih == 'Seluruh Dunia' else negara_dipilih}")
        st.dataframe(total_global)

        total_sum = total_global["Total Subsidi (Miliar USD)"].sum()
        st.markdown(
            f"""
            <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center; padding: 10px;'>
                <h4 style='color: #007acc;'>Total Keseluruhan: {total_sum:,.2f} miliar USD</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("Silakan pilih jenis subsidi untuk melihat tren.")
