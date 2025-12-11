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
            "Panathur Junction, Marathahalli",
            "Kaikondrahalli, Bellandur",
            "Outer Ring Road, Bellandur",
            "Complex, Domlur",
            "Whitefield Road"
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
# 3. MODERN UI (Google Fonts + Your Palette + Bootstrap Feel)
# ====================
def inject_modern_ui():
    st.markdown("""
    <style>
    /* GOOGLE FONT — clean + visible */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

    :root {
        --deep-twilight: #03045e;
        --french-blue: #023e8a;
        --bright-teal-blue: #0077b6;
        --blue-green: #0096c7;
        --turquoise-surf: #00b4d8;
        --sky-aqua: #48cae4;
        --frosted-blue: #90e0ef;
        --frosted-blue-2: #ade8f4;
        --light-cyan: #caf0f8;
    }

    /* GLOBAL */
    body, .stApp {
        font-family: 'Poppins', sans-serif;
        background: var(--light-cyan);
        color: #012a4a;
    }

    .block-container {
        padding: 24px 40px;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--deep-twilight), var(--bright-teal-blue));
        color: white;
        padding: 22px;
        border-radius: 0px 16px 16px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }

    [data-testid="stSidebar"] h2 {
        font-weight: 600;
        margin-bottom: 18px;
        color: white;
    }

    /* NAV HEADER */
    .top-header {
        padding: 20px 10px;
        text-align: left;
    }
    .top-header h1 {
        font-size: 2.6rem;
        font-weight: 700;
        background: linear-gradient(90deg, var(--deep-twilight), var(--blue-green));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    /* METRIC CARDS */
    .metric-card {
        padding: 22px;
        border-radius: 18px;
        background: linear-gradient(135deg, var(--bright-teal-blue), var(--sky-aqua));
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        transition: 0.4s ease;
    }
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.25);
    }

    .metric-label {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
    }

    /* TABLE */
    .stDataFrameWrapper {
        border-radius: 18px;
        overflow: hidden;
        background: white;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }

    .stDataFrame table {
        font-size: 0.95rem;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, var(--deep-twilight), var(--blue-green));
        color: white;
        border-radius: 12px;
        padding: 8px 14px;
        font-weight: 600;
        transition: 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.04);
        box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    }

    /* MAP TOOLTIP */
    .map-tooltip {
        background: var(--bright-teal-blue);
        color: white;
        padding: 10px;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

inject_modern_ui()

# ====================
# 4. MAP VIEWS
# ====================
MAP_STYLES = {
    "Light": "light",
    "Dark": "dark",
    "Road": "mapbox://styles/mapbox/streets-v11",
    "Satellite": "mapbox://styles/mapbox/satellite-streets-v11"
}

def create_map(data: pd.DataFrame, selected_branch: Optional[str], pitch, zoom, style):
    ICON_DATA = {
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128, "height": 128, "anchorY": 128
    }

    df = data.copy()
    df["icon_data"] = [ICON_DATA] * len(df)
    df["icon_size"] = 1.2

    if selected_branch != "All Branches":
        df["icon_size"] = df.apply(
            lambda r: 1.9 if r["Branch"] == selected_branch else 0.8, axis=1
        )

    layer = pdk.Layer(
        "IconLayer",
        data=df,
        get_icon="icon_data",
        get_size="icon_size",
        size_scale=20,
        get_position=["Longitude", "Latitude"],
        pickable=True,
        auto_highlight=True,
    )

    center_lat = df["Latitude"].mean()
    center_lon = df["Longitude"].mean()

    if selected_branch != "All Branches":
        selected = df[df["Branch"] == selected_branch]
        if not selected.empty:
            center_lat = selected["Latitude"].iloc[0]
            center_lon = selected["Longitude"].iloc[0]
            zoom = 14

    view = pdk.ViewState(latitude=center_lat, longitude=center_lon, zoom=zoom, pitch=pitch)

    return pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        map_style=MAP_STYLES[style],
        tooltip={"html": "<b>{Branch}</b><br>{Address}"}
    )

# ====================
# 5. METRIC CARDS
# ====================
def render_metrics(df):
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Branches</div>
            <div class="metric-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cities Covered</div>
            <div class="metric-value">{df['City'].nunique()}</div>
        </div>
        """, unsafe_allow_html=True)

# ====================
# 6. MAIN APP
# ====================
def main():
    st.sidebar.title("Navigation")

    selected_branch = st.sidebar.selectbox(
        "Focus Branch", ["All Branches"] + list(data["Branch"])
    )

    map_view = st.sidebar.selectbox("Map View", ["Light", "Dark", "Road", "Satellite"])
    pitch = st.sidebar.slider("3D Tilt", 0, 60, 40)
    zoom = st.sidebar.slider("Zoom", 5, 20, 11)

    st.markdown("""
        <div class="top-header">
            <h1>SBI Network Dashboard</h1>
        </div>
    """, unsafe_allow_html=True)

    render_metrics(data)
    st.divider()

    st.pydeck_chart(
        create_map(data, selected_branch, pitch, zoom, map_view),
        use_container_width=True
    )

    st.divider()
    st.markdown("### Branch Details")
    st.dataframe(data, use_container_width=True)

if __name__ == "__main__":
    main()
