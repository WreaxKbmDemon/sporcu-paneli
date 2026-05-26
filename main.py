import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import unicodedata
from modules.supplement import render_supplement_tab

DATA_DIR = Path("data")
HOME_MATRIX_FILE = DATA_DIR / "anasayfa_matrisi.csv"
ROUTINE_NOTES_FILE = DATA_DIR / "rutin_notlari.csv"
ROUTINE_WEEKLY_FILE = DATA_DIR / "rutin_haftalik_takip.csv"
NUTRITION_PLAN_FILE = DATA_DIR / "beslenme_plani.csv"
WORKOUT_ANALYSIS_FILE = DATA_DIR / "antreman_analiz.csv"

HOME_MATRIX_COLUMNS = ["Hafta", "Kilo", "Kilo Analizi", "Su Tüketimi (L)", "Yağ Oranı (%)"]
ROUTINE_NOTE_COLUMNS = ["TarihSaat", "Not"]
ROUTINE_WEEKLY_COLUMNS = ["Hafta", "Gün", "Sabah KG", "Su", "Not"]
NUTRITION_PLAN_COLUMNS = ["Plan", "Öğün", "Besin", "Miktar", "Birim", "Kalori", "Protein", "Karbonhidrat", "Yağ", "Öğün Toplamları"]
WORKOUT_ANALYSIS_COLUMNS = ["TarihSaat", "Hafta", "Gun", "Hareket", "Set", "KiloKg", "Tekrar", "Not"]
DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma", "Cumartesi", "Pazar"]
TRAINING_DAYS = ["Pazartesi", "Salı", "Çarşamba", "Perşembe", "Cuma"]
WEEK_OPTIONS = [f"{i}. Hafta" for i in range(1, 51)]
WORKOUT_PROGRAM = {
    "Pazartesi": [
        {"hareket": "Bench Press", "set": 2},
        {"hareket": "Incline Dumbbell Press", "set": 2},
        {"hareket": "Pec Deck", "set": 2},
        {"hareket": "Düz Bar Pushdown", "set": 2},
        {"hareket": "Overhead Cable V Bar Extension", "set": 2},
    ],
    "Salı": [
        {"hareket": "Barfiks", "set": 2},
        {"hareket": "Lat Machine", "set": 2},
        {"hareket": "Chest Supported Single Arm Machine Row", "set": 2},
        {"hareket": "Incline Dumbbell Curl", "set": 2},
        {"hareket": "Preacher Curl", "set": 2},
        {"hareket": "Hanging Leg Raise", "set": 2},
        {"hareket": "Crunch", "set": 2},
        {"hareket": "Ağırlıklı Plank", "set": 2},
    ],
    "Çarşamba": [
        {"hareket": "Shoulder Press Machine", "set": 2},
        {"hareket": "Dumbbell Shoulder Press", "set": 2},
        {"hareket": "Seated Dumbbell Lateral Raise", "set": 2},
        {"hareket": "Cable Lateral Raise", "set": 2},
        {"hareket": "Ters Pec Deck", "set": 4},
    ],
    "Perşembe": [
        {"hareket": "Bench Press", "set": 2},
        {"hareket": "Incline Dumbbell Press", "set": 2},
        {"hareket": "Pec Deck", "set": 2},
        {"hareket": "Düz Bar Pushdown", "set": 2},
        {"hareket": "Overhead Cable V Bar Extension", "set": 2},
    ],
    "Cuma": [
        {"hareket": "Barfiks", "set": 2},
        {"hareket": "Lat Machine", "set": 2},
        {"hareket": "Chest Supported Single Arm Machine Row", "set": 2},
        {"hareket": "Incline Curl", "set": 2},
        {"hareket": "Preacher Curl", "set": 2},
        {"hareket": "Hanging Leg Raise", "set": 2},
        {"hareket": "Crunch", "set": 2},
        {"hareket": "Ağırlıklı Plank", "set": 2},
    ],
}


def ensure_csv_file(file_path, columns):
    DATA_DIR.mkdir(exist_ok=True)
    if not file_path.exists():
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)


def load_csv(file_path, columns):
    ensure_csv_file(file_path, columns)
    try:
        df = pd.read_csv(file_path)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=columns)

    for column in columns:
        if column not in df.columns:
            df[column] = None

    return df[columns]


def append_csv_row(file_path, columns, row):
    ensure_csv_file(file_path, columns)
    pd.DataFrame([row], columns=columns).to_csv(file_path, mode="a", header=False, index=False)


