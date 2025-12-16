import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
import json
import time
import io
from typing import Optional, List, Dict, Any
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ====================
# 1. PAGE CONFIG
# ====================
st.set_page_config(
    page_title="SBI Bank Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. CONSTANTS & CONFIG
# ====================
APIFY_API_URL = "https://api.apify.com/v2/acts/powerai~google-map-nearby-search-scraper/run-sync-get-dataset-items"
APIFY_TOKEN = st.secrets.get("TOKEN")  # Replace with your actual token

# Common POI categories
POI_CATEGORIES = {
    "Education": ["college", "university", "school", "educational institute"],
    "Business": ["tech park", "business park", "office", "corporate office", "startup"],
    "Healthcare": ["hospital", "clinic", "medical center"],
    "Retail": ["shopping mall", "market", "mall"],
    "Food": ["restaurant", "cafe", "food court"],
    "Government": ["government office", "municipal office"],
    "Banking": ["bank", "atm", "financial institution"]
}

# ====================
# 3. DATA FUNCTIONS
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

def get_selected_branches_data(selected_branches: List[str]) -> pd.DataFrame:
    """Get data for selected branches."""
    data = load_branch_data()
    if "All Branches" in selected_branches:
        return data
    return data[data['Branch'].isin(selected_branches)]

# ====================
# 4. POI SEARCH FUNCTIONS
# ====================
def search_poi_apify(query: str, lat: float, lng: float, max_items: int = 50, 
                    country: str = "IN", lang: str = "en", zoom: int = 12) -> List[Dict]:
    """Search for POI using Apify API."""
    
    payload = {
        "query": query,
        "lat": str(lat),
        "lng": str(lng),
        "maxItems": max_items,
        "country": country,
        "lang": lang,
        "zoom": zoom
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        params = {"token": APIFY_TOKEN}
        
        with st.spinner(f"Searching for {query} near location..."):
            response = requests.post(
                APIFY_API_URL,
                params=params,
                json=payload,
                headers=headers,
                timeout=30
            )
            
        if response.status_code in [200, 201]:
            results = response.json()
            # Add source info
            for item in results:
                item['search_query'] = query
                item['search_center_lat'] = lat
                item['search_center_lng'] = lng
                item['distance_km'] = calculate_distance(
                    lat, lng, 
                    item.get('latitude', lat), 
                    item.get('longitude', lng)
                )
            return results
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        st.error(f"Error searching POI: {str(e)}")
        return []

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in kilometers."""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def search_multiple_branches_poi(selected_branches: List[str], query: str, 
                               max_items_per_branch: int = 30) -> pd.DataFrame:
    """Search POI for multiple branches and combine results."""
    all_results = []
    branch_data = get_selected_branches_data(selected_branches)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, (idx, branch) in enumerate(branch_data.iterrows()):
        status_text.text(f"Searching near {branch['Branch']}... ({i+1}/{len(branch_data)})")
        
        results = search_poi_apify(
            query=query,
            lat=branch['Latitude'],
            lng=branch['Longitude'],
            max_items=max_items_per_branch
        )
        
        # Add branch info to each result
        for result in results:
            result['source_branch'] = branch['Branch']
            result['source_ifsc'] = branch['IFSC_Code']
            result['source_address'] = branch['Address']
        
        all_results.extend(results)
        
        progress_bar.progress((i + 1) / len(branch_data))
        time.sleep(0.5)  # Rate limiting
    
    progress_bar.empty()
    status_text.empty()
    
    if all_results:
        return pd.DataFrame(all_results)
    return pd.DataFrame()

# ====================
# 5. VISUALIZATION FUNCTIONS
# ====================
def create_poi_map(branch_data: pd.DataFrame, poi_data: pd.DataFrame) -> pdk.Deck:
    """Create map showing branches and POIs."""
    layers = []
    
    # Branch layer
    branch_layer = pdk.Layer(
        "ScatterplotLayer",
        data=branch_data,
        get_position=['Longitude', 'Latitude'],
        get_radius=200,
        get_fill_color=[0, 0, 255, 200],
        pickable=True,
        auto_highlight=True,
        radius_min_pixels=8,
        radius_max_pixels=20,
    )
    layers.append(branch_layer)
    
    # POI layer
    if not poi_data.empty:
        # Color POIs by category
        poi_data = poi_data.copy()
        poi_data['color'] = poi_data['types'].apply(lambda x: get_poi_color(x))
        
        poi_layer = pdk.Layer(
            "ScatterplotLayer",
            data=poi_data,
            get_position=['longitude', 'latitude'],
            get_radius=150,
            get_fill_color='color',
            pickable=True,
            auto_highlight=True,
            radius_min_pixels=6,
            radius_max_pixels=16,
        )
        layers.append(poi_layer)
    
    # Calculate view state
    if not branch_data.empty:
        center_lat = branch_data['Latitude'].mean()
        center_lon = branch_data['Longitude'].mean()
        zoom = 11
    else:
        center_lat = 12.9716
        center_lon = 77.5946
        zoom = 10
    
    view_state = pdk.ViewState(
        latitude=center_lat,
        longitude=center_lon,
        zoom=zoom,
        pitch=40
    )
    
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style='light',
        tooltip={
            "html": """
            {% if layer.id.includes('branch') %}
                <b>Branch: {Branch}</b><br>
                IFSC: {IFSC_Code}<br>
                Address: {Address}
            {% else %}
                <b>{name}</b><br>
                Address: {full_address}<br>
                Rating: {rating}/5<br>
                Distance: {distance_km:.1f} km
            {% endif %}
            """
        }
    )

def get_poi_color(types: str) -> List[int]:
    """Get color based on POI type."""
    types_str = str(types).lower()
    
    if any(word in types_str for word in ['college', 'university', 'school']):
        return [255, 0, 0, 200]  # Red for education
    elif any(word in types_str for word in ['tech', 'office', 'corporate']):
        return [0, 255, 0, 200]  # Green for business
    elif any(word in types_str for word in ['hospital', 'clinic', 'medical']):
        return [255, 255, 0, 200]  # Yellow for healthcare
    elif any(word in types_str for word in ['mall', 'shopping', 'market']):
        return [255, 0, 255, 200]  # Magenta for retail
    elif any(word in types_str for word in ['restaurant', 'cafe', 'food']):
        return [255, 165, 0, 200]  # Orange for food
    else:
        return [128, 128, 128, 200]  # Gray for others


def create_poi_analysis_chart(poi_data: pd.DataFrame):
    """Create analysis charts for POI data."""
    if poi_data.empty:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # POI type distribution - FIXED
        if 'types' in poi_data.columns:
            # Flatten lists to get individual types
            all_types = []
            for type_list in poi_data['types'].dropna():
                if isinstance(type_list, list):
                    all_types.extend(type_list)
                else:
                    all_types.append(str(type_list))
            
            # Count frequency of each type
            from collections import Counter
            type_counts = Counter(all_types)
            
            # Get top 10 types
            top_types = dict(type_counts.most_common(10))
            
            fig1 = px.pie(
                values=list(top_types.values()),
                names=list(top_types.keys()),
                title="Top 10 POI Types"
            )
            st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Rating distribution (unchanged)
        if 'rating' in poi_data.columns:
            poi_data['rating'] = pd.to_numeric(poi_data['rating'], errors='coerce')
            fig2 = px.histogram(
                poi_data.dropna(subset=['rating']),
                x='rating',
                nbins=20,
                title="Rating Distribution"
            )
            st.plotly_chart(fig2, use_container_width=True)
            

def extract_main_type(types_str: str) -> str:
    """Extract main type from types array string."""
    try:
        types = eval(types_str) if isinstance(types_str, str) else types_str
        if isinstance(types, list) and types:
            return types[0]
    except:
        pass
    return "Unknown"
def clean_poi_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and validate POI data from Apify API."""
    if df.empty:
        return df
    
    df_clean = df.copy()
    
    # Ensure rating is numeric
    if 'rating' in df_clean.columns:
        df_clean['rating'] = pd.to_numeric(df_clean['rating'], errors='coerce')
    
    # Ensure distance_km is numeric
    if 'distance_km' in df_clean.columns:
        df_clean['distance_km'] = pd.to_numeric(df_clean['distance_km'], errors='coerce')
    
    # Convert any string representations of lists to actual lists for 'types'
    if 'types' in df_clean.columns:
        def parse_types(val):
            if isinstance(val, list):
                return val
            elif isinstance(val, str):
                try:
                    # Handle string representation of list
                    import ast
                    return ast.literal_eval(val)
                except:
                    return [val]
            return []
        
        df_clean['types'] = df_clean['types'].apply(parse_types)
    
    return df_clean
# ====================
# 6. EXPORT FUNCTIONS
# ====================
def export_data(df: pd.DataFrame, format: str = 'csv'):
    """Export data in specified format."""
    if df.empty:
        return None
    
    if format == 'csv':
        return df.to_csv(index=False).encode('utf-8')
    elif format == 'json':
        return df.to_json(orient='records', indent=2).encode('utf-8')
    elif format == 'excel':
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='POI_Data')
        return output.getvalue()
    return None

# ====================
# 7. MODERN UI STYLING
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

    [data-testid="stSidebar"] h3 {
        color: var(--light-cyan);
        margin-top: 20px;
        margin-bottom: 10px;
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

    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: var(--light-cyan);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 12px 24px;
        border-radius: 8px 8px 0 0;
        background-color: var(--frosted-blue-2);
        color: var(--deep-twilight);
        font-weight: 600;
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--blue-green) !important;
        color: white !important;
    }

    /* BUTTONS */
    .stButton>button {
        background: linear-gradient(135deg, var(--deep-twilight), var(--blue-green));
        color: white;
        border-radius: 12px;
        padding: 8px 14px;
        font-weight: 600;
        transition: 0.3s ease;
        border: none;
    }
    .stButton>button:hover {
        transform: scale(1.04);
        box-shadow: 0 8px 18px rgba(0,0,0,0.25);
    }

    /* SEARCH RESULT CARDS */
    .poi-card {
        background: white;
        border-radius: 12px;
        padding: 16px;
        margin: 10px 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border-left: 4px solid var(--blue-green);
    }

    .poi-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--deep-twilight);
        margin-bottom: 8px;
    }

    .poi-detail {
        font-size: 0.9rem;
        color: #666;
        margin: 4px 0;
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

    /* MAP TOOLTIP */
    .map-tooltip {
        background: var(--bright-teal-blue);
        color: white;
        padding: 10px;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# ====================
# 8. MAP FUNCTIONS
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
        tooltip={"html": "<b>{Branch}</b><br>{Address}<br>IFSC: {IFSC_Code}"}
    )

# ====================
# 9. METRIC CARDS
# ====================
def render_metrics(df):
    c1, c2, c3, c4 = st.columns(4)
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
    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Area Coverage</div>
            <div class="metric-value">{(df['Latitude'].max() - df['Latitude'].min()):.2f}°</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Last Updated</div>
            <div class="metric-value">Now</div>
        </div>
        """, unsafe_allow_html=True)

# ====================
# 10. MAIN APPLICATION
# ====================
def main():
    # Inject CSS
    inject_modern_ui()
    
    # Load data
    data = load_branch_data()
    
    # Session state for POI results
    if 'poi_results' not in st.session_state:
        st.session_state.poi_results = pd.DataFrame()
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []
    
    # ===== SIDEBAR =====
    st.sidebar.title(" Navigation")
    
    # Branch selection for main map
    selected_branch = st.sidebar.selectbox(
        "Focus Branch", ["All Branches"] + list(data["Branch"])
    )
    
    # Map controls
    st.sidebar.markdown("###  Map Controls")
    map_view = st.sidebar.selectbox("Map Style", list(MAP_STYLES.keys()))
    pitch = st.sidebar.slider("3D Tilt", 0, 60, 40)
    zoom = st.sidebar.slider("Zoom Level", 5, 20, 11)
    
    # POI Search in sidebar
    st.sidebar.markdown("###  POI Search")
    
    # Quick search category
    quick_search = st.sidebar.selectbox(
        "Quick Search Category",
        ["Select category..."] + list(POI_CATEGORIES.keys())
    )
    
    # Custom search
    custom_query = st.sidebar.text_input("Custom Search Query", placeholder="e.g., coffee shops, gyms, parks")
    
    # Branch selection for POI search
    st.sidebar.markdown("###  Select Branches")
    all_branches = ["All Branches"] + list(data["Branch"])
    selected_poi_branches = st.sidebar.multiselect(
        "Search near these branches:",
        all_branches,
        default=["All Branches"]
    )
    
    # Search radius
    search_radius = st.sidebar.slider("Search Radius (km)", 1, 10, 3)
    max_results = st.sidebar.slider("Max Results per Branch", 10, 100, 30)
    
    # Manual coordinates search
    st.sidebar.markdown("###  Manual Search")
    manual_search = st.sidebar.checkbox("Search at specific coordinates")
    
    manual_lat, manual_lon = None, None
    if manual_search:
        col1, col2 = st.sidebar.columns(2)
        with col1:
            manual_lat = st.number_input("Latitude", value=12.9716, format="%.6f")
        with col2:
            manual_lon = st.number_input("Longitude", value=77.5946, format="%.6f")
    
    # Search button
    search_query = ""
    if quick_search != "Select category...":
        search_query = POI_CATEGORIES[quick_search][0]
    elif custom_query:
        search_query = custom_query
    
    search_clicked = st.sidebar.button(
        " Search POI",
        type="primary",
        use_container_width=True,
        disabled=not search_query
    )
    
    # Clear results button
    if st.sidebar.button(" Clear Results", use_container_width=True):
        st.session_state.poi_results = pd.DataFrame()
        st.rerun()
    
    # ===== MAIN CONTENT =====
    st.markdown("""
        <div class="top-header">
            <h1> SBI Network Dashboard</h1>
            <p style="color: var(--french-blue); font-size: 1.1rem; margin-top: 0.5rem;">
                Branch Network & POI Intelligence Platform
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([" Branch Network", " POI Search Results", " POI Analysis"])
    
    # ===== TAB 1: BRANCH NETWORK =====
    with tab1:
        render_metrics(data)
        st.divider()
        
        # Map
        st.pydeck_chart(
            create_map(data, selected_branch, pitch, zoom, map_view),
            use_container_width=True
        )
        
        st.divider()
        st.markdown("###  Branch Details")
        st.dataframe(data, use_container_width=True)
    
    # ===== SEARCH EXECUTION =====
    if search_clicked and search_query:
        with st.spinner("Searching for Points of Interest..."):
            if manual_search and manual_lat and manual_lon:
                # Manual coordinate search
                results = search_poi_apify(
                    query=search_query,
                    lat=manual_lat,
                    lng=manual_lon,
                    max_items=max_results
                )
                if results:
                    df_results = pd.DataFrame(results)
                    df_results['source_branch'] = 'Manual Search'
                    df_results = clean_poi_data(df_results)
                    st.session_state.poi_results = df_results
                    
                    # Add to history
                    st.session_state.search_history.append({
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'query': search_query,
                        'location': f"({manual_lat}, {manual_lon})",
                        'results': len(results)
                    })
            elif selected_poi_branches:
                # Branch-based search
                df_results = search_multiple_branches_poi(
                    selected_branches=selected_poi_branches,
                    query=search_query,
                    max_items_per_branch=max_results
                )
                df_results = clean_poi_data(df_results)
                st.session_state.poi_results = df_results
                
                # Add to history
                st.session_state.search_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'query': search_query,
                    'branches': selected_poi_branches,
                    'results': len(df_results) if not df_results.empty else 0
                })
    
    # ===== TAB 2: POI SEARCH RESULTS =====
    with tab2:
        if not st.session_state.poi_results.empty:
            # Results summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total POIs Found", len(st.session_state.poi_results))
            with col2:
                
                if 'types' in st.session_state.poi_results.columns:
    # Flatten all lists and count unique individual type strings
                    all_types = []
                    for type_list in st.session_state.poi_results['types'].dropna():
                        if isinstance(type_list, list):
                            all_types.extend(type_list)
                        else:
                            all_types.append(str(type_list))
                    unique_types = len(set(all_types))
                else:
                    unique_types = 0
                
                st.metric("Unique Types", unique_types)
            with col3:
                if 'rating' in st.session_state.poi_results.columns:
                    avg_rating = st.session_state.poi_results['rating'].mean()
                    st.metric("Avg Rating", f"{avg_rating:.1f}/5")
            
            # POI Map
            st.markdown("###  POI Distribution Map")
            selected_branches_data = get_selected_branches_data(
                selected_poi_branches if not manual_search else []
            )
            poi_map = create_poi_map(selected_branches_data, st.session_state.poi_results)
            st.pydeck_chart(poi_map, use_container_width=True)
            
            # Results table
            st.markdown("###  POI Results Table")
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                if 'rating' in st.session_state.poi_results.columns:
                    min_rating = st.slider("Minimum Rating", 0.0, 5.0, 0.0, 0.1)
                    filtered_results = st.session_state.poi_results[
                        st.session_state.poi_results['rating'] >= min_rating
                    ]
                else:
                    filtered_results = st.session_state.poi_results
                    
            with col2:
                if 'distance_km' in st.session_state.poi_results.columns:
                    max_distance = st.slider("Max Distance (km)", 0.0, 20.0, 10.0, 0.1)
                    filtered_results = filtered_results[
                        filtered_results['distance_km'] <= max_distance
                    ]
            
            # Display table
            display_cols = ['name', 'full_address', 'rating', 'distance_km', 'types', 'source_branch']
            available_cols = [col for col in display_cols if col in filtered_results.columns]
            
            st.dataframe(
                filtered_results[available_cols],
                use_container_width=True,
                height=400
            )
            
            # Export options
            st.markdown("###  Export Options")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                csv_data = export_data(filtered_results, 'csv')
                if csv_data:
                    st.download_button(
                        label=" Download CSV",
                        data=csv_data,
                        file_name=f"poi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
            
            with col2:
                json_data = export_data(filtered_results, 'json')
                if json_data:
                    st.download_button(
                        label=" Download JSON",
                        data=json_data,
                        file_name=f"poi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
            
            with col3:
                excel_data = export_data(filtered_results, 'excel')
                if excel_data:
                    st.download_button(
                        label=" Download Excel",
                        data=excel_data,
                        file_name=f"poi_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            
            with col4:
                if st.button(" Copy to Clipboard"):
                    json_str = filtered_results.head(10).to_json(orient='records', indent=2)
                    st.code(json_str, language='json')
                    st.success("First 10 results copied to code block above")
            
            # Individual POI cards view
            st.markdown("###  POI Details")
            for idx, row in filtered_results.head(20).iterrows():
                with st.expander(f" {row.get('name', 'Unknown')}"):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"**Address:** {row.get('full_address', 'N/A')}")
                        if 'rating' in row:
                            st.markdown(f"**Rating:** {row['rating']}/5 ({row.get('review_count', 0)} reviews)")
                        if 'phone_number' in row and pd.notna(row['phone_number']):
                            st.markdown(f"**Phone:** {row['phone_number']}")
                        if 'website' in row and pd.notna(row['website']):
                            st.markdown(f"**Website:** {row['website']}")
                        if 'types' in row:
                            st.markdown(f"**Categories:** {row['types']}")
                        if 'distance_km' in row:
                            st.markdown(f"**Distance:** {row['distance_km']:.1f} km")
                        if 'source_branch' in row:
                            st.markdown(f"**Nearest Branch:** {row['source_branch']}")
                    
                    with col2:
                        if 'place_link' in row and pd.notna(row['place_link']):
                            st.markdown(f"[Open in Google Maps]({row['place_link']})")
            
        else:
            st.info(" Use the sidebar to search for Points of Interest near SBI branches.")
    
    # ===== TAB 3: POI ANALYSIS =====
    with tab3:
        if not st.session_state.poi_results.empty:
            # Analysis charts
            create_poi_analysis_chart(st.session_state.poi_results)
            
            # Search history
            st.markdown("###  Search History")
            if st.session_state.search_history:
                history_df = pd.DataFrame(st.session_state.search_history)
                st.dataframe(history_df, use_container_width=True)
            else:
                st.info("No search history yet.")
        else:
            st.info("Search for POIs to see analysis here.")

if __name__ == "__main__":
    main()
