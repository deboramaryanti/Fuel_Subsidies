import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def tampilkan_analysis():
    st.title("Analisis Interaktif Subsidi Energi Dunia")

    # Pilih jenis visualisasi
    pilihan_chart = st.radio("Pilih Chart:", [
        "Chart 1",
        "Chart 2",
        "Chart 3"
    ])

    # --- CHART 1: Tren Subsidi Global ---
    if pilihan_chart.startswith("Chart 1"):
        import global_sub
        global_sub.chart_1()
    
    # --- CHART 2: Top 10 Negara per Tahun ---
    elif pilihan_chart.startswith("Chart 2"):
        import top10
        top10.chart_2()

    # --- CHART 3: Negara dengan Subsidi Eksplisit vs Implisit ---
    elif pilihan_chart.startswith("Chart 3"):
        import jenis
        jenis.chart_3()