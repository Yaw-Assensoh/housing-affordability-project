import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Regression — Housing Analysis",
    page_icon="📐",
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

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    predictions = pd.read_csv(os.path.join(base, 'data/cleaned/regression_predictions.csv'))
    importance  = pd.read_csv(os.path.join(base, 'data/cleaned/regression_feature_importance.csv'))
    scenarios   = pd.read_csv(os.path.join(base, 'data/cleaned/regression_scenarios.csv'))
    return predictions, importance, scenarios

predictions, importance, scenarios = load_data()

# LIGHT HEADER - UPDATED
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
        📐 Regression Analysis
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        Using multiple linear regression to identify which economic
        factors most strongly drive home values — and to model
        what would happen to prices under different economic scenarios.
    </p>
</div>
""", unsafe_allow_html=True)

# What is regression
st.markdown("""
<div class="card" style="margin-bottom:24px; border-left:5px solid #2980B9;">
    <h4 style="color:#2980B9!important; margin:0 0 8px 0;">
        📖 What Is Multiple Linear Regression?
    </h4>
    <p style="color:#333333!important; margin:0; font-size:0.92rem; line-height:1.7;">
        Regression models the relationship between a target variable
        (home values) and multiple predictor variables simultaneously
        (income, rent, affordability index, year, month, city).
        The model learns a coefficient for each predictor —
        a number that tells us how much home value changes
        when that predictor increases by one unit, holding
        everything else constant. This lets us quantify
        which factors matter most and by how much.
    </p>
</div>
""", unsafe_allow_html=True)

# Model KPIs
actual    = predictions['actual']
predicted = predictions['predicted']
residuals = predictions['residual']
r2   = float(1 - (np.sum(residuals**2) /
                   np.sum((actual - actual.mean())**2)))
rmse = float(np.sqrt(np.mean(residuals**2)))
mae  = float(np.mean(np.abs(residuals)))
mape = float(np.mean(np.abs(residuals / actual)) * 100)

st.markdown("### 📊 Model Performance")
st.markdown("""
<p class="section-desc">
These four metrics measure how accurate the model is.
R² tells us what proportion of home value variation the
model can explain — higher is better.
MAPE tells us the average percentage error per prediction.
</p>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("R² Score",
          f"{r2:.4f}",
          f"{r2*100:.1f}% of variance explained")
c2.metric("RMSE",
          f"${rmse:,.0f}",
          "Avg error in dollars")
c3.metric("MAE",
          f"${mae:,.0f}",
          "Avg absolute error")
c4.metric("MAPE",
          f"{mape:.2f}%",
          "Avg % prediction error")

st.markdown("---")

# Feature importance
st.markdown("### 🏆 Feature Importance — What Drives Home Values?")
st.markdown("""
<p class="section-desc">
Green bars show features that increase home values.
Red bars show features that decrease them.
Bar length represents the strength of the effect.
These are standardised coefficients — each bar shows
the effect of increasing that feature by one standard
deviation, holding all other features constant.
</p>
""", unsafe_allow_html=True)

imp = importance.copy()
imp['direction'] = imp['coefficient'].apply(
    lambda x: 'Increases Home Value' if x > 0 else 'Decreases Home Value')

fig = px.bar(
    imp.sort_values('coefficient'),
    x='coefficient', y='feature',
    color='direction',
    color_discrete_map={
        'Increases Home Value': '#27AE60',
        'Decreases Home Value': '#DC3545'
    },
    orientation='h', text='coefficient',
    labels={'coefficient': 'Regression Coefficient',
            'feature': 'Feature', 'direction': 'Direction'}
)
fig.update_traces(
    texttemplate='%{text:,.0f}', textposition='outside',
    textfont=dict(color='#333333'))
fig.add_vline(x=0, line_color='#333333', line_dash='dash', opacity=0.5)
fig.update_layout(
    height=420, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=False, tickfont=dict(color='#444444')),
    legend=dict(font=dict(color='#333333'))
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Actual vs Predicted
st.markdown("### 🎯 Actual vs Predicted Home Values")
st.markdown("""
<p class="section-desc">
Each dot is one observation from the test set — 20% of the data
the model never saw during training. If the model were perfect,
every dot would fall exactly on the red diagonal line.
The tighter the cluster around that line, the more accurate
the predictions. Dots far from the line are cases where
the model over or under-predicted.
</p>
""", unsafe_allow_html=True)

