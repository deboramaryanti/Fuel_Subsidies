import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def chart_3():
    st.subheader("Negara dengan Subsidi Eksplisit vs Implisit")

    # Load data
    df = pd.read_csv("IMF_FFS.csv")
    df = df[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # Miliar USD

    tahun_min = df["TIME_PERIOD"].min()
    tahun_max = df["TIME_PERIOD"].max()
    now = datetime.now().year
    negara_unik = sorted(df["REF_AREA_NAME"].unique())

    # === SIDEBAR FILTER ===
    with st.sidebar:
        st.markdown("Filter Subsidi Eksplisit vs Implisit")
        
        # Rentang tahun default: 5 tahun terakhir
        tahun_awal_default = max(tahun_min, now - 4)
        tahun_akhir_default = min(tahun_max, now)

        rentang_tahun = st.slider(
            "Pilih Rentang Tahun:",
            min_value=int(tahun_min),
            max_value=int(tahun_max),
            value=(tahun_awal_default, tahun_akhir_default),
            step=1
        )

        negara_dipilih = st.multiselect("Pilih Negara:", negara_unik)

    # === FILTER DATA ===
    df = df[
        (df["TIME_PERIOD"] >= rentang_tahun[0]) &
        (df["TIME_PERIOD"] <= rentang_tahun[1])
    ]

    if negara_dipilih:
        df = df[df["REF_AREA_NAME"].isin(negara_dipilih)]

    df_filter = df[df["INDICATOR_NAME"].str.contains("Explicit|Implicit", case=False)]
    eksplisit = df_filter[df_filter["INDICATOR_NAME"].str.contains("Explicit", case=False)]
    implisit = df_filter[df_filter["INDICATOR_NAME"].str.contains("Implicit", case=False)]

    # === Hitung total per negara ===
    sum_eksplisit = eksplisit.groupby("REF_AREA_NAME")["OBS_VALUE"].sum()
    sum_implisit = implisit.groupby("REF_AREA_NAME")["OBS_VALUE"].sum()

    gabung = pd.concat([sum_eksplisit, sum_implisit], axis=1).fillna(0)
    gabung.columns = ["Eksplisit", "Implisit"]
    gabung["Total"] = gabung["Eksplisit"] + gabung["Implisit"]
    gabung["Negara"] = gabung.index

    top10 = gabung.sort_values("Total", ascending=False).head(10)

    # === Ubah ke format long untuk plot ===
    long_df = top10.melt(
        id_vars="Negara",
        value_vars=["Eksplisit", "Implisit"],
        var_name="Jenis",
        value_name="Subsidi"
    )

    # === Plot ===
    if not long_df.empty:
        judul = f"Top 10 Negara: Subsidi Eksplisit vs Implisit ({rentang_tahun[0]}–{rentang_tahun[1]})"
        if negara_dipilih:
            judul += " (Negara Terpilih)"

        fig = px.bar(
            long_df,
            x="Negara",
            y="Subsidi",
            color="Jenis",
            barmode="group",
            title=judul,
            labels={"Subsidi": "Subsidi (Miliar USD)"},
            color_discrete_map={"Eksplisit": "#1f77b4", "Implisit": "#ff7f0e"}
        )
        st.plotly_chart(fig)

        st.write("Tabel Total Subsidi per Negara:")
        st.dataframe(top10[["Eksplisit", "Implisit", "Total"]].sort_values("Total", ascending=False), use_container_width=True)

        st.write("Total Global:")
        st.success(f"Total Eksplisit: {round(top10['Eksplisit'].sum(), 2)} miliar USD")
        st.info(f"Total Implisit: {round(top10['Implisit'].sum(), 2)} miliar USD")
    else:
        st.warning("Data tidak ditemukan untuk kombinasi filter tersebut.")
        st.markdown(
            f"""
            <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center;'>
                <h4 style='color: #007acc;'>Total Keseluruhan: {gabung['Total'].sum():,.2f} miliar USD</h4>
            </div>
            """,
            unsafe_allow_html=True
        )