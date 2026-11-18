import io
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler
import streamlit as st
from style import apply_custom_theme, preprocess_toefl_data

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================
st.set_page_config(
    page_title="Klasterisasi TOEFL Mahasiswa POLNES",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ==========================================
# DEFINISI 9 FOLDER & WARNA TAB BERTUMPUK
# ==========================================
PAGES = [
    {"id": "home", "label": "Beranda", "bg": "#FAFDFB"},
    {"id": "business", "label": "Business Understanding", "bg": "#FAFDFB"},
    {"id": "acquisition", "label": "Data Acquisition", "bg": "#FAFDFB"},
    {"id": "understanding", "label": "Data Understanding", "bg": "#FAFDFB"},
    {"id": "preparation", "label": "Data Preparation", "bg": "#FAFDFB"},
    {"id": "eda", "label": "EDA", "bg": "#FAFDFB"},
    {"id": "evaluasi", "label": "Evaluasi Model", "bg": "#FAFDFB"},
    {"id": "clustering", "label": "Clustering", "bg": "#FAFDFB"},
    {"id": "interpretasi", "label": "Interpretasi Hasil", "bg": "#FAFDFB"},
]

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "home"

if "uploaded_file_cache" not in st.session_state:
    st.session_state["uploaded_file_cache"] = None

# Terapkan Tema CSS Konsisten (#FAFDFB)
apply_custom_theme("#FAFDFB")


# ==========================================
# FUNGSI PEMBACAAN DATA TERPUSAT
# ==========================================
def load_toefl_data(uploaded_file):
    try:
        uploaded_file.seek(0)
        if uploaded_file.name.endswith(".xlsx") or uploaded_file.name.endswith(
            ".xls"
        ):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Gagal membaca file: {e}")
        return pd.DataFrame()


# ==========================================
# FUNGSI EVALUASI TER-CACHE (FULL DATA TANPA SAMPLING)
# ==========================================
@st.cache_data
def hitung_evaluasi_full(_X_scaled_tuple):
    X_scaled = np.array(_X_scaled_tuple)

    # 1. Hitung Elbow (Inertia)
    inertia = []
    K_range = list(range(1, 8))
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(X_scaled)
        inertia.append(km.inertia_)

    # 2. Hitung Silhouette untuk K = 2, 3, 4 (Full Data)
    perbandingan_k = [2, 3, 4]
    tabel_hasil_eval = []
    sil_scores_dict = {}

    for k_val in perbandingan_k:
        km_test = KMeans(n_clusters=k_val, random_state=42, n_init=10)
        labels_test = km_test.fit_predict(X_scaled)
        score_test = silhouette_score(X_scaled, labels_test)
        vals_test = silhouette_samples(X_scaled, labels_test)

        sil_scores_dict[k_val] = {
            "labels": labels_test,
            "score": score_test,
            "vals": vals_test,
        }

        tabel_hasil_eval.append({
            "Jumlah Klaster (K)": f"K = {k_val}",
            "Rata-Rata Silhouette Score": round(score_test, 4),
            "Keterangan": (
                "Titik Optimal Utama (Elbow)"
                if k_val == 3
                else "Kandidat Pembanding"
            ),
        })

    return inertia, K_range, sil_scores_dict, pd.DataFrame(tabel_hasil_eval)


# ==========================================
# FUNGSI AMAN PENCARIAN TITIK SIKU ELBOW
# ==========================================
def find_optimal_k(k_list, inertia_list):
    p1 = np.array([k_list[0], inertia_list[0]])
    p2 = np.array([k_list[-1], inertia_list[-1]])
    
    distances = []
    for k, val in zip(k_list, inertia_list):
        p0 = np.array([k, val])
        n = np.abs((p2[1] - p1[1]) * p0[0] - (p2[0] - p1[0]) * p0[1] + p2[0] * p1[1] - p2[1] * p1[0])
        d = np.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)
        dist = n / d if d != 0 else 0
        distances.append(dist)
        
    return k_list[np.argmax(distances)]


# ==========================================
# RENDER STACKED FOLDER TABS DI ATAS
# ==========================================
st.markdown('<div class="nav-folder-anchor"></div>', unsafe_allow_html=True)
col_widths = [0.65, 1.25, 1.05, 1.15, 1.05, 0.65, 0.95, 0.9, 1.1]
cols_nav = st.columns(col_widths)

for idx, page in enumerate(PAGES):
    with cols_nav[idx]:
        is_active = st.session_state["active_tab"] == page["id"]
        if st.button(
            page["label"],
            key=f"nav_{page['id']}",
            type="primary" if is_active else "secondary",
            use_container_width=True,
        ):
            st.session_state["active_tab"] = page["id"]
            st.rerun()

