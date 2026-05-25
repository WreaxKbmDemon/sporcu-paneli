import streamlit as st
import pandas as pd

def render_cardio_tab():
    st.subheader("⏱️ Haftalık Kardiyo Takip Matriksi")
    st.success("PROTOKOL: 15 Eğim, 5.5 Hız, 30 Dakika Hafta İçi Hergün | HaftaSonu Offday (Kardio Yok)")
    
    df_kardiyo = pd.DataFrame({
        "Gün": ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"],
        "Tip": ["Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "Koşu Bandı", "OFFDAY 💤", "OFFDAY 💤"],
        "Eğim/Hız": ["15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "15 / 5.5", "-", "-"],
        "Süre": ["30 Dk ⏱️", "30 Dk", "30 Dk", "30 Dk", "30 Dk", "-", "-"],
        "Durum": ["BİTTİ 🏆", "Bekliyor", "Bekliyor", "Bekliyor", "Bekliyor", "DİNLENME", "DİNLENME"]
    })
    st.table(df_kardiyo)
    
    st.write("---")
    st.subheader("🔥 15 Eğim & 5.5 Hız METs Kalori Analizörü")
    st.write("Yüksek eğimli yürüyüşlerin normal koşudan daha fazla yağ yaktığını bilişimsel formüllerle kanıtlıyoruz aslanım!")
    
    c_kilo = st.number_input("Güncel Kilonuz (Kardiyo Analizi İçin):", min_value=40.0, max_value=150.0, value=71.25, step=0.5)
    c_sure = st.number_input("Kardiyo Süresi (Dakika):", min_value=1, max_value=120, value=45, step=5) # Bugün 45 yaptın diye 45 aldım amınakoyim!
    
    # Bilimsel MET Değeri: 15 Eğim ve 5.5 Hız için tahmini MET değeri ~8.5'tir.
    # Kalori Formülü: (MET * 3.5 * Kilo / 200) * Süre
    yakilan_kalori = (8.5 * 3.5 * c_kilo / 200) * c_sure
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.metric(label="🔥 Tahmini Yakılan Saf Enerji", value=f"{yakilan_kalori:.1f} kcal")
    with col_k2:
        # 1 gram saf yağ yaklaşık 9 kaloridir, ama kardiyodaki verimle ~7.7 kalori baz alınır
        yakilan_yag = yakilan_kalori / 7.7
        st.metric(label="💧 Eritilen Saf Yağ Dokusu", value=f"{yakilan_yag:.1f} Gram")
        
    st.info("💡 NOT: 15 Eğimde yapılan yürüyüş, omurgaya ve diz kapaklarına sıfır baskı (low-impact) uygulayarak merkezi sinir sistemini ($CNS$) korur ve bacak kaslarını yıkmadan saf yağ yakımını tetikler amınakoyim!")