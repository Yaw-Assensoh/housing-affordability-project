import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os

st.set_page_config(
    page_title="Time Series — Housing Analysis",
    page_icon="📈",
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
    .stSelectbox label, .stCheckbox label { color: #1A1A2E !important; font-weight: 600 !important; }
    
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
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    cities_long   = pd.read_csv(os.path.join(base, 'data/cleaned/cities_long.csv'))
    forecasts     = pd.read_csv(os.path.join(base, 'data/cleaned/forecasts_2025_2027.csv'))
    model_summary = pd.read_csv(os.path.join(base, 'data/cleaned/arima_model_summary.csv'))
    cities_long['date'] = pd.to_datetime(cities_long['date'])
    forecasts['date']   = pd.to_datetime(forecasts['date'])
    return cities_long, forecasts, model_summary

cities_long, forecasts, model_summary = load_data()

# LIGHT HEADER - UPDATED
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
        📈 Time Series & Forecasting
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        SARIMA models trained on 10 years of monthly data, generating
        36-month forecasts through December 2027 with 95% confidence
        intervals for all 5 cities.
    </p>
</div>
""", unsafe_allow_html=True)

# What is SARIMA
st.markdown("""
<div class="card" style="margin-bottom:24px; border-left:5px solid #2980B9;">
    <h4 style="color:#2980B9!important; margin:0 0 8px 0;">
        📖 What Is SARIMA Forecasting?
    </h4>
    <p style="color:#333333!important; margin:0; font-size:0.92rem; line-height:1.7;">
        SARIMA stands for Seasonal Autoregressive Integrated Moving Average.
        It is the industry standard model for forecasting time series data
        with seasonal patterns. It works by learning from three things:
        past values (how prices moved historically), past errors
        (where previous forecasts were wrong), and seasonal cycles
        (the consistent summer peak and winter dip in home prices every year).
        All parameters were automatically selected using the AIC score —
        the model that fits best without overfitting.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 🔧 Settings")
    selected_city = st.selectbox(
        "Select City for Detailed View",
        options=list(CITY_COLORS.keys()),
        format_func=lambda x: x.split(',')[0]
    )
    show_ci = st.checkbox("Show 95% Confidence Interval", value=True)
    st.markdown("---")
    st.markdown("**💡 What the confidence interval means:**")
    st.markdown("The shaded band shows the range of likely outcomes. It widens the further into the future we go — uncertainty naturally increases over time.")

# Forecast KPIs
st.markdown("### 🔮 2027 Home Value Forecasts")
st.markdown("""
<p class="section-desc">
Projected home values for December 2027 based on SARIMA models
trained on monthly data from 2015 to 2024.
The percentage shows expected change from the current 2024 values.
These are directional forecasts — not guarantees.
</p>
""", unsafe_allow_html=True)

cols = st.columns(5)
for col, city in zip(cols, list(CITY_COLORS.keys())):
    city_fc   = forecasts[forecasts['city'] == city]
    city_hist = cities_long[cities_long['city'] == city]
    if len(city_fc) == 0:
        continue
    current = float(city_hist['home_value'].iloc[-1])
    fc_2027 = float(city_fc['forecast'].iloc[-1])
    change  = ((fc_2027 - current) / current) * 100
    color   = CITY_COLORS[city]
    with col:
        st.markdown(f"""
        <div class="card" style="border-top:5px solid {color}; text-align:center;">
            <p style="margin:0 0 4px 0; font-size:0.78rem;
                      color:#888888!important; font-weight:600;
                      text-transform:uppercase; letter-spacing:0.5px;">
                {city.split(',')[0]}
            </p>
            <h3 style="margin:4px 0; color:{color}!important;
                       font-size:1.7rem; font-weight:900;">
                ${fc_2027/1000:.0f}k
            </h3>
            <p style="margin:0; font-size:0.82rem;
                      color={'#DC3545' if change > 15 else '#E67E22' if change > 5 else '#27AE60'}!important;
                      font-weight:600;">
                {change:+.1f}% vs 2024
            </p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Individual city forecast
st.markdown(f"### 📊 Detailed Forecast — {selected_city.split(',')[0]}")
st.markdown("""
<p class="section-desc">
The solid line shows historical home values (2015–2024).
The dashed line shows the SARIMA forecast (2025–2027).
The shaded band is the 95% confidence interval — the range
within which the true value is likely to fall.
Notice how the band widens over time as uncertainty accumulates.
</p>
""", unsafe_allow_html=True)

city_hist = cities_long[
    cities_long['city'] == selected_city].sort_values('date')
city_fc   = forecasts[
    forecasts['city'] == selected_city].sort_values('date')
color     = CITY_COLORS[selected_city]
r = int(color[1:3], 16)
g = int(color[3:5], 16)
b = int(color[5:7], 16)
rgba_fill = f"rgba({r},{g},{b},0.12)"

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=city_hist['date'], y=city_hist['home_value'],
    mode='lines', name='Historical',
    line=dict(color=color, width=2.5)
))
fig.add_trace(go.Scatter(
    x=city_fc['date'], y=city_fc['forecast'],
    mode='lines', name='Forecast',
    line=dict(color=color, width=2.5, dash='dash')
))
if show_ci:
    upper = city_fc['upper_95'].tolist()
    lower = city_fc['lower_95'].tolist()
    dates = city_fc['date'].tolist()
    fig.add_trace(go.Scatter(
        x=dates + dates[::-1],
        y=upper + lower[::-1],
        fill='toself', fillcolor=rgba_fill,
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence Interval'
    ))
fig.add_shape(
    type='line', x0='2025-01-31', x1='2025-01-31',
    y0=0, y1=1, yref='paper',
    line=dict(color='#555555', dash='dash', width=1.5)
)
fig.add_annotation(
    x='2025-01-31', y=0.96, yref='paper',
    text='← Historical | Forecast →',
    showarrow=False, font=dict(size=11, color='#555555'),
    xanchor='center'
)
fig.update_layout(
    height=450, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444')),
    legend=dict(orientation='h', yanchor='bottom', y=1.02,
                xanchor='right', x=1, font=dict(color='#333333')),
    margin=dict(l=10, r=10, t=40, b=10)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# All cities combined
st.markdown("### 📊 All Cities — Combined Forecast (2015–2027)")
st.markdown('<p class="section-desc">All 5 cities on one chart — solid lines for historical data, dashed for forecasts. The widening gap between LA and the other cities is the most striking pattern.</p>', unsafe_allow_html=True)

fig2 = go.Figure()
for city in CITY_COLORS:
    hist  = cities_long[cities_long['city'] == city].sort_values('date')
    fc    = forecasts[forecasts['city'] == city].sort_values('date')
    color = CITY_COLORS[city]
    short = city.split(',')[0]
    fig2.add_trace(go.Scatter(
        x=hist['date'], y=hist['home_value'],
        mode='lines', name=short,
        line=dict(color=color, width=2),
        legendgroup=short
    ))
    fig2.add_trace(go.Scatter(
        x=fc['date'], y=fc['forecast'],
        mode='lines',
        line=dict(color=color, width=2, dash='dash'),
        legendgroup=short, showlegend=False
    ))
fig2.add_shape(
    type='line', x0='2025-01-31', x1='2025-01-31',
    y0=0, y1=1, yref='paper',
    line=dict(color='#555555', dash='dash', width=1.5)
)
fig2.add_annotation(
    x='2025-01-31', y=0.96, yref='paper',
    text='← Historical | Forecast →',
    showarrow=False, font=dict(size=11, color='#555555'),
    xanchor='center'
)
fig2.update_layout(
    height=450, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444')),
    legend=dict(orientation='h', yanchor='bottom', y=1.02,
                xanchor='right', x=1, font=dict(color='#333333')),
    margin=dict(l=10, r=10, t=40, b=10)
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Model summary
st.markdown("### 🤖 ARIMA Model Parameters")
st.markdown("""
<p class="section-desc">
The parameters (p, d, q) were automatically selected for each city
using auto_arima. Lower AIC = better model fit. All cities use d=1
(one round of differencing) because home price data is non-stationary
— it trends upward. The seasonal component (m=12) captures the
consistent summer peak and winter dip in prices every year.
</p>
""", unsafe_allow_html=True)
st.dataframe(model_summary, use_container_width=True, hide_index=True)

st.markdown("---")

# Findings
st.markdown("### 💡 Key Forecasting Findings")
ts_findings = [
    ("#E74C3C", "🔴 Los Angeles Is Approaching $1 Million",
     "The SARIMA forecast projects LA home values will approach $1 million by December 2027. At that price point, a household would need an annual income of roughly $200,000 just to meet the standard mortgage affordability guidelines. The median US household income is $83,730."),
    ("#9B59B6", "📈 Miami Has the Steepest Forecast Trajectory",
     "Miami's forecast line has the steepest slope of any city — consistent with its post-2020 acceleration pattern. It also has one of the widest confidence intervals, reflecting the higher uncertainty around a market that has been changing this rapidly. The model is less certain about Miami than any other city."),
    ("#27AE60", "🟢 Houston and Chicago Are the Most Predictable",
     "Both cities show the narrowest confidence intervals in the forecast — their markets follow stable, predictable patterns. This is valuable in itself: predictability means less risk for buyers, renters, and policymakers. Stable markets allow for better long-term planning."),
    ("#555555", "⚠️ What These Forecasts Cannot Predict",
     "SARIMA models are trained on historical patterns. They cannot account for sudden interest rate changes, new housing policy, economic recessions, or demographic shifts. These forecasts should be treated as directional indicators based on current trends — not precise predictions of the future."),
]
for color, title, body in ts_findings:
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