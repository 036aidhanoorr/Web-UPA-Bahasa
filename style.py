import pandas as pd
import streamlit as st


def apply_custom_theme(page_bg="#FAFDFB"):
  st.markdown(
      f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&display=swap');

        /* Sembunyikan Sidebar & Header Bawaan Streamlit */
        [data-testid="stSidebar"], [data-testid="collapsedControl"], header[data-testid="stHeader"] {{
            display: none !important;
        }}

        /* Background Utama Halaman Disamakan Jadi #FAFDFB */
        .stApp {{
            background-color: #FAFDFB !important;
            background-image: 
                linear-gradient(to right, rgba(10, 61, 46, 0.05) 1px, transparent 1px),
                linear-gradient(to bottom, rgba(10, 61, 46, 0.05) 1px, transparent 1px) !important;
            background-size: 28px 28px !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            color: #0F2922 !important;
        }}

        .block-container {{
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2.2rem !important;
            padding-right: 2.2rem !important;
            max-width: 100% !important;
        }}

        /* =========================================
           WADAH STACKED FOLDER TABS KE SAMPING
           ========================================= */
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] {{
            background-color: #1A3026 !important;
            margin-left: -2.2rem !important;
            margin-right: -2.2rem !important;
            margin-top: -1.5rem !important;
            padding: 14px 24px 0px 24px !important;
            gap: 6px !important;
            border-bottom: 4px solid #0A3D2E !important;
            align-items: flex-end !important;
            overflow-x: auto;
        }}

        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] button {{
            border-radius: 14px 14px 0px 0px !important;
            border: 2px solid #0A3D2E !important;
            border-bottom: none !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            font-weight: 800 !important;
            font-size: 0.76rem !important;
            padding: 0.55rem 0.3rem 0.75rem 0.3rem !important;
            min-height: 44px !important;
            line-height: 1.15 !important;
            transition: all 0.15s ease !important;
        }}

        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(1) button {{ background-color: #B7F0CE !important; color: #0A3D2E !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(2) button {{ background-color: #FFE066 !important; color: #5F4C00 !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(3) button {{ background-color: #FFA94D !important; color: #5F2C00 !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(4) button {{ background-color: #B197FC !important; color: #3B1E85 !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(5) button {{ background-color: #FF8787 !important; color: #5A1A1A !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(6) button {{ background-color: #74C0FC !important; color: #0B3C65 !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(7) button {{ background-color: #63E6BE !important; color: #0B4C33 !important; }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] > div:nth-child(8) button {{ background-color: #38D9A9 !important; color: #08412B !important; }}

        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] button[kind="secondary"] {{
            opacity: 0.82;
            transform: translateY(6px);
            box-shadow: inset 0 4px 6px rgba(0,0,0,0.15);
        }}
        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {{
            opacity: 1;
            transform: translateY(2px);
        }}

        div[data-testid="stElementContainer"]:has(.nav-folder-anchor) + div[data-testid="stHorizontalBlock"] button[kind="primary"] {{
            background-color: #B7F0CE !important;
            color: #0A3D2E !important;
            transform: translateY(0px) scaleY(1.08);
            box-shadow: 0 -6px 12px rgba(0,0,0,0.2) !important;
            z-index: 30 !important;
            border-top: 3px solid #0A3D2E !important;
            filter: brightness(1.05);
        }}

        .cover-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 1rem 0.5rem 0.2rem 0.5rem;
            width: 100%;
        }}

        .cover-badge {{
            display: inline-block;
            background-color: #FF8A4C;
            color: #0A3D2E !important;
            font-weight: 800;
            font-size: 0.74rem;
            letter-spacing: 0.06em;
            padding: 4px 14px;
            border-radius: 7px;
            border: 2px solid #0A3D2E;
            box-shadow: 3px 3px 0px #0A3D2E;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
        }}

        .cover-title {{
            font-family: 'Playfair Display', serif;
            font-size: 1.9rem;
            font-weight: 700;
            color: #0A3D2E !important;
            line-height: 1.3;
            max-width: 880px;
            margin: 0 auto 0.8rem auto;
            text-align: center !important;
        }}

        .highlight-mint {{
            background-color: #B7F0CE;
            color: #0A3D2E !important;
            padding: 0px 8px;
            border-radius: 7px;
            border: 2px solid #0A3D2E;
            display: inline-block;
        }}

        .highlight-purple {{
            background-color: #D6C7FF;
            color: #0A3D2E !important;
            padding: 0px 8px;
            border-radius: 7px;
            border: 2px solid #0A3D2E;
            display: inline-block;
        }}

        .flow-section-title {{
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.09em;
            color: #0A3D2E !important;
            margin-top: 0.1rem !important;
            margin-bottom: 0.55rem;
            text-align: center;
        }}

        .flow-grid-top {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 10px;
            width: 100%;
            max-width: 1100px;
            margin: 0 auto 10px auto;
        }}

        .flow-grid-bottom {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            width: 100%;
            max-width: 820px;
            margin: 0 auto;
        }}

        @media (max-width: 900px) {{
            .flow-grid-top, .flow-grid-bottom {{
                grid-template-columns: 1fr;
            }}
        }}

        .flow-card {{
            background-color: #FFFFFF;
            border: 2px solid #0A3D2E;
            border-radius: 12px;
            padding: 0.65rem 0.85rem;
            text-align: left;
            box-shadow: 3px 3px 0px #0A3D2E;
        }}

        .flow-card-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3px;
        }}

        .flow-step-num {{
            font-size: 0.64rem;
            font-weight: 800;
            color: #0A3D2E !important;
            border: 1.5px solid #0A3D2E;
            border-radius: 5px;
            padding: 1px 5px;
        }}

        .flow-step-name {{
            font-size: 0.84rem;
            font-weight: 800;
            color: #0A3D2E !important;
            margin: 0;
        }}

        .flow-step-desc {{
            font-size: 0.72rem;
            color: #2D4A3E !important;
            margin: 2px 0 0 0;
            line-height: 1.3;
        }}

        .page-header-box {{
            padding-top: 1rem;
            margin-bottom: 1rem;
            border-bottom: 2px dashed rgba(10, 61, 46, 0.22);
            padding-bottom: 0.7rem;
        }}

        .folder-tag {{
            display: inline-block;
            background-color: #FFFFFF;
            color: #0A3D2E !important;
            border: 1.5px solid #0A3D2E;
            border-radius: 6px;
            padding: 2px 10px;
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}

        .section-heading {{
            font-family: 'Playfair Display', serif;
            font-size: 1.65rem;
            font-weight: 700;
            color: #0A3D2E !important;
            margin: 0 0 0.2rem 0;
        }}

        .section-desc {{
            font-size: 0.88rem;
            color: #1E3F33 !important;
            margin: 0;
        }}

        .paper-card {{
            background-color: #FFFFFF;
            border: 2px solid #0A3D2E;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.8rem;
            box-shadow: 4px 4px 0px #0A3D2E;
            color: #0F2922 !important;
        }}

        .paper-card-accent {{
            background-color: #FFFFFF;
            border: 2px solid #0A3D2E;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.8rem;
            box-shadow: 4px 4px 0px #FF8A4C;
            color: #0F2922 !important;
        }}

        .paper-card h4, .paper-card-accent h4 {{
            color: #0A3D2E !important;
            font-weight: 800 !important;
            margin-top: 0 !important;
            font-size: 1.02rem !important;
        }}

        .paper-card p, .paper-card li, .paper-card-accent p, .paper-card-accent li {{
            color: #18362B !important;
            font-size: 0.88rem !important;
        }}

        h1, h2, h3, h4, p, li, label, span {{
            color: #0F2922;
        }}

        [data-testid="stMetric"] {{
            background-color: #FFFFFF !important;
            border: 2px solid #0A3D2E !important;
            border-radius: 13px !important;
            padding: 0.7rem 0.9rem !important;
            box-shadow: 4px 4px 0px #0A3D2E !important;
        }}

        [data-testid="stMetricLabel"] p {{
            color: #1E4D3B !important;
            font-weight: 700 !important;
        }}

        [data-testid="stMetricValue"] div {{
            color: #0A3D2E !important;
            font-weight: 800 !important;
        }}

        [data-testid="stAlert"] {{
            background-color: #FFFFFF !important;
            border: 2px solid #0A3D2E !important;
            border-radius: 13px !important;
            color: #0F2922 !important;
            box-shadow: 4px 4px 0px #FF8A4C !important;
        }}

        [data-testid="stFileUploader"] {{
            background-color: #FFFFFF !important;
            border: 2.5px dashed #0A3D2E !important;
            border-radius: 14px !important;
            padding: 0.8rem !important;
        }}

        [data-testid="stExpander"] {{
            background-color: #FFFFFF !important;
            border: 2px solid #0A3D2E !important;
            border-radius: 13px !important;
            box-shadow: 3px 3px 0px #0A3D2E !important;
        }}

        .stDownloadButton button {{
            background-color: #10C35D !important;
            color: #FFFFFF !important;
            border: 2px solid #0A3D2E !important;
            border-radius: 11px !important;
            font-weight: 700 !important;
            box-shadow: 4px 4px 0px #0A3D2E !important;
            padding: 0.6rem 1.4rem !important;
        }}

        .stDownloadButton button span {{
            color: #FFFFFF !important;
        }}

        .stDownloadButton button:hover {{
            background-color: #0DAA50 !important;
            transform: translate(-1px, -1px);
        }}
    </style>
    """,
      unsafe_allow_html=True,
  )


def preprocess_toefl_data(df_raw):
  df = df_raw.copy()
  df = df.loc[:, ~df.columns.str.contains("^Unnamed", na=False)]
  df = df.dropna(how="all")
  df = df.loc[:, ~df.columns.duplicated()]

  for col in ["Section 1", "Section 2", "Section 3", "Total"]:
    if col in df.columns:
      df[col] = pd.to_numeric(
          df[col].astype(str).str.replace(",", "."), errors="coerce"
      )

  # KOLOM "Total" IKUT DIMASUKKAN SEBAGAI FITUR UTAMA PEMODELAN
  kolom_fitur = [
      c
      for c in ["Section 1", "Section 2", "Section 3", "Total"]
      if c in df.columns
  ]

  all_cols_lower = {str(c).lower(): c for c in df.columns}
  kolom_identitas = []

  for target in ["no", "nim", "nama", "prodi", "tahun_tes"]:
    if target in all_cols_lower:
      orig_col_name = all_cols_lower[target]
      if (
          orig_col_name not in kolom_fitur
          and orig_col_name not in kolom_identitas
      ):
        kolom_identitas.append(orig_col_name)

  df_clean = df.dropna(subset=kolom_fitur).copy()

  kolom_dipertahankan = kolom_identitas + kolom_fitur
  df_clean = df_clean[
      [col for col in kolom_dipertahankan if col in df_clean.columns]
  ]

  return df, df_clean, kolom_fitur, kolom_identitas