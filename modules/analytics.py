import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 gokalaf.com REPLİKA HESAPLAMA LABORATUVARI")
    st.write("Sitedeki tüm matematiksel formüller, çarpanlar ve makro dağılımları birebir kalibre edilmiştir amınakoyim!")
    st.write("---")

    # ==========================================
    # 🧮 GOKALAF KALORİ & MAKRO MOTORU (BİREBİR KLON)
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FFA500;'>
            <h3 style='color: #FFA500 !important; margin-top:0;'>🔥 GOKALAF KALORİ HESAPLAYICI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        g_kilo = st.slider("Mevcut Kilonuz (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="gk_kilo")
        g_boy = st.slider("Boyunuz (cm):", min_value=120, max_value=220, value=173, key="gk_boy")
        g_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="gk_yas")
        g_cins = st.selectbox("Cinsiyetiniz:", ["Erkek", "Kadın"], key="gk_cins")
        
        g_akt = st.selectbox(
            "Aktivite Seviyeniz:", 
            [
                "Hareketsiz (Egzersiz Yok / Masa Başı)", 
                "Hafif Aktif (Haftada 1-3 Gün Hafif Egzersiz)", 
                "Orta Aktif (Haftada 3-5 Gün Yoğun Egzersiz)", 
                "Çok Aktif (Haftada 6-7 Gün Ağır Hardcore İdman)",
                "Hiper Aktif (Günde 2 Kez Ağır İdman / Ağır İşçi)"
            ],
            index=2, key="gk_akt"
        )
        
        g_hed = st.selectbox("Hedefiniz Nedir?", ["Yağ Yakımı (Kilo Ver)", "Kilo Koruma", "Kas Kazanımı (Bulk)"], index=0, key="gk_hed")
        
    with col2:
        # Gokalaf.com'un Kullandığı Revize Harris-Benedict Formülü:
        if g_cins == "Erkek":
            bmr = 66.47 + (13.75 * g_kilo) + (5.003 * g_boy) - (6.755 * g_yas)
        else:
            bmr = 655.1 + (9.563 * g_kilo) + (1.85 * g_boy) - (4.676 * g_yas)
            
        # Milimetrik Aktivite Çarpanları
        if "Hareketsiz" in g_akt: çarpan = 1.2
        elif "Hafif" in g_akt: çarpan = 1.375
        elif "Orta" in g_akt: çarpan = 1.55
        elif "Çok" in g_akt: çarpan = 1.725
        else: çarpan = 1.9
        
        tdee = bmr * çarpan
        
        # Gokalaf Kalori Açığı / Fazlası Algoritması (%20 Defisit veya %10 Surplus)
        if "Yağ Yakımı" in g_hed:
            nihai_kalori = tdee * 0.80  # Tam %20 kalori açığı amınakoyim
        elif "Kas Kazanımı" in g_hed:
            nihai_kalori = tdee + 300   # Lean bulk fazlası
        else:
            nihai_kalori = tdee
            
        # Gokalaf Protein Dağılımı: Kilo başına net 2.2g Protein baz alınır
        p_gram = g_kilo * 2.2
        p_kcal = p_gram * 4
        
        # Gokalaf Yağ Dağılımı: Toplam kalorinin %25'i sağlıklı yağlara gider
        f_kcal = nihai_kalori * 0.25
        f_gram = f_kcal / 9
        
        # Gokalaf Karbonhidrat Dağılımı: Kalan tüm kalori karbonhidrata mühürlenir
        c_kcal = nihai_kalori - (p_kcal + f_kcal)
        c_gram = c_kcal / 4
        if c_gram < 0: c_gram = 0

        st.markdown(f"""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #00FFCC; min-height: 400px;'>
            <h3 style='color: #00FFCC !important; text-align: center; margin-top:0;'>🎯 CANLI SONUÇ PANELDEN ÇIKTILAR</h3>
            <hr style='border-color: #30363D;'>
            <p style='color: #8B949E; font-size:14px; text-align:center;'>BMR (Bazal Metabolizma): {int(bmr)} kcal | TDEE (Yaktığın): {int(tdee)} kcal</p>
            <h1 style='color: #FFFFFF !important; text-align: center; font-size: 45px; margin: 15px 0;'>{int(nihai_kalori)} <span style='font-size:20px; color:#00FFCC;'>kcal</span></h1>
            <p style='color: #FFFFFF; text-align: center; font-weight: bold; margin-bottom: 25px;'>GÜNLÜK HEDEF ENERJİ</p>
            
            <div style='display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🍗 PROTEİN (2.2g/Kilo):</span>
                <span style='color: #00FFCC; font-weight:bold;'>{int(p_gram)} Gram</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🍚 KARBONHİDRAT (Kalan):</span>
                <span style='color: #FFA500; font-weight:bold;'>{int(c_gram)} Gram</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin: 12px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🥑 YAĞ (%25 Dengesi):</span>
                <span style='color: #FF0055; font-weight:bold;'>{int(f_gram)} Gram</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 📐 GOKALAF YAĞ ORANI & 1RM MOTORU (BİREBİR)
    # ==========================================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #9932CC;'>
            <h3 style='color: #9932CC !important; margin-top:0;'>📐 GOKALAF VÜCUT YAĞ ORANI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        y_boy = st.slider("Boyunuz (cm):", min_value=120, max_value=220, value=173, key="ny_boy")
        y_bel = st.slider("Bel Çevresi (cm):", min_value=50, max_value=150, value=78, key="ny_bel")
        y_boyun = st.slider("Boyun Çevresi (cm):", min_value=20, max_value=60, value=38, key="ny_boyun")
        
        if y_bel > y_boyun:
            yag_orani = 86.010 * math.log10(y_bel - y_boyun) - 70.041 * math.log10(y_boy) + 36.76
            st.success(f"🎯 Hesaplanan Yağ Oranı: %{yag_orani:.1f}")
            yag_klesi = g_kilo * (yag_orani / 100)
            st.caption(f"Yağsız Kütle: {g_kilo - yag_klesi:.1f} kg | Saf Yağ: {yag_klesi:.1f} kg")
        else:
            st.caption("Verileri giriniz...")

    with col4:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FF0055;'>
            <h3 style='color: #FF0055 !important; margin-top:0;'>💪 GOKALAF PERFORMANCE (1RM)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        orm_w = st.slider("Kaldırılan Ağırlık (kg):", min_value=10, max_value=250, value=100, key="ny_orm_w")
        orm_r = st.slider("Yapılan Tekrar Sayısı:", min_value=1, max_value=20, value=2, key="ny_orm_r")
        
        # Gokalaf Epley 1RM Kalibrasyonu
        if orm_r == 1: 
            one_rm_sonuc = orm_w
        else: 
            one_rm_sonuc = orm_w * (1 + (orm_r / 30))
            
        st.success(f"🚀 Tahmini 1RM Kapasiteniz: **{one_rm_sonuc:.1f} KG**")
        st.caption("Olası Alt Tekrar Dağılımları:")
        st.code(f"3 Tekrar: {int(one_rm_sonuc * 0.93)} kg | 5 Tekrar: {int(one_rm_sonuc * 0.87)} kg")