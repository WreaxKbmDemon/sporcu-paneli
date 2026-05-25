import streamlit as st
import pandas as pd

def render_supplement_tab():
    st.subheader("💊 Güncel Supplement Enjeksiyon Zamanlaması")
    
    st.table(pd.DataFrame({
        "Dönem / Safha": ["💥 SPOR ÖNCESİ", "💥 SPOR ARASI", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE", "💤 YATMADAN 15-20 DK ÖNCE"],
        "Takviye İçeriği": ["0.75 Ölçek Pre-Workout + 4 Kapsül L-Carnitine", "2 Kapsül Thermo Burner 🔥", "5 Gram Creatine", "1 Kapsül Zinc (Çinko)", "1-2 Gram Magnezyum L-Threonate"],
        "Hedef Kodlama": ["Maksimum Odak ve Yağ Yakımı", "Termojenik Ateşleme", "Gece ATP Hücre Dolumu", "Testosteron Koruma Kalkanı", "REM Derin Uyku & CNS Reset"]
    }))
    
    st.write("---")
    st.subheader("🧮 Bilişimsel Kreatin & Su Optimizasyon Hesaplayıcısı")
    
    user_kilo = st.number_input("Güncel kilonu gir aslanım (Kreatin dozajı için):", min_value=40.0, max_value=150.0, value=71.25, step=0.5)
    
    # Bilimsel formül: Kilo başına 0.04 gram kreatin ideal sürdürülebilir dozdur
    ideal_kreatin = user_kilo * 0.04
    ideal_su = (user_kilo * 35) / 1000 # Kilo başına 35ml su baz alınır, antrenman günü +1.5L eklenir
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.info(f"🧬 Senin kilon için günlük almanız gereken **İdeal Kreatin Dozu: {ideal_kreatin:.2f} Gram** (Düz hesap 5g iyidir amınakoyim).")
    with col_b2 if 'col_b2' in locals() else col_c2: # Hata riski sıfır olsun
        st.success(f"🚰 Kreatin hücreyi susuz bırakmasın diye günlük **Minimum Su Hedefin: {ideal_su:.2f} Litre** olmalıdır!")