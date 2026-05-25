import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 🖥️ SAYFA YAPILANDIRMASI VE DARK MODE ESTETİĞİ
st.set_page_config(page_title="SPORCU PANELİ V2.0", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; color: #FFFFFF; }
    h1, h2, h3 { color: #00FFCC !important; font-family: 'Courier New', monospace; }
    .stButton>button { background-color: #00FFCC; color: #000000; font-weight: bold; border-radius: 8px; width: 100%; }
    .stTabs [data-baseweb="tab"] { color: #FFFFFF; font-size: 16px; font-weight: bold; }
    .stTabs [data-baseweb="tab"]:hover { color: #00FFCC; }
    .stTabs [aria-selected="true"] { color: #00FFCC !important; border-bottom-color: #00FFCC !important; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ MACROFLOW // SPORCU PANELİ - HARDCORE V2.0")
st.write(f"⚙️ Sistem Kararlılığı: VERİ TABANI AKTİF | 📅 Bugün: {datetime.now().strftime('%d.%m.%Y')}")

# 💾 CSV VERİ TABANI ALTYAPISI (DATA PERSISTENCE)
CSV_FILE = "data/sporcu_verileri.csv"

# Eğer dosya yoksa ilk dizini ve kolonları jilet gibi oluştur
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Kilo", "Su_ml"])
    df_init.to_csv(CSV_FILE, index=False)

# 🗂️ SEKMELERİ OLUŞTURMA
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "👤 Sporcu Paneli", "📝 Veri Giriş Reaktörü", "🍗 Beslenme Planı", 
    "🏃‍♂️ Kardiyo Takip", "🏋️‍♂️ Antrenman Takip", "💊 Supplement & Cycle"
])

# ==========================================
# 👤 TAB 1: SPORCU PANELİ & GRAFİK ÖZET
# ==========================================
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📋 Sporcu Profil Logları")
        st.info("**Eren** | 16 Yaş (9-Bilişim)\n\n**Boy:** 173 cm | **Bel:** 78 cm 🎯\n\n**Durum:** Canavar Modu")
        st.subheader("🔥 Günlük Makro Çıktısı")
        st.code("Kalori: ~1700-2000 kcal\nProtein: ~140-195.5g (Çiğden)\nCarb: ~137.2-250g\nSu Hedefi: 4.5 - 5 Litre 🚰")
    with col2:
        st.subheader("📉 Gerçek Zamanlı Kilo Değişim Grafiği")
        df_read = pd.read_csv(CSV_FILE)
        if not df_read.empty:
            fig = px.line(df_read, x="Tarih", y="Kilo", markers=True, title="Veri Tabanından Çekilen Canlı Kilo Grafiği")
            fig.update_traces(line_color="#00FFCC", marker=dict(size=8, color="#FF007F"))
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("⚠️ Veri tabanında henüz kayıtlı veri yok! Yan sekmeden ilk verini gir amınakoyim!")

# ==========================================
# 📝 TAB 2: VERİ GİRİŞ REAKTÖRÜ (DÜZELTİLDİ 🚀)
# ==========================================
with tab2:
    st.subheader("🚀 Telefondan Anlık Veri Giriş Paneli")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        input_kilo = st.number_input("Sabah Aç Karnına Kilonuz (kg):", min_value=30.0, max_value=150.0, value=71.25, step=0.05)
    with col_input2:
        input_su = st.number_input("Bugün İçilen Toplam Su (ml):", min_value=0, max_value=10000, value=3000, step=250)
        
    if st.button("🔥 VERİLERİ VERİ TABANINA MÜHÜRLE"):
        df_current = pd.read_csv(CSV_FILE)
        bugun_str = datetime.now().strftime("%d.%m.%Y")
        
        # Eğer bugün zaten kayıt girildiyse üzerine yaz (güncelle), yoksa yeni satır ekle
        if bugun_str in df_current["Tarih"].values:
            df_current.loc[df_current["Tarih"] == bugun_str, ["Kilo", "Su_ml"]] = [input_kilo, input_su]
        else:
            new_row = pd.DataFrame([{"Tarih": bugun_str, "Kilo": input_kilo, "Su_ml": input_su}])
            df_current = pd.concat([df_current, new_row], ignore_index=True)
            
        df_current.to_csv(CSV_FILE, index=False)
        st.success(f"✅ Veriler `data/sporcu_verileri.csv` dosyasına jilet gibi işlendi! İlk sekmeyi yenileyebilirsin amınakoyim.")

    st.write("---")
    st.subheader("📋 Kayıtlı Tüm Geçmiş Verilerin (CSV Çıktısı)")
    st.dataframe(pd.read_csv(CSV_FILE), use_container_width=True)

# ==========================================
# 🍗 TAB