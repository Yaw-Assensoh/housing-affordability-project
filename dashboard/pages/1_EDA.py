import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="EDA — Housing Analysis",
    page_icon="📊",
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
    div[data-testid="stMetricValue"] { color: #1A1A2E !important; font-weight: 800 !important; }
    div[data-testid="stMetricLabel"] { color: #555555 !important; font-weight: 600 !important; }
    .stAlert > div { color: #1A1A2E !important; font-size: 0.93rem !important; line-height: 1.65 !important; }
    .stSelectbox label, .stMultiSelect label, .stSlider label {
        color: #1A1A2E !important; font-weight: 600 !important;
    }
    
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
    
    .stTabs [data-baseweb="tab"] { color: #444444 !important; font-weight: 600 !important; }
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

@st.cache_data
def load_data():
    df = pd.read_csv('../data/cleaned/cities_long.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

cities_long = load_data()

# LIGHT HEADER
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
        📊 Exploratory Data Analysis
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        A thorough exploration of the data — examining distributions,
        trends, and correlations across all 5 cities over 10 years.
        Every chart here informed the deeper analyses that followed.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔧 Filters")
    selected_cities = st.multiselect(
        "Select Cities",
        options=list(CITY_COLORS.keys()),
        default=list(CITY_COLORS.keys()),
        format_func=lambda x: x.split(',')[0]
    )
    year_range = st.slider("Year Range", 2015, 2024, (2015, 2024))
    st.markdown("---")
    st.markdown("**💡 Tip:** Try comparing just LA and Houston to see the two extremes side by side.")

filtered = cities_long[
    (cities_long['city'].isin(selected_cities)) &
    (cities_long['year'].between(year_range[0], year_range[1]))
]

# KPIs
st.markdown("### 📋 Dataset Overview")
st.markdown('<p class="section-desc">A summary of the currently filtered data. Adjust the sidebar filters to focus on specific cities or time periods.</p>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Observations", f"{len(filtered):,}")
c2.metric("Avg Home Value",     f"${filtered['home_value'].mean():,.0f}")
c3.metric("Avg Affordability Index", f"{filtered['affordability_index'].mean():.3f}")
c4.metric("Avg Monthly Rent",   f"${filtered['monthly_rent'].mean():,.0f}")

st.markdown("---")

# Trend charts
st.markdown("### 📈 Trends Over Time")
st.markdown("""
<p class="section-desc">
These charts show how home values and the affordability index changed
year by year. The red shaded area marks the COVID-19 period —
notice how every city accelerated sharply after 2020.
The dashed line at 1.0 on the second chart marks the
affordability threshold. Cities above it are unaffordable
for the average household.
</p>
""", unsafe_allow_html=True)

yearly = (filtered.groupby(['city', 'year'])
          .agg(home_value=('home_value', 'mean'),
               affordability_index=('affordability_index', 'mean'))
          .reset_index())

tab1, tab2 = st.tabs(["🏠 Home Value Trends", "📊 Affordability Index Trends"])

with tab1:
    fig = px.line(
        yearly, x='year', y='home_value',
        color='city', color_discrete_map=CITY_COLORS, markers=True,
        labels={'year': 'Year', 'home_value': 'Avg Home Value ($)',
                'city': 'City'}
    )
    fig.add_vrect(x0=2020, x1=2022, fillcolor='#E74C3C', opacity=0.06,
                  annotation_text='Post-COVID Surge',
                  annotation_position='top left',
                  annotation_font=dict(color='#C0392B'))
    fig.update_layout(
        height=420, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
        xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
                   tickmode='linear', dtick=1,
                   tickfont=dict(color='#444444')),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
                   tickformat='$,.0f',
                   tickfont=dict(color='#444444')),
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='right', x=1,
                    font=dict(color='#333333'))
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig2 = px.line(
        yearly, x='year', y='affordability_index',
        color='city', color_discrete_map=CITY_COLORS, markers=True,
        labels={'year': 'Year',
                'affordability_index': 'Affordability Index',
                'city': 'City'}
    )
    fig2.add_hline(y=1.0, line_dash='dash', line_color='#333333',
                   opacity=0.7, annotation_text='Affordable Threshold (1.0)',
                   annotation_position='bottom right',
                   annotation_font=dict(color='#333333'))
    fig2.add_vrect(x0=2020, x1=2022, fillcolor='#E74C3C', opacity=0.06,
                   annotation_text='Post-COVID Surge',
                   annotation_position='top left',
                   annotation_font=dict(color='#C0392B'))
    fig2.update_layout(
        height=420, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
        xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
                   tickmode='linear', dtick=1,
                   tickfont=dict(color='#444444')),
        yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
                   tickfont=dict(color='#444444')),
        legend=dict(orientation='h', yanchor='bottom',
                    y=1.02, xanchor='right', x=1,
                    font=dict(color='#333333'))
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Distribution
st.markdown("### 📊 Distribution Analysis")
st.markdown("""
<p class="section-desc">
A histogram shows how values are spread across all 10 years for
each city. A wide spread means prices varied a lot over time —
a tight cluster means the city was more consistent.
Los Angeles has the widest home value spread, reflecting its
continuous upward trajectory. Houston's distribution clusters
tightly at the lower end, confirming its stability.
</p>
""", unsafe_allow_html=True)

metric = st.selectbox(
    "Select Metric to Explore",
    ['home_value', 'monthly_rent',
     'affordability_index', 'median_income'],
    format_func=lambda x: x.replace('_', ' ').title()
)
fig3 = px.histogram(
    filtered, x=metric, color='city',
    color_discrete_map=CITY_COLORS,
    nbins=30, barmode='overlay', opacity=0.65,
    labels={metric: metric.replace('_', ' ').title(), 'city': 'City'}
)
fig3.update_layout(
    height=400, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    legend=dict(orientation='h', yanchor='bottom',
                y=1.02, xanchor='right', x=1,
                font=dict(color='#333333'))
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Correlation heatmap
st.markdown("### 🔗 Correlation Heatmap")
st.markdown("""
<p class="section-desc">
This heatmap shows how strongly each metric relates to the others.
Values close to 1.0 mean a strong positive relationship — when
one rises, the other rises too. Values close to -1.0 mean the
opposite. The key finding here: home value and affordability index
are strongly correlated, confirming that rising prices — not
falling incomes — are driving the crisis.
</p>
""", unsafe_allow_html=True)

corr = (filtered[['home_value', 'monthly_rent',
                   'median_income', 'affordability_index']]
        .corr().round(3))
fig4 = px.imshow(
    corr, text_auto=True,
    color_continuous_scale='RdBu_r',
    aspect='auto', zmin=-1, zmax=1,
    labels=dict(color='Correlation')
)
fig4.update_layout(
    height=380,
    font=dict(color='#333333')
)
st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# Key findings
st.markdown("### 💡 Key EDA Findings")
st.markdown('<p class="section-desc">The four most important conclusions from the exploratory analysis — each one supported directly by the charts above.</p>', unsafe_allow_html=True)

findings_eda = [
    ("#2980B9", "📈 All Cities Trended Upward — No Exceptions",
     "Every single city in the dataset shows a consistent upward trajectory in home values from 2015 to 2024. Not one city experienced a meaningful price decline over the full period. The steepest acceleration happened post-2020 across all 5 cities simultaneously — driven by the COVID-19 demand surge and supply constraints."),
    ("#E67E22", "📅 2020–2022 Was the Turning Point",
     "The post-COVID period is visible as a sharp inflection in every chart. Before 2020, most cities were rising gradually. After 2020, the rate of increase nearly doubled in some markets. Miami's index went from 0.757 in 2020 to 1.084 in 2022 — crossing the affordability threshold for the first time in just two years."),
    ("#DC3545", "🔴 Los Angeles Has Been in Crisis Since Before 2015",
     "Los Angeles had an affordability index of 1.378 in January 2015 — already 38% above the affordable threshold before our dataset even begins. By 2024 it reached 2.22. This is not a recent problem — it is a structural failure decades in the making, and the data shows no sign of reversal."),
    ("#27AE60", "🟢 Income Did Not Keep Pace — Wages Grew $11k, Prices Grew $400k",
     "The correlation heatmap tells the most important story: median income barely moved (standard deviation of just $3,505 over 10 years), while home values had a standard deviation of $197,826. The affordability crisis is entirely driven by price growth outpacing wages — not by people earning less."),
]
for color, title, body in findings_eda:
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