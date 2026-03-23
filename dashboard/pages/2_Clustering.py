import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Clustering — Housing Analysis",
    page_icon="🔵",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #F4F6F9 !important; }
    .block-container { padding-top: 2rem !important; }
    section[data-testid="stSidebar"] { background-color: #1A1A2E !important; }
    section[data-testid="stSidebar"] * { color: #EEEEEE !important; }
    h1, h2, h3, h4 { color: #1A1A2E !important; font-weight: 700 !important; }
    p, li { color: #333333 !important; line-height: 1.7 !important; }
    .stAlert > div { color: #1A1A2E !important; font-size: 0.93rem !important; line-height: 1.65 !important; }
    .stSelectbox label { color: #1A1A2E !important; font-weight: 600 !important; }
    
    /* Fix for selectbox dropdown and input */
    .stSelectbox [data-baseweb="select"] {
        background-color: white !important;
        border: 1px solid #D0D5DD !important;
        border-radius: 8px !important;
    }
    .stSelectbox [data-baseweb="select"] div {
        color: #1A1A2E !important;
        background-color: white !important;
    }
    .stSelectbox svg {
        fill: #1A1A2E !important;
    }
    div[data-baseweb="popover"] div {
        background-color: white !important;
        color: #1A1A2E !important;
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
    
    .section-desc { color: #555555 !important; font-size: 0.93rem !important;
                    margin-bottom: 16px !important; line-height: 1.65 !important; }
    .card { background: #FFFFFF; border-radius: 12px; padding: 22px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.07); border: 1px solid #E8ECF0; }
</style>
""", unsafe_allow_html=True)

CITY_COLORS = {
    'Chicago, IL':     '#28A745',
    'Houston, TX':     '#9B59B6',
    'Los Angeles, CA': '#E67E22',
    'Miami, FL':       '#E74C3C',
    'New York, NY':    '#2980B9',
}
CLUSTER_COLORS = {
    'Most Affordable':  '#27AE60',
    'Moderate':         '#E67E22',
    'Least Affordable': '#DC3545',
}

@st.cache_data
def load_data():
    cities_long = pd.read_csv('../data/cleaned/cities_long.csv')
    clustering  = pd.read_csv('../data/cleaned/clustering_results.csv')
    return cities_long, clustering

cities_long, clustering = load_data()

# LIGHT HEADER - UPDATED
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
        🔵 K-Means Clustering
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        Grouping the 5 cities into natural market segments based on
        9 housing metrics simultaneously. Clustering confirms the
        SQL Phase 2 risk classifications through a completely
        different analytical method.
    </p>
</div>
""", unsafe_allow_html=True)

# What is clustering
st.markdown("""
<div class="card" style="margin-bottom:24px; border-left:5px solid #2980B9;">
    <h4 style="color:#2980B9!important; margin:0 0 8px 0;">
        📖 What Is K-Means Clustering?
    </h4>
    <p style="color:#333333!important; margin:0; font-size:0.92rem; line-height:1.7;">
        K-Means is an unsupervised machine learning algorithm that groups
        data points into K clusters based on similarity. It does not know
        anything about affordability thresholds or risk levels in advance
        — it discovers natural groupings purely from the numbers.
        The fact that its clusters perfectly match the risk levels
        identified in Phase 2 SQL analysis is a powerful validation
        that the findings are real, not an artefact of how we defined things.
    </p>
</div>
""", unsafe_allow_html=True)

# Cluster cards
st.markdown("### 🏷️ The Three Market Segments")
st.markdown('<p class="section-desc">K-Means identified 3 distinct groups. Each group shares similar characteristics across all 9 housing metrics — price level, rent, growth rate, and affordability stress.</p>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
for col, label, emoji, desc in zip(
        [c1, c2, c3],
        ['Most Affordable', 'Moderate', 'Least Affordable'],
        ['🟢', '🟡', '🔴'],
        [
            "These cities stayed below the 1.0 affordability threshold throughout the entire 10-year period. Lower land costs, fewer zoning restrictions, and stronger housing supply kept prices manageable relative to incomes.",
            "This city was affordable until 2022 when the post-COVID migration wave pushed prices through the threshold. It represents a market in transition — affordable by historical standards but deteriorating rapidly.",
            "These cities have been above the affordability threshold for years, some since before our dataset begins in 2015. They share the highest prices, highest rents, and most severe affordability stress in the dataset.",
        ]):
    group = clustering[clustering['cluster_label'] == label]
    if len(group) == 0:
        continue
    cities_in = ', '.join(group['city_short'].tolist())
    avg_ai    = float(group['avg_affordability'].mean())
    avg_hv    = float(group['avg_home_value'].mean())
    color     = CLUSTER_COLORS[label]
    with col:
        st.markdown(f"""
        <div class="card" style="border-top:5px solid {color}; height:100%;">
            <h4 style="color:{color}!important; margin:0 0 10px 0;">
                {emoji} {label}
            </h4>
            <p style="margin:4px 0; color:#333333!important; font-size:0.9rem;">
                <b>Cities:</b> {cities_in}
            </p>
            <p style="margin:4px 0; color:#333333!important; font-size:0.9rem;">
                <b>Avg Index:</b>
                <span style="color:{color}!important; font-weight:700;">
                    {avg_ai:.3f}
                </span>
            </p>
            <p style="margin:4px 0 12px 0; color:#333333!important; font-size:0.9rem;">
                <b>Avg Home Value:</b> ${avg_hv:,.0f}
            </p>
            <p style="color:#555555!important; font-size:0.85rem;
                      margin:0; line-height:1.6; border-top:1px solid #F0F0F0;
                      padding-top:10px;">
                {desc}
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Scatter
st.markdown("### 📊 Cluster Scatter — Affordability vs Home Value")
st.markdown("""
<p class="section-desc">
Each dot is a city. The further right on the x-axis, the more
expensive the average home. The higher on the y-axis, the less
affordable. The dashed line at 1.0 is the threshold — anything
above it is unaffordable for median income households.
Bubble size represents 10-year home value growth.
</p>
""", unsafe_allow_html=True)

fig = px.scatter(
    clustering,
    x='avg_home_value', y='avg_affordability',
    color='cluster_label', color_discrete_map=CLUSTER_COLORS,
    text='city_short', size='home_value_growth', size_max=45,
    labels={
        'avg_home_value':    'Avg Home Value ($)',
        'avg_affordability': 'Avg Affordability Index',
        'cluster_label':     'Cluster',
        'home_value_growth': '10yr Growth (%)'
    },
    hover_data={
        'city_short':        True,
        'avg_home_value':    ':$,.0f',
        'avg_affordability': ':.3f',
        'home_value_growth': ':.1f',
        'cluster_label':     True
    }
)
fig.add_hline(y=1.0, line_dash='dash', line_color='#333333',
              opacity=0.7, annotation_text='Affordable Threshold (1.0)',
              annotation_font=dict(color='#333333'))
fig.update_traces(textposition='top center',
                  textfont=dict(size=12, color='#1A1A2E'))
fig.update_layout(
    height=450, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    legend=dict(font=dict(color='#333333'))
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Radar chart
st.markdown("### 🕸️ Radar Chart — Full Feature Comparison")
st.markdown("""
<p class="section-desc">
Each axis of this radar chart represents one housing metric,
normalised to a 0–1 scale so all metrics can be compared fairly.
A city with a large shaded area scores high across many metrics.
In housing, that is not always good — a large footprint in
affordability stress metrics means the market is under severe pressure.
</p>
""", unsafe_allow_html=True)

radar_features = ['avg_home_value', 'avg_monthly_rent', 'avg_affordability',
                  'home_value_growth', 'rent_growth', 'affordability_range']
radar_labels   = ['Home Value', 'Monthly Rent', 'Affordability',
                  'HV Growth', 'Rent Growth', 'AI Range']

radar_data = clustering.set_index('city_short')[radar_features].copy()
radar_norm = ((radar_data - radar_data.min()) /
              (radar_data.max() - radar_data.min()))

fig2 = go.Figure()
for city_short in radar_norm.index:
    city_full = clustering[
        clustering['city_short'] == city_short]['city'].values[0]
    color  = CITY_COLORS.get(city_full, '#999999')
    values = radar_norm.loc[city_short].tolist() + [radar_norm.loc[city_short].tolist()[0]]
    fig2.add_trace(go.Scatterpolar(
        r=values,
        theta=radar_labels + [radar_labels[0]],
        fill='toself', fillcolor=color,
        line=dict(color=color, width=2.5),
        opacity=0.35, name=city_short
    ))
fig2.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1],
                        tickfont=dict(color='#555555')),
        angularaxis=dict(tickfont=dict(color='#333333', size=12))
    ),
    showlegend=True, height=500,
    paper_bgcolor='#F4F6F9',
    legend=dict(font=dict(color='#333333', size=11)),
    title=dict(text='All features normalised to 0–1 scale',
               font=dict(color='#555555', size=11))
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Feature bar
st.markdown("### 📊 City-by-City Feature Comparison")
st.markdown('<p class="section-desc">Select any metric to compare all 5 cities directly. Color shows which cluster each city belongs to.</p>', unsafe_allow_html=True)

feat = st.selectbox(
    "Select Feature to Compare",
    ['avg_home_value', 'avg_monthly_rent', 'avg_affordability',
     'home_value_growth', 'rent_growth'],
    format_func=lambda x: x.replace('_', ' ').title()
)
fig3 = px.bar(
    clustering.sort_values(feat, ascending=False),
    x='city_short', y=feat,
    color='cluster_label', color_discrete_map=CLUSTER_COLORS,
    text=feat,
    labels={'city_short': 'City',
            feat: feat.replace('_', ' ').title(),
            'cluster_label': 'Cluster'}
)
fig3.update_traces(
    texttemplate=('$%{text:,.0f}' if 'value' in feat or 'rent' in feat
                  else '%{text:.2f}'),
    textposition='outside',
    textfont=dict(color='#333333')
)
fig3.update_layout(
    height=400, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    legend=dict(font=dict(color='#333333'))
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Findings
st.markdown("### 💡 Key Clustering Findings")
cluster_findings = [
    ("#27AE60", "🟢 Houston & Chicago — The Affordable Cluster",
     "These two cities formed a clear cluster throughout the analysis. Both stayed below the 1.0 threshold for the entire period. Their radar chart footprints are the smallest of all cities — they score low on every stress metric. This is not a coincidence: both cities have relatively permissive zoning laws and more available land than coastal metros."),
    ("#DC3545", "🔴 Los Angeles & New York — The Crisis Cluster",
     "LA and NY share a cluster because they are fundamentally different from the other three cities — not just more expensive, but more expensive by a different order of magnitude. Their combined characteristics (extreme home values, high rents, severe affordability stress) set them apart from every other market in the dataset."),
    ("#E67E22", "🟡 Miami — The Transition Cluster",
     "Miami stands alone in the moderate cluster — not because it is average, but because it is changing. Its 2015 profile looked like Houston. Its 2024 profile is approaching New York. The 10-year trajectory is more concerning than any other city because the speed of deterioration is unmatched."),
    ("#2980B9", "📊 Clustering Confirms SQL Findings Independently",
     "The K-Means algorithm had no knowledge of the SQL risk classifications from Phase 2. It discovered the same groupings purely from the numbers — HIGH RISK, MODERATE RISK, LOW RISK — using 9 features simultaneously. Two completely different analytical methods reaching the same conclusion is strong evidence that the findings are robust and not artefacts of methodology."),
]
for color, title, body in cluster_findings:
    st.markdown(f"""
    <div class="card" style="margin-bottom:12px; border-left:5px solid {color};">
        <h4 style="color:{color}!important; margin:0 0 8px 0; font-size:0.97rem;">
            {title}
        </h4>
        <p style="color:#333333!important; margin:0; font-size:0.91rem;
                  line-height:1.7;">
            {body}
        </p>
    </div>
    """, unsafe_allow_html=True)