def create_default_home_matrix():
    weeks = [f"{i}. HAFTA" for i in range(1, 51)]
    return pd.DataFrame({
        "Hafta": weeks,
        "Kilo": [71.25 if i == 1 else None for i in range(1, 51)],
        "Kilo Analizi": ["BAŞLANGIÇ" if i == 1 else None for i in range(1, 51)],
        "Su Tüketimi (L)": [4.0 if i == 1 else None for i in range(1, 51)],
        "Yağ Oranı (%)": [12.0 if i == 1 else None for i in range(1, 51)],
    })


def load_home_matrix():
    if not HOME_MATRIX_FILE.exists():
        matrix = create_default_home_matrix()
        DATA_DIR.mkdir(exist_ok=True)
        matrix.to_csv(HOME_MATRIX_FILE, index=False)
        return matrix

    matrix = pd.read_csv(HOME_MATRIX_FILE)
    if "Ortalama Kilo" in matrix.columns and "Kilo" not in matrix.columns:
        matrix = matrix.rename(columns={"Ortalama Kilo": "Kilo"})
    for column in HOME_MATRIX_COLUMNS:
        if column not in matrix.columns:
            matrix[column] = None
    matrix = matrix[HOME_MATRIX_COLUMNS].head(50)
    if len(matrix) < 50:
        default_matrix = create_default_home_matrix()
        matrix = pd.concat([matrix, default_matrix.iloc[len(matrix):]], ignore_index=True)
    if matrix.empty:
        matrix = create_default_home_matrix()
        matrix.to_csv(HOME_MATRIX_FILE, index=False)
    matrix.to_csv(HOME_MATRIX_FILE, index=False)
    return matrix


def create_default_weekly_tracking():
    rows = []
    for week in WEEK_OPTIONS:
        for day in DAYS:
            rows.append({"Hafta": week, "Gün": day, "Sabah KG": None, "Su": None, "Not": ""})
    return pd.DataFrame(rows, columns=ROUTINE_WEEKLY_COLUMNS)


def load_weekly_tracking():
    if not ROUTINE_WEEKLY_FILE.exists():
        weekly = create_default_weekly_tracking()
        DATA_DIR.mkdir(exist_ok=True)
        weekly.to_csv(ROUTINE_WEEKLY_FILE, index=False)
        return weekly

    weekly = load_csv(ROUTINE_WEEKLY_FILE, ROUTINE_WEEKLY_COLUMNS)
    defaults = create_default_weekly_tracking()
    existing_keys = set(zip(weekly["Hafta"].astype(str), weekly["Gün"].astype(str)))
    missing_rows = defaults[
        ~defaults.apply(lambda row: (row["Hafta"], row["Gün"]) in existing_keys, axis=1)
    ]
    if not missing_rows.empty:
        weekly = pd.concat([weekly, missing_rows], ignore_index=True)

    weekly["Sabah KG"] = pd.to_numeric(weekly["Sabah KG"], errors="coerce")
    weekly["Su"] = pd.to_numeric(weekly["Su"], errors="coerce")
    weekly["Not"] = weekly["Not"].fillna("").astype(str)
    return weekly[ROUTINE_WEEKLY_COLUMNS]


def get_active_routine_week(weekly_data):
    for week in WEEK_OPTIONS:
        week_rows = weekly_data[weekly_data["Hafta"] == week]
        kg_values = pd.to_numeric(week_rows["Sabah KG"], errors="coerce").dropna()
        if len(kg_values) < 7:
            return week
    return WEEK_OPTIONS[-1]


def sync_week_to_home_matrix(week, weekly_data):
    week_rows = weekly_data[weekly_data["Hafta"] == week]
    kg_values = pd.to_numeric(week_rows["Sabah KG"], errors="coerce").dropna()
    su_values = pd.to_numeric(week_rows["Su"], errors="coerce").dropna()
    if len(kg_values) < 7:
        return False

    matrix = load_home_matrix()
    week_label = week.replace("Hafta", "HAFTA")
    target_index = matrix.index[matrix["Hafta"] == week_label]
    if target_index.empty:
        return False

    matrix.loc[target_index[0], "Kilo"] = round(float(kg_values.mean()), 2)
    if len(su_values) > 0:
        matrix.loc[target_index[0], "Su Tüketimi (L)"] = round(float(su_values.mean()), 2)
    matrix.to_csv(HOME_MATRIX_FILE, index=False)
    return True


