import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Trends Analysis",
    page_icon="📈",
    layout="wide"
)

# Apply same styling
st.markdown("""
<style>
    .stApp { background-color: #FFFFFF !important; }
    .block-container { padding-top: 1.5rem !important; }
    html, body, [class*="css"] {
        color: #1A1A2E !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    h1, h2, h3, h4 {
        color: #1A1A2E !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1A1A2E !important;
    }
    [data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    .stSelectbox label, .stMultiSelect label {
        color: #1A1A2E !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

CITY_COLORS = {
    'Chicago, IL': '#28A745',
    'Houston, TX': '#B84FD8',
    'Los Angeles, CA': '#FF6B35',
    'Miami, FL': '#FF3860',
    'New York, NY': '#2D87F0',
}

@st.cache_data
def load_data():
    cities_long = pd.read_csv('../data/cleaned/cities_long.csv')
    annual_summary = pd.read_csv('../data/cleaned/annual_summary.csv')
    cities_long['date'] = pd.to_datetime(cities_long['date'])
    return cities_long, annual_summary

cities_long, annual_summary = load_data()

# Light header
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
        📈 Affordability Trends Analysis
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        Explore how affordability indices, home values, and rental prices have evolved across major US cities from 2015 to 2024.
    </p>
</div>
""", unsafe_allow_html=True)

# Filters
col1, col2 = st.columns([1, 2])
with col1:
    cities = st.multiselect(
        "Select Cities",
        options=sorted(cities_long['city'].unique()),
        default=['New York, NY', 'Los Angeles, CA', 'Chicago, IL']
    )
    metrics = st.multiselect(
        "Select Metrics",
        options=['affordability_index', 'avg_home_value', 'avg_monthly_rent'],
        default=['affordability_index'],
        format_func=lambda x: x.replace('_', ' ').title()
    )

if cities and metrics:
    filtered = cities_long[cities_long['city'].isin(cities)]
    
    for metric in metrics:
        fig = px.line(
            filtered, x='date', y=metric,
            color='city', color_discrete_map=CITY_COLORS,
            title=metric.replace('_', ' ').title(),
            labels={'date': 'Year', metric: metric.replace('_', ' ').title(), 'city': 'City'}
        )
        if metric == 'affordability_index':
            fig.add_hline(y=1.0, line_dash='dash', line_color='red', opacity=0.5,
                         annotation_text='Threshold (1.0)')
        fig.update_layout(
            height=450, plot_bgcolor='white', paper_bgcolor='white',
            hovermode='x unified',
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Select at least one city and one metric to view trends")

# YoY Changes
st.markdown("---")
st.markdown("### 📊 Year-over-Year Changes")
st.markdown('<p style="color:#555555; font-size:0.9rem;">See which cities experienced the biggest changes in affordability year over year.</p>', unsafe_allow_html=True)

yoy = annual_summary.copy()
yoy['affordability_yoy'] = yoy.groupby('city')['affordability_index'].pct_change() * 100

latest_yoy = yoy[yoy['year'] == 2024].sort_values('affordability_yoy', ascending=False)

fig_yoy = px.bar(
    latest_yoy, x='city', y='affordability_yoy',
    color='affordability_yoy',
    color_continuous_scale=['#28A745', '#FFC107', '#DC3545'],
    title='Affordability Index Change (2023 → 2024)',
    labels={'affordability_yoy': 'Year-over-Year Change (%)', 'city': 'City'}
)
fig_yoy.update_layout(height=450, plot_bgcolor='white')
st.plotly_chart(fig_yoy, use_container_width=True)