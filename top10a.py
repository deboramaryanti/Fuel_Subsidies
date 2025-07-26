import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gdown

def total_sub():
    st.subheader("Visualisasi Total Subsidi Negara per Tahun")

    # Load dan persiapan data
    file_id = "15kwCyRwyenxTdiSINSOI7NLqI5LVN1Wz"
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    data = pd.read_csv(download_url)

    df = data[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # miliar

    tahun_unik = sorted(df["TIME_PERIOD"].unique())
    negara_unik = sorted(df["REF_AREA_NAME"].unique())

    # Tentukan default tahun (now jika ada, jika tidak pakai tahun max dari data)
    now = datetime.now().year
    tahun_default = now if now in tahun_unik else max(tahun_unik)

    # === SIDEBAR FILTER ===
    with st.sidebar:
        st.markdown("### Filter")
        tahun_dipilih = st.multiselect("Pilih Tahun:", tahun_unik, default=[tahun_default])
        negara_dipilih = st.multiselect("Pilih Negara:", negara_unik)

    # === FILTER DATA ===
    df_filter = df.copy()
    if tahun_dipilih:
        df_filter = df_filter[df_filter["TIME_PERIOD"].isin(tahun_dipilih)]
    if negara_dipilih:
        df_filter = df_filter[df_filter["REF_AREA_NAME"].isin(negara_dipilih)]

    # === AGREGASI & TOP 10 ===
    df_agg = df_filter.groupby("REF_AREA_NAME")["OBS_VALUE"].sum().reset_index()
    top10 = df_agg.sort_values(by="OBS_VALUE", ascending=False).head(10)

    # === PLOT ===
    if not top10.empty:
        judul = "Top 10 Negara dengan Subsidi Tertinggi"
        if tahun_dipilih:
            judul += f" pada Tahun {', '.join(map(str, tahun_dipilih))}"
        if negara_dipilih:
            judul += " (Negara Terpilih)"

        fig = px.bar(
            top10, 
            x="REF_AREA_NAME", 
            y="OBS_VALUE",
            title=judul,
            labels={"REF_AREA_NAME": "Negara", "OBS_VALUE": "Subsidi (Miliar USD)"},
            color="OBS_VALUE",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig)
    else:
        st.warning("Data tidak ditemukan untuk kombinasi filter tersebut.")
        st.markdown(
            f"""
            <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center;'>
                <h4 style='color: #007acc;'>Total Keseluruhan: {top10['Top 10 Negara dengan Subsidi Tertinggi'].sum():,.2f} miliar USD</h4>
            </div>
            """,
            unsafe_allow_html=True
        )