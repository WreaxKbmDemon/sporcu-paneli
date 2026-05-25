import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# 🔌 MODÜLER ENJEKSİYON YAPILANDIRMASI
from modules.workout import render_workout_tab
from modules.nutrition import render_nutrition_tab
from modules.analytics import render_analytics_tab
from modules.supplement import render_supplement_tab
from modules.cardio import render_cardio_tab

# 🖥️ SAYFA YAPILANDIRMASI
st.set_page_config(page_title="SPORCU PANELİ V2.6", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

st.title("⚡ MACROFLOW // SPORCU PANELİ - FULL HYPERDRIVE V2.6")
st.write(f"⚙️ Sistem: AKILLI NOT BELLEĞİ + MODÜLER MİMARİ AKTİF | 📅 Bugün: {datetime.now().strftime('%d.%m.%Y')}")

CSV_FILE = "data/sporcu_verileri.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Kilo", "Su_ml", "Gunluk_Not"])
    df_init.to_csv(CSV_FILE, index=False)

df_read_init = pd.read_csv(CSV_FILE)
varsayilan_not = "100 kg bench press 2 tekrar atıldı 15 eğim 5,5 hız 45 dakika kardio yapıldı."

if not df_read_init.empty and "Gunluk_Not" in df_read_init.columns:
    son_not = df_read_init["Gunluk_Not"].iloc[-1]
    if pd.notna(son_not) and str(son_not).strip() != "":
        varsayilan_not = str(son_not)

# 🗂️ 7 EFSANE SEKME OLUŞTURULDU
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Sporcu Paneli", "📝 Veri Giriş Reaktörü", "📊 Gelişmiş Analiz", 
    "🍗 Beslenme Planı", "🏃‍♂️ Kardiyo Takip", "🏋️‍♂️ Antrenman Takip", "💊 Supplement & Hesaplayıcı"
])

# TAB 1: ÖZET PANEL
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
            st.warning("⚠️ Veri tabanında veri yok!")

# TAB 2: VERİ GİRİŞİ
with tab2:
    st.subheader("🚀 Telefondan Anlık Veri Giriş Paneli")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        input_kilo = st.number_input("Sabah Aç Karnına Kilonuz (kg):", min_value=30.0, max_value=150.0, value=71.25, step=0.05, key="giris_kilo")
    with col_input2:
        input_su = st.number_input("Bugün İçilen Toplam Su (ml):", min_value=0, max_value=10000, value=3000, step=250, key="giris_su")
        
    input_not = st.text_input("Bugünkü Zafer Notlarınız (İdman Raporu / Hissiyat):", value=varsayilan_not)
        
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
        st.success(f"✅ Veriler ve Notunuz başarıyla mühürlendi! Sayfayı yenileyebilirsin aslanım.")
        st.rerun()

    st.write("---")
    st.dataframe(pd.read_csv(CSV_FILE), use_container_width=True)

# TAB 3: GELİŞMİŞ ANALİZ
with tab3:
    render_analytics_tab(CSV_FILE)

# TAB 4: BESLENME PLANI
with tab4:
    render_nutrition_tab()

# TAB 5: KARDİYO
with tab5:
    render_cardio_tab()

# TAB 6: ANTRENMAN TAKİP
with tab6:
    render_workout_tab()

# TAB 7: SUPPLEMENT VE HESAPLAYICI
with tab7:
    render_supplement_tab()