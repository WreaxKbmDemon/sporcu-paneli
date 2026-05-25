import streamlit as st
import pandas as pd
import plotly.express as px
import math

def render_analytics_tab(csv_file):
    st.subheader("📊 MACROFLOW Gelişmiş Gokalaf Analiz Merkezi")
    
    try:
        df = pd.read_csv(csv_file)
        if df.empty or len(df) < 1:
            st.info("💡 Analiz ve grafikler için veri giriş paneline en az 1 günlük veri mühürlemiş olman gerekir aslanım.")
        else:
            # Genel Metrik Çıktıları
            toplam_gun = len(df)
            en_guncel_kilo = df["Kilo"].iloc[-1]
            en_guncel_bel = df["Bel_cm"].iloc[-1] if "Bel_cm" in df.columns else 78.0
            
            col_m1, col_m2, col_m3 = st.columns(3)
            with col_m1:
                st.metric(label="🎯 Güncel Tartı", value=f"{en_guncel_kilo} kg")
            with col_m2:
                st.metric(label="📏 Güncel Bel Ölçüsü", value=f"{en_guncel_bel} cm")
            with col_m3:
                st.metric(label="📅 Toplam Kayıtlı Gün", value=f"{toplam_gun} Gün")
            
            # 📉 ÇİFTE GRAFİK YAPILANDIRMASI
            st.write("---")
            st.subheader("📉 Bel Çevresi ve Form Değişim Grafiği")
            if "Bel_cm" in df.columns and not df["Bel_cm"].isna().all():
                fig_bel = px.line(df, x="Tarih", y="Bel_cm", markers=True, title="Veri Tabanından Çekilen Canlı Bel Ölçüsü Grafiği")
                fig_bel.update_traces(line_color="#00FFCC", marker=dict(size=8, color="#FF007F"))
                fig_bel.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_bel, use_container_width=True)
                
    except Exception as e:
        st.error(f"Analizör motorunda hata: {e}")

    # 🧮 GOKALAF STANDARTLARINDA US NAVY YAĞ ORANI LABORATUVARI
    st.write("---")
    st.subheader("🧮 Gokalaf Tarzı US Navy Yağ Oranı Hesaplayıcı")
    st.write("Boy, bel ve boyun ölçülerini milimetrik gir, gerçek yağ oranını saniyede hesaplayalım amınakoyim!")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    with col_g1:
        g_boy = st.number_input("Boyunuz (cm):", min_value=120.0, max_value=220.0, value=173.0, step=0.5)
    with col_g2:
        g_bel = st.number_input("Aç Karnına Bel Çevresi (cm):", min_value=50.0, max_value=150.0, value=78.0, step=0.1)
    with col_g3:
        g_boyun = st.number_input("Boyun Çevresi (cm):", min_value=20.0, max_value=60.0, value=38.0, step=0.1)
        
    # US Navy Erkek Yağ Oranı Matematiksel Denklemi:
    # %Fat = 86.010 * log10(bel - boyun) - 70.041 * log10(boy) + 36.76
    try:
        if g_bel > g_boyun:
            log_bel_boyun = math.log10(g_bel - g_boyun)
            log_boy = math.log10(g_boy)
            hesaplanan_yag = 86.010 * log_bel_boyun - 70.041 * log_boy + 36.76
            
            st.success(f"🎯 Gokalaf / US Navy Algoritma Sonucu Vücut Yağ Oranınız: **%{hesaplanan_yag:.1f}**")
            
            # Form Durumu Değerlendirmesi
            if hesaplanan_yag <= 11:
                st.success("🚀 DURUM: PARÇALANMIŞ (DEFINED)! Karın kasları kabak gibi dışarıda, mermi gibi form!")
            elif hesaplanan_yag <= 14:
                st.warning("⚡ DURUM: PLAJ FORMU (LEAN)! Estetik, hatlar belirgin, definasyona aynen devam aslanım.")
            else:
                st.info("💪 DURUM: BULK MODU! Kütle yerinde, temiz büyümeye veya hafif kardiyoları artırmaya odaklan.")
        else:
            st.error("⚠️ Bel ölçüsü boyun ölçüsünden küçük olamaz amınakoyim, sayıları kontrol et!")
    except Exception as ex:
        st.error(f"Matematik motoru hesaplayamadı: {ex}")