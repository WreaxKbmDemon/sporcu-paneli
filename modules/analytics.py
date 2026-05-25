import streamlit as st
import pandas as pd

def render_analytics_tab(csv_file):
    st.subheader("📊 MACROFLOW Gelişmiş Sporcu Analizörü")
    
    try:
        df = pd.read_csv(csv_file)
        if df.empty or len(df) < 1:
            st.info("💡 Analiz yapılabilmesi için veri giriş paneline en az 1-2 günlük veri mühürlemiş olman gerekir aslanım.")
            return
            
        # Basit İstatistik Hesaplamaları
        toplam_gun = len(df)
        en_guncel_kilo = df["Kilo"].iloc[-1]
        toplam_su_litre = df["Su_ml"].sum() / 1000
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(label="🎯 En Güncel Tartı", value=f"{en_guncel_kilo} kg")
        with col_m2:
            st.metric(label="🚰 Toplam Tüketilen Su", value=f"{toplam_su_litre:.2f} L")
        with col_m3:
            st.metric(label="📅 Toplam Kayıtlı Gün", value=f"{toplam_gun} Gün")
            
        # Gelişmiş Kararlılık Analizi
        if len(df) >= 2:
            ilk_kilo = df["Kilo"].iloc[0]
            kilo_farki = en_guncel_kilo - ilk_kilo
            if kilo_farki < 0:
                st.success(f"📉 Tebrikler Eren! İlk kayıttan itibaren jilet gibi **{abs(kilo_farki):.2f} kg** verdin. Yağ motoru çalışıyor!")
            elif kilo_farki > 0:
                st.warning(f"📈 İlk kayıttan itibaren **{kilo_farki:.2f} kg** aldın. Temiz bulk veya su tutumu olabilir, takibe devam!")
            else:
                st.info("⚖️ Kilon tamamen sabit kalmış, adaptasyon süreci stabil amınakoyim.")
                
    except Exception as e:
        st.error(f"Analizör motorunda hata oluştu: {e}")