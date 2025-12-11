import streamlit as st
import pandas as pd
import pydeck as pdk

# ====================
# 1. PAGE CONFIGURATION
# ====================
st.set_page_config(
    page_title="SBI Bank Network - 3D Dashboard",
    page_icon="",
    layout="wide"
)

# ====================
# 2. APPLY SMOOTH, PROFESSIONAL STYLING
# ====================
st.markdown("""
    <style>
    /* Smooth background gradient */
    .stApp {
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%);
        color: #ffffff;
    }
    /* Elegant title styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #00b4db, #0083b0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #a1d6f5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    /* Smooth card transitions */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px;
        border-left: 5px solid #0083b0;
        transition: transform 0.3s ease-in-out;
    }
    .stMetric:hover {
        transform: translateY(-5px);
        background-color: rgba(255, 255, 255, 0.12);
    }
    /* Custom button styling */
    .stButton > button {
        background: linear-gradient(to right, #00b4db, #0083b0);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 131, 176, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# ====================
# 3. YOUR SAMPLE DATA (Integrated)
# ====================
data = pd.DataFrame({
    "Branch": ["PANATHUR", "BELLANDUR", "BELLANDUR", "PANATHUR", "BRIGADE METROPOLIS"],
    "IFSC_Code": ["SBIN0017040", "SBIN0015647", "SBIN0041171", "SBIN0016877", "SBIN0015034"],
    "Address": ["SBI BANK,NO.132 BY 8,PANATHUR JUNCTION,PANATHUR,MARATHAHALLI",
                "SBI BANK, SURAJPUR MAIN ROAD, KAIKONDRAHALLI, BELANDUR WARD",
                "SBI BANK,THANUSH ARCADE, BELLANDUR OUTER RING ROAD,NEXT TO COFFEE DAY",
                "SBI BANK,NO. 535, GURMUKH SINGH COMMERCIAL COMPLEX, AMARJYOTHI H.B.C.S. LAYOUT, DOMLUR",
                "SBI BANK,MS BRIGADE ENTERPRISES, WHITEFIELD ROAD"],
    "City": ["BANGALORE"] * 5,
    "State": ["KARNATAKA"] * 5,
    "Pincode": ["560037", "560035", "560103", "560071", "560016"],
    "Country": ["India"] * 5,
    "Latitude": [12.9382107, 12.9188658, 12.9246927, 12.9534312, 12.9927608],
    "Longitude": [77.6992385, 77.6700914, 77.672937, 77.6406167, 77.7021471]
})

# ====================
# 4. DASHBOARD HEADER
# ====================
st.markdown('<h1 class="main-header"> SBI Bank Network - 3D Intelligence Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore the branch network with immersive 3D visualization and real-time insights</p>', unsafe_allow_html=True)

# ====================
# 5. INTERACTIVE CONTROLS SIDEBAR
# ====================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2830/2830284.png", width=80) # Optional: Add an SBI logo
    st.title("Dashboard Controls")

    # Branch Selector with smooth transition effect
    selected_branch = st.selectbox(
        " Focus on a Branch",
        options=['All Branches'] + list(data['Branch'].unique()),
        help="Select a branch to zoom and highlight on the map."
    )

    # 3D Effect Slider
    elevation_scale = st.slider(
        " 3D Extrusion Height",
        min_value=50,
        max_value=1000,
        value=300,
        step=50,
        help="Control the height of the 3D bars for visual impact."
    )

    # Animated Icons Toggle
    show_animation = st.toggle("✨ Enable Point Animations", value=True)

    # Color Theme Selector
    color_theme = st.selectbox(
        " Map Color Theme",
        options=["Light", "Dark", "Satellite", "Custom Gradient"]
    )

# ====================
# 6. KEY METRICS - Animated Cards
# ====================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Branches", value=f"{len(data):,}", delta="5 Locations")
with col2:
    st.metric(label="Cities Covered", value=data['City'].nunique(), delta="1 City")
with col3:
    st.metric(label="Avg. Latitude", value=f"{data['Latitude'].mean():.4f}")
with col4:
    st.metric(label="Avg. Longitude", value=f"{data['Longitude'].mean():.4f}")

# ====================
# 7. CORE 3D MAP VISUALIZATION
# ====================
st.subheader(" Interactive 3D Branch Map")

# Prepare data for the selected branch
if selected_branch != 'All Branches':
    view_data = data[data['Branch'] == selected_branch]
    view_state_lat = view_data['Latitude'].iloc[0]
    view_state_lon = view_data['Longitude'].iloc[0]
    zoom_level = 13
else:
    view_data = data
    view_state_lat = data['Latitude'].mean()
    view_state_lon = data['Longitude'].mean()
    zoom_level = 11

# Define the Pydeck 3D Layer (Column Layer for "pins")
layer = pdk.Layer(
    "ColumnLayer",  # Creates 3D cylindrical columns
    data=view_data,
    get_position=['Longitude', 'Latitude'],
    get_elevation="100",  # Base elevation value
    elevation_scale=elevation_scale,  # Controlled by the slider
    radius=150,  # Radius of each column in meters
    get_fill_color=[0, 180, 219, 200],  # RGB for #00b4db with transparency
    pickable=True,  # Enables tooltips on click/hover
    auto_highlight=True,  # Smooth highlight on hover
    extruded=True,  # Makes it a 3D shape
    transitions={
        'get_elevation': 1000,  # Animation duration for height change in ms
        'get_fill_color': 1000,  # Animation duration for color change
    }
)

# Define the initial view of the map
view_state = pdk.ViewState(
    latitude=view_state_lat,
    longitude=view_state_lon,
    zoom=zoom_level,
    pitch=50,  # Tilts the map for a 3D perspective (0 = top-down, 60 is very tilted)
    bearing=0   # Rotation (0 = North up)
)

# Render the map in Streamlit
st.pydeck_chart(
    pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='dark',  # Matches the dark theme. Can also be 'light', 'road', 'satellite', etc.
        tooltip={
            "html": """
            <b>{Branch}</b><br/>
            <b>IFSC:</b> {IFSC_Code}<br/>
            <b>Address:</b> {Address}<br/>
            <b>Pincode:</b> {Pincode}
            """,
            "style": {
                "backgroundColor": "#0f2027",
                "color": "white",
                "borderRadius": "5px",
                "padding": "10px"
            }
        }
    )
)

# ====================
# 8. DATA TABLE WITH INTERACTIVITY
# ====================
st.subheader(" Branch Details Table")
# Use an interactive data editor for a modern feel
edited_df = st.data_editor(
    data,
    use_container_width=True,
    column_config={
        "IFSC_Code": st.column_config.TextColumn("IFSC Code", width="medium"),
        "Latitude": st.column_config.NumberColumn(format="%.6f"),
        "Longitude": st.column_config.NumberColumn(format="%.6f"),
    },
    hide_index=True,
    num_rows="dynamic"
)

