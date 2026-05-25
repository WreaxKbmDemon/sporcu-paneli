import streamlit as st

def render_analytics_tab(csv_file):
    # İstediğin gibi en üstteki o başlıkları ve test sürümü yazılarını tamamen kazıdık amınakoyim!
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
        st.write("Boy ve kilo bilgilerinizi girin")
        
        d_boy = st.slider("Boyunuz (cm)", min_value=140, max_value=220, value=170, step=1, key="gk_js_boy")
        i_kilo = st.slider("Kilonuz (kg)", min_value=35.0, max_value=160.0, value=70.0, step=0.5, key="gk_js_kilo")
        w_cins = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"], key="gk_js_cins")
        
        btn_hesapla = st.button("⚖️ HESAPLA", use_container_width=True)

    with col2:
        if btn_hesapla:
            a_metre = d_boy / 100
            n_bke = i_kilo / (a_metre * a_metre)
            s_bke = round(n_bke, 1)
            
            min_ideal = round(18.5 * a_metre * a_metre, 1)
            max_ideal = round(24.9 * a_metre * a_metre, 1)
            
            if s_bke < 18.5:
                label = "Düşük Kilo"
                color = "#38bdf8"
                bg_badge = "#0284c7"
                aciklama = "Kilo almanız önerilir."
                detay = "Vücut kütleniz boyunuza göre düşük. Dengeli beslenme ile sağlıklı kilo alımı hedeflenebilir."
            elif s_bke < 25:
                label = "Sağlıklı"
                color = "#34d399"
                bg_badge = "#10b981"
                aciklama = "Harika! Formunu koru."
                detay = "Boy ve kilonuz dengeli. Bu sağlıklı aralığı korumaya devam edin."
            elif s_bke < 30:
                label = "Kilolu"
                color = "#fbbf24"
                bg_badge = "#f59e0b"
                aciklama = "Kalori açığı oluşturmalısın."
                detay = "Boyunuza göre biraz fazla kilonuz var. Beslenme düzeni ve egzersiz ile iyileştirilebilir."
            else:
                label = "Obez"
                color = "#fb7185"
                bg_badge = "#f43f5e"
                aciklama = "Profesyonel destek al."
                detay = "Sağlık riskleri açısından bir uzmana danışmanız önerilir."

            if i_kilo < min_ideal:
                fark_metni = f"+{round(min_ideal - i_kilo, 1)} kg al"
                fark_color = "#38bdf8"
            elif i_kilo > max_ideal:
                fark_metni = f"-{round(i_kilo - max_ideal, 1)} kg ver"
                fark_color = "#fb7185"
            else:
                fark_metni = "Dengeli"
                fark_color = "#34d399"

            st.markdown(f"""
                <div class="result-box" style="border: 2px solid {color};">
                    <p style="color: #8B949E; text-transform: uppercase; letter-spacing: 2px; font-size: 11px; text-align: center; margin-bottom: 5px;">Boy Kilo Endeksiniz</p>
                    <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 20px;">
                        <span style="color: #FFFFFF; font-size: 55px; font-weight: bold;">{s_bke}</span>
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
        else:
            st.markdown("""
                <div class="result-box" style="border: 1px dashed #30363D; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <h3 style="color: #FFFFFF; font-size: 18px; margin-bottom: 5px;">⏳ Sonuç Bekleniyor</h3>
                    <p style="color: #8B949E; font-size: 13px; max-w: 240px; margin: 0;">Boy ve kilo bilgilerinizi girerek boy kilo endeksinizi hesaplayın amınakoyim.</p>
                </div>
            """, unsafe_allow_html=True)