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
st.set_page_config(page_title="SPORCU PANELİ V2.7", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("assets/style.css")

st.title("⚡ MACROFLOW // SPORCU PANELİ - GOKALAF EDITION V2.7")
st.write(f"⚙️ Sistem: US NAVY YAĞ ANALİZÖRÜ AKTİF | 📅 Bugün: {datetime.now().strftime('%d.%m.%Y')}")

CSV_FILE = "data/sporcu_verileri.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(CSV_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Kilo", "Su_ml", "Bel_cm", "Boyun_cm", "Yag_Orani", "Gunluk_Not"])
    df_init.to_csv(CSV_FILE, index=False)

df_read_init = pd.read_csv(CSV_FILE)
varsayilan_not = "100 kg bench press 2 tekrar atıldı 15 eğim 5,5 hız 45 dakika kardio yapıldı."

if not df_read_init.empty and "Gunluk_Not" in df_read_init.columns:
    son_not = df_read_init["Gunluk_Not"].iloc[-1]
    if pd.notna(son_not) and str(son_not).strip() != "":
        varsayilan_not = str(son_not)

# 🗂️ 7 EFSANE SEKME
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Sporcu Paneli", "📝 Veri Giriş Reaktörü", "📊 Gelişmiş Analiz", 
    "🍗 Beslenme Planı", "🏃‍♂️ Kardiyo Takip", "🏋️‍♂️ Antrenman Takip", "💊 Supplement & Hesaplayıcı"
])

# TAB 1: ÖZET PANEL
with tab1:
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("📋 Sporcu Profil Logları")
        st.info("**Eren** | 16 Yaş (9-Bilişim)\n\n**Boy:** 173 cm | **Bel:** 78 cm 🎯\n\n**Durum:** Gokalaf Yağ Analizörü Bağlandı")
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

# TAB 2: VERİ GİRİŞİ (GOKALAF ENJEKSİYONU YAPILDI 🚀)
with tab2:
    st.subheader("🚀 Telefondan Anlık Veri Giriş Paneli")
    col_input1, col_input2, col_input3, col_input4 = st.columns(4)
    with col_input1:
        input_kilo = st.number_input("Aç Karnına Kilo (kg):", min_value=30.0, max_value=150.0, value=71.25, step=0.05)
    with col_input2:
        input_su = st.number_input("İçilen Su (ml):", min_value=0, max_value=10000, value=3000, step=250)
    with col_input3:
        input_bel = st.number_input("Bel Çevresi (cm):", min_value=50.0, max_value=150.0, value=78.0, step=0.1)
    with col_input4:
        input_boyun = st.number_input("Boyun Çevresi (cm):", min_value=20.0, max_value=60.0, value=38.0, step=0.1)
        
    input_not = st.text_input("Bugünkü Zafer Notlarınız:", value=varsayilan_not)
        
    if st.button("🔥 VERİLERİ VE NOTU VERİ TABANINA MÜHÜRLE"):
        import math
        df_current = pd.read_csv(CSV_FILE)
        bugun_str = datetime.now().strftime("%d.%m.%Y")
        
        # Anlık otomatik US Navy yağ oranı hesaplama
        yag_orani_hesap = 0.0
        if input_bel > input_boyun:
            yag_orani_hesap = round(86.010 * math.log10(input_bel - input_boyun) - 70.041 * math.log10(173.0) + 36.76, 1)
            
        if bugun_str in df_current["Tarih"].values:
            df_current.loc[df_current["Tarih"] == bugun_str, ["Kilo", "Su_ml", "Bel_cm", "Boyun_cm", "Yag_Orani", "Gunluk_Not"]] = [input_kilo, input_su, input_bel, input_boyun, yag_orani_hesap, input_not]
        else:
            new_row = pd.DataFrame([{"Tarih": bugun_str, "Kilo": input_kilo, "Su_ml": input_su, "Bel_cm": input_bel, "Boyun_cm": input_boyun, "Yag_Orani": yag_orani_hesap, "Gunluk_Not": input_not}])
            df_current = pd.concat([df_current, new_row], ignore_index=True)
            
        df_current.to_csv(CSV_FILE, index=False)
        st.success(f"✅ Gokalaf ölçüleri veri tabanına mühürlendi!")
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