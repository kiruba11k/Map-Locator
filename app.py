import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import os
from typing import Optional, Dict, Any

# ====================
# 1. INITIALIZATION & CONFIG
# ====================
@st.cache_resource
def load_design_tokens() -> Dict[str, Any]:
    return {
        "color": {
            "primary": {"500": "#0d6efd", "700": "#0a58ca"},
            "surface": {"0": "#ffffff", "1": "#f8f9fa"},
            "text": {"primary": "#212529", "secondary": "#6c757d"},
            "accent": {"success": "#198754", "warning": "#ffc107", "danger": "#dc3545"}
        },
        "spacing": {"base": "8px"},
        "typography": {
            "heading": {"lg": "1.5rem", "md": "1.125rem"},
            "body": {"md": "1rem", "sm": "0.875rem"}
        },
        "elevation": {"shadow": {"md": "0 4px 12px rgba(0,0,0,0.1)", "lg": "0 8px 24px rgba(0,0,0,0.15)"}}
    }

TOKENS = load_design_tokens()

PRIMARY = TOKENS["color"]["primary"]["500"]
PRIMARY_DARK = TOKENS["color"]["primary"]["700"]
SURFACE_0 = TOKENS["color"]["surface"]["0"]
SURFACE_1 = TOKENS["color"]["surface"]["1"]
TEXT_PRIMARY = TOKENS["color"]["text"]["primary"]
TEXT_SECONDARY = TOKENS["color"]["text"]["secondary"]
SHADOW_MD = TOKENS["elevation"]["shadow"]["md"]
SHADOW_LG = TOKENS["elevation"]["shadow"]["lg"]

st.set_page_config(
    page_title="SBI Bank Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. CUSTOM CSS FOR MODERN LIGHT UI
# ====================
def inject_light_ui():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    .stApp {{
        font-family: 'Inter', sans-serif;
        background: {SURFACE_1};
        color: {TEXT_PRIMARY};
    }}
    .block-container {{
        padding: 24px 32px;
        max-width: 1400px;
        margin: auto;
    }}
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {SURFACE_0};
        padding: 20px;
        box-shadow: {SHADOW_MD};
        border-radius: 12px;
    }}
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {{
        color: {PRIMARY};
    }}
    /* Metric cards */
    .metric-card {{
        background: {SURFACE_0};
        border-radius: 12px;
        padding: 20px;
        box-shadow: {SHADOW_MD};
        transition: transform 0.3s, box-shadow 0.3s;
        cursor: default;
    }}
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: {SHADOW_LG};
    }}
    .metric-label {{
        font-size: 0.875rem;
        color: {TEXT_SECONDARY};
    }}
    .metric-value {{
        font-size: 1.5rem;
        font-weight: 600;
        color: {PRIMARY_DARK};
        margin-top: 8px;
    }}
    /* Table */
    .stDataFrameWrapper {{
        background: {SURFACE_0};
        border-radius: 12px;
        padding: 12px;
        box-shadow: {SHADOW_MD};
    }}
    </style>
    """, unsafe_allow_html=True)

# ====================
# 3. LOAD DATA
# ====================
@st.cache_data
def load_branch_data() -> pd.DataFrame:
    return pd.DataFrame({
        "Branch": ["PANATHUR", "BELLANDUR", "BELLANDUR-OUTER", "DOMLUR", "BRIGADE METROPOLIS"],
        "IFSC_Code": ["SBIN0017040", "SBIN0015647", "SBIN0041171", "SBIN0016877", "SBIN0015034"],
        "Address": [
            "No.132 By 8, Panathur Junction, Marathahalli",
            "Surajpur Main Road, Kaikondrahalli, Bellandur",
            "Thanush Arcade, Outer Ring Road, near Coffee Shop",
            "Gurmukh Singh Commercial Complex, Domlur",
            "MS Brigade Enterprises, Whitefield Road"
        ],
        "City": ["BANGALORE"] * 5,
        "State": ["KARNATAKA"] * 5,
        "Pincode": ["560037", "560035", "560103", "560071", "560016"],
        "Country": ["India"] * 5,
        "Latitude": [12.9382107, 12.9188658, 12.9246927, 12.9534312, 12.9927608],
        "Longitude": [77.6992385, 77.6700914, 77.672937, 77.6406167, 77.7021471],
    })

# ====================
# 4. MAP FUNCTIONS
# ====================
def create_3d_icon_layer(data: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Layer:
    ICON_DATA = {"url": "https://cdn-icons-png.flaticon.com/512/684/684908.png", "width": 128, "height": 128, "anchorY": 128}
    data = data.copy()
    data["icon_data"] = [ICON_DATA] * len(data)
    data["icon_size"] = 1.2
    if selected_branch and selected_branch != "All Branches":
        data["icon_size"] = data.apply(lambda r: r["icon_size"]*1.6 if r["Branch"]==selected_branch else r["icon_size"]*0.9, axis=1)
    return pdk.Layer(
        "IconLayer",
        data=data,
        pickable=True,
        auto_highlight=True,
        get_icon="icon_data",
        get_size="icon_size",
        get_position=["Longitude","Latitude"],
        size_scale=20,
        get_color=[13,110,253,200],
        highlight_color=[255,255,255,180]
    )

def create_map_view(data: pd.DataFrame, selected_branch: Optional[str]=None, pitch:int=50, zoom:int=11) -> pdk.Deck:
    layers = [create_3d_icon_layer(data, selected_branch)]
    lat, lon = float(data["Latitude"].mean()), float(data["Longitude"].mean())
    if selected_branch and selected_branch != "All Branches":
        s = data[data["Branch"]==selected_branch]
        if not s.empty: lat, lon = float(s["Latitude"].iloc[0]), float(s["Longitude"].iloc[0]); zoom=14
    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=pitch)
    return pdk.Deck(layers=layers, initial_view_state=view_state, map_style="light", tooltip={"html": "<b>{Branch}</b><br>{Address}"}, width="100%", height=640)

# ====================
# 5. DASHBOARD COMPONENTS
# ====================
def render_metric_cards(data: pd.DataFrame):
    col1, col2 = st.columns(2, gap="large")
    total_branches = len(data)
    cities = data["City"].nunique()
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Total Branches</div><div class="metric-value">{total_branches}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Cities Covered</div><div class="metric-value">{cities}</div></div>""", unsafe_allow_html=True)

def render_branch_table(data: pd.DataFrame):
    st.markdown("### Branch Network Details")
    st.dataframe(data, use_container_width=True)

# ====================
# 6. MAIN
# ====================
def main():
    inject_light_ui()
    data = load_branch_data()

    st.sidebar.markdown(f"<h2 style='color:{PRIMARY}'>SBI Dashboard</h2>", unsafe_allow_html=True)
    selected_branch = st.sidebar.selectbox("Focus on Branch", options=["All Branches"] + list(data["Branch"].unique()))
    map_pitch = st.sidebar.slider("3D Tilt", 0, 60, 45)
    map_zoom = st.sidebar.slider("Zoom Level", 5, 20, 11)

    st.markdown(f"<h1 style='color:{PRIMARY}'>SBI Bank Network Intelligence</h1><p style='color:{TEXT_SECONDARY}'>Modern light-themed 3D dashboard</p>", unsafe_allow_html=True)

    render_metric_cards(data)
    st.divider()
    st.pydeck_chart(create_map_view(data, selected_branch, pitch=map_pitch, zoom=map_zoom), use_container_width=True)
    st.divider()
    render_branch_table(data)

if __name__=="__main__":
    main()
