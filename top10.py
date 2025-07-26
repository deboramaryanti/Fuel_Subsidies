import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

def chart_2():
    st.subheader("Top 10 Negara Pemberi Subsidi per Tahun")

    # Pilih jenis visualisasi
    sub_pilihan_chart = st.radio("Mau chart yang apa?", [
        "Total Subsidi Negara tiap Tahun",
        "Rata-rata Subsidi"
    ])
    
    if sub_pilihan_chart.startswith("Total Subsidi Negara tiap Tahun"):
        import top10a
        top10a.total_sub()
    
    # --- CHART 2: Top 10 Negara per Tahun ---
    elif sub_pilihan_chart.startswith("Rata-rata Subsidi"):
        import top10b
        top10b.rata_sub()
