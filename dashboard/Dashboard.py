import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Housing Affordability Analysis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #FFFFFF !important; }
    .block-container { padding-top: 1.5rem !important; }

    /* All text defaults */
    html, body, [class*="css"] {
        color: #1A1A2E !important;
        font-family: 'Segoe UI', sans-serif !important;
    }

    /* Headers */
    h1, h2, h3, h4 {
        color: #1A1A2E !important;
        font-weight: 700 !important;
    }

    /* Paragraphs and list items */
    p, li, span, label, div {
        color: #1A1A2E !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1A1A2E !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    /* Metric cards */
    [data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: 1.5px solid #E0E0E0 !important;
        border-radius: 12px !important;
        padding: 18px !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08) !important;
    }
    [data-testid="metric-container"] label,
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"],
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #1A1A2E !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #28A745 !important;
        font-weight: 600 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #1A1A2E !important;
        font-weight: 600 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #2D87F0 !important;
        border-bottom: 3px solid #2D87F0 !important;
    }

    /* Dataframe */
    .stDataFrame {
        border-radius: 10px !important;
        overflow: hidden !important;
    }

    /* Selectbox and multiselect */
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #1A1A2E !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
    }

    /* Buttons */
    .stButton button {
        background: #2D87F0 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }

    /* Info / success / warning / error boxes */
    .stAlert {
        border-radius: 10px !important;
    }
    .stAlert p, .stAlert div {
        color: #1A1A2E !important;
        font-size: 0.92rem !important;
        line-height: 1.6 !important;
    }
    
    /* Fix for Plotly chart text visibility */
    .js-plotly-plot .main-svg text,
    .plotly .main-svg text,
    .plotly text,
    .gtitle,
    .xtitle,
    .ytitle,
    .legendtext,
    .hovertext text,
    .annotation-text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
    }
    
    /* Fix for axis tick labels */
    .xtick text, .ytick text {
        fill: #333333 !important;
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    /* Fix for legend text */
    .legend text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
        font-weight: 500 !important;
    }
    
    /* Fix for chart titles */
    .gtitle {
        fill: #1A1A2E !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    /* Fix for axis titles */
    .xtitle, .ytitle {
        fill: #1A1A2E !important;
        font-weight: 600 !important;
    }
    
    /* Fix for hover labels */
    .hoverlayer text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
    }
    
    /* Fix for Plotly modebar (toolbar icons) */
    .modebar {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    .modebar .icon {
        fill: #1A1A2E !important;
        stroke: #1A1A2E !important;
    }
    .modebar .icon:hover {
        fill: #2D87F0 !important;
        stroke: #2D87F0 !important;
    }
    
    /* Fix for hover tooltips */
    .hovertext text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
        font-weight: 500 !important;
    }
    .hoverlayer .hovertext {
        background-color: white !important;
        border: 1px solid #DDDDDD !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    .hoverlayer .hovertext text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
    }
    .hoverlayer .hovertext path {
        fill: white !important;
        stroke: #DDDDDD !important;
    }
    
    /* Fix for selection boxes and range sliders */
    .selection-box {
        stroke: #2D87F0 !important;
        fill: rgba(45, 135, 240, 0.1) !important;
    }
    .graticule {
        stroke: #EEEEEE !important;
    }
    .slider-handle {
        fill: #2D87F0 !important;
        stroke: #2D87F0 !important;
    }
    .slider-track {
        stroke: #CCCCCC !important;
    }
    .slider-track-inset {
        stroke: #2D87F0 !important;
    }
    
    /* Fix for annotation arrows */
    .annotation-arrow {
        fill: #1A1A2E !important;
        stroke: #1A1A2E !important;
    }
    .annotation-text {
        fill: #1A1A2E !important;
        color: #1A1A2E !important;
        font-weight: 500 !important;
    }
    
    /* Executive Summary Cards */
    .summary-card {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 4px solid;
        margin-bottom: 15px;
        transition: transform 0.2s;
    }
    .summary-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    .summary-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .summary-text {
        font-size: 0.9rem;
        line-height: 1.6;
        color: #555555 !important;
    }
    .kpi-highlight {
        font-size: 2rem;
        font-weight: 800;
        color: #2D87F0 !important;
        margin: 5px 0;
    }
