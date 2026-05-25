import streamlit as st
import pandas as pd
import math

def render_analytics_tab(csv_file):
    st.title("🧱 GELECEK SÜRÜM: GELİŞİM ARAÇLARI")
    st.write("Profesyonel koçluk sistemlerindeki hesaplama araçlarını kendi sistemine entegre ettik amınakoyim! Verilerini gir, haritanı çıkar.")
    st.write("---")

    # 🗂️ 1. SATIR: SAKLIK VE ENERJİ ARAÇLARI (3 KOLON GRİD YAPISI)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #0099FF; min-height: 280px;'>
            <h3 style='color: #0099FF !important; margin-top:0;'>💙 VÜCUT KİTLE ENDEKSİ</h3>
            <p style='color: #8B949E; font-size: 14px;'>Boy ve kilonuza göre BMI değerinizi ve ideal aralığınızı hesaplayın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        bmi_boy = st.number_input("Boy (cm):", min_value=120, max_value=220, value=173, key="bmi_b")
        bmi_kilo = st.number_input("Kilo (kg):", min_value=40.0, max_value=150.0, value=71.25, key="bmi_k")
        
        bmi_sonuc = bmi_kilo / ((bmi_boy / 100) ** 2)
        st.info(f"📋 BMI Endeksiniz: {bmi_sonuc:.1f}")

    with col2:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #FFA500; min-height: 280px;'>
            <h3 style='color: #FFA500 !important; margin-top:0;'>🧡 KALORİ HESAPLAMA</h3>
            <p style='color: #8B949E; font-size: 14px;'>Hedefinize göre günlük almanız gereken kalori miktarını hesaplayın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        kalori_hedef = st.selectbox("Hedef Seçimi:", ["Yağ Yakımı (Definasyon)", "Temiz Büyüme (Lean Bulk)", "Kilo Koruma"], key="cal_h")
        st.code("🔥 Öneri: ~1700 - 2000 kcal\n(Mevcut planınızla senkronize)")

    with col3:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #00FFCC; min-height: 280px;'>
            <h3 style='color: #00FFCC !important; margin-top:0;'>💚 MAKRO HESAPLAMA</h3>
            <p style='color: #8B949E; font-size: 14px;'>Protein, karbonhidrat ve yağ miktarlarınızı jilet gibi dağıtın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.code("🍗 Protein: ~140-195.5g\n🍚 Carb: ~137.2-250g\n🥑 Yağ: ~50-65g")

    st.write("---")

    # 🗂️ 2. SATIR: ANALİZ VE GÜÇ ARAÇLARI (3 KOLON GRİD YAPISI)
    col4, col5, col6 = st.columns(3)

    with col4:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #9932CC; min-height: 280px;'>
            <h3 style='color: #9932CC !important; margin-top:0;'>💜 YAĞ ORANI (US NAVY)</h3>
            <p style='color: #8B949E; font-size: 14px;'>US Navy formülüyle vücut yağ yüzdenizi ve yağsız kas kütlenizi analiz edin.</p>
        </div>
        """, unsafe_allow_html=True)
        
        navy_bel = st.number_input("Bel Çevresi (cm):", min_value=50.0, max_value=150.0, value=78.0, key="navy_be")
        navy_boyun = st.number_input("Boyun Çevresi (cm):", min_value=20.0, max_value=60.0, value=38.0, key="navy_bo")
        
        if navy_bel > navy_boyun:
            yag_orani = 86.010 * math.log10(navy_bel - navy_boyun) - 70.041 * math.log10(173.0) + 36.76
            st.success(f"🎯 Yağ Oranı: %{yag_orani:.1f}")
        else:
            st.caption("Verileri giriniz...")

    with col5:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #FF0055; min-height: 280px;'>
            <h3 style='color: #FF0055 !important; margin-top:0;'>❤️ ONE REP MAX (1RM)</h3>
            <p style='color: #8B949E; font-size: 14px;'>Kaldırdığınız ağırlık ve tekrardan maksimum kaldırma kapasitenizi hesaplayın.</p>
        </div>
        """, unsafe_allow_html=True)
        
        orm_kilo = st.number_input("Ağırlık (kg):", min_value=1.0, max_value=300.0, value=100.0, key="orm_ki")
        orm_tekrar = st.number_input("Tekrar:", min_value=1, max_value=30, value=2, key="orm_te")
        
        if orm_tekrar == 1:
            max_power = orm_kilo
        else:
            max_power = orm_kilo * (1 + (orm_tekrar / 30))
        st.success(f"🚀 Maksimum Güç: {max_power:.1f} KG")

    with col6:
        st.markdown("""
        <div style='background-color: #161B22; padding: 20px; border-radius: 12px; border: 2px solid #00FFFF; min-height: 280px;'>
            <h3 style='color: #00FFFF !important; margin-top:0;'>🚰 SU İHTİYACI</h3>
            <p style='color: #8B949E; font-size: 14px;'>Kilonuza ve aktivite seviyenize göre günlük su ihtiyacınızı hesaplayın.</p>
        </div>
        """, unsafe_allow_html=True)
        st.info("💧 Minimum Hedef: 4.5 - 5 Litre\n(Kreatin dolumu için kilitli)")