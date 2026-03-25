import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from streamlit.components.v1 import html as st_html

st.set_page_config(
    page_title="Geospatial — Housing Analysis",
    page_icon="🗺️",
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
    .stRadio label { color: #1A1A2E !important; font-weight: 600 !important; }
    
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
CITY_COORDS = {
    'Chicago, IL':     {'lat': 41.8781, 'lon': -87.6298, 'state': 'IL'},
    'Houston, TX':     {'lat': 29.7604, 'lon': -95.3698, 'state': 'TX'},
    'Los Angeles, CA': {'lat': 34.0522, 'lon': -118.2437,'state': 'CA'},
    'Miami, FL':       {'lat': 25.7617, 'lon': -80.1918, 'state': 'FL'},
    'New York, NY':    {'lat': 40.7128, 'lon': -74.0060, 'state': 'NY'},
}

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    annual  = pd.read_csv(os.path.join(base, 'data/cleaned/annual_summary.csv'))
    cluster = pd.read_csv(os.path.join(base, 'data/cleaned/clustering_results.csv'))
    annual.columns = (annual.columns.str.strip().str.lower()
                      .str.replace(r'[^a-z0-9_]', '_', regex=True)
                      .str.strip('_'))
    return annual, cluster

annual_summary, clustering = load_data()

@st.cache_data
def build_geo(_annual, _clustering):
    rows = []
    for city, coords in CITY_COORDS.items():
        r2015 = _annual[(_annual['city']==city) & (_annual['year']==2015)]
        r2024 = _annual[(_annual['city']==city) & (_annual['year']==2024)]
        if len(r2015) == 0 or len(r2024) == 0:
            continue
        hv2015 = float(r2015['avg_home_value'].values[0])
        hv2024 = float(r2024['avg_home_value'].values[0])
        ai2024 = float(r2024['affordability_index'].values[0])
        rent   = float(r2024['avg_monthly_rent'].values[0])
        growth = ((hv2024 - hv2015) / hv2015) * 100
        cl_row = _clustering[_clustering['city'] == city]
        cluster_label = cl_row['cluster_label'].values[0] if len(cl_row) > 0 else 'N/A'
        rows.append({
            'city':          city,
            'city_short':    city.split(',')[0],
            'lat':           coords['lat'],
            'lon':           coords['lon'],
            'state':         coords['state'],
            'home_value':    hv2024,
            'affordability': ai2024,
            'rent':          rent,
            'growth_pct':    growth,
            'cluster':       cluster_label,
            'risk': ('HIGH RISK'     if ai2024 > 1.5 else
                     'MODERATE RISK' if ai2024 > 1.0 else 'LOW RISK')
        })
    return pd.DataFrame(rows)

geo_df = build_geo(annual_summary, clustering)

# LIGHT HEADER - UPDATED
st.markdown("""
<div style='background: linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%);
            padding:30px 35px; border-radius:14px; margin-bottom:28px;
            box-shadow:0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #E0E0E0;'>
    <p style='color:#1A1A2E!important; font-size:1.8rem; margin:0;
              font-weight:700; line-height:1.2;'>
         Geospatial Analysis
    </p>
    <p style='color:#4A4A5A!important; font-size:0.95rem;
              margin:10px 0 0 0; line-height:1.5;'>
        Four interactive maps visualising housing affordability patterns
        geographically — showing that this is not a uniform national
        crisis but a geographically concentrated one.
    </p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("###  Map Options")
    map_type = st.radio(
        "Select Map Type",
        ["Choropleth Map",
         "Bubble Map",
         "Interactive Folium Map",
         "Time Animation"]
    )
    st.markdown("---")
    map_descriptions = {
        "Choropleth Map":       "States coloured by affordability index. Green = affordable, red = crisis.",
        "Bubble Map":           "Bubble size = home value. Colour = affordability risk. Hover for full metrics.",
        "Interactive Folium Map": "Click any city marker for a full data popup.",
        "Time Animation":       "Press Play to watch affordability deteriorate year by year from 2015 to 2024."
    }
    st.markdown(f"** {map_descriptions[map_type]}**")

st.markdown(f"###  {map_type}")
st.markdown("""
<p class="section-desc">
Geography tells a story that tables and charts cannot.
The affordability crisis in the US is not spread evenly —
it is concentrated on the coasts, in cities with the most
restrictive zoning and the least available land.
Houston and Chicago prove that major metros can remain
affordable with different land use policies.
</p>
""", unsafe_allow_html=True)

if map_type == "Choropleth Map":
    fig = px.choropleth(
        geo_df, locations='state', locationmode='USA-states',
        color='affordability', hover_name='city_short',
        hover_data={'state': False, 'home_value': ':$,.0f',
                    'affordability': ':.3f',
                    'growth_pct': ':.1f', 'risk': True},
        color_continuous_scale=[
            [0.0, '#27AE60'], [0.5, '#F39C12'], [1.0, '#DC3545']],
        range_color=[0.5, 2.5], scope='usa',
        title='Housing Affordability Index by State (2024) — Green: Affordable | Red: Crisis',
        labels={'affordability': 'Affordability Index'}
    )
    fig.update_layout(
        height=540,
        paper_bgcolor='#F4F6F9',
        font=dict(color='#333333'),
        title_font=dict(color='#1A1A2E', size=13)
    )
    st.plotly_chart(fig, use_container_width=True)

elif map_type == "Bubble Map":
    fig = px.scatter_geo(
        geo_df, lat='lat', lon='lon',
        size='home_value', color='affordability',
        hover_name='city_short', text='city_short',
        hover_data={'lat': False, 'lon': False,
                    'home_value': ':$,.0f',
                    'affordability': ':.3f',
                    'growth_pct': ':.1f', 'risk': True},
        color_continuous_scale=[
            [0.0, '#27AE60'], [0.4, '#F39C12'], [1.0, '#DC3545']],
        size_max=60, scope='usa',
        title='Bubble Size = Home Value | Colour = Affordability Risk (2024)',
        labels={'affordability': 'Affordability Index',
                'home_value': 'Home Value ($)'}
    )
    fig.update_layout(
        height=540,
        geo=dict(projection_type='albers usa'),
        paper_bgcolor='#F4F6F9',
        font=dict(color='#333333'),
        title_font=dict(color='#1A1A2E', size=13)
    )
    fig.update_traces(textposition='top center',
                      textfont=dict(size=11, color='#1A1A2E'))
    st.plotly_chart(fig, use_container_width=True)

elif map_type == "Interactive Folium Map":
    map_file = '../assets/geospatial_interactive_map.html'
    if os.path.exists(map_file):
        with open(map_file, 'r', encoding='utf-8') as f:
            map_html = f.read()
        st_html(map_html, height=540)
    else:
        st.warning("Map file not found. Please run 05_geospatial.ipynb to generate it.")

elif map_type == "Time Animation":
    anim_file = '../assets/geospatial_animation.html'
    if os.path.exists(anim_file):
        with open(anim_file, 'r', encoding='utf-8') as f:
            anim_html = f.read()
        st_html(anim_html, height=600)
    else:
        st.warning("Animation file not found. Please run 05_geospatial.ipynb to generate it.")

st.markdown("---")

# City metrics table
st.markdown("###  City Metrics Summary (2024)")
st.markdown('<p class="section-desc">All key metrics for 2024, sorted from most to least unaffordable. Combines home values from Phase 1, risk classification from Phase 2, and cluster assignment from Phase 3.</p>', unsafe_allow_html=True)

display = geo_df[['city_short','home_value','rent',
                   'affordability','growth_pct','cluster','risk']].copy()
display.columns = ['City','Home Value ($)','Monthly Rent ($)',
                   'Affordability Index','10yr Growth (%)','Cluster','Risk Level']
display['Home Value ($)']   = display['Home Value ($)'].apply(lambda x: f'${x:,.0f}')
display['Monthly Rent ($)'] = display['Monthly Rent ($)'].apply(lambda x: f'${x:,.0f}')
display['10yr Growth (%)']  = display['10yr Growth (%)'].apply(lambda x: f'{x:.1f}%')
display['Risk Level'] = display['Risk Level'].apply(
    lambda x: f"🔴 {x}" if x=='HIGH RISK' else
              f"🟡 {x}" if x=='MODERATE RISK' else f"🟢 {x}")
st.dataframe(
    display.sort_values('Affordability Index', ascending=False),
    use_container_width=True, hide_index=True
)

st.markdown("---")

# Findings
st.markdown("###  Key Geospatial Findings")
geo_findings = [
    ("#DC3545", "🔴 The Crisis Is Geographically Concentrated on the Coasts",
     "Los Angeles and New York are both coastal cities with severe land constraints and restrictive zoning laws. Their affordability crisis is not primarily an income problem — it is a geography and policy problem. The maps make this visible instantly in a way that tables cannot."),
    ("#9B59B6", "📈 Miami Is the Transition Story",
     "The time animation is the most powerful visual in the entire project. Watch Miami's bubble shift from green in 2015 to amber by 2022 in real time. No chart or table communicates the speed of Miami's deterioration as clearly as watching it happen on the map year by year."),
    ("#27AE60", "🟢 The Midwest and South Show What Is Possible",
     "Chicago and Houston stay green on every map throughout the entire animation. They are not small cities — Chicago has 2.7 million people and Houston has 2.3 million. Their affordability is not a coincidence of size. It is a direct result of zoning policies, available land, and deliberate housing supply decisions."),
    ("#2980B9", "📍 Policy Needs to Be City-Specific — Not National",
     "The choropleth map makes the policy implication clear: three states are green and two are red or amber. A national housing policy that treats all cities the same will be too restrictive for Houston and too weak for Los Angeles. Solutions need to be tailored to the specific geography, zoning laws, and supply constraints of each market."),
]
for color, title, body in geo_findings:
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