</style>
""", unsafe_allow_html=True)

CITY_COLORS = {
    'Chicago, IL':     '#28A745',
    'Houston, TX':     '#B84FD8',
    'Los Angeles, CA': '#FF6B35',
    'Miami, FL':       '#FF3860',
    'New York, NY':    '#2D87F0',
}

@st.cache_data
def load_data():
    # Get the absolute path to the project root
    current_file = os.path.abspath(__file__)
    dashboard_folder = os.path.dirname(current_file)
    project_root = os.path.dirname(dashboard_folder)
    
    cities_long = pd.read_csv(os.path.join(project_root, 'data', 'cleaned', 'cities_long.csv'))
    annual_summary = pd.read_csv(os.path.join(project_root, 'data', 'cleaned', 'annual_summary.csv'))
    clustering = pd.read_csv(os.path.join(project_root, 'data', 'cleaned', 'clustering_results.csv'))
    forecasts = pd.read_csv(os.path.join(project_root, 'data', 'cleaned', 'forecasts_2025_2027.csv'))
    
    cities_long['date'] = pd.to_datetime(cities_long['date'])
    forecasts['date'] = pd.to_datetime(forecasts['date'])
    annual_summary.columns = (
        annual_summary.columns.str.strip().str.lower()
        .str.replace(r'[^a-z0-9_]', '_', regex=True)
        .str.strip('_'))
    return cities_long, annual_summary, clustering, forecasts

cities_long, annual_summary, clustering, forecasts = load_data()

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:20px 0;">
        <div style="font-size:3.5rem;">🏠</div>
        <h2 style="color:white !important; margin:8px 0 4px 0;
                   font-size:1.3rem;">Housing Analysis</h2>
        <p style="color:#AAAAAA !important; font-size:0.8rem; margin:0;">
            Data Analytics Portfolio Project
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="color:white!important;"><b>👤 Author:</b> Yaw Assensoh Opoku</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:white!important;"><b>📅 Period:</b> 2015 – 2024</p>', unsafe_allow_html=True)
    st.markdown('<p style="color:white!important;"><b>🏙️ Cities:</b> NY · LA · Chicago · Houston · Miami</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="color:#AAAAAA!important; font-size:0.85rem;"><b style="color:white!important;">🛠️ Tools Used:</b><br>Excel · PostgreSQL · Python<br>Scikit-learn · Statsmodels<br>Plotly · Folium · Streamlit</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="color:#888888!important; font-size:0.75rem;">📊 Data Sources:<br>Zillow Research & FRED</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<p style="color:#888888!important; font-size:0.75rem;">📁 <b>Navigation:</b><br>Use the tabs above to explore:<br>📊 EDA · 🔵 Clustering · 📈 Time Series<br>📐 Regression · 🗺️ Geospatial</p>', unsafe_allow_html=True)

# ── HEADER (First) ────────────────────────────────────────────
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:40px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 6px 24px rgba(0,0,0,0.08);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:2.3rem; margin:0;
              font-weight:800; line-height:1.2;'>
        🏠 US Housing Affordability Analysis
    </p>
    <p style='color:#4A4A5A!important; font-size:1rem;
              margin:14px 0 18px 0; line-height:1.7; max-width:750px;'>
        A 3-phase data analytics project examining the US housing affordability
        crisis across 5 major cities from 2015 to 2024 — using Excel for
        data exploration, SQL for market intelligence, and Python for
        machine learning and forecasting.
    </p>
    <div style='display:flex; gap:12px; flex-wrap:wrap;'>
        <span style='background:rgba(45,135,240,0.12); color:#2D87F0!important;
                     padding:5px 15px; border-radius:20px; font-size:0.82rem;
                     font-weight:600; border:1px solid rgba(45,135,240,0.3);'>
            📊 600 Monthly Observations
        </span>
        <span style='background:rgba(45,135,240,0.12); color:#2D87F0!important;
                     padding:5px 15px; border-radius:20px; font-size:0.82rem;
                     font-weight:600; border:1px solid rgba(45,135,240,0.3);'>
            🏙️ 5 Major US Cities
        </span>
        <span style='background:rgba(45,135,240,0.12); color:#2D87F0!important;
                     padding:5px 15px; border-radius:20px; font-size:0.82rem;
                     font-weight:600; border:1px solid rgba(45,135,240,0.3);'>
            📅 10 Years of Data
        </span>
        <span style='background:rgba(45,135,240,0.12); color:#2D87F0!important;
                     padding:5px 15px; border-radius:20px; font-size:0.82rem;
                     font-weight:600; border:1px solid rgba(45,135,240,0.3);'>
            🔬 5 Analytical Methods
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── EXECUTIVE SUMMARY SECTION ─────────────────────────────────
st.markdown("## 📋 Executive Summary")

# Get latest data for summary
latest = annual_summary[annual_summary['year'] == 2024]
la_ai = latest[latest['city'] == 'Los Angeles, CA']['affordability_index'].values[0]
ny_ai = latest[latest['city'] == 'New York, NY']['affordability_index'].values[0]
miami_ai = latest[latest['city'] == 'Miami, FL']['affordability_index'].values[0]
chicago_ai = latest[latest['city'] == 'Chicago, IL']['affordability_index'].values[0]
houston_ai = latest[latest['city'] == 'Houston, TX']['affordability_index'].values[0]

# Summary cards row
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="summary-card" style="border-left-color: #DC3545;">
        <div class="summary-title">🔴 The Crisis</div>
        <div class="summary-text">
            Los Angeles and New York have been unaffordable since before 2015. 
            LA's affordability index hit <b>{la_ai:.2f}</b> in 2024 — a household needs 
            <b>$200K+ annual income</b> to afford a median home.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="summary-card" style="border-left-color: #28A745;">
        <div class="summary-title">🟢 The Outliers</div>
        <div class="summary-text">
            Chicago ({chicago_ai:.2f}) and Houston ({houston_ai:.2f}) remained <b>affordable</b> throughout 
            the entire 10-year period. Proving major metros CAN stay affordable 
            with the right land use policies.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="summary-card" style="border-left-color: #FF6B35;">
        <div class="summary-title">🟡 The Transition</div>
        <div class="summary-text">
            Miami crossed the affordability threshold in 2022 (now {miami_ai:.2f}) 
            and is the <b>fastest deteriorating</b> market in the dataset. 
            A cautionary tale of post-COVID migration pressure.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── KEY TAKEAWAYS SECTION ────────────────────────────────────
st.markdown("## 💡 Key Takeaways")

takeaways = st.columns(4)

with takeaways[0]:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:#F8F9FA; border-radius:10px;">
        <div style="font-size:2rem;">📈</div>
        <div style="font-size:1.3rem; font-weight:800; color:#2D87F0;">+$400K</div>
        <div style="font-size:0.85rem;">LA home values grew $400K while incomes grew only $11K</div>
    </div>
    """, unsafe_allow_html=True)

