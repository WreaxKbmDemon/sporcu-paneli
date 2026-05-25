import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 İNTERAKTİF SPORCU LABORATUVARI (GOKALAF METRİKS)")
    st.write("Kutulardaki ayarları değiştirip HESAPLA butonuna basarak anlık analizini yap amınakoyim!")
    st.write("---")

    # ==========================================
    # GRİD 1: KALORİ & MAKRO LABORATUVARI
    # ==========================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FFA500;'>
            <h3 style='color: #FFA500 !important; margin-top:0;'>🔥 KALORİ REAKTÖRÜ (Mifflin-St Jeor)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cal_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="c_yas")
        cal_cinsiyet = st.selectbox("Cinsiyet:", ["Erkek", "Kadın"], key="c_cins")
        cal_boy = st.slider("Boy (cm):", min_value=120, max_value=220, value=173, key="c_boy")
        cal_kilo = st.slider("Kilo (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="c_kilo")
        
        cal_aktivite = st.selectbox(
            "Aktivite Seviyesi:", 
            ["Hareketsiz (Masa başı)", "Hafif Aktif (Haftada 1-3 gün idman)", "Orta Aktif (Haftada 3-5 gün idman)", "Çok Aktif (Haftada 6-7 gün hardcore idman)"],
            index=2, key="c_akt"
        )
        
        cal_hedef = st.selectbox("Hedefiniz nedir aslanım?", ["KİLO VER (Definasyon)", "KORU (Stabil)", "KAS YAP (Bulk)"], index=0, key="c_hed")
        
        btn_cal = st.button("🔥 KALORİ HESAPLA", key="btn_cal_reaktor")

    with col2:
        if btn_cal:
            if cal_cinsiyet == "Erkek":
                bmr = 10 * cal_kilo + 6.25 * cal_boy - 5 * cal_yas + 5
            else:
                bmr = 10 * cal_kilo + 6.25 * cal_boy - 5 * cal_yas - 161
                
            akt_carpan = 1.2
            if "Hafif" in cal_aktivite: akt_carpan = 1.375
            elif "Orta" in cal_aktivite: akt_carpan = 1.55
            elif "Çok" in cal_aktivite: akt_carpan = 1.725
            
            tdee = bmr * akt_carpan
            
            if "VER" in cal_hedef: nihai_kalori = tdee - 400
            elif "YAP" in cal_hedef: nihai_kalori = tdee + 350
            else: nihai_kalori = tdee
            
            st.markdown(f"""
            <div style='background-color: #161B22; padding: 25px; border-radius: 12px; border: 2px solid #00FFCC; text-align: center;'>
                <h2 style='color: #00FFCC !important;'>🎯 HESAPLAMA SONUCU</h2>
                <h1 style='color: #FFFFFF !important; font-size: 40px;'>{int(nihai_kalori)} kcal</h1>
                <p style='color: #8B949E;'>Günlük Tüketmeniz Gereken Enerji Miktarı</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #161B22; padding: 55px; border-radius: 12px; border: 1px dashed #30363D; text-align: center; min-height: 250px;'>
                <h2 style='color: #8B949E !important;'>🔥 SONUÇ BEKLENİYOR</h2>
                <p style='color: #8B949E;'>Bilgilerinizi girin ve hesapla butonuna basın aslanım.</p>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # GRİD 2: MAKRO DAĞILIM LABORATUVARI
    # ==========================================
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #00FFCC;'>
            <h3 style='color: #00FFCC !important; margin-top:0;'>📊 MAKRO DAĞILIM REAKTÖRÜ</h3>
        </div>
        """, unsafe_allow_html=True)
        
        cal_girdi = st.number_input("Hesaplanacak Kalori Değeri (kcal):", min_value=1000, max_value=5000, value=2000, key="m_cal_input")
        p_orani = st.slider("Protein Oranı (%):", min_value=20, max_value=50, value=30, step=5, key="m_prot")
        st.caption(f"Yağ %25 sabit, Karbonhidrat %{100 - p_orani - 25} olarak atanacaktır.")
        
        btn_makro = st.button("📊 MAKRO HESAPLA", key="btn_makro_reaktor")

    with col_m2:
        if btn_makro:
            p_gram = (cal_girdi * (p_orani / 100)) / 4
            f_gram = (cal_girdi * 0.25) / 9
            c_gram = (cal_girdi * ((100 - p_orani - 25) / 100)) / 4
            
            st.markdown(f"""
            <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #00FFCC;'>
                <h3 style='color: #00FFCC !important; text-align: center;'>🎯 ENJEKSİYON RAPORU</h3>
                <h4 style='color: #FFFFFF !important;'>🍗 Protein: {int(p_gram)}g</h4>
                <h4 style='color: #FFFFFF !important;'>🍚 Karbonhidrat: {int(c_gram)}g</h4>
                <h4 style='color: #FFFFFF !important;'>🥑 Yağ: {int(f_gram)}g</h4>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='background-color: #161B22; padding: 50px; border-radius: 12px; border: 1px dashed #30363D; text-align: center;'>
                <h2 style='color: #8B949E !important;'>📊 SONUÇ BEKLENİYOR</h2>
            </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # GRİD 3: YAĞ ORANI & PERFORMANCE & SU (3 KOLON GRİD)
    # ==========================================
    col3, col4, col5 = st.columns(3)

    with col3:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #9932CC;'>
            <h3 style='color: #9932CC !important; margin-top:0;'>% ÖLÇÜMLERİNİZ (YAĞ)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        y_boy = st.slider("Boyunuz (cm):", min_value=120, max_value=220, value=173, key="navy_boy")
        y_bel = st.slider("Bel Çevresi (cm):", min_value=50, max_value=150, value=78, key="navy_bel")
        y_boyun = st.slider("Boyun Çevresi (cm):", min_value=20, max_value=60, value=38, key="navy_boyun")
        
        btn_navy = st.button("📐 YAĞ ORANI HESAPLA", key="btn_navy_reaktor")
        
        if btn_navy:
            if y_bel > y_boyun:
                yag_orani = 86.010 * math.log10(y_bel - y_boyun) - 70.041 * math.log10(y_boy) + 36.76
                st.success(f"🎯 Yağ Oranı: %{yag_orani:.1f}")
            else:
                st.error("Hatalı Ölçü!")

    with col4:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FF0055;'>
            <h3 style='color: #FF0055 !important; margin-top:0;'>💪 PERFORMANSINIZ (1RM)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        egzersiz = st.selectbox("Egzersiz Tipi:", ["BENCH PRESS", "SQUAT", "DEADLIFT", "OVERHEAD PRESS"], key="orm_egz")
        orm_w = st.slider("Basılan Ağırlık (kg):", min_value=10, max_value=250, value=100, key="orm_w_slider")
        orm_r = st.slider("Tekrar Sayısı (Reps):", min_value=1, max_value=20, value=2, key="orm_r_slider")
        
        btn_orm = st.button("💪 1RM GÜCÜNÜ HESAPLA", key="btn_orm_reaktor")
        
        if btn_orm:
            if orm_r == 1: 
                one_rm_sonuc = orm_w
            else: 
                one_rm_sonuc = orm_w * (1 + (orm_r / 30))
            st.success(f"🚀 Maks {egzersiz} Gücün: {one_rm_sonuc:.1f} KG")

    with col5:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #00FFFF;'>
            <h3 style='color: #00FFFF !important; margin-top:0;'>🚰 SU İHTİYACI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        su_kilo = st.slider("Mevcut Kilo (kg):", min_value=40, max_value=150, value=71, key="su_k_slider")
        su_iklim = st.select_slider("İklim Sıcaklığı:", options=["Soğuk", "Normal", "Sıcak", "Çok Sıcak"], value="Normal", key="su_iklim_slider")
        
        btn_su = st.button("🚰 SU İHTİYACI HESAPLA", key="btn_su_reaktor")
        
        if btn_su:
            temel_su = (su_kilo * 35)
            if su_iklim == "Sıcak": temel_su += 500
            elif su_iklim == "Çok Sıcak": temel_su += 1000
            st.info(f"💧 Su Hedefin: {(temel_su/1000):.2f} Litre")