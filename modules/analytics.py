import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 gokalaf.com %100 MİLİMETRİK REPLİKA LABORATUVARI")
    st.write("Sitedeki küsurat hataları ve kalori sapmaları tamamen sıfırlanmıştır amınakoyim!")
    st.write("---")

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FFA500;'>
            <h3 style='color: #FFA500 !important; margin-top:0;'>🔥 GOKALAF KALORİ & MAKRO MOTORU</h3>
        </div>
        """, unsafe_allow_html=True)
        
        g_kilo = st.slider("Mevcut Kilonuz (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="gk_kilo_v4")
        g_boy = st.slider("Boyunuz (cm):", min_value=120, max_value=220, value=173, key="gk_boy_v4")
        g_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="gk_yas_v4")
        g_cins = st.selectbox("Cinsiyetiniz:", ["Erkek", "Kadın"], key="gk_cins_v4")
        
        g_akt = st.selectbox(
            "Aktivite Seviyeniz:", 
            [
                "Hareketsiz (Egzersiz Yok / Masa Başı)", 
                "Hafif Aktif (Haftada 1-3 Gün Hafif Egzersiz)", 
                "Orta Aktif (Haftada 3-5 Gün Yoğun Egzersiz)", 
                "Çok Aktif (Haftada 6-7 Gün Ağır Hardcore İdman)",
                "Hiper Aktif (Günde 2 Kez Ağır İdman)"
            ],
            index=2, key="gk_akt_v4"
        )
        
        g_hed = st.selectbox("Hedefiniz Nedir?", ["Yağ Yakımı (Kilo Ver)", "Kilo Koruma", "Kas Kazanımı (Bulk)"], index=0, key="gk_hed_v4")
        
    with col2:
        # Gokalaf.com Milimetrik Mifflin-St Jeor Hassas Denklem Kalibrasyonu
        if g_cins == "Erkek":
            bmr = (10.0 * g_kilo) + (6.25 * g_boy) - (5.0 * g_yas) + 5.0
        else:
            bmr = (10.0 * g_kilo) + (6.25 * g_boy) - (5.0 * g_yas) - 161.0
            
        # Sitedeki birebir küsuratlı TDEE aktivite çarpanları
        if "Hareketsiz" in g_akt: carpan = 1.2
        elif "Hafif" in g_akt: carpan = 1.375
        elif "Orta" in g_akt: carpan = 1.55
        elif "Çok" in g_akt: carpan = 1.725
        else: carpan = 1.9
        
        tdee = bmr * carpan
        
        # Gokalaf Metot: Yağ yakımında tam %20 defisit, bulkta +300 temiz kalori
        if "Yağ Yakımı" in g_hed:
            nihai_kalori = tdee * 0.80
        elif "Kas Kazanımı" in g_hed:
            nihai_kalori = tdee + 300.0
        else:
            nihai_kalori = tdee
            
        # Gokalaf Makro Formülü: Kilo başına net 2.2g Protein
        p_gram = g_kilo * 2.2
        p_kcal = p_gram * 4.0
        
        # Yağ Formülü: Toplam nihai kalorinin %25'i
        f_kcal = nihai_kalori * 0.25
        f_gram = f_kcal / 9.0
        
        # Karbonhidrat Formülü: Kalan tüm enerji kalorisi (Nihai - Protein - Yağ) / 4
        c_kcal = nihai_kalori - (p_kcal + f_kcal)
        c_gram = c_kcal / 4.0
        if c_gram < 0: c_gram = 0.0

        st.markdown(f"""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #00FFCC; min-height: 380px;'>
            <h3 style='color: #00FFCC !important; text-align: center; margin-top:0;'>🎯 BİLİŞİMSEL KALİBRASYON PANELİ</h3>
            <hr style='border-color: #30363D;'>
            <p style='color: #8B949E; font-size:13px; text-align:center;'>BMR: {bmr:.1f} kcal | TDEE: {tdee:.1f} kcal</p>
            <h1 style='color: #FFFFFF !important; text-align: center; font-size: 45px; margin: 10px 0;'>{round(nihai_kalori)} <span style='font-size:20px; color:#00FFCC;'>kcal</span></h1>
            <p style='color: #8B949E; text-align: center; font-weight: bold; margin-bottom: 20px;'>GÜNLÜK NET HEDEF</p>
            
            <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🍗 PROTEİN (2.2g/Kilo):</span>
                <span style='color: #00FFCC; font-weight:bold;'>{round(p_gram)} Gram</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🍚 KARBONHİDRAT (Net Kalan):</span>
                <span style='color: #FFA500; font-weight:bold;'>{round(c_gram)} Gram</span>
            </div>
            <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                <span style='color: #FFFFFF; font-weight:bold;'>🥑 YAĞ (Kalori %25):</span>
                <span style='color: #FF0055; font-weight:bold;'>{round(f_gram)} Gram</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 📐 YAĞ ORANI & 1RM MOTORLARI
    # ==========================================
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #9932CC;'>
            <h3 style='color: #9932CC !important; margin-top:0;'>📐 VÜCUT YAĞ ORANI (US NAVY)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        y_boy = st.slider("Boyunuz (cm):", min_value=120, max_value=220, value=173, key="ny_boy_v4")
        y_bel = st.slider("Bel Çevresi (cm):", min_value=50, max_value=150, value=78, key="ny_bel_v4")
        y_boyun = st.slider("Boyun Çevresi (cm):", min_value=20, max_value=60, value=38, key="ny_boyun_v4")
        
        if y_bel > y_boyun:
            yag_orani = 86.010 * math.log10(y_bel - y_boyun) - 70.041 * math.log10(y_boy) + 36.76
            st.success(f"🎯 Yağ Yüzdesi: %{yag_orani:.1f}")
        else:
            st.caption("Verileri giriniz...")

    with col4:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FF0055;'>
            <h3 style='color: #FF0055 !important; margin-top:0;'>💪 MAXIMUM GÜÇ (1RM EPLEY)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        orm_w = st.slider("Kaldırılan Ağırlık (kg):", min_value=10, max_value=250, value=100, key="ny_orm_w_v4")
        orm_r = st.slider("Yapılan Tekrar:", min_value=1, max_value=20, value=2, key="ny_orm_r_v4")
        
        if orm_r == 1: 
            one_rm_sonuc = orm_w
        else: 
            one_rm_sonuc = orm_w * (1.0 + (orm_r / 30.0))
            
        st.success(f"🚀 Tahmini 1RM: {one_rm_sonuc:.1f} KG")