with takeaways[1]:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:#F8F9FA; border-radius:10px;">
        <div style="font-size:2rem;">🎯</div>
        <div style="font-size:1.3rem; font-weight:800; color:#2D87F0;">3 Clusters</div>
        <div style="font-size:0.85rem;">K-Means confirmed 3 distinct market segments matching SQL risk classifications</div>
    </div>
    """, unsafe_allow_html=True)

with takeaways[2]:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:#F8F9FA; border-radius:10px;">
        <div style="font-size:2rem;">🔮</div>
        <div style="font-size:1.3rem; font-weight:800; color:#2D87F0;">$990K</div>
        <div style="font-size:0.85rem;">LA home values projected to approach $1M by 2027</div>
    </div>
    """, unsafe_allow_html=True)

with takeaways[3]:
    st.markdown("""
    <div style="text-align:center; padding:15px; background:#F8F9FA; border-radius:10px;">
        <div style="font-size:2rem;">🏗️</div>
        <div style="font-size:1.3rem; font-weight:800; color:#2D87F0;">Supply</div>
        <div style="font-size:0.85rem;">Regression confirms: you cannot solve a supply problem with demand-side subsidies</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── KPI Cards ─────────────────────────────────────────────────
st.markdown("### 📊 2024 Market Snapshot")
st.markdown('<p style="color:#555555; font-size:0.92rem; margin-bottom:15px;">The affordability index measures home price relative to income. A score of 1.0 is the threshold — anything above means housing costs more than a household earning the median income can comfortably afford.</p>', unsafe_allow_html=True)

city_order = [
    ('Los Angeles, CA', '🔴'),
    ('New York, NY',    '🟡'),
    ('Miami, FL',       '🟡'),
    ('Chicago, IL',     '🟢'),
    ('Houston, TX',     '🟢'),
]
cols = st.columns(5)

for (city, emoji), col in zip(city_order, cols):
    row = latest[latest['city'] == city]
    if len(row) == 0:
        continue
    ai    = float(row['affordability_index'].values[0])
    hv    = float(row['avg_home_value'].values[0])
    risk  = ('HIGH RISK'     if ai > 1.5 else
             'MODERATE RISK' if ai > 1.0 else 'LOW RISK')
    color = ('#DC3545' if ai > 1.5 else
             '#FFC107' if ai > 1.0 else '#28A745')
    short = city.split(',')[0]
    with col:
        st.markdown(f"""
        <div style="background:#FFFFFF; padding:20px 15px;
                    border-radius:12px; border-left:5px solid {color};
                    box-shadow:0 3px 12px rgba(0,0,0,0.09);
                    border: 1px solid #EEEEEE;
                    border-left: 5px solid {color};">
            <p style="margin:0 0 4px 0; font-size:0.8rem;
                      color:#777777 !important; font-weight:600;">
                {emoji} {short}
            </p>
            <h2 style="margin:0 0 4px 0; color:{color} !important;
                       font-size:2.2rem; font-weight:900;
                       line-height:1;">
                {ai:.2f}
            </h2>
            <p style="margin:0 0 6px 0; font-size:0.72rem;
                      font-weight:700; color:{color} !important;
                      letter-spacing:0.5px;">
                {risk}
            </p>
            <p style="margin:0; font-size:0.78rem;
                      color:#444444 !important; font-weight:500;">
                Avg: ${hv:,.0f}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Risk Summary Table ────────────────────────────────────────
st.markdown("### 🚨 Market Risk Summary")
st.markdown('<p style="color:#555555; font-size:0.92rem; margin-bottom:15px;">A full comparison of all 5 cities across key housing metrics for 2024. The risk level is determined by the affordability index threshold.</p>', unsafe_allow_html=True)

risk_rows = []
for city, _ in city_order:
    row = latest[latest['city'] == city]
    if len(row) == 0:
        continue
    ai   = float(row['affordability_index'].values[0])
    hv   = float(row['avg_home_value'].values[0])
    rent = float(row['avg_monthly_rent'].values[0])
    row2015 = annual_summary[
        (annual_summary['city'] == city) &
        (annual_summary['year'] == 2015)]
    hv2015  = float(row2015['avg_home_value'].values[0]) if len(row2015) > 0 else hv
    growth  = ((hv - hv2015) / hv2015) * 100
    cl_row  = clustering[clustering['city'] == city]
    cluster = cl_row['cluster_label'].values[0] if len(cl_row) > 0 else 'N/A'
    risk_rows.append({
        'City':                city.split(',')[0],
        'Avg Home Value':      f'${hv:,.0f}',
        'Monthly Rent':        f'${rent:,.0f}',
        'Affordability Index': round(ai, 3),
        '10yr Growth':         f'{growth:.1f}%',
        'Cluster':             cluster,
        'Risk Level':          ('🔴 HIGH RISK'     if ai > 1.5 else
                                '🟡 MODERATE RISK' if ai > 1.0 else
                                '🟢 LOW RISK'),
    })

risk_df = pd.DataFrame(risk_rows)
st.dataframe(risk_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Affordability Trend Chart ─────────────────────────────────
st.markdown("### 📈 Affordability Index Trends (2015–2024)")
st.markdown('<p style="color:#555555; font-size:0.92rem; margin-bottom:15px;">This chart shows how the affordability index changed over time. The black dashed line at 1.0 is the affordability threshold — cities above it are considered unaffordable for median income households. The red shaded area marks the COVID-19 period when all cities deteriorated sharply.</p>', unsafe_allow_html=True)

yearly = (cities_long.groupby(['city', 'year'])
          .agg(affordability_index=('affordability_index', 'mean'))
          .reset_index())

fig = px.line(
    yearly, x='year', y='affordability_index',
    color='city', color_discrete_map=CITY_COLORS,
    markers=True,
    labels={'year': 'Year',
            'affordability_index': 'Affordability Index',
            'city': 'City'}
)
fig.add_hline(
    y=1.0, line_dash='dash', line_color='black', opacity=0.6,
    annotation_text='Affordable Threshold (1.0)',
    annotation_position='bottom right',
    annotation_font_color='#333333'
)
fig.add_vrect(
    x0=2020, x1=2022, fillcolor='red', opacity=0.06,
    annotation_text='COVID-19 Period',
    annotation_position='top left',
    annotation_font_color='#CC0000'
)
fig.update_layout(
    height=440, plot_bgcolor='white', paper_bgcolor='white',
    font=dict(family='Segoe UI', color='#1A1A2E', size=12),
    xaxis=dict(showgrid=True, gridcolor='#F0F0F0',
               tickmode='linear', dtick=1, title='Year',
               tickfont=dict(color='#333333')),
    yaxis=dict(showgrid=True, gridcolor='#F0F0F0',
               title='Affordability Index',
               tickfont=dict(color='#333333')),
    legend=dict(orientation='h', yanchor='bottom',
                y=1.02, xanchor='right', x=1,
                font=dict(color='#1A1A2E'))
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── Project Structure ─────────────────────────────────────────
st.markdown("### 📁 Project Structure")
st.markdown('<p style="color:#555555; font-size:0.92rem; margin-bottom:20px;">This project is structured in 3 phases, each using a different tool and analytical method to examine the housing affordability crisis from a different angle.</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div style="background:#FFFFFF; padding:22px; border-radius:12px;
                border-top:5px solid #2D87F0;
                box-shadow:0 3px 12px rgba(0,0,0,0.08);
                border:1px solid #E8E8E8; border-top:5px solid #2D87F0;">
        <h4 style="color:#2D87F0 !important; margin:0 0 10px 0;
                   font-size:1rem;">✅ Phase 1 — Excel Dashboard</h4>
        <p style="color:#444444 !important; font-size:0.88rem;
                  margin:0 0 10px 0; line-height:1.6;">
            Built an affordability index tracking home prices
            relative to income across 5 cities. Cleaned raw
            Zillow and FRED data, applied VLOOKUP and
            PivotTables, and created trend visualisations.
        </p>
        <p style="margin:0; font-size:0.82rem; color:#666 !important;">
            <b>Tool:</b> Microsoft Excel
        </p>
    </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown("""
    <div style="background:#FFFFFF; padding:22px; border-radius:12px;
                border-top:5px solid #28A745;
                box-shadow:0 3px 12px rgba(0,0,0,0.08);
                border:1px solid #E8E8E8; border-top:5px solid #28A745;">
        <h4 style="color:#28A745 !important; margin:0 0 10px 0;
                   font-size:1rem;">✅ Phase 2 — SQL Analysis</h4>
        <p style="color:#444444 !important; font-size:0.88rem;
                  margin:0 0 10px 0; line-height:1.6;">
            Wrote 10 SQL queries to rank cities, calculate
            year-over-year changes, identify when cities
            crossed the affordability threshold, and classify
            markets by risk level.
        </p>
        <p style="margin:0; font-size:0.82rem; color:#666 !important;">
            <b>Tool:</b> PostgreSQL 14
        </p>
    </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown("""
    <div style="background:#FFFFFF; padding:22px; border-radius:12px;
                border-top:5px solid #FF6B35;
                box-shadow:0 3px 12px rgba(0,0,0,0.08);
                border:1px solid #E8E8E8; border-top:5px solid #FF6B35;">
        <h4 style="color:#FF6B35 !important; margin:0 0 10px 0;
                   font-size:1rem;">✅ Phase 3 — Python Analysis</h4>
        <p style="color:#444444 !important; font-size:0.88rem;
                  margin:0 0 10px 0; line-height:1.6;">
            5 Python notebooks covering EDA, K-Means
            clustering, ARIMA forecasting, regression
            analysis, and interactive geospatial maps
            using Folium and Plotly.
        </p>
        <p style="margin:0; font-size:0.82rem; color:#666 !important;">
            <b>Tools:</b> Python · Scikit-learn · Plotly
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; padding:20px; color:#888888 !important;
            font-size:0.82rem; border-top:2px solid #EEEEEE;
            margin-top:10px; background:#FAFAFA;
            border-radius:0 0 12px 12px;">
    🏠 <b>Housing Affordability Analysis</b> &nbsp;·&nbsp;
    Yaw Assensoh Opoku &nbsp;·&nbsp;
    Data: Zillow Research & FRED &nbsp;·&nbsp;
    Built with Python & Streamlit
</div>
""", unsafe_allow_html=True)