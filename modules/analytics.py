import streamlit as st
import math

def render_analytics_tab(csv_file):
    # Siberpunk Dark Mode ve Neon Kart Tasarımları
    st.markdown("""
        <style>
            .stSlider [data-baseweb="slider"] { margin-bottom: 12px; }
            .matrix-card {
                background-color: #161B22;
                padding: 20px;
                border-radius: 12px;
                border: 1px solid #30363D;
                margin-bottom: 15px;
            }
            .neon-text-cyan { color: #00FFCC !important; font-weight: bold; }
            .neon-text-orange { color: #FFA500 !important; font-weight: bold; }
            .neon-text-pink { color: #FF0055 !important; font-weight: bold; }
            .neon-text-purple { color: #9932CC !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🧱 MULTI-FUNCTIONAL SPORCU LABORATUVARI (REAL-TIME)")
    st.write("Attığın tüm bilimsel metinlerdeki formüller arka planda senkronize edildi. Değerleri değiştirdiğin an her şey otomatik hesaplanır amınakoyim!")
    st.write("---")

    # 🎛️ SOL TARAF: DİNAMİK PARAMETRE SENSÖRLERİ (INPUTS)
    col_in, col_out = st.columns([1, 1.2])

    with col_in:
        st.markdown("### 🎛️ ANLIK GİRDİ PANELİ")
        
        # Temel Fiziksel Parametreler
        u_boy = st.slider("Boyunuz (cm):", min_value=140, max_value=220, value=173, step=1, key="lab_v7_boy")
        u_kilo = st.slider("Kilonuz (kg):", min_value=35.0, max_value=160.0, value=71.25, step=0.05, key="lab_v7_kilo")
        u_yas = st.slider("Yaşınız:", min_value=10, max_value=80, value=16, key="lab_v7_yas")
        u_cins = st.selectbox("Cinsiyetiniz:", ["Erkek", "Kadın"], key="lab_v7_cins")
        
        st.write("---")
        # Gokalaf TDEE & Makro Parametreleri
        u_akt = st.selectbox(
            "Aktivite Seviyeniz:", 
            ["Hareketsiz (1.2)", "Hafif Aktif (1.375)", "Orta Aktif (1.55)", "Çok Aktif (1.725)", "Ekstra Aktif (1.9)"],
            index=2, key="lab_v7_akt"
        )
        u_hed = st.selectbox("Beslenme Hedefi:", ["KİLO VER (-500 kcal)", "KORU (±0 kcal)", "KAS YAP (+300 kcal)"], index=0, key="lab_v7_hed")
        u_prot_pct = st.slider("Protein Enerji Oranı (%):", min_value=20, max_value=50, value=30, step=5, key="lab_v7_ppct")
        
        st.write("---")
        # Gokalaf Vücut Yağ Oranı Parametreleri
        u_bel = st.slider("Aç Karnına Bel Çevresi (cm):", min_value=50.0, max_value=150.0, value=78.0, step=0.1, key="lab_v7_bel")
        u_boyun = st.slider("Boyun Çevresi (cm):", min_value=20.0, max_value=60.0, value=38.0, step=0.1, key="lab_v7_boyun")
        
        st.write("---")
        # 1RM Güç Testi Parametreleri
        u_lift_w = st.slider("Kaldırılan Ağırlık (kg):", min_value=10, max_value=250, value=100, step=2, key="lab_v7_liftw")
        u_lift_r = st.slider("Yapılan Tekrar Sayısı:", min_value=1, max_value=20, value=2, step=1, key="lab_v7_liftr")

    # 📊 SAĞ TARAF: REAL-TIME BİLİMSEL ÇIKTI PANAROMASI (OUTPUTS)
    with col_out:
        st.markdown("### 📊 GERÇEK ZAMANLI ANALİZ ÇIKTILARI")

        # 1️⃣ MATEMATİK MOTORU: VÜCUT KİTLE İNDEKSİ (VKİ)
        a_m = u_boy / 100
        vki = u_kilo / (a_m * a_m)
        min_id = 18.5 * a_m * a_m
        max_id = 24.9 * a_m * a_m
        
        if vki < 18.5: vki_lbl, vki_clr = "Zayıf", "#38bdf8"
        elif vki <= 24.9: vki_lbl, vki_clr = "Normal", "#34d399"
        elif vki <= 29.9: vki_lbl, vki_clr = "Fazla Kilolu", "#fbbf24"
        else: vki_lbl, vki_clr = "Obez", "#fb7185"

        # 2️⃣ MATEMATİK MOTORU: MIFFLIN-ST JEOR & TDEE & MAKROLAR
        if u_cins == "Erkek":
            bmr = (10.0 * u_kilo) + (6.25 * u_boy) - (5.0 * u_yas) + 5.0
        else:
            bmr = (10.0 * u_kilo) + (6.25 * u_boy) - (5.0 * u_yas) - 161.0
            
        carpan_map = {"Hareketsiz (1.2)": 1.2, "Hafif Aktif (1.375)": 1.375, "Orta Aktif (1.55)": 1.55, "Çok Aktif (1.725)": 1.725, "Ekstra Aktif (1.9)": 1.9}
        tdee = bmr * carpan_map[u_akt]
        
        if "KİLO VER" in u_hed: hedef_kcal = tdee - 500
        elif "KAS YAP" in u_hed: hedef_kcal = tdee + 300
        else: hedef_kcal = tdee
        
        p_g = (hedef_kcal * (u_prot_pct / 100)) / 4
        f_g = (hedef_kcal * 0.25) / 9
        c_g = (hedef_kcal * ((100 - u_prot_pct - 25) / 100)) / 4

        # 3️⃣ MATEMATİK MOTORU: US NAVY VÜCUT YAĞ ORANI
        if u_bel > u_boyun:
            yag_pct = 86.010 * math.log10(u_bel - u_boyun) - 70.041 * math.log10(u_boy) + 36.76
        else:
            yag_pct = 0.0

        # 4️⃣ MATEMATİK MOTORU: 1RM EPLEY
        one_rm = u_lift_w if u_lift_r == 1 else u_lift_w * (1.0 + (u_lift_r / 30.0))

        # 5️⃣ MATEMATİK MOTORU: SU & KALP HIZI (TANAKA)
        su_ml = (u_kilo * 35) + 1000 # Temel hidrasyon + sporcu payı
        mkh = 208 - (0.7 * u_yas)

        # 🖥️ UI KARTLARININ OTOMATİK RENDER EDİLMESİ amınakoyim
        st.markdown(f"""
            <div class="matrix-card" style="border-left: 5px solid {vki_clr};">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">01 // VÜCUT KİTLE İNDEKSİ & İDEAL KİLO</span>
                <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">VKİ: <span style="color: {vki_clr}; font-size: 24px;">{vki:.1f}</span> ({vki_lbl})</h3>
                <p style="color: #8B949E; font-size: 13px; margin: 3px 0 0 0;">İdeal Kilo Aralığın: <b>{min_id:.1f} - {max_id:.1f} kg</b></p>
            </div>
            
            <div class="matrix-card" style="border-left: 5px solid #FFA500;">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">02 // MİFFLİN-ST JEOR & TDEE ENERJİ REAKTÖRÜ</span>
                <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">Hedef Kalori: <span class="neon-text-orange" style="font-size: 24px;">{int(hedef_kcal)} kcal</span></h3>
                <p style="color: #8B949E; font-size: 13px; margin: 3px 0 0 0;">BMR (Bazal): {int(bmr)} kcal | TDEE (Yaktığın): {int(tdee)} kcal</p>
            </div>
            
            <div class="matrix-card" style="border-left: 5px solid #00FFCC;">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">03 // GOKALAF GERÇEK MAKRO DAĞILIMI</span>
                <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                    <span style="color: #FFFFFF;">🍗 Protein: <b class="neon-text-cyan">{int(p_g)}g</b></span>
                    <span style="color: #FFFFFF;">🍚 Karbonhidrat: <b class="neon-text-orange">{int(c_g)}g</b></span>
                    <span style="color: #FFFFFF;">🥑 Yağ: <b class="neon-text-pink">{int(f_g)}g</b></span>
                </div>
            </div>
            
            <div class="matrix-card" style="border-left: 5px solid #9932CC;">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">04 // US NAVY GERÇEK VÜCUT YAĞ ORANI</span>
                <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">Yağ Oranı: <span class="neon-text-purple" style="font-size: 24px;">%{yag_pct:.1f}</span></h3>
                <p style="color: #8B949E; font-size: 13px; margin: 3px 0 0 0;">Yağsız Kas Kütlen: <b>{u_kilo * (1 - yag_pct/100):.1f} kg</b> | Saf Yağ Kütlen: <b>{u_kilo * (yag_pct/100):.1f} kg</b></p>
            </div>
            
            <div class="matrix-card" style="border-left: 5px solid #FF0055;">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">05 // 1RM EPLEY MAKSİMAL GÜÇ SENSÖRÜ</span>
                <h3 style="margin: 5px 0 0 0; color: #FFFFFF;">Tahmini 1RM: <span class="neon-text-pink" style="font-size: 24px;">{one_rm:.1f} KG</span></h3>
                <p style="color: #8B949E; font-size: 13px; margin: 3px 0 0 0;">Hipertrofi Aralığın (%65-85): {int(one_rm*0.65)}-{int(one_rm*0.85)} kg | Güç Aralığın (%85-95): {int(one_rm*0.85)}-{int(one_rm*0.95)} kg</p>
            </div>
            
            <div class="matrix-card" style="border-left: 5px solid #00FFFF;">
                <span style="color: #8B949E; font-size: 12px; font-weight: bold;">06 // HİDRASYON & KALP HIZI KONTROLÜ</span>
                <div style="display: flex; justify-content: space-between; margin-top: 5px;">
                    <span style="color: #FFFFFF;">🚰 Günlük Su İhtiyacı: <b style="color: #00FFFF;">{su_ml/1000:.2f} Litre</b></span>
                    <span style="color: #FFFFFF;">❤️ Maks Kalp Hızı (Tanaka): <b style="color: #FF0055;">{int(mkh)} bpm</b></span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ==========================================
    # 📚 ALT KISIM: AKORDEON REHBERLER (SABİT)
    # ==========================================
    st.write("---")
    st.subheader("📚 MACROFLOW // BİLİMSEL SPORCU ANSİKLOPEDİSİ")
    
    with st.expander("⚖️ Boy Kilo Endeksi ve Yorumlama Rehberi"):
        st.markdown("### Boy Kilo Endeksi Nedir? Nasıl Hesaplanır?\nBoy Kilo Endeksi (BKE), vücut ağırlığını boy ile karşılaştıran ve sağlık riskini değerlendirmeye yardımcı olan bir ölçümdür...")
    with st.expander("🔥 Kalori Hesaplama ve Mifflin-St Jeor Denklemi"):
        st.markdown("### Kalori Nedir? Nasıl Hesaplanır?\nKalori, besinlerin içerdiği enerji miktarını ifade eden bir birimdir...")
    with st.expander("📊 TDEE (Toplam Günlük Enerji Harcaması) ve Hedef Kalibrasyonu"):
        st.markdown("### TDEE Nedir? Nasıl Hesaplanır?\nTDEE (Total Daily Energy Expenditure)...")
    with st.expander("🍗 Makro Besin Değerleri ve Fonksiyonları"):
        st.markdown("### Her Makronun Vücuttaki Rolü\n* **Protein (4 kcal / gram)...")
    with st.expander("⚖️ İdeal Kilo Hesaplama ve Formüller"):
        st.markdown("### İdeal Kilo Nedir? Nasıl Hesaplanır?...")
    with st.expander("📐 US Navy Vücut Yağ Oranı Laboratuvarı"):
        st.markdown("### Vücut Yağ Oranı Nedir?...")
    with st.expander("💪 1RM (One Rep Max) ve Performance Yüzdeleri"):
        st.markdown("### 1 Tekrar Maksimum Nedir?...")
    with st.expander("🚰 Günlük Su İhtiyacı ve Dehidrasyon Sınırları"):
        st.markdown("### Su Tüketim Stratejisi...")
    with st.expander("❤️ Kalp Atış Hızı Bölgeleri (Heart Rate Zones)"):
        st.markdown("### Maksimum Kalp Hızı Tahmini...")
    with st.expander("🧬 Protein İhtiyacı ve Kas Sentezi Gerçekleri"):
        st.markdown("### Günlük Ne Kadar Protein?...")
    with st.expander("⏱️ Setler Arası Dinlenme Süresi ve Kas Toparlanması"):
        st.markdown("### Setler Arası Dinlenme Neden Önemlidir?...")
    with st.expander("📏 Bel-Kalça Oranı ve Visseral Yağ Riskleri"):
        st.markdown("### Bel Kalça Oranı Nedir? Nasıl Hesaplanır?...")
    with st.expander("🧬 Üç Temel Vücut Tipi ve Genetik Yapı Şablonları"):
        st.markdown("### Vücut Tiplerinin Özellikleri...")