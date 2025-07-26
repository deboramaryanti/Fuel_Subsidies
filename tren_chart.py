import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def chart_1():
    st.subheader("Tren Subsidi Energi Global")

    # Pilih jenis visualisasi
    sub_pilihan_chart = st.radio("Mau chart yang apa?", [
        "Tren Subsidi Energi Global (Total Implicit & Explicit)",
        "Tren Subsidi Energi Global (Berdasarkan Jenis)"
    ])
    
    if sub_pilihan_chart.startswith("Tren Subsidi Energi Global (Total Implicit & Explicit)"):
        import tren1
        tren1.tren_chart_1()
    
    # --- CHART 2: Top 10 Negara per Tahun ---
    elif sub_pilihan_chart.startswith("Tren Subsidi Energi Global (Berdasarkan Jenis)"):
        import tren2
        tren2.tren_chart_2()
