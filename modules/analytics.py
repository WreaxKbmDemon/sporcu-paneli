import streamlit as st

def render_analytics_tab(csv_file):
    # CSS Tasarımı - Siberpunk Dark Mode ve Neon Geçiş Barları
    st.markdown("""
        <style>
            .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
            .result-box {
                background-color: #161B22;
                padding: 25px;
                border-radius: 16px;
                min-height: 320px;
            }
        </style>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='color: #FFFFFF; font-size: 18px;'>📋 ÖLÇÜMLERİNİZ</h3>", unsafe_allow_html=True)
        st.write("Boy ve kilo bilgilerinizi slider ile değiştirdiğiniz an otomatik hesaplanır aslanım.")
        
        # Giriş Elemanları
        d_boy = st.slider("Boyunuz (cm)", min_value=140, max_value=220, value=170, step=1, key="vki_auto_boy")
        i_kilo = st.slider("Kilonuz (kg)", min_value=35.0, max_value=160.0, value=70.0, step=0.5, key="vki_auto_kilo")
        w_cins = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"], key="vki_auto_cins")

    # 🔥 BUTON KONTROLÜNÜ KALDIRDIK! DEĞERLER DEĞİŞTİĞİ AN BURASI DOĞRUDAN ÇALIŞIR AMINAKOYIM!
    with col2:
        a_metre = d_boy / 100
        n_vki = i_kilo / (a_metre * a_metre)
        s_vki = round(n_vki, 1) # Tek basamak yuvarlama
        
        # İdeal Kilo Aralığı Sınırları
        min_ideal = round(18.5 * a_metre * a_metre, 1)
        max_ideal = round(24.9 * a_metre * a_metre, 1)
        
        # Kategoriler ve Durum Eşleşmeleri
        if s_vki < 18.5:
            label = "Zayıf"
            color = "#38bdf8" # Sky-400
            bg_badge = "#0284c7" # Sky-500
            aciklama = "Kilo almanız önerilir."
            detay = "Yetersiz kalori alımı, kas kaybı riski, bağışıklık sistemi zayıflığı görülebilir. Dengeli beslenme ile sağlıklı kilo alımı hedeflenmelidir."
        elif s_vki <= 24.9:
            label = "Normal"
            color = "#34d399" # Emerald-400
            bg_badge = "#10b981" # Emerald-500
            aciklama = "Harika! Formunu koru."
            detay = "Boy ve kilonuz dengeli, betitneklikleriniz antlarman hamıştır. Kardiyovasküler hastalık ve diyabet riski en düşük aralıktır."
        elif s_vki <= 29.9:
            label = "Fazla Kilolu"
            color = "#fbbf24" # Amber-400
            bg_badge = "#f59e0b" # Amber-500
            aciklama = "Kalori açığı oluşturmalısın."
            detay = "Kronik hastalık riski yükselmeye başlar. Kalori kısıtlaması ve düzenli egzersizle ideal aralığa inmek mümkündür."
        else:
            label = "Obez"
            color = "#fb7185" # Rose-400
            bg_badge = "#f43f5e" # Rose-500
            aciklama = "Profesyonel destek al."
            detay = "Tip 2 diyabet, kalp hastalığı ve eklem problemleri riski belirgin biçimde artar. Yaşam tarzı değişikliği önerilir."

        # Dinamik Kilo Farkı Durumu
        if i_kilo < min_ideal:
            fark_metni = f"+{round(min_ideal - i_kilo, 1)} kg al"
            fark_color = "#38bdf8"
        elif i_kilo > max_ideal:
            fark_metni = f"-{round(i_kilo - max_ideal, 1)} kg ver"
            fark_color = "#fb7185"
        else:
            fark_metni = "Dengeli"
            fark_color = "#34d399"

        # Sağ Panel Orijinal UI Çıktısı (Slider oynatıldığı an anlık tepki verir)
        st.markdown(f"""
            <div class="result-box" style="border: 2px solid {color};">
                <p style="color: #8B949E; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; text-align: center; margin-bottom: 5px;">Vücut Kitle İndeksiniz</p>
                <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 20px;">
                    <span style="color: #FFFFFF; font-size: 55px; font-weight: bold;">{s_vki}</span>
                    <div style="text-align: left;">
                        <span style="color: #8B949E; font-size: 12px; display: block;">kg/m²</span>
                        <span style="background-color: {bg_badge}; color: #000000; font-weight: bold; text-transform: uppercase; font-size: 11px; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-top: 2px;">{label}</span>
                    </div>
                </div>
                <div style="background-color: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; margin-bottom: 20px;">
                    <p style="color: {color}; font-weight: bold; margin: 0; font-size: 14px;">{aciklama}</p>
                    <p style="color: #8B949E; margin: 5px 0 0 0; font-size: 12px; line-height: 1.4;">{detay}</p>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                    <div style="background-color: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #8B949E; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px;">İdeal Kilo Aralığı</span>
                        <span style="color: #FFFFFF; font-size: 16px; font-weight: bold;">{min_ideal} - {max_ideal} <span style="font-size: 11px; color: #8B949E;">kg</span></span>
                    </div>
                    <div style="background-color: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #8B949E; font-size: 11px; text-transform: uppercase; display: block; margin-bottom: 2px;">Kilo Farkı</span>
                        <span style="color: {fark_color}; font-size: 16px; font-weight: bold;">{fark_metni}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 📚 ALT KISIM: GOKALAF BÜTÜNSEL REHBER AKORDEONLARI (SABİT)
    # ==========================================
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