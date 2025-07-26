import streamlit as st
import pandas as pd
from prophet import Prophet
import plotly.express as px
from datetime import datetime
import gdown

def tampilkan_prediction():
    st.set_page_config(page_title="Prediksi Subsidi Energi Global", layout="wide")
    st.title("Prediksi Subsidi Energi dengan Prophet")

    # Load data
    file_id = "15kwCyRwyenxTdiSINSOI7NLqI5LVN1Wz"
    download_url = f"https://drive.google.com/uc?id={file_id}"
    
    data = pd.read_csv(download_url)

    df = data[["TIME_PERIOD", "REF_AREA_NAME", "INDICATOR_NAME", "OBS_VALUE"]].dropna()
    df["TIME_PERIOD"] = df["TIME_PERIOD"].astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce") / 1e9  # dalam miliar USD

    # Sidebar
    with st.sidebar:
        st.header("Filter")
        tahun_min = int(df["TIME_PERIOD"].min())
        tahun_max = int(df["TIME_PERIOD"].max())
        negara_opsi = ["Seluruh Dunia"] + sorted(df["REF_AREA_NAME"].unique())
        negara_dipilih = st.selectbox("Pilih Negara:", options=negara_opsi)
        indikator_dipilih = st.selectbox("Pilih Jenis Subsidi:", sorted(df["INDICATOR_NAME"].unique()))
        tahun_prediksi = st.slider("Prediksi Hingga Tahun:", tahun_max + 1, tahun_max + 10, tahun_max + 5)

    # Filter data
    df_pilih = df[df["INDICATOR_NAME"] == indikator_dipilih]
    if negara_dipilih != "Seluruh Dunia":
        df_pilih = df_pilih[df_pilih["REF_AREA_NAME"] == negara_dipilih]

    # Agregasi jika seluruh dunia
    df_agg = df_pilih.groupby("TIME_PERIOD")["OBS_VALUE"].sum().reset_index()

    if df_agg.shape[0] < 5:
        st.warning("Data terlalu sedikit untuk membuat prediksi.")
    else:
        # Siapkan untuk Prophet
        df_prophet = df_agg.rename(columns={"TIME_PERIOD": "ds", "OBS_VALUE": "y"})
        df_prophet["ds"] = pd.to_datetime(df_prophet["ds"], format="%Y")

        model = Prophet(yearly_seasonality=True)
        model.fit(df_prophet)

        # Buat future frame
        future_years = list(range(df_prophet["ds"].dt.year.max() + 1, tahun_prediksi + 1))
        future = pd.DataFrame({"ds": pd.date_range(start=f"{future_years[0]}-01-01", end=f"{tahun_prediksi}-01-01", freq="YS")})
        full_future = pd.concat([df_prophet[["ds"]], future])

        forecast = model.predict(full_future)

        hasil = forecast[["ds", "yhat"]]
        hasil["Tahun"] = hasil["ds"].dt.year
        hasil["Subsidi (Prediksi)"] = hasil["yhat"]
        hasil = hasil[hasil["Tahun"] <= tahun_prediksi]

        # Visualisasi
        judul = f"Prediksi Subsidi {'Global' if negara_dipilih == 'Seluruh Dunia' else negara_dipilih} ({indikator_dipilih}) hingga {tahun_prediksi}"
        fig = px.line(hasil, x="Tahun", y="Subsidi (Prediksi)", markers=True,
                      title=judul,
                      labels={"Subsidi (Prediksi)": "Subsidi (Miliar USD)"})
        st.plotly_chart(fig)

        # Tabel
        st.write("Data Prediksi:")
        st.dataframe(hasil[["Tahun", "Subsidi (Prediksi)"]].round(2))

        # Prediksi tahun terakhir
        if tahun_prediksi in hasil["Tahun"].values:
            pred_specific = hasil[hasil["Tahun"] == tahun_prediksi]["Subsidi (Prediksi)"].values[0]
            st.success(f"Prediksi subsidi tahun {tahun_prediksi}: {pred_specific:.2f} miliar USD")
        else:
            st.warning(f"Tidak ada prediksi untuk tahun {tahun_prediksi}.")

        # Total semua prediksi
        st.markdown(
            f"""
            <div style='background-color: #e6f7ff; border-radius: 10px; text-align: center; padding: 10px;'>
                <h4 style='color: #007acc;'>Total Prediksi hingga {tahun_prediksi}: {hasil['Subsidi (Prediksi)'].sum():,.2f} miliar USD</h4>
            </div>
            """,
            unsafe_allow_html=True
        )
