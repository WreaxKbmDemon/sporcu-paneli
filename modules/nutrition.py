import streamlit as st
import pandas as pd

def render_nutrition_tab():
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("🍗 Antrenman Günü")
        st.table(pd.DataFrame({
            "Öğün": ["Kahvaltı", "İdman Öncesi", "Akşam"],
            "İçerik": ["350g Çiğden Tavuk + 2 Yumurta + Lor", "1 Büyük Muz", "Bulgur + Patates + 300g Çiğden Tavuk"]
        }))
    with col_b:
        st.subheader("💤 Dinlenme Günü")
        st.warning("Karb döngüsü için kalibre edilecektir.")