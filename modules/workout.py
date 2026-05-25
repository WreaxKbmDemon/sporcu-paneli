import streamlit as st
import pandas as pd

def render_workout_tab():
    st.subheader("⚔️ BUGÜNKÜ PAZARTESİ İDMAN LOGLARI (GERÇEKLEŞEN METRİK)")
    col_pzt, col_pro = st.columns([2, 1])
    
    with col_pzt:
        st.markdown("### 🔴 BUGÜN BASILAN REKOR KİLOLAR (PZT)")
        df_bugun = pd.DataFrame({
            "Hareket": [
                "Bench Press (Set 1)", "Bench Press (Set 2)", 
                "Incline DB Press (Set 1)", "Incline DB Press (Set 2)", 
                "Pec Deck (Set 1)", "Pec Deck (Set 2)", 
                "Düz Bar Pushdown (Set 1)", "Düz Bar Pushdown (Set 2)", 
                "Overhead Cable V Bar Ext (Set 1)", "Overhead Cable V Bar Ext (Set 2)", 
                "Hanging Leg Raise", "Crunch", "Plank (Ağırlıksız)"
            ],
            "Ağırlık (kg)": [
                "100 kg", "90 kg", "30 kg (DB)", "30 kg (DB)", 
                "84 kg", "77 kg", "60 kg", "55 kg", "40 kg", "40 kg", 
                "Vücut", "Vücut", "Süre"
            ],
            "Tekrar / Süre": [
                "2 Tekrar 🚀", "5 Tekrar", "4 Tekrar", "5 Tekrar", 
                "5 Tekrar", "5 Tekrar", "6 Tekrar", "7 Tekrar", 
                "8 Tekrar", "9 Tekrar", "1.Set: 20 | 2.Set: 14", 
                "1.Set: 30 | 2.Set: 30", "1.Set: 1:30 Dk | 2.Set: 1:00 Dk"
            ]
        })
        st.dataframe(df_bugun, use_container_width=True, hide_index=True)
        
    with col_pro:
        st.markdown("### 🗓️ Haftalık split şablonu")
        st.info("Pzt/Per: Göğüs-Triceps\n\nSal/Cum: Sırt-Biceps-Karın\n\nÇarş: Omuz\n\nCmt/Paz: RECOVERY (OFFDAY)")