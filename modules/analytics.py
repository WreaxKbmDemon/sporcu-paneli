import streamlit as st
import streamlit.components.v1 as components

def render_analytics_tab(csv_file):
    st.title("🧱 gokalaf.com REAL-TIME DOMAIN REPLİKASYONU")
    st.write("Gokalaf.com sitesindeki hesaplama araçları doğrudan senin domainine mühürlenmiştir. Veriler %100 orijinal motor üzerinden çalışır amınakoyim!")
    st.write("---")

    # Gokalaf.com Kalori ve Araçlar Sayfasını Doğrudan Senin Arayüze Gömiyoruz
    # Genişlik ve yükseklik ayarları sporcu paneline göre optimize edildi.
    
    st.markdown("""
        <style>
            .gokalaf-container {
                border: 2px solid #00FFCC;
                border-radius: 12px;
                overflow: hidden;
                background-color: #161B22;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='gokalaf-container'>", unsafe_allow_html=True)
    
    # Gokalaf'ın araçlar sayfasını iframe ile senin domaine köklüyoruz
    components.iframe("https://gokalaf.com/araclar", height=900, scrolling=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.write("---")
    st.caption("⚡ Siberpunk Entegrasyon Sistemi Aktif | 9-Bilişim Departmanı Gururla Sunar amınakoyim!")