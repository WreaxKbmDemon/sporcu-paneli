import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 gokalaf.com ARAÇLAR PROTOKOLÜ V4.5")
    st.write("Siteden çekilen JavaScript mantığıyla %100 senkronize çalışır amınakoyim!")
    st.write("---")

    # ==========================================
    # 🗂️ 1. ARAÇ: BOY KİLO ENDEKSİ (BİREBİR REPLİKA)
    # ==========================================
    st.subheader("🟢 BOY KİLO ENDEKSİ")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #00FFCC;'>📋 ÖLÇÜMLERİNİZ</div>", unsafe_allow_html=True)
        bke_boy = st.slider("Boyunuz (cm):", min_value=140, max_value=220, value=170, key="bke_boy_slider")
        bke_kilo = st.slider("Kilonuz (kg):", min_value=35, max_value=160, value=70, key="bke_kilo_slider")
        bke_cins = st.selectbox("Cinsiyetiniz:", ["Erkek", "Kadın"], key="bke_cins_select")
        btn_bke = st.button("🚀 BOY KİLO ENDEKSİ HESAPLA", key="btn_bke_trigger")

    with col2:
        if btn_bke:
            # JS Motorundaki formül: kg / (m^2)
            bke_sonuc = bke_kilo / ((bke_boy / 100) ** 2)
            
            # İdeal Kilo Aralığı Hesabı (JS kodundaki alt/üst sınırlar)
            ideal_alt = 18.5 * ((bke_boy / 100) ** 2)
            ideal_ust = 24.9 * ((bke_boy / 100) ** 2)
            
            # JS durum kontrol mekanizması
            if bke_sonuc < 18.5:
                durum_renk = "#FFCC00"
                durum_metni = "Düşük Kilolu"
                tavsiye = "Sağlıklı şekilde kütle kazanmaya odaklan aslanım."
            elif 18.5 <= bke_sonuc < 25:
                durum_renk = "#00FFCC"
                durum_metni = "SĂĞLIKLI"
                tavsiye = "Harika! Formunu koru. Boy ve kilonuz dengeli."
            elif 25 <= bke_sonuc < 30:
                durum_renk = "#FFA500"
                durum_metni = "Yüksek Kilolu"
                tavsiye = "Hafif bir kalori açığı ve kararlı kardiyo ile yağ yakımına başla."
            else:
                durum_renk = "#FF0055"
                durum_metni = "Riskli Seviye"
                tavsiye = "Hardcore bir definasyon reaktörünü devreye almamız şart amınakoyim."

            st.markdown(f"""
            <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid {durum_renk}; min-height: 250px; text-align: center;'>
                <h3 style='color: #8B949E !important; margin-top:0;'>BOY KİLO ENDEKSİNİZ</h3>
                <h1 style='color: #FFFFFF !important; font-size: 50px; margin: 5px 0;'>{bke_sonuc:.1f} <span style='font-size:16px; color:{durum_renk}; background-color:rgba(0,255,204,0.1); padding:4px 8px; border-radius:4px;'>{durum_metni}</span></h1>
                <p style='color: #FFFFFF; font-weight: bold; margin-top:15px;'>{tavsiye}</p>
                <hr style='border-color: #30363D;'>
                <div style='display: flex; justify-content: space-between; margin-top:10px;'>
                    <span style='color: #8B949E;'>İdeal Kilo Aralığı:</span>
                    <span style='color: #00FFCC; font-weight:bold;'>{ideal_alt:.1f} - {ideal_ust:.1f} kg</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #161B22; padding: 85px 20px; border-radius: 12px; border: 1px dashed #30363D; text-align: center; min-height: 250px;'>
                <h2 style='color: #8B949E !important;'>⚖️ SONUÇ BEKLENİYOR</h2>
                <p style='color: #8B949E;'>Verilerini gir ve hesapla butonuna bas amınakoyim.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 🧮 2. ARAÇ: TDEE VE MAKRO SENSÖRÜ (BİREBİR REPLİKA)
    # ==========================================
    st.subheader("🔥 TDEE VE MAKRO HESAPLAMA ÜSSÜ")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #FFA500;'>🔥 BİLGİLERİNİZ</div>", unsafe_allow_html=True)
        t_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="t_yas_v45")
        t_boy = st.slider("Boy (cm):", min_value=120, max_value=220, value=173, key="t_boy_v45")
        t_kilo = st.slider("Kilo (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="t_kilo_v45")
        t_cins = st.selectbox("Cinsiyet:", ["Erkek", "Kadın"], key="t_cins_v45")
        
        t_akt = st.selectbox(
            "Aktivite Seviyesi:", 
            ["Hareketsiz", "Hafif Aktif", "Orta Aktif", "Çok Aktif", "Sporcu"],
            index=2, key="t_akt_v45"
        )
        t_hed = st.radio("Hedefiniz:", ["KİLO VER", "KORU", "KAS YAP"], index=0, key="t_hed_v45")
        t_p_oran = st.slider("Protein Oranı (%):", min_value=20, max_value=50, value=30, step=5, key="t_poran_v45")
        
        btn_tdee = st.button("🔥 TDEE VE MAKRO HESAPLA", key="btn_tdee_v45")

    with col4:
        if btn_tdee:
            # JS Mifflin-St Jeor Milimetrik Altyapısı
            if t_cins == "Erkek":
                bmr = (10.0 * t_kilo) + (6.25 * t_boy) - (5.0 * t_yas) + 5.0
            else:
                bmr = (10.0 * t_kilo) + (6.25 * t_boy) - (5.0 * t_yas) - 161.0
                
            carpanlar = {"Hareketsiz": 1.2, "Hafif Aktif": 1.375, "Orta Aktif": 1.55, "Çok Aktif": 1.725, "Sporcu": 1.9}
            tdee = bmr * carpanlar[t_akt]
            
            if t_hed == "KİLO VER": nihai_kalori = tdee - 500
            elif t_hed == "KAS YAP": nihai_kalori = tdee + 300
            else: nihai_kalori = tdee
            
            # JS Orijinal Makro Dağılım Bölümü
            p_gram = (nihai_kalori * (t_p_oran / 100)) / 4
            f_gram = (nihai_kalori * 0.25) / 9
            c_gram = (nihai_kalori * ((100 - t_p_oran - 25) / 100)) / 4

            st.markdown(f"""
            <div style='background-color: #161B22; padding: 25px; border-radius: 12px; border: 2px solid #00FFCC; min-height: 400px;'>
                <h3 style='color: #00FFCC !important; text-align: center; margin-top:0;'>🎯 ENJEKSİYON RAPORU</h3>
                <hr style='border-color: #30363D;'>
                <h1 style='color: #FFFFFF !important; text-align: center; font-size: 45px; margin: 10px 0;'>{int(nihai_kalori)} <span style='font-size:20px; color:#00FFCC;'>kcal</span></h1>
                <p style='color: #8B949E; text-align: center; font-weight: bold;'>GÜNLÜK HEDEF ENERJİ</p>
                <div style='margin-top: 20px;'>
                    <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🍗 PROTEİN (%{t_p_oran}):</span>
                        <span style='color: #00FFCC; font-weight:bold;'>{int(p_gram)} Gram</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🍚 KARBONHİDRAT (%{100-t_p_oran-25}):</span>
                        <span style='color: #FFA500; font-weight:bold;'>{int(c_gram)} Gram</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 10px 0; padding: 8px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🥑 YAĞ (%25):</span>
                        <span style='color: #FF0055; font-weight:bold;'>{int(f_gram)} Gram</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #161B22; padding: 130px 20px; border-radius: 12px; border: 1px dashed #30363D; text-align: center; min-height: 400px;'>
                <h2 style='color: #8B949E !important;'>🔥 SONUÇ BEKLENİYOR</h2>
            </div>
            """, unsafe_allow_html=True)