import streamlit as st
from datetime import date, timedelta
from generate_pdf import generate_offer_letter
from templates import TEAM_LIST

st.set_page_config(
    page_title="Tericsoft – Offer Letter Generator",
    page_icon="📄",
    layout="centered",
)

st.markdown("""
<style>
  .stApp { background-color: #f0f2f6; }
  .header-bar {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b3a5c 100%);
    border-radius: 12px;
    padding: 1.8rem 2rem;
    margin-bottom: 2rem;
  }
  .header-bar h1 { color: #fff; font-size: 1.6rem; margin: 0; font-weight: 700; }
  .header-bar p  { color: #90afc5; margin: 0.3rem 0 0; font-size: 0.88rem; }
  .req { color: #c0392b; font-size: 0.8rem; margin-bottom: 1rem; display: block; }
  .section-label {
    font-size: 0.75rem; font-weight: 700; letter-spacing: 0.09em;
    text-transform: uppercase; color: #1b3a5c;
    margin: 1.4rem 0 0.6rem;
  }
  .stTextInput > label, .stDateInput > label,
  .stSelectbox > label, .stRadio > label {
    font-weight: 600 !important; color: #2d3748 !important; font-size: 0.88rem !important;
  }
  div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #1b3a5c, #2e6da4) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    padding: 0.7rem 0 !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important; margin-top: 1rem;
  }
  div[data-testid="stDownloadButton"] > button {
    background: #27ae60 !important; color: #fff !important; border: none !important;
    border-radius: 8px !important; font-size: 1rem !important;
    font-weight: 700 !important; width: 100% !important; padding: 0.7rem 0 !important;
  }
  hr { margin: 1rem 0 !important; border-color: #e2e8f0 !important; }
  .stRadio > div label p { color: #1a202c !important; }
  .stRadio div[role="radiogroup"] label { color: #1a202c !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-bar">
  <h1>📄 Offer Letter Generator</h1>
  <p>Tericsoft Technology Solutions Pvt. Ltd. — Internal HR Tool</p>
</div>
""", unsafe_allow_html=True)

with st.form("offer_form"):

    st.markdown('<span class="req">* Required fields</span>', unsafe_allow_html=True)

    # ── Employment type ───────────────────────────────────────────────────────
    employment_type = st.radio(
        "Employment Type *",
        ["Internship", "Full-Time"],
        horizontal=True,
    )

    st.markdown("---")

    # ── Candidate details ─────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Candidate Details</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        candidate_name = st.text_input("First Name *", placeholder="e.g. Anirudh")
    with col2:
        candidate_full = st.text_input("Full Name *", placeholder="e.g. Kotla Anirudh")

    col3, col4 = st.columns(2)
    with col3:
        role = st.text_input("Role / Position *", placeholder="e.g. AI Intern")
    with col4:
        reporting_to = st.text_input("Reporting To *", placeholder="e.g. Muqtadar")

    st.markdown("---")

    # ── Role & schedule ───────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Role & Schedule</p>', unsafe_allow_html=True)

    col5, col6 = st.columns(2)
    with col5:
        team = st.selectbox("Team / Department *", TEAM_LIST)
    with col6:
        joining_date = st.date_input(
            "Date of Joining *",
            value=date.today() + timedelta(days=7),
            min_value=date.today(),
        )

    # Duration — plain number input in months, auto-converts to years
    dur_col1, dur_col2 = st.columns([2, 3])
    with dur_col1:
        custom_months = st.number_input(
            "Duration (months) *", min_value=1, max_value=120, value=3, step=1,
            help="Enter duration in months. 12 → 1 year, 18 → 1 year and 6 months, etc."
        )
    with dur_col2:
        if custom_months % 12 == 0:
            duration = f"{custom_months // 12} year{'s' if custom_months // 12 > 1 else ''}"
        elif custom_months > 12:
            yrs = custom_months // 12
            mos = custom_months % 12
            duration = f"{yrs} year{'s' if yrs > 1 else ''} and {mos} month{'s' if mos > 1 else ''}"
        else:
            duration = f"{custom_months} month{'s' if custom_months > 1 else ''}"
        st.markdown(f"<br><span style='color:#1b3a5c;font-weight:600;font-size:0.95rem'>→ {duration}</span>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Offer date ────────────────────────────────────────────────────────────
    st.markdown('<p class="section-label">Offer Details</p>', unsafe_allow_html=True)
    offer_date = st.date_input("Offer Letter Date", value=date.today())

    submitted = st.form_submit_button("✨  Generate Offer Letter PDF")

# ── Validation & generation ───────────────────────────────────────────────────
if submitted:
    errors = []
    if not candidate_name.strip(): errors.append("First Name is required.")
    if not candidate_full.strip(): errors.append("Full Name is required.")
    if not role.strip():           errors.append("Role / Position is required.")
    if not reporting_to.strip():   errors.append("Reporting To is required.")
    if not duration.strip():       errors.append("Duration is required.")

    if errors:
        for e in errors:
            st.error(f"⚠️  {e}")
    else:
        with st.spinner("Generating offer letter…"):
            pdf_bytes = generate_offer_letter(
                candidate_name      = candidate_name.strip(),
                role                = role.strip(),
                reporting_to        = reporting_to.strip(),
                joining_date        = joining_date,
                team                = team,
                employment_type     = employment_type,
                duration            = duration.strip(),
                offer_date          = offer_date,
                candidate_full_name = candidate_full.strip(),
            )

        st.success("✅  Offer letter generated successfully!")
        fname = f"Offer_Letter_{candidate_full.strip().replace(' ', '_')}.pdf"
        st.download_button(
            label     = "⬇️  Download Offer Letter PDF",
            data      = pdf_bytes,
            file_name = fname,
            mime      = "application/pdf",
        )