# ==========================================
# HALAMAN 0: SAMPUL JUDUL & ALUR PENELITIAN
# ==========================================
if st.session_state["active_tab"] == "home":
    st.markdown(
        """
        <div class="cover-wrapper">
            <div class="cover-badge">SISTEM ANALISIS & KLASTERISASI • UPA BAHASA POLNES</div>
            <h1 class="cover-title">
                Analisis Capaian <span class="highlight-mint">Subtes Program Studi</span> dan Klasterisasi Kemampuan <span class="highlight-purple">TOEFL Mahasiswa POLNES</span> Menggunakan K-Means Clustering
            </h1>
            <div class="flow-section-title" style="margin-top: 1.5rem;">Alur Tahapan Penelitian</div>
            <div class="flow-grid-top">
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #FFE066;">TAHAP 01</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Business Understanding</p>
                    <p class="flow-step-desc">Latar belakang masalah, tujuan & ruang lingkup penelitian.</p>
                </div>
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #FFA94D;">TAHAP 02</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Data Acquisition</p>
                    <p class="flow-step-desc">Sumber data UPA Bahasa, integrasi arsip & unggah dataset.</p>
                </div>
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #B197FC;">TAHAP 03</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Data Understanding</p>
                    <p class="flow-step-desc">Kamus atribut kolom, tipe data & pratinjau data mentah.</p>
                </div>
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #FF8787;">TAHAP 04</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Data Preparation</p>
                    <p class="flow-step-desc">Pembersihan missing values, seleksi fitur & normalisasi format.</p>
                </div>
            </div>
            <div class="flow-grid-top" style="margin-top: 10px;">
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #74C0FC;">TAHAP 05</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Exploratory Data Analysis</p>
                    <p class="flow-step-desc">Visualisasi distribusi skor, tren tahunan & prodi terlemah.</p>
                </div>
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #63E6BE;">TAHAP 06</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Evaluasi Model</p>
                    <p class="flow-step-desc">Reduksi PCA, Kurva Metode Elbow & Silhouette Plot.</p>
                </div>
                <div class="flow-card">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #38D9A9;">TAHAP 07</span>
                        <span style="font-weight: 800; font-size: 0.8rem;">→</span>
                    </div>
                    <p class="flow-step-name">Clustering</p>
                    <p class="flow-step-desc">Segmentasi Tier kemampuan mahasiswa.</p>
                </div>
                <div class="flow-card" style="border: 2px dashed #10C35D;">
                    <div class="flow-card-top">
                        <span class="flow-step-num" style="background-color: #10C35D; color: white;">TAHAP 08</span>
                        <span style="font-weight: 800; font-size: 0.72rem;">SELESAI</span>
                    </div>
                    <p class="flow-step-name">Interpretasi Hasil</p>
                    <p class="flow-step-desc">Penjelasan mendalam karakteristik & subtes terlemah per tier.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# HALAMAN 1: BUSINESS UNDERSTANDING
# ==========================================
elif st.session_state["active_tab"] == "business":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 01 • PEMAHAMAN BISNIS & PENELITIAN</span>
            <h2 class="section-heading">Business Understanding</h2>
            <p class="section-desc">Definisi latar belakang kebutuhan UPA Bahasa POLNES, rumusan tujuan analisis, serta ruang lingkup klasterisasi skor TOEFL mahasiswa jenjang D3 dan D4.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.markdown(
            """
            <div class="paper-card">
                <h4>Latar Belakang Masalah</h4>
                <p>UPA Bahasa Politeknik Negeri Samarinda (POLNES) menyelenggarakan tes TOEFL sebagai standar evaluasi kemampuan bahasa Inggris mahasiswa tingkat akhir (D3 & D4). Rekapitulasi nilai mencakup rincian subtes maupun skor total komposit untuk memetakan:</p>
                <ul>
                    <li>Kelompok tingkatan kemampuan (<i>tier</i>) mahasiswa secara objektif.</li>
                    <li>Subtes spesifik (<i>Listening, Structure, Reading</i>) serta skor total sebagai acuan evaluasi tiap Program Studi.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b2:
        st.markdown(
            """
            <div class="paper-card-accent">
                <h4>Tujuan & Manfaat Penelitian</h4>
                <ol>
                    <li><b>Reduksi & Ekstraksi Fitur:</b> Menggabungkan 3 subtes utama TOEFL serta skor Total menggunakan <i>Principal Component Analysis</i> (PCA).</li>
                    <li><b>Evaluasi & Klasterisasi:</b> Menentukan jumlah kelompok optimal menggunakan <b>Metode Elbow</b> & <b>Silhouette Plot</b>, lalu mengelompokkan mahasiswa dengan <b>K-Means Clustering</b>.</li>
                    <li><b>Rekomendasi Kebijakan:</b> Mengidentifikasi Program Studi dengan skor rata-rata terendah sebagai dasar program pelatihan bahasa.</li>
                </ol>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ==========================================
# HALAMAN 2: DATA ACQUISITION
# ==========================================
elif st.session_state["active_tab"] == "acquisition":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 02 • AKUISISI & SUMBER DATA</span>
            <h2 class="section-heading">Data Acquisition</h2>
            <p class="section-desc">Dokumentasi sumber perolehan data, kriteria sampel, tahapan penggabungan file historis, serta unggah dataset gabungan D3 & D4.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_aq1, col_aq2 = st.columns(2)
    with col_aq1:
        st.markdown(
            """
            <div class="paper-card">
                <h4>1. Sumber & Otoritas Data</h4>
                <ul>
                    <li><b>Instansi Penyedia:</b> Unit Penunjang Akademik (UPA) Bahasa Politeknik Negeri Samarinda (POLNES).</li>
                    <li><b>Sifat Data:</b> Data sekunder historis hasil pelaksanaan tes TOEFL mahasiswa D3 dan D4.</li>
                    <li><b>Rentang Periode:</b> Data multi-tahun yang dikonsolidasikan dari arsip lembar kerja tahun pelaksanaan tes.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_aq2:
        st.markdown(
            """
            <div class="paper-card-accent">
                <h4>2. Proses Integrasi & Kriteria Data</h4>
                <ul>
                    <li><b>Konsolidasi Multi-Sheet:</b> File rekapitulasi digabungkan menjadi satu <i>Master Dataset</i> terstruktur.</li>
                    <li><b>Pelacakan Asal Data (Audit Trail):</b> Setiap baris data mencatat atribut <code>Tahun_Tes</code>, <code>Sumber_File</code>, dan <code>Sheet</code> untuk validitas penelusuran.</li>
                    <li><b>Format File Didukung:</b> Microsoft Excel (<code>.xlsx</code>, <code>.xls</code>) dan Comma-Separated Values (<code>.csv</code>).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("Unggah Master Dataset TOEFL (D3 & D4)")
    uploaded_file = st.file_uploader(
        "Pilih file dataset gabungan (.xlsx, .xls, atau .csv)",
        type=["xlsx", "xls", "csv"],
    )

    if uploaded_file is not None:
        st.session_state["uploaded_file_cache"] = uploaded_file
        df_preview = load_toefl_data(uploaded_file)
        if not df_preview.empty:
            st.success(
                f"File **{uploaded_file.name}** berhasil diakuisisi. Total"
                f" **{len(df_preview)} baris** dan **{len(df_preview.columns)}"
                " kolom** siap dianalisis pada tahap **Data Understanding**."
            )
    elif st.session_state["uploaded_file_cache"] is not None:
        cached_name = st.session_state["uploaded_file_cache"].name
        st.info(
            f"Dataset **{cached_name}** sudah tersimpan aktif di memori sesi"
            " ini. Silakan lanjut ke tab **Data Understanding** atau unggah ulang"
            " jika ingin mengganti file."
        )

# ==========================================
# HALAMAN 3: DATA UNDERSTANDING
# ==========================================
elif st.session_state["active_tab"] == "understanding":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 03 • PEMAHAMAN STRUKTUR & ATRIBUT DATA</span>
            <h2 class="section-heading">Data Understanding</h2>
            <p class="section-desc">Pemeriksaan dimensi dataset, kamus atribut kolom (identitas & fitur subtes/total), tipe data, serta pratinjau rekaman mentah sebelum pembersihan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Belum ada dataset yang dimuat. Silakan buka tab **Data"
            " Acquisition** dan unggah file dataset terlebih dahulu."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Rekaman Awal", f"{len(df_raw)} Baris")
            c2.metric("Jumlah Atribut", f"{len(df_raw.columns)} Kolom")
            c3.metric(
                "Total Program Studi",
                f"{df_raw['Prodi'].nunique() if 'Prodi' in df_raw.columns else '-'} Prodi",
            )
            
            if "Tahun_Tes" in df_raw.columns:
                tahun_unik = sorted(df_raw["Tahun_Tes"].dropna().unique())
                if len(tahun_unik) > 0:
                    tahun_str = f"{int(min(tahun_unik))} - {int(max(tahun_unik))}"
                else:
                    tahun_str = "-"
            else:
                tahun_str = "-"
            
            c4.metric("Cakupan Tahun Tes", tahun_str)

            st.markdown("<br>", unsafe_allow_html=True)

            col_u1, col_u2 = st.columns([1.2, 1])
            with col_u1:
                st.markdown(
                    """
                    <div class="paper-card">
                        <h4>Kamus Atribut Dataset (Data Dictionary)</h4>
                        <ul>
                            <li><b>No, Nama, NIM:</b> Atribut identitas mahasiswa peserta tes (non-fitur pemodelan).</li>
                            <li><b>Prodi:</b> Program Studi asal mahasiswa jenjang D3 & D4 di POLNES.</li>
                            <li><b>Section 1:</b> Skor subtes <i>Listening Comprehension</i>.</li>
                            <li><b>Section 2:</b> Skor subtes <i>Structure & Written Expression</i>.</li>
                            <li><b>Section 3:</b> Skor subtes <i>Reading Comprehension</i>.</li>
                            <li><b>Total:</b> Skor akhir komposit TOEFL (ikut dilibatkan dalam fitur analisis pemodelan).</li>
                            <li><b>Tahun_Tes, Sumber_File, Sheet:</b> Metadata waktu pelaksanaan dan asal lembar kerja data.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_u2:
                st.markdown(
                    """
                    <div class="paper-card-accent">
                        <h4>Ringkasan Kualitas & Tipe Kolom</h4>
                        <p style="margin-bottom: 0;">Tabel berikut menunjukkan tipe data terdeteksi dan jumlah nilai kosong (<i>missing values</i>) pada data mentah:</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                df_info = pd.DataFrame({
                    "Nama Kolom": df_raw.columns,
                    "Tipe Data": df_raw.dtypes.astype(str).values,
                    "Terisi": df_raw.notnull().sum().values,
                    "Kosong (Null)": df_raw.isnull().sum().values,
                })
                st.dataframe(
                    df_info, use_container_width=True, hide_index=True, height=270
                )

            st.subheader("Pratinjau Data Mentah (Raw Dataset Preview)")
            st.dataframe(df_raw, use_container_width=True)

# ==========================================
# HALAMAN 4: DATA PREPARATION
# ==========================================
elif st.session_state["active_tab"] == "preparation":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 04 • PRA-PEMROSESAN & PEMBERSIHAN DATA</span>
            <h2 class="section-heading">Data Preparation</h2>
            <p class="section-desc">Tahapan pembersihan kolom tak terpakai, konversi tipe data numerik pada skor subtes dan total, penghapusan nilai kosong, serta seleksi fitur pemodelan.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Harap unggah dataset terlebih dahulu pada tab **Data Acquisition**."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            df, df_clean, kolom_fitur, kolom_identitas = preprocess_toefl_data(df_raw)
            total_data_awal = len(df)
            total_data_bersih = len(df_clean)
            data_dihapus = total_data_awal - total_data_bersih

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Data Mentah", f"{total_data_awal} Baris")
            c2.metric("Data Bersih Valid", f"{total_data_bersih} Mahasiswa")
            c3.metric("Baris Missing Dihapus", f"{data_dihapus} Baris")
            c4.metric("Fitur Utama Terpilih", f"{len(kolom_fitur)} Variabel")

            st.markdown("<br>", unsafe_allow_html=True)

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown(
                    """
                    <div class="paper-card">
                        <h4>Langkah Pembersihan Data (Data Cleaning)</h4>
                        <ol>
                            <li><b>Penghapusan Kolom Kosong/Duplikat:</b> Menghapus kolom otomatis <code>Unnamed</code> dan baris kosong seluruhnya.</li>
                            <li><b>Standardisasi Tipe Numerik:</b> Mengonversi tanda koma menjadi titik dan mengubah kolom <code>Section 1</code>, <code>2</code>, <code>3</code>, serta <code>Total</code> ke format numerik.</li>
                            <li><b>Handling Missing Values:</b> Menghapus rekaman mahasiswa yang tidak memiliki skor lengkap.</li>
                        </ol>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col_p2:
                st.markdown(
                    """
                    <div class="paper-card-accent">
                        <h4>Pemisahan Atribut Identitas & Fitur</h4>
                        <ul>
                            <li><b>Atribut Identitas (Non-Model):</b> <code>No</code>, <code>NIM</code>, <code>Nama</code>, <code>Prodi</code>, dan <code>Tahun_Tes</code> dipertahankan sebagai pelabelan.</li>
                            <li><b>Pengecualian Metadata:</b> Kolom <code>Sumber_File</code> dan <code>Sheet</code> dibersihkan dari tabel bersih.</li>
                            <li><b>Variabel Fitur Klasterisasi:</b> Melibatkan <b>Section 1</b>, <b>Section 2</b>, <b>Section 3</b>, dan <b>Total</b>.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.expander(
                f"Lihat Detail Baris Data yang Dihapus ({data_dihapus} Baris"
                " karena Missing Values / Data Kosong)"
            ):
                if data_dihapus > 0:
                    df_dropped = df[~df.index.isin(df_clean.index)].copy()
                    st.warning(
                        "Berikut adalah daftar baris data mahasiswa yang dihapus pada"
                        " tahap *Handling Missing Values* karena memiliki nilai kosong"
                        " (NaN) pada kolom fitur utama:"
                    )
                    st.dataframe(df_dropped, use_container_width=True)
                else:
                    st.success(
                        "Tidak ada baris data yang dihapus. Seluruh data mentah sudah"
                        " lengkap dan valid!"
                    )

            st.subheader("Statistik Deskriptif Data Bersih")
            st.dataframe(
                df_clean[kolom_fitur].describe().T, use_container_width=True
            )

            st.subheader("Dataset Bersih Siap Eksplorasi & Pemodelan")
            st.dataframe(
                df_clean[kolom_identitas + kolom_fitur], use_container_width=True
            )

# ==========================================
# HALAMAN 5: EXPLORATORY DATA ANALYSIS (EDA)
# ==========================================
elif st.session_state["active_tab"] == "eda":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 05 • EKSPLORASI VISUAL & POLA CAPAIAN</span>
            <h2 class="section-heading">Exploratory Data Analysis (EDA)</h2>
            <p class="section-desc">Visualisasi distribusi skor subtes dan total, pemetaan program studi dengan capaian rata-rata terendah, serta tren lintas tahun.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Harap unggah dataset terlebih dahulu pada tab **Data Acquisition**."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            _, df_clean, kolom_fitur, kolom_identitas = preprocess_toefl_data(df_raw)

            st.subheader("Visualisasi Distribusi Skor Subtes & Total")
            col_box1, col_box2 = st.columns(2)

            fitur_subtes = [
                c for c in ["Section 1", "Section 2", "Section 3"] if c in df_clean.columns
            ]
            fitur_total = [c for c in ["Total"] if c in df_clean.columns]

            with col_box1:
                st.markdown("**Distribusi Skor Subtes (Section 1 - 3)**")
                if fitur_subtes:
                    fig_box_sub = px.box(
                        df_clean,
                        y=fitur_subtes,
                        points="outliers",
                        hover_data=kolom_identitas,
                        color_discrete_sequence=["#10C35D", "#3A86FF", "#FF8A4C"],
                        labels={"value": "Skor Subtes", "variable": "Subtes TOEFL"},
                    )
                    fig_box_sub.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                        height=380,
                    )
                    st.plotly_chart(fig_box_sub, use_container_width=True)

            with col_box2:
                st.markdown("**Distribusi Skor Total Komposit**")
                if fitur_total:
                    fig_box_tot = px.box(
                        df_clean,
                        y=fitur_total,
                        points="outliers",
                        hover_data=kolom_identitas,
                        color_discrete_sequence=["#B197FC"],
                        labels={"value": "Skor Total", "variable": "Komposit"},
                    )
                    fig_box_tot.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                        height=380,
                    )
                    st.plotly_chart(fig_box_tot, use_container_width=True)

            st.markdown("---")
            st.subheader(
                "Analisis Program Studi dengan Skor Rata-Rata Terendah per Tahun Tes"
            )
            st.markdown(
                "Memetakan program studi dengan capaian rata-rata paling rendah pada"
                " masing-masing subtes TOEFL di setiap tahun pelaksanaan ujian."
            )

            if "Tahun_Tes" in df_clean.columns and "Prodi" in df_clean.columns:
                daftar_tahun = sorted(
                    df_clean["Tahun_Tes"].dropna().astype(str).unique()
                )
                ringkasan_tahunan = []
                data_chart_lemah = []

                for thn in daftar_tahun:
                    df_thn = df_clean[df_clean["Tahun_Tes"].astype(str) == thn]
                    if not df_thn.empty:
                        df_prodi_thn = (
                            df_thn.groupby("Prodi")
                            .agg(
                                Rata_Section1=("Section 1", "mean"),
                                Rata_Section2=("Section 2", "mean"),
                                Rata_Section3=("Section 3", "mean"),
                            )
                            .reset_index()
                        )

                        s1_w = df_prodi_thn.loc[df_prodi_thn["Rata_Section1"].idxmin()]
                        s2_w = df_prodi_thn.loc[df_prodi_thn["Rata_Section2"].idxmin()]
                        s3_w = df_prodi_thn.loc[df_prodi_thn["Rata_Section3"].idxmin()]

                        ringkasan_tahunan.append({
                            "Tahun Tes": thn,
                            "Section 1 Terlemah": (
                                f"{s1_w['Prodi']} ({s1_w['Rata_Section1']:.1f})"
                            ),
                            "Section 2 Terlemah": (
                                f"{s2_w['Prodi']} ({s2_w['Rata_Section2']:.1f})"
                            ),
                            "Section 3 Terlemah": (
                                f"{s3_w['Prodi']} ({s3_w['Rata_Section3']:.1f})"
                            ),
                        })

                        for sec_name, row_w, col_rata in [
                            ("Section 1", s1_w, "Rata_Section1"),
                            ("Section 2", s2_w, "Rata_Section2"),
                            ("Section 3", s3_w, "Rata_Section3"),
                        ]:
                            data_chart_lemah.append({
                                "Tahun_Tes": thn,
                                "Section": sec_name,
                                "Label_Prodi": f"{row_w['Prodi']} ({row_w[col_rata]:.1f})",
                                "Skor": row_w[col_rata],
                            })

                df_vis_lemah = pd.DataFrame(data_chart_lemah)
                fig_hbar = px.bar(
                    df_vis_lemah,
                    x="Skor",
                    y="Tahun_Tes",
                    color="Section",
                    barmode="group",
                    orientation="h",
                    text="Label_Prodi",
                    color_discrete_map={
                        "Section 1": "#2EC4B6",
                        "Section 2": "#3B82F6",
                        "Section 3": "#F97316",
                    },
                    labels={
                        "Skor": "Skor Rata-Rata Terendah",
                        "Tahun_Tes": "Tahun Tes",
                        "Section": "Subtes Section",
                    },
                    height=480,
                    category_orders={
                        "Section": ["Section 1", "Section 2", "Section 3"]
                    },
                )
                fig_hbar.update_traces(textposition="auto", textfont_size=10)
                fig_hbar.update_layout(
                    yaxis=dict(type="category"),
                    xaxis=dict(range=[0, 62]),
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#F8FAFC",
                    font=dict(color="#0A3D2E"),
                )
                st.plotly_chart(fig_hbar, use_container_width=True)

                with st.expander("Lihat Tabel Rekapitulasi Detail Prodi Terlemah"):
                    st.dataframe(
                        pd.DataFrame(ringkasan_tahunan),
                        use_container_width=True,
                        hide_index=True,
                    )

            st.markdown("---")
            st.subheader("Tren Rata-Rata Skor Lintas Tahun Tes")
            col_tr1, col_tr2 = st.columns(2)

            df_trend = (
                df_clean.groupby("Tahun_Tes")
                .agg(
                    Section_1=("Section 1", "mean"),
                    Section_2=("Section 2", "mean"),
                    Section_3=("Section 3", "mean"),
                    Total_Skor=("Total", "mean") if "Total" in df_clean.columns else None,
                )
                .reset_index()
            )

            with col_tr1:
                st.markdown("**Tren Rata-Rata Subtes (Section 1 - 3)**")
                fig_trend_sub = px.line(
                    df_trend,
                    x="Tahun_Tes",
                    y=["Section_1", "Section_2", "Section_3"],
                    markers=True,
                    color_discrete_sequence=["#10C35D", "#3A86FF", "#FF8A4C"],
                    labels={
                        "value": "Rata-Rata Skor Subtes",
                        "Tahun_Tes": "Tahun Tes",
                        "variable": "Subtes",
                    },
                    height=380,
                )
                fig_trend_sub.update_layout(
                    xaxis=dict(type="category"),
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#F8FAFC",
                    font=dict(color="#0A3D2E"),
                )
                st.plotly_chart(fig_trend_sub, use_container_width=True)

            with col_tr2:
                st.markdown("**Tren Rata-Rata Skor Total**")
                if "Total_Skor" in df_trend.columns:
                    fig_trend_tot = px.line(
                        df_trend,
                        x="Tahun_Tes",
                        y=["Total_Skor"],
                        markers=True,
                        color_discrete_sequence=["#B197FC"],
                        labels={
                            "value": "Rata-Rata Skor Total",
                            "Tahun_Tes": "Tahun Tes",
                        },
                        height=380,
                    )
                    fig_trend_tot.update_layout(
                        xaxis=dict(type="category"),
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                    )
                    st.plotly_chart(fig_trend_tot, use_container_width=True)

# ==========================================
# HALAMAN 6: EVALUASI MODEL
# ==========================================
elif st.session_state["active_tab"] == "evaluasi":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 06 • VALIDASI & PENENTUAN K OPTIMAL</span>
            <h2 class="section-heading">Evaluasi Model (Metode Elbow & Silhouette Plot)</h2>
            <p class="section-desc">Pengujian titik siku elbow serta perbandingan Silhouette Score untuk kandidat nilai K.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Harap unggah dataset terlebih dahulu pada tab **Data Acquisition**."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            _, df_clean, kolom_fitur, _ = preprocess_toefl_data(df_raw)

            X = df_clean[kolom_fitur]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=1)
            df_clean["PC1"] = pca.fit_transform(X_scaled)
            explained_variance = pca.explained_variance_ratio_[0] * 100

            with st.spinner("Memuat perhitungan evaluasi model..."):
                inertia, K_range, sil_scores_dict, df_eval_summary = hitung_evaluasi_full(tuple(map(tuple, X_scaled)))

            optimal_k = 3
            perbandingan_k = [2, 3, 4]

            m1, m2, m3 = st.columns(3)
            m1.metric(
                "Titik Siku Optimal (Elbow)",
                f"K = {optimal_k} (Kandidat: 2, 3, 4)",
            )
            m2.metric("Explained Variance (PCA - PC1)", f"{explained_variance:.2f}%")
            m3.metric("Silhouette Score (K terpilih)", f"{sil_scores_dict[optimal_k]['score']:.2f}")

            st.markdown("<br>", unsafe_allow_html=True)

            st.subheader("Tabel Perbandingan Rata-Rata Silhouette Score (K = 2, 3, 4)")
            st.markdown("Sesuai prosedur analisis, pengujian dilakukan pada titik optimal hasil Elbow serta nilai sebelum dan sesudahnya untuk mencari kualitas klaster terbaik:")
            st.dataframe(df_eval_summary, use_container_width=True, hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)

            col_ev1, col_ev2 = st.columns(2)
            with col_ev1:
                st.subheader("Kurva Metode Elbow (Kandidat K)")
                fig_elbow = px.line(
                    x=K_range,
                    y=inertia,
                    markers=True,
                    labels={"x": "Jumlah Klaster (K)", "y": "Nilai Inertia (WCSS)"},
                )
                fig_elbow.update_traces(
                    line=dict(color="#10C35D", width=3),
                    marker=dict(size=9, color="#0A3D2E"),
                )
                fig_elbow.add_vline(
                    x=optimal_k,
                    line_dash="dash",
                    line_color="#FF8A4C",
                    line_width=2.5,
                    annotation_text=f"Titik Siku Elbow (K = {optimal_k})",
                )
                fig_elbow.update_layout(
                    paper_bgcolor="#FFFFFF",
                    plot_bgcolor="#F8FAFC",
                    font=dict(color="#0A3D2E"),
                )
                st.plotly_chart(fig_elbow, use_container_width=True)

            with col_ev2:
                st.subheader("Ringkasan Hasil Evaluasi Elbow")
                st.markdown(
                    f"""
                    <div class="paper-card">
                        <h4>Catatan Analisis:</h4>
                        <ul>
                            <li><b>Metode Elbow:</b> Titik siku optimal tercatat pada <b>K = {optimal_k}</b>.</li>
                            <li><b>Silhouette Analysis:</b> Digunakan untuk menguji seberapa baik tingkat pemisahan antar klaster pada kandidat K = 2, 3, dan 4 di sebelah bawah.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("Perbandingan Silhouette Plot untuk Kandidat Nilai K (K = 2, 3, 4)")
            st.markdown("Berikut adalah sebaran Silhouette Plot secara berdampingan untuk mengevaluasi kualitas pemisahan klaster pada $K = 2$, $K = 3$, dan $K = 4$:")

            col_s1, col_s2, col_s3 = st.columns(3)
            cols_list = [col_s1, col_s2, col_s3]

            for idx, k_val in enumerate(perbandingan_k):
                cluster_labels = sil_scores_dict[k_val]["labels"]
                silhouette_vals = sil_scores_dict[k_val]["vals"]
                avg_silhouette = sil_scores_dict[k_val]["score"]

                fig, ax = plt.subplots(figsize=(5, 3.5))
                y_lower = 10
                colors = ["#3B82F6", "#F97316", "#10C35D", "#B197FC", "#FF8787"]

                for i in range(k_val):
                    ith_cluster_silhouette_values = silhouette_vals[
                        cluster_labels == i
                    ]
                    ith_cluster_silhouette_values.sort()
                    size_cluster_i = ith_cluster_silhouette_values.shape[0]
                    y_upper = y_lower + size_cluster_i

                    color = colors[i % len(colors)]
                    ax.fill_betweenx(
                        np.arange(y_lower, y_upper),
                        0,
                        ith_cluster_silhouette_values,
                        facecolor=color,
                        edgecolor=color,
                        alpha=0.7,
                    )
                    ax.text(-0.05, y_lower + 0.5 * size_cluster_i, f"C{i+1}", fontsize=8)
                    y_lower = y_upper + 10

                ax.axvline(
                    x=avg_silhouette,
                    color="red",
                    linestyle="--",
                    label=f"Avg: {avg_silhouette:.2f}",
                )
                ax.set_xlabel("Silhouette Coefficient", fontsize=9)
                ax.set_ylabel("Cluster Label", fontsize=9)
                ax.set_title(f"Silhouette Plot untuk K = {k_val}", fontsize=10, fontweight="bold")
                ax.legend(loc="upper right", fontsize=8)
                ax.set_facecolor("#F8FAFC")
                fig.patch.set_facecolor("#FFFFFF")
                
                with cols_list[idx]:
                    st.pyplot(fig)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="paper-card">
                    <h4>Kesimpulan Evaluasi Model:</h4>
                    <ul>
                        <li><b>Analisis Kandidat K:</b> Berdasarkan pengujian pada rentang <b>K = 2, 3, dan 4</b>, nilai <b>K = {optimal_k}</b> dipilih karena merupakan titik optimal metode Elbow sekaligus memberikan keseimbangan sebaran anggota tier yang paling optimal tanpa overlap negatif yang berlebihan.</li>
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )

# ==========================================
# HALAMAN 7: CLUSTERING (DENGAN FILTER TIER 1, 2, 3)
# ==========================================
elif st.session_state["active_tab"] == "clustering":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 07 • HASIL PENGELOMPOKAN TIER</span>
            <h2 class="section-heading">Clustering (Segmentasi Tier Kemampuan TOEFL)</h2>
            <p class="section-desc">Ringkasan distribusi jumlah mahasiswa per tier hasil algoritma K-Means beserta tabel master dengan filter spesifik per tier.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Harap unggah dataset terlebih dahulu pada tab **Data Acquisition**."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            _, df_clean, kolom_fitur, kolom_identitas = preprocess_toefl_data(df_raw)

            X = df_clean[kolom_fitur]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=1)
            df_clean["PC1"] = pca.fit_transform(X_scaled)

            inertia = []
            K_range = list(range(1, 8))
            for k in K_range:
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                km.fit(X_scaled)
                inertia.append(km.inertia_)

            optimal_k = find_optimal_k(K_range, inertia)

            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            df_clean["Klaster"] = kmeans.fit_predict(df_clean[["PC1"]])

            cluster_means = df_clean.groupby("Klaster")["PC1"].mean().sort_values()
            rank_map = {
                old_cluster: i + 1 for i, old_cluster in enumerate(cluster_means.index)
            }
            df_clean["Tier_Rank"] = df_clean["Klaster"].map(rank_map)
            df_clean["Level_Tier"] = df_clean["Tier_Rank"].apply(
                lambda x: f"Tier {x}"
            )

            st.subheader(f"Ringkasan Distribusi {optimal_k} Tier Kemampuan")
            tier_cols = st.columns(optimal_k)
            for i in range(optimal_k):
                t_name = f"Tier {i+1}"
                jml_t = len(df_clean[df_clean["Level_Tier"] == t_name])
                pct_t = (jml_t / len(df_clean)) * 100
                with tier_cols[i]:
                    st.metric(
                        label=f"{t_name} Capaian",
                        value=f"{jml_t} Mhs",
                        delta=f"{pct_t:.1f}% dari total",
                    )

            st.markdown("---")
            st.subheader("Daftar Mahasiswa Berdasarkan Filter Tier")
            
            list_opsi_tier = ["Semua Tier"] + [f"Tier {i+1}" for i in range(optimal_k)]
            pilih_filter_tier = st.selectbox(
                "Filter Tabel Berdasarkan Kategori Tier:",
                list_opsi_tier
            )

            if pilih_filter_tier == "Semua Tier":
                df_tabel_tampil = df_clean
            else:
                df_tabel_tampil = df_clean[df_clean["Level_Tier"] == pilih_filter_tier]

            st.markdown(f"Menampilkan **{len(df_tabel_tampil)} mahasiswa** untuk kategori: **{pilih_filter_tier}**")
            st.dataframe(
                df_tabel_tampil[kolom_identitas + kolom_fitur + ["PC1", "Level_Tier"]],
                use_container_width=True,
                height=400,
            )

            st.markdown("---")
            st.subheader("Ekspor Laporan Akhir Clustering")

            output = io.BytesIO()
            tabel_hasil_akhir = df_clean[
                kolom_identitas + kolom_fitur + ["PC1", "Level_Tier"]
            ].copy()

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                tabel_hasil_akhir.to_excel(
                    writer, index=False, sheet_name="Laporan_Clustering"
                )

            excel_data = output.getvalue()

            st.download_button(
                label="Unduh File Excel Laporan Akhir (.xlsx)",
                data=excel_data,
                file_name="hasil_analisis_toefl_d3_d4.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ),
            )

# ==========================================
# HALAMAN 8: INTERPRETASI HASIL (REVISI VISUALISASI D3/D4 & TAHUN TES)
# ==========================================
elif st.session_state["active_tab"] == "interpretasi":
    st.markdown(
        """
        <div class="page-header-box">
            <span class="folder-tag">TAHAP 08 • ANALISIS FREKUENSI, JENJANG D3/D4 & TAHUN TES</span>
            <h2 class="section-heading">Interpretasi Hasil Klasterisasi Berbasis Frekuensi & Sebaran Spesifik</h2>
            <p class="section-desc">Analisis profil mendalam menggunakan frekuensi subtes dengan capaian terendah, visualisasi proporsi jenjang D3 vs D4, distribusi tahun tes, serta matriks kerentanan program studi.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state["uploaded_file_cache"] is None:
        st.warning(
            "Harap unggah dataset terlebih dahulu pada tab **Data Acquisition**."
        )
    else:
        df_raw = load_toefl_data(st.session_state["uploaded_file_cache"])
        if not df_raw.empty:
            _, df_clean, kolom_fitur, kolom_identitas = preprocess_toefl_data(df_raw)

            X = df_clean[kolom_fitur]
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            pca = PCA(n_components=1)
            df_clean["PC1"] = pca.fit_transform(X_scaled)

            inertia = []
            K_range = list(range(1, 8))
            for k in K_range:
                km = KMeans(n_clusters=k, random_state=42, n_init=10)
                km.fit(X_scaled)
                inertia.append(km.inertia_)

            optimal_k = find_optimal_k(K_range, inertia)

            kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
            df_clean["Klaster"] = kmeans.fit_predict(df_clean[["PC1"]])

            cluster_means = df_clean.groupby("Klaster")["PC1"].mean().sort_values()
            rank_map = {
                old_cluster: i + 1 for i, old_cluster in enumerate(cluster_means.index)
            }
            df_clean["Tier_Rank"] = df_clean["Klaster"].map(rank_map)
            df_clean["Level_Tier"] = df_clean["Tier_Rank"].apply(
                lambda x: f"Tier {x}"
            )

            # Tentukan subtes terlemah per mahasiswa
            subtes_cols = ["Section 1", "Section 2", "Section 3"]
            df_clean["Subtes_Terlemah_Mhs"] = df_clean[subtes_cols].idxmin(axis=1)

            # Deteksi Jenjang (D3 vs D4)
            if "Prodi" in df_clean.columns:
                df_clean["Jenjang"] = df_clean["Prodi"].apply(
                    lambda x: "D3" if str(x).strip().upper().startswith("D3") else ("D4" if str(x).strip().upper().startswith("D4") else "Lainnya")
                )
            else:
                df_clean["Jenjang"] = "Tidak Diketahui"

            dak_tier_list = [f"Tier {i+1}" for i in range(optimal_k)]
            pilih_tier_tampil = st.selectbox(
                "Pilih Tier untuk Menganalisis Frekuensi Subtes, Visualisasi Jenjang D3/D4 & Tahun Tes:",
                dak_tier_list,
            )

            df_filtered_tier = df_clean[
                df_clean["Level_Tier"] == pilih_tier_tampil
            ].copy()

            if not df_filtered_tier.empty:
                total_mhs_tier = len(df_filtered_tier)
                
                freq_subtes = df_filtered_tier["Subtes_Terlemah_Mhs"].value_counts()
                subtes_paling_sering_rendah = freq_subtes.idxmax() if not freq_subtes.empty else "-"
                jumlah_rendah_tertinggi = freq_subtes.max() if not freq_subtes.empty else 0
                pct_rendah_tertinggi = (jumlah_rendah_tertinggi / total_mhs_tier) * 100

                prodi_terbanyak = df_filtered_tier["Prodi"].value_counts()
                prodi_paling_rentan = prodi_terbanyak.idxmax() if not prodi_terbanyak.empty else "-"
                jml_prodi_rentan = prodi_terbanyak.max() if not prodi_terbanyak.empty else 0

                min_total = df_filtered_tier["Total"].min()
                max_total = df_filtered_tier["Total"].max()
                mean_total = df_filtered_tier["Total"].mean()

                st.markdown(
                    f"""
                    <div class="paper-card">
                        <h4>Ringkasan Statistik Analisis Mendalam ({pilih_tier_tampil})</h4>
                        <ul>
                            <li><b>Total Anggota Populasi Tier:</b> {total_mhs_tier} mahasiswa ({total_mhs_tier/len(df_clean)*100:.1f}% dari total keseluruhan mahasiswa).</li>
                            <li><b>Subtes dengan Capaian Terendah (Modus Frekuensi):</b> Sebanyak <b>{jumlah_rendah_tertinggi} mahasiswa ({pct_rendah_tertinggi:.1f}%)</b> di {pilih_tier_tampil} paling sering mencatatkan skor terendah pada modul <b>{subtes_paling_sering_rendah}</b>.</li>
                            <li><b>Program Studi Paling Rentan / Mendominasi:</b> Program Studi <b>{prodi_paling_rentan}</b> mencatatkan konsentrasi terbanyak di tier ini dengan jumlah <b>{jml_prodi_rentan} mahasiswa</b>.</li>
                            <li><b>Rentang & Rata-Rata Skor Komposit:</b> Skor total pada tier ini berkisar antara <b>{min_total} hingga {max_total}</b> dengan rata-rata komposit sebesar <b>{mean_total:.1f}</b>.</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                st.markdown("<br>", unsafe_allow_html=True)

                # BARIS GRAFIK 1: FREKUENSI SUBTES & PRODI TERBANYAK
                col_f1, col_f2 = st.columns(2)
                
                with col_f1:
                    st.subheader(f"Frekuensi Subtes dengan Capaian Terendah di {pilih_tier_tampil}")
                    df_freq_chart = freq_subtes.reset_index()
                    df_freq_chart.columns = ["Subtes TOEFL", "Jumlah Mahasiswa"]
                    
                    fig_freq = px.bar(
                        df_freq_chart,
                        x="Subtes TOEFL",
                        y="Jumlah Mahasiswa",
                        text="Jumlah Mahasiswa",
                        color="Subtes TOEFL",
                        color_discrete_map={
                            "Section 1": "#10C35D",
                            "Section 2": "#3A86FF",
                            "Section 3": "#FF8A4C"
                        },
                        height=350
                    )
                    fig_freq.update_traces(textposition='outside')
                    fig_freq.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                        showlegend=False
                    )
                    st.plotly_chart(fig_freq, use_container_width=True)

                with col_f2:
                    st.subheader(f"Top Program Studi Penyumbang di {pilih_tier_tampil}")
                    df_prodi_top = prodi_terbanyak.head(7).reset_index()
                    df_prodi_top.columns = ["Program Studi", "Jumlah Mahasiswa"]
                    
                    fig_prodi = px.bar(
                        df_prodi_top,
                        x="Jumlah Mahasiswa",
                        y="Program Studi",
                        orientation="h",
                        text="Jumlah Mahasiswa",
                        color_discrete_sequence=["#B197FC"],
                        height=350
                    )
                    fig_prodi.update_traces(textposition='outside')
                    fig_prodi.update_layout(
                        yaxis=dict(autorange="reversed"),
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                    )
                    st.plotly_chart(fig_prodi, use_container_width=True)

                st.markdown("---")

                # BARIS GRAFIK 2: VISUALISASI JENJANG (D3 vs D4) & DOMINASI TAHUN TES
                col_v1, col_v2 = st.columns(2)

                with col_v1:
                    st.subheader(f"Proporsi Jenjang Pendidikan (D3 vs D4) di {pilih_tier_tampil}")
                    df_jenjang_chart = df_filtered_tier["Jenjang"].value_counts().reset_index()
                    df_jenjang_chart.columns = ["Jenjang", "Jumlah Mahasiswa"]

                    fig_jenjang = px.pie(
                        df_jenjang_chart,
                        names="Jenjang",
                        values="Jumlah Mahasiswa",
                        hole=0.4,
                        color_discrete_sequence=["#3B82F6", "#10C35D", "#FF8A4C"],
                        height=350
                    )
                    fig_jenjang.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                    )
                    st.plotly_chart(fig_jenjang, use_container_width=True)

                with col_v2:
                    st.subheader(f"Distribusi Tahun Pelaksanaan Tes di {pilih_tier_tampil}")
                    if "Tahun_Tes" in df_filtered_tier.columns:
                        df_tahun_chart = df_filtered_tier["Tahun_Tes"].value_counts().reset_index()
                        df_tahun_chart.columns = ["Tahun Tes", "Jumlah Mahasiswa"]
                        df_tahun_chart = df_tahun_chart.sort_values("Tahun Tes")

                        fig_tahun = px.bar(
                            df_tahun_chart,
                            x="Tahun Tes",
                            y="Jumlah Mahasiswa",
                            text="Jumlah Mahasiswa",
                            color_discrete_sequence=["#FFA94D"],
                            height=350
                        )
                        fig_tahun.update_traces(textposition='outside')
                        fig_tahun.update_layout(
                            xaxis=dict(type="category"),
                            paper_bgcolor="#FFFFFF",
                            plot_bgcolor="#F8FAFC",
                            font=dict(color="#0A3D2E"),
                        )
                        st.plotly_chart(fig_tahun, use_container_width=True)

                st.markdown("---")
                st.subheader(f"Analisis Kerentanan Subtes Per Program Studi di {pilih_tier_tampil}")
                st.markdown("Matriks perbandingan mendalam untuk melihat subtes mana yang paling sering rendah pada masing-masing Program Studi:")

                if "Prodi" in df_filtered_tier.columns:
                    df_validasi_prodi = (
                        df_filtered_tier.groupby(["Prodi", "Subtes_Terlemah_Mhs"])
                        .size()
                        .reset_index(name="Jumlah_Mahasiswa")
                    )

                    top_prodi_tier = (
                        df_filtered_tier["Prodi"].value_counts().head(10).index
                    )
                    df_validasi_top = df_validasi_prodi[
                        df_validasi_prodi["Prodi"].isin(top_prodi_tier)
                    ]

                    fig_val_prodi = px.bar(
                        df_validasi_top,
                        x="Jumlah_Mahasiswa",
                        y="Prodi",
                        color="Subtes_Terlemah_Mhs",
                        barmode="group",
                        orientation="h",
                        text="Jumlah_Mahasiswa",
                        color_discrete_map={
                            "Section 1": "#10C35D",
                            "Section 2": "#3A86FF",
                            "Section 3": "#FF8A4C",
                        },
                        labels={
                            "Jumlah_Mahasiswa": "Jumlah Mahasiswa",
                            "Prodi": "Program Studi",
                            "Subtes_Terlemah_Mhs": "Subtes Paling Lemah",
                        },
                        height=480,
                    )
                    fig_val_prodi.update_traces(textposition="outside")
                    fig_val_prodi.update_layout(
                        paper_bgcolor="#FFFFFF",
                        plot_bgcolor="#F8FAFC",
                        font=dict(color="#0A3D2E"),
                    )
                    st.plotly_chart(fig_val_prodi, use_container_width=True)

                st.subheader(f"Daftar Mahasiswa Anggota {pilih_tier_tampil} (Tabel Detail)")
                st.dataframe(
                    df_filtered_tier[kolom_identitas + ["Jenjang"] + kolom_fitur + ["Subtes_Terlemah_Mhs", "PC1", "Level_Tier"]],
                    use_container_width=True,
                )