def create_default_nutrition_plan():
    rows = []
    for plan in ["Plan 1", "Plan 2"]:
        for meal_number in range(1, 7):
            for row_index in range(3):
                rows.append({
                    "Plan": plan,
                    "Öğün": f"{meal_number}. ÖĞÜN" if row_index == 0 else "",
                    "Besin": "",
                    "Miktar": None,
                    "Birim": "",
                    "Kalori": None,
                    "Protein": None,
                    "Karbonhidrat": None,
                    "Yağ": None,
                    "Öğün Toplamları": "",
                })
        rows.append({
            "Plan": plan,
            "Öğün": "GÜN SONU TOPLAMI",
            "Besin": "",
            "Miktar": None,
            "Birim": "",
            "Kalori": None,
            "Protein": None,
            "Karbonhidrat": None,
            "Yağ": None,
            "Öğün Toplamları": "",
        })
    return pd.DataFrame(rows, columns=NUTRITION_PLAN_COLUMNS)


def load_nutrition_plan():
    if not NUTRITION_PLAN_FILE.exists():
        nutrition = create_default_nutrition_plan()
        DATA_DIR.mkdir(exist_ok=True)
        nutrition.to_csv(NUTRITION_PLAN_FILE, index=False)
        return nutrition

    nutrition = load_csv(NUTRITION_PLAN_FILE, NUTRITION_PLAN_COLUMNS)
    text_columns = ["Plan", "Öğün", "Besin", "Birim", "Öğün Toplamları"]
    for column in text_columns:
        nutrition[column] = nutrition[column].fillna("").astype(str)
    numeric_columns = ["Miktar", "Kalori", "Protein", "Karbonhidrat", "Yağ"]
    for column in numeric_columns:
        nutrition[column] = pd.to_numeric(nutrition[column], errors="coerce")
    return nutrition[NUTRITION_PLAN_COLUMNS]


def normalize_workout_analysis(df):
    text_columns = ["TarihSaat", "Hafta", "Gun", "Hareket", "Not"]
    for column in text_columns:
        df[column] = df[column].fillna("").astype(str)

    df["Set"] = pd.to_numeric(df["Set"], errors="coerce").fillna(1).astype(int)
    df["KiloKg"] = pd.to_numeric(df["KiloKg"], errors="coerce").fillna(0.0)
    df["Tekrar"] = pd.to_numeric(df["Tekrar"], errors="coerce").fillna(0).astype(int)
    return df


def normalize_name(value):
    text = str(value).strip().lower()
    text = text.replace("dumbell", "dumbbell")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return " ".join(text.split())


def get_next_workout_step(records, week, day):
    day_program = WORKOUT_PROGRAM.get(day, [])
    if not day_program:
        return "", 1

    day_records = records[(records["Hafta"] == week) & (records["Gun"] == day)]
    for exercise in day_program:
        movement = exercise["hareket"]
        target_sets = exercise["set"]
        completed_sets = day_records[
            day_records["Hareket"].map(normalize_name) == normalize_name(movement)
        ].shape[0]

        if completed_sets < target_sets:
            return movement, completed_sets + 1

    last_exercise = day_program[-1]
    return last_exercise["hareket"], last_exercise["set"]


def render_workout_program_reference():
    with st.expander("Haftalik Antreman Duzeni Referansi", expanded=True):
        st.markdown("""
        **Pazartesi / Persembe - Gogus / Triceps**
        * Bench Press - 2 Set x 6-7 Tekrar
        * Incline Dumbbell Press - 2 Set x 6-7 Tekrar
        * Pec Deck - 2 Set x 8 Tekrar
        * Duz Bar Pushdown - 2 Set x 9 Tekrar
        * Overhead Cable V Bar Extension - 2 Set x 7 Tekrar

        **Sali / Cuma - Sirt / Biceps / Karin**
        * Barfiks - 2 Set x Max Tekrar
        * Lat Machine - 2 Set x 7 Tekrar
        * Chest Supported Single Arm Machine Row - 2 Set x 6-8 Tekrar
        * Incline Dumbbell Curl - 2 Set x 6 Tekrar
        * Preacher Curl - 2 Set x 6 Tekrar
        * Hanging Leg Raise / Crunch / Agirlikli Plank

        **Carsamba - Omuz**
        * Shoulder Press Machine - 2 Set x 6 Tekrar
        * Dumbbell Shoulder Press - 2 Set x 6 Tekrar
        * Seated Dumbbell Lateral Raise - 2 Set x 12 Tekrar
        * Cable Lateral Raise - 2 Set x 12 Tekrar
        * Ters Pec Deck - 4 Set x 8 Tekrar
        """)


