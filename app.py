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
# 📝 TAB 2: VERİ GİRİŞ REAKTÖRÜ (YENİ INTERAKTİF MODÜL)
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
        st.success(s"✅ Veriler `data/sporcu_verileri.csv` dosyasına jilet gibi işlendi! İlk sekmeyi yenileyebilirsin amınakoyim.")

    st.write("---")
    st.subheader("📋 Kayıtlı Tüm Geçmiş Verilerin (CSV Çıktısı)")
    st.dataframe(pd.read_csv(CSV_FILE), use_container_width=True)

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
        "Takviye İçeriği": ["0.75 Ölçek Pre-Workout + 4 Kapsül L-Carnitine", "2 Kapsül Thermo Burner 🔥", "5 Gram Creatine", "1 Kapsül Zinc (Çinko)", "1-2 Gram Magnezyum L-Threonate"],
        "Hedef Kodlama": ["Maksimum Odak ve Yağ Yakımı", "Termojenik Ateşleme", "Gece ATP Hücre Dolumu", "Testosteron Koruma Kalkanı", "REM Derin Uyku & CNS Reset"]
    }))