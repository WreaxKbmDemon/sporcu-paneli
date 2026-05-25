import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 INTERAKTİF SPORCU LABORATUVARI (GOKALAF METRİKS)")
    st.write("Kutulardaki ayarları, slider'ları ve butonları değiştirerek anlık analizini yap amınakoyim! Her şey %100 dinamik hale getirildi.")
    st.write("---")

    # 🗂️ GRİD 1: KALORİ & MAKRO LABORATUVARI (GÜNCELLENDİ 🚀)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FFA500;'>
            <h3 style='color: #FFA500 !important; margin-top:0;'>🔥 KALORİ REAKTÖRÜ (Mifflin-St Jeor)</h3>
            <p style='color: #8B949E; font-size: 13px;'>Yaş, boy, kilo ve aktivite seviyene göre metabolizma hızını hesapla.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # İnteraktif Slider Girişleri
        cal_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="c_yas")
        cal_cinsiyet = st.selectbox("Cinsiyet:", ["Erkek", "Kadın"], key="c_cins")
        cal_boy = st.slider("Boy (cm):", min_value=120, max_value=220, value=173, key="c_boy")
        cal_kilo = st.slider("Kilo (kg):", min_value=40.0, max_value=150.0, value=71.25, step=0.05, key="c_kilo")
        
        cal_aktivite = st.selectbox(
            "Aktivite Seviyesi:", 
            ["Hareketsiz (Masa başı)", "Hafif Aktif (Haftada 1-3 gün idman)", "Orta Aktif (Haftada 3-5 gün idman)", "Çok Aktif (Haftada 6-7 gün hardcore idman)"],
            index=2, key="c_akt"
        )
        
        cal_hedef = st.radio("Hedefiniz nedir aslanım?", ["KİLO VER (Definasyon)", "KORU (Stabil)", "KAS YAP (Bulk)"], index=0, key="c_hed")
        
        # BMR Hesaplama (Mifflin-St Jeor)
        if cal_cinsiyet == "Erkek":
            bmr = 10 * cal_kilo + 6.25 * cal_boy - 5 * cal_yas + 5
        else:
            bmr = 10 * cal_kilo + 6.25 * cal_boy - 5 * cal_yas - 161
            
        # Aktivite Çarpanı
        akt_carpan = 1.2
        if "Hafif" in cal_aktivite: akt_carpan = 1.375
        elif "Orta" in cal_aktivite: akt_carpan = 1.55
        elif "Çok" in cal_aktivite: akt_carpan = 1.725
        
        tdee = bmr * akt_carpan
        
        # Hedefe Göre Kalori Kalibrasyonu
        if "VER" in cal_hedef: nihai_kalori = tdee - 400
        elif "YAP" in cal_hedef: nihai_kalori = tdee + 350
        else: nihai_kalori = tdee
        
        st.success(f"📋 Günlük Enerji İhtiyacın: **{int(nihai_kalori)} kcal**")

    with col2:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #00FFCC;'>
            <h3 style='color: #00FFCC !important; margin-top:0;'>📊 MAKRO DAĞILIM REAKTÖRÜ</h3>
            <p style='color: #8B949E; font-size: 13px;'>Protein oranını slider ile değiştir, gramajlar anlık hesaplansın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Gokalaf.com'daki o meşhur yüzde bazlı makro slider'ı amınakoyim!
        p_orani = st.slider("Protein Oranı (%):", min_value=20, max_value=50, value=30, step=5, key="m_prot")
        st.caption(f"Geri kalan enerji: Yağ %25 sabit, Karbonhidrat %{100 - p_orani - 25} olarak dağıtıldı.")
        
        # Gramaj Hesapları (Protein 4 kcal, Carb 4 kcal, Yağ 9 kcal)
        p_gram = (nihai_kalori * (p_orani / 100)) / 4
        f_gram = (nihai_kalori * 0.25) / 9
        c_gram = (nihai_kalori * ((100 - p_orani - 25) / 100)) / 4
        
        st.info(f"🍗 **Protein:** {int(p_gram)}g | 🍚 **Karbonhidrat:** {int(c_gram)}g | 🥑 **Yağ:** {int(f_gram)}g")
        st.code(f"Dağılım Çıktısı:\nProtein Enerjisi: {int(nihai_kalori * (p_orani/100))} kcal\nKarbonhidrat Enerjisi: {int(nihai_kalori * ((100-p_orani-25)/100))} kcal")

    st.write("---")

    # 🗂️ GRİD 2: YAĞ ORANI & PERFORMANCE & SU (3 KOLON YAPISI)
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
        
        if y_bel > y_boyun:
            yag_orani = 86.010 * math.log10(y_bel - y_boyun) - 70.041 * math.log10(y_boy) + 36.76
            st.success(f"🎯 Yağ Oranı: %{yag_orani:.1f}")
            
            yag_klesi = cal_kilo * (yag_orani / 100)
            kas_klesi = cal_kilo - yag_klesi
            st.caption(f"Saf Kas Kitlen: {kas_klesi:.1f} kg | Yağ Kitlen: {yag_klesi:.1f} kg")
        else:
            st.error("Hatalı Ölçü!")

    with col4:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #FF0055;'>
            <h3 style='color: #FF0055 !important; margin-top:0;'>💪 PERFORMANSINIZ (1RM)</h3>
        </div>
        """, unsafe_allow_html=True)
        
        egzersiz = st.radio("Egzersiz Tipi:", ["BENCH PRESS", "SQUAT", "DEADLIFT", "OVERHEAD PRESS"], key="orm_egz")
        orm_w = st.slider("Basılan Ağırlık (kg):", min_value=10, max_value=250, value=100, key="orm_w_slider")
        orm_r = st.slider("Tekrar Sayısı (Reps):", min_value=1, max_value=20, value=2, key="orm_r_slider")
        
        if orm_r == 1: 1rm_sonuc = orm_w
        else: 1rm_sonuc = orm_w * (1 + (orm_r / 30))
        
        st.success(f"🚀 Maks {egzersiz} Gücün: **{1rm_sonuc:.1f} KG**")

    with col5:
        st.markdown("""
        <div style='background-color: #161B22; padding: 15px; border-radius: 12px; border: 2px solid #00FFFF;'>
            <h3 style='color: #00FFFF !important; margin-top:0;'>🚰 SU İHTİYACI</h3>
        </div>
        """, unsafe_allow_html=True)
        
        su_kilo = st.slider("Mevcut Kilo (kg):", min_value=40, max_value=150, value=71, key="su_k_slider")
        su_iklim = st.select_slider("İklim Sıcaklığı:", options=["Soğuk", "Normal", "Sıcak", "Çok Sıcak"], value="Normal", key="su_iklim_slider")
        
        # Temel formül + İklim çarpanı
        temel_su = (su_kilo * 35)
        if su_iklim == "Sıcak": temel_su += 500
        elif su_iklim == "Çok Sıcak": temel_su += 1000
        
        st.info(f"💧 Günlük Hidrasyon Amiral Gemisi Hedefin: **{(temel_su/1000):.2f} Litre** olmalıdır amınakoyim!")