if not HOME_MATRIX_FILE.exists():
    DATA_DIR.mkdir(exist_ok=True)
    create_default_home_matrix().to_csv(HOME_MATRIX_FILE, index=False)
ensure_csv_file(ROUTINE_NOTES_FILE, ROUTINE_NOTE_COLUMNS)
if not ROUTINE_WEEKLY_FILE.exists():
    create_default_weekly_tracking().to_csv(ROUTINE_WEEKLY_FILE, index=False)
if not NUTRITION_PLAN_FILE.exists():
    create_default_nutrition_plan().to_csv(NUTRITION_PLAN_FILE, index=False)
ensure_csv_file(WORKOUT_ANALYSIS_FILE, WORKOUT_ANALYSIS_COLUMNS)

# Siberpunk / Neon Karanlık Tema Ayarları
st.set_page_config(page_title="Eren Aydın - Sporcu Paneli", page_icon="🦾", layout="wide")

st.markdown("""
    <style>
    .reportview-container { background: #1A1D29; color: #FFFFFF; }
    h1, h2, h3 { color: #00E5FF !important; }
    .stButton>button { background-color: #00FFCC; color: #1A1D29; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🦾 SİBERPUNK SPORCU PANELİ // v2.0")

# Sol Panel: Profil ve Hedef Kilitleme
with st.sidebar:
    st.header("📋 PROFİL BİLGİLERİ")
    st.write("**Adı Soyadı:** Eren Aydın")
    st.write("**Yaş:** 16 | **Boy:** 173 cm | **Başlangıç Kilo:** 71 kg")
    st.write(f"**Güncel Tarih:** {datetime.now().strftime('%d.%m.%Y')}")
    st.markdown("---")
    st.success("🎯 Hedef: Maksimum Tanım & Yağ Yakımı")

# 8 Ana Sekme Bölümü
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 SPORCU PANELİ",
    "📝 RUTİN TAKİP VE NOTLAR",
    "🥗 BESLENME PLANI",
    "🏃‍♂️ KARDİYO",
    "🏋️‍♂️ ANTREMAN PROGRAMI",
    "📈 ANTREMAN ANALİZ",
    "📏 ÖLÇÜ ANALİZ",
    "💊 SUPPLEMENT"
])

with tab1:
    st.subheader("SPORCU PANELİ")

    col_profile, col_coaching = st.columns(2)
    with col_profile:
        st.markdown("### DANIŞMAN BİLGİLERİ")
        st.dataframe(
            pd.DataFrame({
                "Bilgi": ["Adı Soyadı", "Yaş", "Boy (cm)", "Başlangıç Kilo"],
                "Değer": ["Eren Aydın", "16", "173", "71 kg"],
            }),
            use_container_width=True,
            hide_index=True,
        )
    with col_coaching:
        st.markdown("### KOÇLUK BİLGİLERİ")
        st.dataframe(
            pd.DataFrame({
                "Bilgi": ["Başlangıç Tarihi", "Bitiş Tarihi"],
                "Değer": [datetime.now().strftime("%d.%m.%Y"), ""],
            }),
            use_container_width=True,
            hide_index=True,
        )

    st.markdown("### HEDEFLER")
    st.data_editor(
        pd.DataFrame({
            "Gün": DAYS,
            "Kalori": [None for _ in DAYS],
            "Protein": [None for _ in DAYS],
            "Karbonhidrat": [None for _ in DAYS],
            "Yağ": [None for _ in DAYS],
            "Su": [None for _ in DAYS],
        }),
        use_container_width=True,
        hide_index=True,
        key="hedefler_editor",
    )

    st.markdown("### 50 HAFTALIK GELİŞİM TABLOSU")
    st.info("Rutin takipte 7 günlük sabah kilosu girilince haftalık ortalama kilo buraya otomatik düşer.")
    df_matrix = load_home_matrix()
    edited_matrix = st.data_editor(
        df_matrix,
        use_container_width=True,
        height=350,
        hide_index=True,
        disabled=["Hafta"],
        column_config={
            "Kilo": st.column_config.NumberColumn("Kilo", step=0.05, format="%.2f"),
            "Su Tüketimi (L)": st.column_config.NumberColumn("Su Tüketimi (L)", step=0.1, format="%.1f"),
            "Yağ Oranı (%)": st.column_config.NumberColumn("Yağ Oranı (%)", step=0.1, format="%.1f"),
        },
        key="anasayfa_matrisi_editor",
    )
    if st.button("Ana Sayfa Matrisini Kaydet"):
        edited_matrix.to_csv(HOME_MATRIX_FILE, index=False)
        st.success("Ana sayfa matrisi kalıcı olarak kaydedildi.")

with tab2:
    st.subheader("RUTİN TAKİP VE NOTLAR")
    weekly_tracking = load_weekly_tracking()
    selected_week = get_active_routine_week(weekly_tracking)
    st.info(f"Aktif hafta: {selected_week}. 7 gün sabah kilosu girilince ortalama otomatik Sporcu Paneli'ne aktarılır ve ekran sonraki haftaya geçer.")
    current_week = weekly_tracking[weekly_tracking["Hafta"] == selected_week].copy()

    tracking_table = current_week[["Gün", "Sabah KG", "Su"]].copy()
    kg_average = tracking_table["Sabah KG"].mean(skipna=True)
    su_average = tracking_table["Su"].mean(skipna=True)
    tracking_display = pd.concat([
        tracking_table,
        pd.DataFrame([{
            "Gün": "ORTALAMA",
            "Sabah KG": round(float(kg_average), 2) if pd.notna(kg_average) else None,
            "Su": round(float(su_average), 2) if pd.notna(su_average) else None,
        }]),
    ], ignore_index=True)

    notes_table = current_week[["Gün", "Not"]].copy()
    col_tracking, col_notes = st.columns([1, 1])
    with col_tracking:
        st.markdown("### GENEL HAFTALIK TAKİP")
        edited_tracking = st.data_editor(
            tracking_table,
            use_container_width=True,
            hide_index=True,
            disabled=["Gün"],
            column_config={
                "Sabah KG": st.column_config.NumberColumn("Sabah KG", min_value=30.0, max_value=200.0, step=0.05, format="%.2f"),
                "Su": st.column_config.NumberColumn("Su", min_value=0.0, max_value=15.0, step=0.1, format="%.1f"),
            },
            key=f"genel_haftalik_takip_{selected_week}",
        )
        edited_kg_average = edited_tracking["Sabah KG"].mean(skipna=True)
        edited_su_average = edited_tracking["Su"].mean(skipna=True)
        st.dataframe(
            pd.DataFrame([{
                "Gün": "ORTALAMA",
                "Sabah KG": round(float(edited_kg_average), 2) if pd.notna(edited_kg_average) else None,
                "Su": round(float(edited_su_average), 2) if pd.notna(edited_su_average) else None,
            }]),
            use_container_width=True,
            hide_index=True,
        )

    with col_notes:
        st.markdown("### SPORCU GÜNLÜK NOTLAR")
        edited_notes = st.data_editor(
            notes_table,
            use_container_width=True,
            hide_index=True,
            disabled=["Gün"],
            column_config={
                "Not": st.column_config.TextColumn("Not", width="large"),
            },
            key=f"sporcu_gunluk_notlar_{selected_week}",
        )

    if st.button("Rutin Takibi Kaydet"):
        edited_days = edited_tracking[edited_tracking["Gün"].isin(DAYS)].copy()
        edited_notes = edited_notes.copy()
        for day in DAYS:
            tracking_row = edited_days[edited_days["Gün"] == day]
            note_row = edited_notes[edited_notes["Gün"] == day]
            row_index = weekly_tracking[
                (weekly_tracking["Hafta"] == selected_week) & (weekly_tracking["Gün"] == day)
            ].index
            if row_index.empty:
                continue

            weekly_tracking.loc[row_index[0], "Sabah KG"] = tracking_row["Sabah KG"].iloc[0]
            weekly_tracking.loc[row_index[0], "Su"] = tracking_row["Su"].iloc[0]
            weekly_tracking.loc[row_index[0], "Not"] = note_row["Not"].iloc[0] if not note_row.empty else ""

        weekly_tracking.to_csv(ROUTINE_WEEKLY_FILE, index=False)
        synced = sync_week_to_home_matrix(selected_week, weekly_tracking)
        if synced:
            st.success(f"{selected_week} kaydedildi. 7 günlük ortalama kilo Sporcu Paneli'ne otomatik aktarıldı.")
            st.rerun()
        else:
            st.success(f"{selected_week} kaydedildi. 7 sabah kilosu tamamlanınca ortalama Sporcu Paneli'ne aktarılacak.")

with tab3:
    st.subheader("BESLENME PLANI")
    st.info("İçerik şimdilik boş bırakıldı; öğünleri ve makroları ilerleyen zamanda buradan dolduracağız.")

    nutrition_plan = load_nutrition_plan()
    edited_nutrition_parts = []
    col_plan_1, col_plan_2 = st.columns(2)
    for plan_name, column in [("Plan 1", col_plan_1), ("Plan 2", col_plan_2)]:
        with column:
            st.markdown(f"### {plan_name}")
            plan_rows = nutrition_plan[nutrition_plan["Plan"] == plan_name].copy()
            edited_plan = st.data_editor(
                plan_rows.drop(columns=["Plan"]),
                use_container_width=True,
                height=620,
                hide_index=True,
                column_config={
                    "Öğün": st.column_config.TextColumn("ÖĞÜN", width="small"),
                    "Besin": st.column_config.TextColumn("BESİN", width="medium"),
                    "Miktar": st.column_config.NumberColumn("MİKTAR", min_value=0.0, step=1.0, width="small"),
                    "Birim": st.column_config.TextColumn("BİRİM", width="small"),
                    "Kalori": st.column_config.NumberColumn("KALORİ", min_value=0.0, step=1.0, width="small"),
                    "Protein": st.column_config.NumberColumn("PROTEİN", min_value=0.0, step=0.1, width="small"),
                    "Karbonhidrat": st.column_config.NumberColumn("KARBONHİDRAT", min_value=0.0, step=0.1, width="small"),
                    "Yağ": st.column_config.NumberColumn("YAĞ", min_value=0.0, step=0.1, width="small"),
                    "Öğün Toplamları": st.column_config.TextColumn("ÖĞÜN TOPLAMLARI", width="medium"),
                },
                key=f"beslenme_plani_{plan_name}",
            )
            edited_plan.insert(0, "Plan", plan_name)
            edited_nutrition_parts.append(edited_plan[NUTRITION_PLAN_COLUMNS])

    if st.button("Beslenme Planını Kaydet"):
        pd.concat(edited_nutrition_parts, ignore_index=True).to_csv(NUTRITION_PLAN_FILE, index=False)
        st.success("Beslenme planı kaydedildi.")

with tab4:
    st.subheader("Haftalık Kardiyo ve Supplement Protokolü")
    st.markdown("### 🏃‍♂️ KOŞU BANDI: **15 EĞİM** // **5 HIZ** // **45 DAKİKA**")
    st.markdown("""
    * **İdman Öncesi:** 1 Ölçek Pre-Workout + 1 Adet Özkaynak Maden Suyu
    * **Salona Giriş:** 4 Kapsül L-Carnitine
    * **İdman Arası (Kardiyodan 15 dk önce):** 2 Kapsül Thermo Burner
    """)

with tab5:
    st.subheader("🏋️‍♂️ ANTREMAN PROGRAMI")

    with st.expander("PAZARTESİ – GÖĞÜS / TRİCEPS", expanded=True):
        st.markdown("""
        **Göğüs**
        * Bench Press — 2 × 6–7
        * Incline Dumbbell Press — 2 × 6–7
        * Pec Deck — 2 × 8

        **Triceps**
        * Düz Bar Pushdown — 2 × 9
        * Overhead Cable V Bar Extension — 2 × 7
        """)

    with st.expander("SALI – SIRT / BICEPS / KARIN"):
        st.markdown("""
        **Sırt**
        * Barfiks — 2 × Max
        * Lat Machine — 2 × 7
        * Chest Supported Single Arm Machine Row — 2 × 6–8

        **Biceps**
        * Incline Dumbbell Curl — 2 × 6
        * Preacher Curl — 2 × 6

        **Karın**
        * Hanging Leg Raise — 2 × Max
        * Crunch — 2 × 25-30
        * Ağırlıklı Plank — 2 × Max
        """)

    with st.expander("ÇARŞAMBA – OMUZ"):
        st.markdown("""
        **Omuz**
        * Shoulder Press Machine — 2 × 6
        * Dumbbell Shoulder Press — 2 × 6
        * Seated Dumbbell Lateral Raise — 2 × 12
        * Cable Lateral Raise — 2 × 12
        * Ters Pec Deck — 4 × 8
        """)

    with st.expander("PERŞEMBE – GÖĞÜS / TRİCEPS"):
        st.markdown("""
        **Göğüs**
        * Bench Press — 2 × 6–7
        * Incline Dumbbell Press — 2 × 6–7
        * Pec Deck — 2 × 8

        **Triceps**
        * Düz Bar Pushdown — 2 × 9
        * Overhead Cable V Bar Extension — 2 × 7
        """)

    with st.expander("CUMA – SIRT / BICEPS / KARIN"):
        st.markdown("""
        **Sırt**
        * Barfiks — 2 × Max
        * Lat Machine — 2 × 7
        * Chest Supported Single Arm Machine Row — 2 × 6–8

        **Biceps**
        * Incline Curl — 2 × 6
        * Preacher Curl — 2 × 6

        **Karın**
        * Hanging Leg Raise — 2 × Max
        * Crunch — 2 × 25-30
        * Ağırlıklı Plank — 2 × Max
        """)

with tab6:
    st.subheader("📈 ANTREMAN ANALİZ // KALICI PERFORMANS DEFTERİ")
    st.info("Her hareketi tarih/saat, hafta, set, kilo ve tekrar bilgisiyle kalıcı olarak kaydedebilirsin.")

    render_workout_program_reference()
    analiz_kayitlari = normalize_workout_analysis(load_csv(WORKOUT_ANALYSIS_FILE, WORKOUT_ANALYSIS_COLUMNS))

    st.markdown("### Yeni Performans Kaydı")
    col_week, col_day = st.columns(2)
    with col_week:
        hafta = st.selectbox("Hafta", WEEK_OPTIONS, key="antreman_kayit_hafta")
    with col_day:
        gun = st.selectbox("Gün", DAYS, key="antreman_kayit_gun")

    suggested_movement, suggested_set = get_next_workout_step(analiz_kayitlari, hafta, gun)
    movement_options = [exercise["hareket"] for exercise in WORKOUT_PROGRAM.get(gun, [])]
    suggested_index = movement_options.index(suggested_movement) if suggested_movement in movement_options else 0

    if gun in WORKOUT_PROGRAM:
        st.caption(f"Sıradaki öneri: {suggested_movement} - {suggested_set}. set")
    else:
        st.caption("Bu gün için tanımlı program yok; hareketi serbest olarak seçebilirsin.")

    with st.form("antreman_analiz_formu", clear_on_submit=True):
        col_move, col_set = st.columns([2, 1])
        with col_move:
            if movement_options:
                hareket = st.selectbox("Hareket", movement_options, index=suggested_index)
            else:
                hareket = st.text_input("Hareket", placeholder="Serbest hareket adı")
        with col_set:
            set_no = st.number_input("Set", min_value=1, max_value=20, value=int(suggested_set), step=1)

        col_weight, col_reps = st.columns(2)
        with col_weight:
            kilo = st.number_input("Kilo (kg)", min_value=0.0, max_value=400.0, value=0.0, step=0.5)
        with col_reps:
            tekrar = st.number_input("Tekrar", min_value=0, max_value=200, value=0, step=1)

        analiz_not = st.text_area("Ekstra Not", placeholder="Form, zorlanma, pump, RIR, ağrı veya özel detay...")
        analiz_kaydet = st.form_submit_button("Kaydet")

    if analiz_kaydet:
        if str(hareket).strip():
            append_csv_row(
                WORKOUT_ANALYSIS_FILE,
                WORKOUT_ANALYSIS_COLUMNS,
                {
                    "TarihSaat": datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
                    "Hafta": hafta,
                    "Gun": gun,
                    "Hareket": str(hareket).strip(),
                    "Set": int(set_no),
                    "KiloKg": float(kilo),
                    "Tekrar": int(tekrar),
                    "Not": analiz_not.strip(),
                },
            )
            st.success("Antreman analizi tarih/saat ile kalıcı olarak kaydedildi.")
        else:
            st.warning("Kaydetmek için hareket adını doldur.")

    st.markdown("---")
    st.markdown("### Haftalık Analiz Kayıtları")
    filtre_hafta = st.selectbox(
        "Görüntülenecek Hafta",
        WEEK_OPTIONS,
        key="antreman_analiz_filtre_hafta",
    )
    haftalik_kayitlar = analiz_kayitlari[analiz_kayitlari["Hafta"] == filtre_hafta].copy()

    if haftalik_kayitlar.empty:
        st.info(f"{filtre_hafta} için henüz kayıt yok.")
    else:
        edited_days = []
        display_columns = ["TarihSaat", "Hareket", "Set", "KiloKg", "Tekrar", "Not"]
        for day in TRAINING_DAYS:
            day_records = haftalik_kayitlar[haftalik_kayitlar["Gun"] == day].copy()
            with st.expander(f"{day} ({len(day_records)} kayıt)", expanded=not day_records.empty):
                if day_records.empty:
                    st.info(f"{day} için kayıt yok.")
                    continue

                edited_day = st.data_editor(
                    day_records[display_columns],
                    use_container_width=True,
                    height=min(420, 80 + (len(day_records) * 38)),
                    hide_index=True,
                    disabled=["TarihSaat"],
                    column_config={
                        "TarihSaat": st.column_config.TextColumn("Tarih"),
                        "Hareket": st.column_config.TextColumn("Hareket", width="medium"),
                        "Set": st.column_config.NumberColumn("Set", min_value=1, max_value=20, step=1, width="small"),
                        "KiloKg": st.column_config.NumberColumn("Kilo", min_value=0.0, max_value=400.0, step=0.5, width="small"),
                        "Tekrar": st.column_config.NumberColumn("Tekrar", min_value=0, max_value=200, step=1, width="small"),
                        "Not": st.column_config.TextColumn("Not", width="large"),
                    },
                    key=f"antreman_analiz_editor_{filtre_hafta}_{day}",
                )
                edited_day["Hafta"] = filtre_hafta
                edited_day["Gun"] = day
                edited_days.append(edited_day[WORKOUT_ANALYSIS_COLUMNS])

        if edited_days and st.button("Haftalık Analiz Kayıtlarını Güncelle"):
            edited_weekly_records = pd.concat(edited_days).sort_index()
            analiz_kayitlari.update(edited_weekly_records)
            analiz_kayitlari.to_csv(WORKOUT_ANALYSIS_FILE, index=False)
            st.success(f"{filtre_hafta} kayıtları güncellendi.")

with tab7:
    st.subheader("📏 ÖLÇÜ ANALİZ")
    st.info("Vücut ölçülerini hızlıca girip takip edebileceğin ölçü analiz alanı.")

    col_olcu_1, col_olcu_2, col_olcu_3 = st.columns(3)
    with col_olcu_1:
        kilo_olcu = st.number_input("Güncel Kilo (kg)", min_value=30.0, max_value=200.0, value=71.25, step=0.05)
        bel = st.number_input("Bel (cm)", min_value=40.0, max_value=160.0, value=78.0, step=0.1)
        boyun = st.number_input("Boyun (cm)", min_value=20.0, max_value=70.0, value=38.0, step=0.1)
    with col_olcu_2:
        gogus = st.number_input("Göğüs (cm)", min_value=40.0, max_value=180.0, value=100.0, step=0.1)
        kol = st.number_input("Kol (cm)", min_value=15.0, max_value=70.0, value=35.0, step=0.1)
        omuz = st.number_input("Omuz (cm)", min_value=60.0, max_value=180.0, value=120.0, step=0.1)
    with col_olcu_3:
        bacak = st.number_input("Bacak (cm)", min_value=30.0, max_value=100.0, value=55.0, step=0.1)
        kalca = st.number_input("Kalça (cm)", min_value=50.0, max_value=180.0, value=90.0, step=0.1)
        boy = st.number_input("Boy (cm)", min_value=120.0, max_value=230.0, value=173.0, step=1.0)

    vki = kilo_olcu / ((boy / 100) ** 2)
    bel_boy_orani = bel / boy
    st.markdown("---")
    metric_1, metric_2, metric_3 = st.columns(3)
    metric_1.metric("VKİ", f"{vki:.1f}")
    metric_2.metric("Bel / Boy Oranı", f"{bel_boy_orani:.2f}")
    metric_3.metric("Ölçü Özeti", f"Bel {bel:.1f} cm")

    st.dataframe(
        pd.DataFrame({
            "Ölçü": ["Kilo", "Bel", "Boyun", "Göğüs", "Kol", "Omuz", "Bacak", "Kalça"],
            "Değer": [kilo_olcu, bel, boyun, gogus, kol, omuz, bacak, kalca],
            "Birim": ["kg", "cm", "cm", "cm", "cm", "cm", "cm", "cm"],
        }),
        use_container_width=True,
        hide_index=True,
    )

with tab8:
    render_supplement_tab()
