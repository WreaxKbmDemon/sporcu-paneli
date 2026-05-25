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
            .expander-header {
                color: #00FFCC !important;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # 📐 ÜST KISIM: İNTERAKTİF HESAPLAMA MOTORU
    # ==========================================
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 style='color: #FFFFFF; font-size: 18px;'>📋 ÖLÇÜMLERİNİZ</h3>", unsafe_allow_html=True)
        st.write("Boy ve kilo bilgilerinizi girerek Vücut Kitle İndeksinizi hesaplayın.")
        
        d_boy = st.slider("Boyunuz (cm)", min_value=140, max_value=220, value=170, step=1, key="vki_js_boy_v6")
        i_kilo = st.slider("Kilonuz (kg)", min_value=35.0, max_value=160.0, value=70.0, step=0.5, key="vki_js_kilo_v6")
        w_cins = st.selectbox("Cinsiyetiniz", ["Erkek", "Kadın"], key="vki_js_cins_v6")
        
        btn_hesapla = st.button("⚖️ HESAPLA", use_container_width=True, key="vki_btn_v6")

    with col2:
        if btn_hesapla:
            a_metre = d_boy / 100
            n_vki = i_kilo / (a_metre * a_metre)
            s_vki = round(n_vki, 1)
            
            min_ideal = round(18.5 * a_metre * a_metre, 1)
            max_ideal = round(24.9 * a_metre * a_metre, 1)
            
            if s_vki < 18.5:
                label = "Zayıf"
                color = "#38bdf8"
                bg_badge = "#0284c7"
                aciklama = "Kilo almanız önerilir."
                detay = "Yetersiz kalori alımı, kas kaybı riski, bağışıklık sistemi zayıflığı görülebilir. Dengeli beslenme ile sağlıklı kilo alımı hedeflenmelidir."
            elif s_vki <= 24.9:
                label = "Normal"
                color = "#34d399"
                bg_badge = "#10b981"
                aciklama = "Harika! Formunu koru."
                detay = "Boy ve kilonuz dengeli, betitneklikleriniz antlarman hamıştır. Kardiyovasküler hastalık ve diyabet riski en düşük aralıktır."
            elif s_vki <= 29.9:
                label = "Fazla Kilolu"
                color = "#fbbf24"
                bg_badge = "#f59e0b"
                aciklama = "Kalori açığı oluşturmalısın."
                detay = "Kronik hastalık riski yükselmeye başlar. Kalori kısıtlaması ve düzenli egzersizle ideal aralığa inmek mümkündür."
            else:
                label = "Obez"
                color = "#fb7185"
                bg_badge = "#f43f5e"
                aciklama = "Profesyonel destek al."
                detay = "Tip 2 diyabet, kalp hastalığı ve eklem problemleri riski belirgin biçimde artar. Yaşam tarzı değişikliği önerilir."

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
        else:
            st.markdown("""
                <div class="result-box" style="border: 1px dashed #30363D; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                    <h3 style="color: #FFFFFF; font-size: 18px; margin-bottom: 5px;">⏳ Sonuç Bekleniyor</h3>
                    <p style="color: #8B949E; font-size: 13px; max-w: 240px; margin: 0;">Boy ve kilo bilgilerinizi girerek vücut kitle indeksinizi hesaplayın amınakoyim.</p>
                </div>
            """, unsafe_allow_html=True)

    st.write("---")

    # ==========================================
    # 📚 ALT KISIM: GOKALAF BÜTÜNSEL REHBER AKORDEONLARI
    # ==========================================
    st.subheader("📚 MACROFLOW // BİLİMSEL SPORCU ANSİKLOPEDİSİ")
    st.write("Attığın tüm orijinal makale ve rehber verileri sisteme jilet gibi işlendi aslanım:")

    with st.expander("⚖️ Boy Kilo Endeksi ve Yorumlama Rehberi"):
        st.markdown("""
        ### Boy Kilo Endeksi Nedir? Nasıl Hesaplanır?
        Boy Kilo Endeksi (BKE), vücut ağırlığını boy ile karşılaştıran ve sağlık riskini değerlendirmeye yardımcı olan bir ölçümdür. Bu hesap makinesinde kullanılan endeks, geleneksel VKİ formülünden farklı bir yaklaşım benimseyerek boya göreli ağırlık dağılımını değerlendirir. Özellikle Çin ve Uzak Doğu kaynaklı tıp araştırmalarında yaygın kullanım alanıulan bu yöntem, Asya popülasyonuna özgü sağlık riski eşiklerini daha doğru yansıtır.
        
        Standart VKİ hesabında boy'un karesi paydada yer alırken, bazı boy kilo endeksi uygulamaları farklı ağırlıklandırma faktörleri kullanır. Bu yaklaşım, boy ile kilo arasındaki orantısallık ilişkisini farklı bir perspektiften ele alarak aynı VKİ değerine sahip ancak farklı boylu bireyler arasındaki sağlık farklılıklarını daha iyi açıklamaya çalışır.
        
        ### Sonuçları Nasıl Yorumlamalısın?
        * **Zayıf (VKİ < 18.5):** Yetersiz kalori alımı, kas kaybı riski, bağışıklık sistemi zayıflığı ve kemik yoğunluğu kaybı görülebilir.
        * **Normal (18.5 – 24.9):** Kardiyovasküler hastalık, tip 2 diyabet ve hipertansiyon riski en düşük aralıktır.
        * **Fazla Kilolu (25 – 29.9):** Kronik hastalık riski yükselmeye başlar. Özellikle bel çevresi 94 cm'yi (erkek) veya 80 cm'yi (kadın) aşıyorsa risk anlamlı düzeyde artar.
        * **Obez (VKİ ≥ 30):** Tip 2 diyabet, kalp hastalığı, uyku apnesi, eklem problemleri riski belirgin biçimde artar. Profesyonel destek alınması önerilir.
        """)

    with st.expander("🔥 Kalori Hesaplama ve Mifflin-St Jeor Denklemi"):
        st.markdown("""
        ### Kalori Nedir? Nasıl Hesaplanır?
        Kalori, besinlerin içerdiği enerji miktarını ifade eden bir birimdir. Teknik tanımıyla bir kilokalori (kcal), bir litre suyu 1°C ısıtmak için gereken enerji miktarına eşittir.
        
        ### Mifflin-St Jeor Denklemi
        Modern spor biliminde altın standart kabul edilen formülümüz:
        * **Erkek:** $BMR = (10 \\times kilo) + (6.25 \\times boy) - (5 \\times yaş) + 5$
        * **Kadın:** $BMR = (10 \\times kilo) + (6.25 \\times boy) - (5 \\times yaş) - 161$
        
        **BMR (Bazal Metabolizma Hızı):** Tamamen dinlenme halindeyken, hiçbir şey yemeden en temel yaşamsal fonksiyonları sürdürmek için vücudun tükettiği kalori miktarıdır.
        """)

    with st.expander("📊 TDEE (Toplam Günlük Enerji Harcaması) ve Hedef Kalibrasyonu"):
        st.markdown("""
        ### TDEE Nedir? Nasıl Hesaplanır?
        TDEE (Total Daily Energy Expenditure), bir günde vücudunuzun tüm aktiviteleri için harcadığı toplam kalori miktarını ifade eder. BMR'ın aktivite çarpanıyla çarpılmasıyla elde edilir:
        * **Hareketsiz:** BMR x 1.2
        * **Hafif Aktif:** BMR x 1.375
        * **Orta Aktif:** BMR x 1.55
        * **Çok Aktif:** BMR x 1.725
        * **Ekstra Aktif:** BMR x 1.9
        
        ### Metabolik Adaptasyon
        Uzun süreli kalori kısıtlamasında vücut, enerji harcamasını düşürerek yeni koşullara adapte olur. Bunu önlemek için her 8-12 haftada bir 1-2 haftalık diyet molaları (TDEE seviyesine çıkma) planlanmalıdır.
        """)

    with st.expander("🍗 Makro Besin Değerleri ve Fonksiyonları"):
        st.markdown("""
        ### Her Makronun Vücuttaki Rolü
        * **Protein (4 kcal / gram):** Kas dokusu, enzimler ve hormonların yapı taşıdır. Sindirimi için harcanan termik etki en yüksek gruptur (%20-30).
        * **Karbonhidrat (4 kcal / gram):** Beynin ve kasların tercih ettiği birincil yakıt kaynağıdır. Glikojen olarak kaslarda depolanır.
        * **Yağ (9 kcal / gram):** Hormon üretimi (özellikle testosteron ve östrojen) için vazgeçilmezdir. Minimum %20 yağ alımının altına düşülmemelidir.
        """)

    with st.expander("⚖️ İdeal Kilo Hesaplama ve Formüller"):
        st.markdown("""
        ### İdeal Kilo Nedir? Nasıl Hesaplanır?
        İdeal kilo, belirli bir boy için sağlık riskleri ve yaşam kalitesi açısından en uygun vücut ağırlığı aralığını ifade eden kavramdır.
        
        ### Kullanılan Başlıca Bilimsel Formüller:
        * **Devine Formülü (1974)**
        * **Robinson Formülü (1983)**
        * **Miller Formülü (1983)**
        * **Hamwi Formülü**
        
        Kademeli ilerleme, alışkanlık geliştirme ve yaşam tarzı değişiklikleri; hedefe çok daha kalıcı biçimde ulaşmayı sağlar. Yo-yo etkisini önlemenin en güçlü stratejisi, kilo verme sürecinde kas kütlesini korumaktır. Bunu sağlamanın yolu ise yeterli protein alımı ve düzenli direnç antrenmanıdır.
        """)

    with st.expander("📐 US Navy Vücut Yağ Oranı Laboratuvarı"):
        st.markdown("""
        ### Vücut Yağ Oranı Nedir?
        Vücut yağ oranı, toplam vücut ağırlığının yüzde kaçının yağ dokusundan oluştuğunu gösteren bir ölçümdür. Hesap makinemizde kullanılan **ABD Deniz Kuvvetleri (US Navy)** formülü bel, boyun ve kalça çevre ölçümlerini kullanarak laboratuvar testlerine %3-4 yakınlıkta oldukça doğru sonuçlar verir.
        
        ### Bölgesel Yağ Yakımı Mümkün mü?
        Bilim şunu net söylemektedir: **Bölgesel yağ yakımı mümkün değildir.** Göbek kaslarını çalıştırmak o bölgedeki yağı eritmez. Göbek yağını azaltmanın tek yolu, genel vücut yağ yüzdesini düşürmektir.
        """)

    with st.expander("💪 1RM (One Rep Max) ve Performans Yüzdeleri"):
        st.markdown("""
        ### 1 Tekrar Maksimum Nedir?
        1RM, bir kişinin belirli bir harekette tek seferde kaldırabileceği maksimum ağırlık miktarıdır. Güç antrenmanının temel referans noktasıdır.
        
        ### 1RM Yüzdelerinin Kullanımı:
        * **Güç Dayanıklılığı (%50-65):** 15-20 tekrar aralığı.
        * **Hipertrofi / Kas Büyümesi (%65-85):** 6-12 tekrar aralığı. Optimal kas büyümesi.
        * **Güç Geliştirme (%85-95):** 2-5 tekrar aralığı. Nöromüsküler adaptasyon.
        * **Maksimal Güç (%95-100):** 1-2 tekrar aralığı. Merkezi sinir sistemini yoğun yorar.
        """)

    with st.expander("🚰 Günlük Su İhtiyacı ve Dehidrasyon Sınırları"):
        st.markdown("""
        ### Su Tüketim Stratejisi
        Temel formül vücut ağırlığının kilogramı başına **30-35 ml** su tüketilmesidir. Ancak kreatin kullanan veya yoğun antrenman yapan sporcularda bu hedefe ekstra su eklenmelidir.
        
        ### İdrar Rengi Takibi:
        * **Açık Sarı (Limonata rengi):** İyi hidrasyon.
        * **Koyu Sarı / Kahverengi:** Yetersiz su alımı (Dehidrasyon riski!).
        """)

    with st.expander("❤️ Kalp Atış Hızı Bölgeleri (Heart Rate Zones)"):
        st.markdown("""
        ### Maksimum Kalp Hızı Tahmini:
        * **Tanaka Formülü:** $208 - (0.7 \\times yaş)$
        
        ### 5 Kalp Hızı Bölgesi:
        * **Bölge 1 (%50-60):** Aktif Dinlenme. Isınma ve soğuma.
        * **Bölge 2 (%60-70):** Aerobik Temel. **Yağ yakımının en yüksek olduğu bölgedir.**
        * **Bölge 3 (%70-80):** Aerobik Geliştirme. Kardiyovasküler verim artar.
        * **Bölge 4 (%80-90):** Anaerobik Eşik. Enerji artık ağırlıklı karbonhidrattır.
        * **Bölge 5 (%90-100):** Maksimal efor. VO2 maks geliştirme.
        """)

    with st.expander("🧬 Protein İhtiyacı ve Kas Sentezi Gerçekleri"):
        st.markdown("""
        ### Günlük Ne Kadar Protein?
        Direnç antrenmanı yapan ve kas kütlesini korumak/geliştirmek isteyen sporcular için bilimsel altın aralık **1.6 - 2.2 g/kg** protein alımıdır.
        
        ### Sabah Protein Tüketiminin Önemi
        Uyku sırasındaki uzun süreli açlıktan sonra vücutta kas yıkımı üstün gelmeye başlar. Sabah yüksek protein içeren bir kahvaltı, bu yıkım sürecini durdurup anabolizmayı (yapımı) anında başlatır amınakoyim!
        """)

    with st.expander("⏱️ Setler Arası Dinlenme Süresi ve Kas Toparlanması"):
        st.markdown("""
        ### Setler Arası Dinlenme Neden Önemlidir?
        Setler arası dinlenme süresi; performansı, kas uyarımını, hormonsal yanıtı ve enerji sistemlerinin kullanımını doğrudan etkiler. Dinlenmenin fizyolojik temeli ATP-PCr (fosfokreatin) sisteminin yenilenmesine dayanır.
        
        ### Hedefe Göre Dinlenme Süreleri:
        * **Maksimal Güç:** 3 – 5 dakika (%85-100 1RM yüklerinde).
        * **Hipertrofi (Kas Büyümesi):** 60 – 90 saniye (Metabolik stres birikimi).
        * **Güç Dayanıklılığı:** 30 – 60 saniye (Kardiyovasküler ve kas dayanıklılığı kapasitesi).
        
        ### Kaslar Ne Zaman Büyür?
        Çok yaygın bir yanılgıyı düzeltmek gerekir: **Kaslar antrenman sırasında değil, sonrasında büyür.** Egzersiz kas dokusunda mikroskobik hasarlar oluşturur ve derin uyku evrelerinde büyüme hormonu (GH) salgılanarak protein senteziyle bu dokular tamir edilir.
        """)

    with st.expander("📏 Bel-Kalça Oranı ve Visseral Yağ Riskleri"):
        st.markdown("""
        ### Bel Kalça Oranı Nedir? Nasıl Hesaplanır?
        Bel-kalça oranı (BKO), bel çevresinin kalça çevresine bölünmesiyle elde edilen basit ancak bilgilendirici bir sağlık göstergesidir: $BKO = Bel \\div Kalça$.
        
        ### Cinsiyete Göre Risk Eşikleri:
        * **Düşük Risk:** Erkeklerde $\le 0.90$ | Kadınlarda $\le 0.80$
        * **Orta Risk:** Erkeklerde $0.91 - 0.99$ | Kadınlarda $0.81 - 0.85$
        * **Yüksek Risk:** Erkeklerde $\ge 1.0$ | Kadınlarda $\ge 0.86$ (İç organ yağlanması tehlikesi!)
        """)

    with st.expander("🧬 Üç Temel Vücut Tipi ve Genetik Yapı Şablonları"):
        st.markdown("""
        ### Vücut Tiplerinin Özellikleri:
        * **Ektomorf:** İnce kemik yapısı, hızlı metabolizma, düşük doğal kas kütlesi. Kilo almakta ve kas yapmakta güçlük çeker.
        * **Mezomorf:** Atletik yapı, orta-geniş kemik çerçevesi, hızlı kas yanıtı. Kas kazanımına ve yağ yakmaya en yatkın tip.
        * **Endomorf:** Geniş kemik yapısı, yavaş metabolizma, yağ depolamaya yüksek eğilim. Kas kazanımı görece kolaydır ancak yağlanmaya müsaittir.
        
        ### Vücut Tipi Kader midir?
        **Kesinlikle hayır.** Epigenetik araştırmalar, genetik eğilimlerin yaşam tarzı seçimleriyle (disiplinli beslenme ve direnç antrenmanı programlarıyla) tamamen değiştirilebileceğini ve fenotipik ifadesinin dönüştürülebileceğini göstermektedir amınakoyim!
        """)