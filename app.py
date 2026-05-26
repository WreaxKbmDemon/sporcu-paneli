import streamlit as st
import pandas as pd
import openpyxl
from datetime import datetime

# Siberpunk / Neon Karanlık Tema Ayarları
st.set_page_config(page_title="Eren Aydın - Sporcu Paneli", page_icon="🦾", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1A1D29; color: #FFFFFF; }
    h1, h2, h3 { color: #00E5FF !important; }
    .stButton>button { background-color: #00FFCC; color: #1A1D29; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 SİBERPUNK SPORCU PANELİ // v2.0")

# Sol Panel: Danışman & Koçluk Bilgileri
with st.sidebar:
    st.header("📋 PROFİL BİLGİLERİ")
    st.write("**Adı Soyadı:** Eren Aydın")
    st.write("**Yaş:** 16 | **Boy:** 175 cm | **Başlangıç Kilo:** 74 kg")
    st.write(f"**Güncel Tarih:** {datetime.now().strftime('%d.%m.%Y')}")
    st.markdown("---")
    st.write("🎯 **Definasyon Hedefi:** Yüksek Protein / Düşük Karbonhidrat")

# Ana Sayfa Tab Yapısı (Excel'deki Sekmelerin Streamlit Karşılığı)
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 ANASAYFA MATRİSİ", 
    "📝 RUTİN TAKİP", 
    "🥗 BESLENME", 
    "🏃‍♂️ KARDİYO PLANI", 
    "🏋️‍♂️ ANTREMAN PROGRAMI"
])

with tab1:
    st.subheader("60 Haftalık Gelişim Döngüsü")
    st.info("Bu matris, haftalık ortalamaları otomatik olarak loglar.")
    # Örnek 60 haftalık veri simülasyonu
    weeks = [f"{i}. HAFTA" for i in range(1, 61)]
    df_matrix = pd.DataFrame({
        "Hafta": weeks,
        "Ortalama Kilo": [72.5 if i==1 else None for i in range(1, 61)],
        "Kilo Analizi": ["BAŞLANGIÇ" if i==1 else None for i in range(1, 61)],
        "Su Tüketimi (L)": [4.0 if i==1 else None for i in range(1, 61)],
        "Yağ Oranı (%)": [12.0 if i==1 else None for i in range(1, 61)]
    })
    st.dataframe(df_matrix, use_container_width=True, height=400)

with tab2:
    st.subheader("Genel Haftalık Takip (Pazartesi - Pazar)")
    st.write("Günlük Sabah KG, Su ve Yağ Oranı girişlerini buradan yapabilirsin.")
    # Hafta içi takip veri tablosu
    days = ["PAZARTESİ", "SALI", "SABAH KG DURUMU", "PERŞEMBE", "CUMA", "CUMARTESİ", "PAZAR"]
    # Form alanları eklenebilir

with tab3:
    st.subheader("10 Öğünlük Beslenme Programı")
    col_ant, col_din = st.columns(2)
    with col_ant:
        st.markdown("### 🏋️‍♂️ Antrenman Günü")
        st.caption("Çiğden 650g Tavuk Göğsü, 2 Yumurta, Lor, Muz, Çay (Makro: ~1092 kcal / 170g Protein)")
    with col_din:
        st.markdown("### 🛌 Dinlenme Günü")
        st.caption("Makrolar sabit, uyarım takviyeleri kapalı.")

with tab4:
    st.subheader("Haftalık Kardiyo Takip Planı")
    st.success("🏃‍♂️ KOŞU BANDI: 15 EĞİM // 5 HIZ // 45 DAKİKA")
    st.warning("⚠️ ZAMANLAMA: İdmandan önce 1 ölçek Pre + 4 Kapsül L-Carnitine. Kardiyoya geçmeden 15 dk önce 2 Kapsül Thermo Burner!")

with tab5:
    st.subheader("🏋️‍♂️ HAFTALIK SİSTEMLİ ANTREMAN PROGRAMI")
    
    # İstediğin Antrenman Programı Detayları
    with st.expander("📅 PAZARTESİ - İTİŞ (PUSH) GÜNÜ", expanded=True):
        st.markdown("""
        * **Göğüs - Omuz - Triceps**
        * 1. Incline Bench Press: 4 Set x 8-10 Tekrar (90sn Dinlenme)
        * 2. Flat Dumbbell Press: 3 Set x 10 Tekrar
        * 3. Seated Dumbbell Shoulder Press: 4 Set x 10 Tekrar
        * 4. Lateral Raise (Yana Açış): 4 Set x 12-15 Tekrar
        * 5. Cable Pushdown: 3 Set x 12 Tekrar
        """)
        
    with st.expander("📅 SALI - ÇEKİŞ (PULL) GÜNÜ"):
        st.markdown("""
        * **Sırt - Arka Omuz - Biceps**
        * 1. Lat Pulldown / Barfiks: 4 Set x 8-10 Tekrar
        * 2. Seated Cable Row: 3 Set x 10 Tekrar
        * 3. Face Pull (Arka Omuz): 4 Set x 15 Tekrar
        * 4. Barbell Curl: 3 Set x 10 Tekrar
        * 5. Hammer Curl: 3 Set x 12 Tekrar
        """)

    with st.expander("📅 ÇARŞAMBA - BACAK (LEGS) GÜNÜ"):
        st.markdown("""
        * **Quadriceps - Hamstrings - Kalf**
        * 1. Barbell Squat: 4 Set x 8 Tekrar
        * 2. Leg Press: 3 Set x 10-12 Tekrar
        * 3. Leg Curl: 4 Set x 12 Tekrar
        * 4. Standing Calf Raise: 4 Set x 15 Tekrar
        """)

    with st.expander("📅 PERŞEMBE - İTİŞ (PUSH) GÜNÜ"):
        st.markdown("Pazartesi rutinindeki hareketlerle progresif overload (ağırlık arttırma) odaklı idman.")

    with st.expander("📅 CUMA - ÇEKİŞ (PULL) GÜNÜ"):
        st.markdown("Salı rutinindeki hareketlerle tonaj ve kas pump odaklı idman.")