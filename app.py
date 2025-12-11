import streamlit as st
import pandas as pd
import pydeck as pdk
from typing import Optional

# ====================
# 1. PAGE CONFIG
# ====================
st.set_page_config(
    page_title="SBI Bank Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. DATA
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

data = load_branch_data()

# ====================
# 3. CSS (Bootstrap-like + Color Theory + Smooth Animations)
# ====================
def inject_modern_ui():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* --- GENERAL --- */
    body, .stApp {
        font-family: 'Inter', sans-serif;
        background: #f4f7fa;
        color: #212529;
        margin:0;
        padding:0;
    }
    .block-container {
        padding: 24px 32px;
        max-width: 1400px;
        margin: auto;
    }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] h2 {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 20px;
    }
    [data-testid="stSidebar"] select, [data-testid="stSidebar"] input, [data-testid="stSidebar"] label {
        color: #212529;
        font-weight: 500;
    }

    /* --- METRIC CARDS --- */
    .metric-card {
        border-radius: 16px;
        padding: 24px;
        color: white;
        font-weight: 700;
        text-align: center;
        transition: transform 0.5s ease, box-shadow 0.5s ease;
        cursor: pointer;
        background: linear-gradient(135deg, #667eea, #764ba2);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    .metric-card.city {
        background: linear-gradient(135deg, #f7971e, #ffd200);
    }
    .metric-card:hover {
        transform: translateY(-10px) scale(1.03);
        box-shadow: 0 14px 35px rgba(0,0,0,0.25);
    }
    .metric-label {
        font-size: 1rem;
        color: rgba(255,255,255,0.8);
    }
    .metric-value {
        font-size: 2rem;
        margin-top: 8px;
    }

    /* --- TABLE --- */
    .stDataFrameWrapper {
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        background: white;
        font-size: 0.95rem;
    }
    .stDataFrameWrapper table {
        border-collapse: separate;
        border-spacing: 0 6px;
    }
    .stDataFrameWrapper th {
        background: #667eea;
        color: white;
        font-weight: 600;
        padding: 12px;
        text-align: left;
    }
    .stDataFrameWrapper td {
        background: #f8f9ff;
        padding: 10px;
        color: #212529;
    }
    .stDataFrameWrapper tr:hover td {
        background: #e0e7ff;
        transition: background 0.3s;
    }

    /* --- HEADER --- */
    .stApp h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .stApp p {
        font-size: 1rem;
        color: #6c757d;
        margin-top: 0;
        margin-bottom: 24px;
    }

    /* --- BUTTONS --- */
    .stButton>button {
        background: linear-gradient(135deg,#667eea,#764ba2);
        color: white;
        border-radius: 12px;
        padding: 10px 16px;
        font-weight: 600;
        transition: transform 0.4s, box-shadow 0.4s;
    }
    .stButton>button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }

    /* --- MAP TOOLTIP --- */
    .map-tooltip {
        font-family: 'Inter', sans-serif;
        border-radius: 10px;
        padding: 12px;
        background: linear-gradient(180deg,#667eea,#764ba2);
        color: white;
        border: none;
        box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

inject_modern_ui()

# ====================
# 4. MAP LAYER
# ====================
def create_3d_icon_layer(data: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Layer:
    ICON_DATA = {"url": "https://cdn-icons-png.flaticon.com/512/684/684908.png", "width": 128, "height": 128, "anchorY":128}
    data = data.copy()
    data["icon_data"] = [ICON_DATA]*len(data)
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
        get_color=[102,126,234,200],
        highlight_color=[255,255,255,200]
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
# 5. METRIC CARDS
# ====================
def render_metric_cards(data: pd.DataFrame):
    col1, col2 = st.columns(2, gap="large")
    total_branches = len(data)
    cities = data["City"].nunique()
    with col1:
        st.markdown(f"""<div class="metric-card"><div class="metric-label">Total Branches</div><div class="metric-value">{total_branches}</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class="metric-card city"><div class="metric-label">Cities Covered</div><div class="metric-value">{cities}</div></div>""", unsafe_allow_html=True)

# ====================
# 6. MAIN DASHBOARD
# ====================
def main():
    st.sidebar.title("SBI Dashboard")
    selected_branch = st.sidebar.selectbox("Focus on Branch", options=["All Branches"] + list(data["Branch"].unique()))
    map_pitch = st.sidebar.slider("3D Tilt", 0, 60, 45)
    map_zoom = st.sidebar.slider("Zoom Level", 5, 20, 11)

    st.markdown("<h1>SBI Bank Network Intelligence</h1><p>Modern 3D dashboard with smooth gradients and animations</p>", unsafe_allow_html=True)

    render_metric_cards(data)
    st.divider()
    st.pydeck_chart(create_map_view(data, selected_branch, pitch=map_pitch, zoom=map_zoom), use_container_width=True)
    st.divider()
    st.markdown("### Branch Network Details")
    st.dataframe(data, use_container_width=True)

if __name__=="__main__":
    main()