fig2 = px.scatter(
    predictions, x='actual', y='predicted', opacity=0.55,
    color_discrete_sequence=['#2980B9'],
    labels={'actual': 'Actual Home Value ($)',
            'predicted': 'Predicted Home Value ($)'}
)
min_val = float(predictions['actual'].min())
max_val = float(predictions['actual'].max())
fig2.add_shape(
    type='line', x0=min_val, y0=min_val,
    x1=max_val, y1=max_val,
    line=dict(color='#DC3545', dash='dash', width=2)
)
fig2.add_annotation(
    x=max_val * 0.7, y=max_val * 0.85,
    text=f"R² = {r2:.4f}",
    showarrow=False,
    font=dict(size=13, color='#1A1A2E'),
    bgcolor='white', bordercolor='#CCCCCC', borderpad=6
)
fig2.update_layout(
    height=430, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444'))
)
st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# Scenario analysis
st.markdown("### 🔮 Scenario Analysis — Los Angeles 2024")
st.markdown("""
<p class="section-desc">
What would happen to predicted home values in Los Angeles
if economic conditions changed? Each bar shows a different
scenario — income increases, rent increases, or both.
This analysis uses the trained regression model to
predict outcomes under conditions that have not yet occurred.
</p>
""", unsafe_allow_html=True)

scen = scenarios.copy()
scen['scenario_clean'] = scen['scenario'].str.replace('\n', ' ')
base_val = float(scen.iloc[0]['predicted_value'])
scen['change_pct'] = ((scen['predicted_value'] - base_val) / base_val * 100)

fig3 = px.bar(
    scen, x='scenario_clean', y='predicted_value',
    color='change_pct',
    color_continuous_scale=[
        [0.0, '#DC3545'], [0.5, '#F5F5F5'], [1.0, '#27AE60']],
    text='predicted_value',
    labels={'scenario_clean': 'Scenario',
            'predicted_value': 'Predicted Home Value ($)',
            'change_pct': 'Change vs Base (%)'}
)
fig3.update_traces(
    texttemplate='$%{text:,.0f}', textposition='outside',
    textfont=dict(color='#333333'))
fig3.update_layout(
    height=440, plot_bgcolor='#FFFFFF', paper_bgcolor='#F4F6F9',
    xaxis=dict(showgrid=False, tickfont=dict(color='#444444')),
    yaxis=dict(showgrid=True, gridcolor='#EEEEEE',
               tickformat='$,.0f', tickfont=dict(color='#444444'))
)
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# Findings
st.markdown("### 💡 Key Regression Findings")
top_feat = imp.iloc[imp['coefficient'].abs().argmax()]['feature']
reg_findings = [
    ("#2980B9", f"🏆 Top Predictor: {top_feat.replace('_',' ').title()}",
     f"The single most important driver of home values in the model is {top_feat.replace('_', ' ')}. This confirms what the data shows intuitively — the existing level of affordability stress and city location are self-reinforcing. Expensive cities attract more demand, which makes them more expensive, which makes them less affordable, which raises prices further. It is a feedback loop."),
    ("#27AE60", f"✅ Model Explains {r2*100:.1f}% of Variance",
     f"An R² of {r2:.4f} means the model accounts for {r2*100:.1f}% of the variation in home values using just 7 features. This is strong performance for a linear model on housing data. The remaining {(1-r2)*100:.1f}% is explained by factors not in our dataset — neighbourhood quality, school ratings, local amenities, and market sentiment."),
    ("#DC3545", "🔴 Policy Implication: Supply Is the Real Lever",
     "The scenario analysis reveals something important: a 10% income increase moves predicted prices very little. A 15% rent increase moves them more. But neither change comes close to addressing the fundamental gap between prices and incomes. The regression confirms what housing economists already know — you cannot solve a supply problem with demand-side interventions like income subsidies."),
    ("#E67E22", "⚠️ Linear Regression Has Limits",
     "Housing markets are non-linear. Prices do not respond to income and rent in a perfectly straight line — there are thresholds, tipping points, and feedback loops. A gradient boosting or random forest model would likely improve prediction accuracy by capturing these non-linear interactions. The regression model here is the foundation, not the ceiling."),
]
for color, title, body in reg_findings:
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