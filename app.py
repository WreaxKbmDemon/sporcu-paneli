import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 🔌 YENİ AÇTIĞIMIZ MODÜLLERİN SİSTEME ENJEKTE EDİLMESİ (IMPORT)
from modules.workout import render_workout_tab
from modules.nutrition import render_nutrition_tab

# 🖥️ SAYFA YAPILANDIRMASI VE DARK MODE ESTETİĞİ
st.set_page_config(page_title="SPORCU PANELİ V2.3", layout="wide")

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

st.title("⚡ MACROFLOW // SPORCU PANELİ - MODULAR V2.3")
st.write(f"⚙️ Sistem Kararlılığı: MODÜLER MİMARİ AKTİF | 📅 Bugün: {datetime.now().strftime('%d.%m.%Y')}")

# 💾 CSV VERİ TABANI ALTYAPISI (DATA PERSISTENCE)
CSV_FILE = "data/sporcu_verileri.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Kilo", "Su_ml", "Gunluk_Not"])
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
        st.info("**Eren** | 16 Yaş (9-Bilişim)\n\n**Boy:** 173 cm | **Bel:** 78 cm 🎯\n\n**Durum:** Yağ Oranı %11,5-11")
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
# 📝 TAB 2: VERİ GİRİŞ REAKTÖRÜ
# ==========================================
with tab2:
    st.subheader("🚀 Telefondan Anlık Veri Giriş Paneli")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        input_kilo = st.number_input("Sabah Aç Karnına Kilonuz (kg):", min_value=30.0, max_value=150.0, value=71.25, step=0.05)
    with col_input2:
        input_su = st.number_input("Bugün İçilen Toplam Su (ml):", min_value=0, max_value=10000, value=3000, step=250)
        
    input_not = st.text_input("Bugünkü Zafer Notlarınız (İdman Raporu / Hissiyat):", value="100 kg bench press 2 tekrar atıldı 15 eğim 5,5 hız 30 dakika kardio yapıldı.")
        
    if st.button("🔥 VERİLERİ VE NOTU VERİ TABANINA MÜHÜRLE"):
        df_current = pd.read_csv(CSV_FILE)
        if "Gunluk_Not" not in df_current.columns:
            df_current["Gunluk_Not"] = ""
            
        bugun_str = datetime.now().strftime("%d.%m.%Y")
        
        if bugun_str in df_current["Tarih"].values:
            df_current.loc[df_current["Tarih"] == bugun_str, ["Kilo", "Su_ml", "Gunluk_Not"]] = [input_kilo, input_su, input_not]
        else:
            new_row = pd.DataFrame([{"Tarih": bugun_str, "Kilo": input_kilo, "Su_ml": input_su, "Gunluk_Not": input_not}])
            df_current = pd.concat([df_current, new_row], ignore_index=True)
            
        df_current.to_csv(CSV_FILE, index=False)
        st.success(f"✅ Veriler ve Notunuz `data/sporcu_verileri.csv` dosyasına jilet gibi işlendi! Sayfa güncellendi amınakoyim.")

    st.write("---")
    st.subheader("📋 Kayıtlı Tüm Geçmiş Verilerin ve Zafer Notların (CSV Çıktısı)")
    st.dataframe(pd.read_csv(CSV_FILE), use_container_width=True)

# ==========================================
# 🍗 TAB 3: BESLENME PLANI (MODÜLDEN ÇAĞRILIYOR 🚀)
# ==========================================
with tab3:
    render_nutrition_tab()

# ==========================================
# 🏃‍♂️ TAB 4: KARDİYO TAKİP PLANI
# ==========================================
with tab4:
    st.subheader("⏱️ Haftalık Kardiyo Takip Matriksi")
    st.success("PROTOKOL: 15 Eğim, 5.5 Hız, 30 Dakika Hafta İçi Hergün | HaftaSonu Offday (Kardio Yok)")
    df_kardiyo = pd.DataFrame({
        "Gün": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
        "Tip": ["Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "OFFDAY 💤", "OFFDAY 💤"],
        "Eğim/Hız": ["15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "-", "-"],
        "Süre": ["30 Dk ⏱️", "30 Dk", "30 Dk", "30 Dk", "30 Dk", "-", "-"],
        "Durum": ["BİTTİ 🏆", "Bekliyor", "Bekliyor", "Bekliyor", "Bekliyor", "DİNLENME", "DİNLENME"]
    })
    st.table(df_kardiyo)

# ==========================================
# 🏋️‍♂️ TAB 5: ANTRENMAN TAKİP (MODÜLDEN ÇAĞRILIYOR 🚀)
# ==========================================
with tab5:
    render_workout_tab()

# ==========================================
# 💊 TAB 6: SUPPLEMENT & CYCLE
# ==========================================
with tab6:
    st.subheader("💊 Güncel Supplement Enjeksiyon Zamanlaması")
    st.table(pd.DataFrame({
        "Dönem / Safha": ["💥 SPOR ÖNCESİ", "💥 SPOR ARASI", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE"],
        "Takviye İçeriği": ["0.75 Ölçek Pre-Workout + 4 Kapsül L-Carnitine", "2 Kapsül Thermo Burner 🔥", "5 Gram Creatine", "1 Kapsül Zinc (Çinko)", "1-2 Gram Magnezyum L-Threonate"],
        "Hedef Kodlama": ["Maksimum Odak ve Yağ Yakımı", "Termojenik Ateşleme", "Gece ATP Hücre Dolumu", "Testosteron Koruma Kalkanı", "REM Derin Uyku & CNS Reset"]
    }))