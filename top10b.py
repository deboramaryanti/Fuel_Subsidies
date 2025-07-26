import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import gdown

def rata_sub():
    st.subheader("Visualisasi Rata-rata Subsidi Energi per Negara")
    
    # Load dan persiapan data
    file_id = "15kwCyRwyenxTdiSINSOI7NLqI5LVN1Wz"
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    data = pd.read_csv(download_url)

    df = data[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # miliar USD

    tahun_unik = sorted(df["TIME_PERIOD"].unique())
    tahun_min = min(tahun_unik)
    tahun_max = max(tahun_unik)
    now = datetime.now().year
    negara_unik = sorted(df["REF_AREA_NAME"].unique())

    # === SIDEBAR FILTER ===
    with st.sidebar:
        st.markdown("Filter Rata-rata Subsidi")

        # Default range 5 tahun terakhir jika tersedia
        tahun_awal_default = max(tahun_min, now - 4)
        tahun_akhir_default = min(tahun_max, now)

        rentang_tahun = st.slider(
            "Pilih Rentang Tahun:",
            min_value=tahun_min,
            max_value=tahun_max,
            value=(tahun_awal_default, tahun_akhir_default),
            step=1
        )

        negara_dipilih = st.multiselect("Pilih Negara:", negara_unik)

    # === FILTER DATA ===
    df_avg = df[
        (df["TIME_PERIOD"] >= rentang_tahun[0]) &
        (df["TIME_PERIOD"] <= rentang_tahun[1])
    ]

    if negara_dipilih:
        df_avg = df_avg[df_avg["REF_AREA_NAME"].isin(negara_dipilih)]

    # === HITUNG RATA-RATA ===
    df_rata = df_avg.groupby("REF_AREA_NAME")["OBS_VALUE"].mean().reset_index()
    df_rata.columns = ["Negara", "Rata-rata Subsidi"]

    top10_rata = df_rata.sort_values(by="Rata-rata Subsidi", ascending=False).head(10)

    # === PLOT HASIL ===
    if not top10_rata.empty:
        judul = f"Top 10 Negara dengan Rata-rata Subsidi Energi Tertinggi ({rentang_tahun[0]}–{rentang_tahun[1]})"
        if negara_dipilih:
            judul += " (Negara Terpilih)"

        fig = px.bar(
            top10_rata,
            x="Negara",
            y="Rata-rata Subsidi",
            title=judul,
            labels={"Rata-rata Subsidi": "Subsidi Rata-rata (Miliar USD)"},
            color="Rata-rata Subsidi",
            color_continuous_scale="Blues"
        )
        st.plotly_chart(fig)

        st.write("Tabel Rata-rata Subsidi (semua negara terfilter):")
        st.dataframe(df_rata.sort_values(by="Rata-rata Subsidi", ascending=False), use_container_width=True)
    else:
        st.warning("Data tidak ditemukan untuk kombinasi filter tersebut.")
        st.markdown(
            f"""
            <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center;'>
                <h4 style='color: #007acc;'>Total Keseluruhan: {df_rata['Rata-rata Subsidi'].sum():,.2f} miliar USD</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
