import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 SPORCU LABORATUVARI (MİLİMETRİK KALİBRASYON)")
    st.write("Verilerini gir, gokalaf.com algoritmasıyla birebir sonuçları kendi sisteminde gör amınakoyim!")
    st.write("---")

    # ==========================================
    # 🔥 1. ARAÇ: KALORİ & MAKRO HESAPLAMA ÜSSÜ
    # ==========================================
    st.subheader("🔥 KALORİ VE MAKRO REAKTÖRÜ")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #FFA500; margin-bottom:10px;'>⚡ BİLGİLERİNİZ</div>", unsafe_allow_html=True)
        cal_yas = st.slider("YAŞ:", min_value=10, max_value=80, value=16, key="lab_yas")
        cal_cins = st.selectbox("CİNSİYET:", ["Erkek", "Kadın"], key="lab_cins")
        cal_boy = st.slider("BOY (cm):", min_value=120, max_value=220, value=173, key="lab_boy")
        cal_kilo = st.slider("KİLO (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="lab_kilo")
        
        cal_akt = st.selectbox(
            "AKTİVİTE:", 
            ["Hareketsiz", "Hafif Aktif (Haftada 1-3 gün)", "Orta Aktif (Haftada 3-5 gün)", "Çok Aktif (Haftada 6-7 gün)", "Sporcu (Günde 2 idman)"],
            index=2, key="lab_akt"
        )
        
        # Gokalaf buton yapısı
        cal_hed = st.radio("HEDEF:", ["KİLO VER", "KORU", "KAS YAP"], index=0, key="lab_hed")
        p_orani = st.slider("PROTEİN ORANI (%):", min_value=20, max_value=50, value=30, step=5, key="lab_poran")
        st.caption("Yağ %25 sabit, kalan enerji karbonhidrata dağıtılır.")
        
        btn_cal = st.button("🚀 HESAPLA", key="btn_gokalaf_core")

    with col2:
        if btn_cal:
            # Gokalaf Orijinal Mifflin-St Jeor Formülü
            if cal_cins == "Erkek":
                bmr = (10.0 * cal_kilo) + (6.25 * cal_boy) - (5.0 * cal_yas) + 5.0
            else:
                bmr = (10.0 * cal_kilo) + (6.25 * cal_boy) - (5.0 * cal_yas) - 161.0
                
            # Kusursuz Aktivite Çarpanları
            carpanlar = {"Hareketsiz": 1.2, "Hafif Aktif (Haftada 1-3 gün)": 1.375, "Orta Aktif (Haftada 3-5 gün)": 1.55, "Çok Aktif (Haftada 6-7 gün)": 1.725, "Sporcu (Günde 2 idman)": 1.9}
            tdee = bmr * carpanlar[cal_akt]
            
            # Hedef Kalori Ayarı
            if cal_hed == "KİLO VER": nihai_kalori = tdee - 500
            elif cal_hed == "KAS YAP": nihai_kalori = tdee + 300
            else: nihai_kalori = tdee
            
            # Makro Dağılım Hesabı
            p_gram = (nihai_kalori * (p_orani / 100)) / 4
            f_gram = (nihai_kalori * 0.25) / 9
            c_gram = (nihai_kalori * ((100 - p_orani - 25) / 100)) / 4
            
            st.markdown(f"""
            <div style='background-color: #161B22; padding: 25px; border-radius: 12px; border: 2px solid #00FFCC; min-height: 350px;'>
                <h3 style='color: #00FFCC !important; text-align: center; margin-top:0;'>🎯 HESAPLAMA SONUÇLARI</h3>
                <hr style='border-color: #30363D;'>
                <h1 style='color: #FFFFFF !important; text-align: center; font-size: 42px; margin: 15px 0;'>{int(nihai_kalori)} <span style='font-size:20px; color:#00FFCC;'>kcal</span></h1>
                <p style='color: #8B949E; text-align: center; font-weight: bold;'>GÜNLÜK HEDEF ENERJİ</p>
                <div style='margin-top: 25px;'>
                    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 10px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🍗 PROTEİN (%{p_orani}):</span>
                        <span style='color: #00FFCC; font-weight:bold;'>{int(p_gram)} Gram</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 10px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🍚 KARBONHİDRAT (%{100-p_orani-25}):</span>
                        <span style='color: #FFA500; font-weight:bold;'>{int(c_gram)} Gram</span>
                    </div>
                    <div style='display: flex; justify-content: space-between; margin: 8px 0; padding: 10px; background-color: #0E1117; border-radius: 6px;'>
                        <span style='color: #FFFFFF; font-weight:bold;'>🥑 YAĞ (%25):</span>
                        <span style='color: #FF0055; font-weight:bold;'>{int(f_gram)} Gram</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #161B22; padding: 100px 20px; border-radius: 12px; border: 1px dashed #30363D; text-align: center; min-height: 350px;'>
                <h2 style='color: #8B949E !important;'>🔥 SONUÇ BEKLENİYOR</h2>
                <p style='color: #8B949E;'>Bilgilerinizi girin ve HESAPLA butonuna basın aslanım.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 📐 2. ARAÇ: YAĞ ORANI & PERFORMANCE & SU (3'LÜ GRİD)
    # ==========================================
    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #9932CC; margin-bottom:10px;'>% ÖLÇÜMLERİNİZ (YAĞ)</div>", unsafe_allow_html=True)
        y_boy = st.slider("BOY (cm):", min_value=120, max_value=220, value=173, key="y_boy_v5")
        y_bel = st.slider("BEL ÇEVRESİ (cm):", min_value=50, max_value=150, value=78, key="y_bel_v5")
        y_boyun = st.slider("BOYUN ÇEVRESİ (cm):", min_value=20, max_value=60, value=38, key="y_boyun_v5")
        btn_yag = st.button("📐 YAĞ ORANI HESAPLA", key="btn_yag_v5")
        
        if btn_yag:
            if y_bel > y_boyun:
                yag_res = 86.010 * math.log10(y_bel - y_boyun) - 70.041 * math.log10(y_boy) + 36.76
                st.success(f"🎯 Yağ Oranı: %{yag_res:.1f}")
            else:
                st.error("Hatalı Ölçü!")

    with col4:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #FF0055; margin-bottom:10px;'>💪 PERFORMANSINIZ (1RM)</div>", unsafe_allow_html=True)
        orm_w = st.slider("AĞIRLIK (kg):", min_value=10, max_value=250, value=100, key="orm_w_v5")
        orm_r = st.slider("TEKRAR SAYISI:", min_value=1, max_value=20, value=2, key="orm_r_v5")
        btn_orm = st.button("💪 1RM HESAPLA", key="btn_orm_v5")
        
        if btn_orm:
            one_rm = orm_w if orm_r == 1 else orm_w * (1.0 + (orm_r / 30.0))
            st.success(f"🚀 Tahmini 1RM: {one_rm:.1f} KG")

    with col5:
        st.markdown("<div style='background-color: #161B22; padding: 10px; border-radius: 8px; border: 1px solid #00FFFF; margin-bottom:10px;'>🚰 SU İHTİYACI</div>", unsafe_allow_html=True)
        su_kilo = st.slider("KİLO (kg):", min_value=40, max_value=150, value=71, key="su_k_v5")
        su_iklim = st.select_slider("İKLİM:", options=["Soğuk", "Normal", "Sıcak", "Çok Sıcak"], value="Normal", key="su_iklim_v5")
        btn_su = st.button("🚰 SU HESAPLA", key="btn_su_v5")
        
        if btn_su:
            su_ml = (su_kilo * 35)
            if su_iklim == "Sıcak": su_ml += 500
            elif su_iklim == "Çok Sıcak": su_ml += 1000
            st.info(f"💧 Su Hedefi: {(su_ml/1000):.2f} Litre")