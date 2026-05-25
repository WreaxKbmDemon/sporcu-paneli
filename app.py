import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# 🖥️ SAYFA YAPILANDIRMASI VE DARK MODE ESTETİĞİ
st.set_page_config(page_title="SPORCU PANELİ V1.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #00FFCC !important; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00FFCC; color: #000000; font-weight: bold; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF; font-size: 16px; font-weight: bold; }
    .stTabs [data-baseweb="tab"]:hover { color: #00FFCC; }
    .stTabs [aria-selected="true"] { color: #00FFCC !important; border-bottom-color: #00FFCC !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ MACROFLOW // SPORCU PANELİ - HARDCORE EDITION")
st.write(f"⚙️ Sistem Kararlılığı: MÜKEMMEL | 📅 Bugün: Pazartesi | 🕒 Güncelleme: {datetime.now().strftime('%H:%M')}")

# 🗂️ SEKMELERİ OLUŞTURMA
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👤 Sporcu Paneli", "📝 Rutin Takip & Notlar", "🍗 Beslenme Planı", 
    "🏃‍♂️ Kardiyo Takip", "🏋️‍♂️ Antrenman Takip", "💊 Supplement & Cycle"
])

# ==========================================
# 👤 TAB 1: SPORCU PANELİ & ÖZET
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📋 Sporcu Profil Logları")
        st.info("**Eren** | 16 Yaş\n\n**Boy:** 173 cm | **Bel:** 78 cm \n\n**Kilo:** 71.25 kg | **Yağ oranı:** %11-11,5")
        st.subheader("🔥 Günlük Makro Çıktısı")
        st.code("Kalori: ~1700-2000 kcal\nProtein: ~140-195.5g\nCarb: ~137.2-250g\nSu : 4,5-5 lt")
    with col2:
        st.subheader("📉 Ağırlık Değişim Grafiği")
        df_kilo = pd.DataFrame({"Hafta": [f"{i}.H" for i in range(1,6)], "Kilo": [73.5, 72.8, 72.1, 71.5, 71.25]})
        fig = px.line(df_kilo, x="Hafta", y="Kilo", markers=True)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

# ==========================================
# 📝 TAB 2: RUTİN TAKİP VE NOTLAR
# ==========================================
with tab2:
    st.subheader("📆 Günlük Metrik Takip Çizelgesi")
    df_rutin = pd.DataFrame({
        "Gün": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
        "Sabah KG": [71.25, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "Su (ml)": [3006, 0, 0, 0, 0, 0, 0],
        "Bugünkü Zafer Notları": ["100 kg bench press 2 tekrar atıldı 15 eğim 5,5 hız 45 dakika kardio yapıldı.", "", "", "", "", "", ""]
    })
    st.data_editor(df_rutin, use_container_width=True)

# ==========================================
# 🍗 TAB 3: BESLENME PLANI
# ==========================================
with tab3:
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

# ==========================================
# 🏃‍♂️ TAB 4: KARDİYO TAKİP PLANI (HAFTA SONU OFF - GÜNCELLENDİ)
# ==========================================
with tab4:
    st.subheader("⏱️ Haftalık Kardiyo Takip Matriksi")
    st.success("PROTOKOL: 15 Eğim, 5.5 Hız, 30 Dakika Hafta İçi Hergün HaftaSonu Offday (Kardio Yok)")
    df_kardiyo = pd.DataFrame({
        "Gün": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
        "Tip": ["Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "OFFDAY 💤", "OFFDAY 💤"],
        "Eğim/Hız": ["15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "-", "-"],
        "Süre": ["30 Dk ⏱️", "30 Dk", "30 Dk", "30 Dk", "30 Dk", "-", "-"],
        "Durum": ["BİTTİ 🏆", "Bekliyor", "Bekliyor", "Bekliyor", "Bekliyor", "DİNLENME", "DİNLENME"]
    })
    st.table(df_kardiyo)

# ==========================================
# 🏋️‍♂️ TAB 5: ANTRENMAN TAKİP
# ==========================================
with tab5:
    st.subheader("⚔️ BUGÜNKÜ PAZARTESİ İDMAN LOGLARI (GERÇEKLEŞEN METRİK)")
    
    col_pzt, col_pro = st.columns([2, 1])
    with col_pzt:
        st.markdown("### 🔴 BUGÜN BASILAN REKOR KİLOLAR (PZT)")
        df_bugun = pd.DataFrame({
            "Hareket": ["Bench Press (Set 1)", "Bench Press (Set 2)", "Incline DB Press (Set 1)", "Incline DB Press (Set 2)", "Pec Deck (Set 1)", "Pec Deck (Set 2)", "Düz Bar Pushdown (Set 1)", "Düz Bar Pushdown (Set 2)", "Overhead Cable V Bar Ext (Set 1)", "Overhead Cable V Bar Ext (Set 2)", "Hanging Leg Raise", "Crunch", "Plank (Ağırlıksız)"],
            "Ağırlık (kg)": ["100 kg", "90 kg", "30 kg (DB)", "30 kg (DB)", "84 kg", "77 kg", "60 kg", "55 kg", "40 kg", "40 kg", "Vücut", "Vücut", "Süre"],
            "Tekrar / Süre": ["2 Tekrar 🚀", "5 Tekrar", "4 Tekrar", "5 Tekrar", "5 Tekrar", "5 Tekrar", "6 Tekrar", "7 Tekrar", "8 Tekrar", "9 Tekrar", "1.Set: 20 | 2.Set: 14", "1.Set: 30 | 2.Set: 30", "1.Set: 1:30 Dk | 2.Set: 1:00 Dk"]
        })
        st.dataframe(df_bugun, use_container_width=True, hide_index=True)
    with col_pro:
        st.markdown("### 🗓️ Haftalık split şablonu")
        st.info("Pzt/Per: Göğüs-Triceps\n\nSal/Cum: Sırt-Biceps-Karın\n\nÇarş: Omuz\n\nCmt/Paz: RECOVERY (OFFDAY)")

# ==========================================
# 💊 TAB 6: SUPPLEMENT & CYCLE
# ==========================================
with tab6:
    st.subheader("💊 Güncel Supplement Enjeksiyon Zamanlaması")
    st.table(pd.DataFrame({
        "Dönem / Safha": ["💥 SPOR ÖNCESİ", "💥 SPOR ARASI", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE"],
        "Takviye İçeriği": ["0.75 ÖlçekPre-Workout + 4 Kapsül L-Carnitine", "2 Kapsül Thermo Burner 🔥", "5 Gram Creatine", "1 Kapsül Zinc (Çinko)", "1-2 Gram Magnezyum L-Threonate"],
        "Hedef Kodlama": ["Maksimum Odak ve Yağ Yakımı", "Termojenik Ateşleme", "Gece ATP Hücre Dolumu", "Testosteron Koruma Kalkanı", "REM Derin Uyku & CNS Reset"]
    }))