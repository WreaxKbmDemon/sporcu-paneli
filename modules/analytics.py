import streamlit as st
import pandas as pd

def render_analytics_tab(csv_file):
    st.subheader("📊 MACROFLOW Gelişmiş Sporcu Analizörü")
    
    try:
        df = pd.read_csv(csv_file)
        if df.empty or len(df) < 1:
            st.info("💡 Analiz yapılabilmesi için veri giriş paneline en az 1 günlük veri mühürlemiş olman gerekir aslanım.")
        else:
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

    st.write("---")
    st.subheader("🏋️‍♂️ 1RM (Tek Tekrar Maksimum Güç) Hesaplama Laboratuvarı")
    st.write("Bugün idmanda bastığın o ağır setin ağırlığını ve tekrarını gir, reaktör gerçek gücünü hesaplasın amınakoyim!")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        rekor_kilo = st.number_input("Basılan Ağırlık (kg):", min_value=1.0, max_value=300.0, value=100.0, step=2.5)
    with col_g2:
        rekor_tekrar = st.number_input("Yapılan Tekrar Sayısı:", min_value=1, max_value=30, value=2, step=1)
        
    # Bilimsel Epley 1RM Formülü: 1RM = Kilo * (1 + (Tekrar / 30))
    if rekor_tekrar == 1:
        bir_rm = rekor_kilo
    else:
        bir_rm = rekor_kilo * (1 + (rekor_tekrar / 30))
        
    st.info(f"⚡ Tahmini **1RM (Tek Tekrar Maksimum Gücün): {bir_rm:.1f} KG** amınakoyim!")
    
    # Güç Seviyesi Yorumlama Algoritması
    if bir_rm >= 100:
        st.success("🔥 Durum: ELİT GÜÇ! 100 kg barajının üzerindesin, göğüs reaktörü salondaki abileri ağlatacak seviyede!")
    elif bir_rm >= 80:
        st.warning("⚡ Durum: İLERİ SEVİYE! Güç gelişimi mermi gibi, yakında 100+ kg kulübüne kalıcı üye olursun.")
    else:
        st.info("💪 Durum: GELİŞMEKTE OLAN MAKiNE! Setleri nizami yap, kilolar jilet gibi artmaya devam edecek.")