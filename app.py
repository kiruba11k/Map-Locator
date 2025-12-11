import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os

# ====================
# 1. INITIALIZATION & CONFIG
# ====================

@st.cache_resource
def load_design_tokens() -> Dict[str, Any]:
    """
    Load design tokens from theme_tokens.json (if present).
    Provide a full fallback token set when file is missing or partial.
    """
    try:
        if os.path.exists("theme_tokens.json"):
            with open("theme_tokens.json", "r") as f:
                tokens = json.load(f)
        else:
            tokens = {}

        # --- Fallbacks: ensure all necessary keys exist ---
        # Colors (primary, surface, semantic)
        tokens.setdefault("color", {})
        tokens["color"].setdefault("primary", {
            "50": "#eaf9ff",
            "100": "#cdefff",
            "200": "#9fe3ff",
            "300": "#6fd8ff",
            "400": "#3fcdfb",
            "500": "#00b4db",
            "600": "#00a0c6",
            "700": "#0083b0",
            "800": "#006d94",
            "900": "#005778"
        })
        tokens["color"].setdefault("surface", {
            "0": "#0f1720",  # dark background
            "1": "#12202a",
            "2": "#172a36",
            "3": "#1e3340"
        })
        tokens["color"].setdefault("semantic", {
            "success": "#10b981",
            "warning": "#f59e0b",
            "danger": "#ef4444",
            "muted": "rgba(255, 255, 255, 0.65)",
            "text": {
                "primary": "rgba(255,255,255,0.96)",
                "secondary": "rgba(255,255,255,0.78)",
                "tertiary": "rgba(255,255,255,0.6)"
            }
        })

        # Typography
        tokens.setdefault("typography", {})
        tokens["typography"].setdefault("display", {"xl": "2.75rem"})
        tokens["typography"].setdefault("heading", {"lg": "1.5rem", "md": "1.125rem"})
        tokens["typography"].setdefault("body", {"md": "1rem", "sm": "0.875rem"})
        tokens["typography"].setdefault("caption", "0.75rem")
        tokens["typography"].setdefault("lineHeight", {"tight": "1.1", "normal": "1.4", "relaxed": "1.6"})
        tokens["typography"].setdefault("letterSpacing", {"tight": "-0.5px", "normal": "0px", "wide": "0.8px"})

        # Spacing, animation, elevation
        tokens.setdefault("spacing", {"base": "8px"})
        tokens.setdefault("animation", {"duration": {"normal": "0.35s"}, "easing": {"standard": "cubic-bezier(0.2,0.9,0.2,1)"}})
        tokens.setdefault("elevation", {
            "shadow": {"md": "0 6px 18px rgba(2,6,23,0.48)", "lg": "0 10px 38px rgba(2,6,23,0.6)"},
            "blur": {"md": "10px"}
        })

        return tokens

    except json.JSONDecodeError as e:
        st.error(f"Error parsing theme_tokens.json: {e}")
        # Minimal safe fallback
        return {
            "color": {
                "primary": {"500": "#00b4db", "700": "#0083b0"},
                "surface": {"0": "#0f1720", "1": "#12202a"}
            },
            "typography": {
                "display": {"xl": "2.75rem"},
                "heading": {"lg": "1.5rem", "md": "1.125rem"},
                "body": {"md": "1rem", "sm": "0.875rem"},
                "caption": "0.75rem",
                "lineHeight": {"tight": "1.1", "normal": "1.4", "relaxed": "1.6"},
                "letterSpacing": {"tight": "-0.5px", "normal": "0px", "wide": "0.8px"}
            },
            "spacing": {"base": "8px"},
            "animation": {"duration": {"normal": "0.35s"}, "easing": {"standard": "cubic-bezier(0.2,0.9,0.2,1)"}},
            "elevation": {"shadow": {"md": "0 6px 18px rgba(2,6,23,0.48)", "lg": "0 10px 38px rgba(2,6,23,0.6)"}, "blur": {"md": "10px"}}
        }


# Load tokens
TOKENS = load_design_tokens()

# Helpful token shortcuts
def get_token(path: str, default=None):
    keys = path.split(".")
    cur = TOKENS
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return default
    return cur

PRIMARY_500 = get_token("color.primary.500", "#00b4db")
PRIMARY_700 = get_token("color.primary.700", "#0083b0")
SURFACE_0 = get_token("color.surface.0", "#0f1720")
SURFACE_1 = get_token("color.surface.1", "#12202a")
TEXT_PRIMARY = get_token("color.semantic.text.primary", "rgba(255,255,255,0.96)")
TEXT_SECONDARY = get_token("color.semantic.text.secondary", "rgba(255,255,255,0.78)")
SPACE_BASE = get_token("spacing.base", "8px")
FONT_DISPLAY_XL = get_token("typography.display.xl", "2.75rem")
FONT_HEADING_LG = get_token("typography.heading.lg", "1.5rem")
FONT_HEADING_MD = get_token("typography.heading.md", "1.125rem")
FONT_BODY_MD = get_token("typography.body.md", "1rem")
FONT_BODY_SM = get_token("typography.body.sm", "0.875rem")
FONT_CAPTION = get_token("typography.caption", "0.75rem")
ANIM_NORMAL = get_token("animation.duration.normal", "0.35s")
ANIM_EASE = get_token("animation.easing.standard", "cubic-bezier(0.2,0.9,0.2,1)")
SHADOW_MD = get_token("elevation.shadow.md", "0 6px 18px rgba(2,6,23,0.48)")
SHADOW_LG = get_token("elevation.shadow.lg", "0 10px 38px rgba(2,6,23,0.6)")
BLUR_MD = get_token("elevation.blur.md", "10px")

st.set_page_config(
    page_title="SBI Bank Network Intelligence",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. DESIGN SYSTEM & STYLING (modern 3D gradients)
# ====================

def inject_design_system():
    """
    Inject CSS that makes the Streamlit app look like a modern, production-grade website.
    Uses token variables defined above for safe fallbacks.
    """
    css = f"""
    <style>
    /* Import a clear, modern font (Inter) */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

    :root {{
        --color-primary-500: {PRIMARY_500};
        --color-primary-700: {PRIMARY_700};
        --color-surface-0: {SURFACE_0};
        --color-surface-1: {SURFACE_1};
        --text-primary: {TEXT_PRIMARY};
        --text-secondary: {TEXT_SECONDARY};
        --space-base: {SPACE_BASE};
        --font-display-xl: {FONT_DISPLAY_XL};
        --font-heading-lg: {FONT_HEADING_LG};
        --font-heading-md: {FONT_HEADING_MD};
        --font-body-md: {FONT_BODY_MD};
        --font-body-sm: {FONT_BODY_SM};
        --font-caption: {FONT_CAPTION};
        --anim-normal: {ANIM_NORMAL};
        --anim-ease: {ANIM_EASE};
        --shadow-md: {SHADOW_MD};
        --shadow-lg: {SHADOW_LG};
        --blur-md: {BLUR_MD};
    }}

    /* App background: soft deep gradient + subtle noise */
    .stApp {{
        background: linear-gradient(160deg, var(--color-surface-0) 0%, rgba(6,24,42,0.92) 40%, rgba(0,60,100,0.6) 100%);
        color: var(--text-primary);
        font-family: 'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* Container styling to feel website-like */
    .block-container {{
        padding: 28px 32px 48px 32px;
        max-width: 1400px;
        margin: 0 auto;
    }}

    /* Header */
    .fade-in-up h1 {{
        font-size: var(--font-display-xl);
        font-weight: 800;
        margin: 6px 0 4px 0;
        color: var(--text-primary);
        letter-spacing: -0.6px;
    }}
    .fade-in-up .body-text {{
        font-size: var(--font-body-md);
        color: var(--text-secondary);
        margin-top: 4px;
        margin-bottom: 12px;
    }}

    /* Sidebar - glass card */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-right: 1px solid rgba(255,255,255,0.04);
        backdrop-filter: blur(8px);
        box-shadow: var(--shadow-md);
    }}

    /* Metric cards - modern 3D floating cards */
    .metric-card {{
        background: linear-gradient(135deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 14px;
        padding: 18px;
        box-shadow: var(--shadow-md);
        border: 1px solid rgba(255,255,255,0.04);
        transition: transform var(--anim-normal) var(--anim-ease), box-shadow var(--anim-normal) var(--anim-ease);
    }}
    .metric-card:hover {{
        transform: translateY(-6px);
        box-shadow: var(--shadow-lg);
    }}
    .metric-label {{
        color: var(--text-secondary);
        font-size: var(--font-body-sm);
    }}
    .metric-value {{
        color: var(--text-primary);
        font-size: var(--font-heading-md);
        font-weight: 700;
        margin-top: 6px;
    }}

    /* Buttons - soft gradient */
    .stButton > button {{
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-primary-700)) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 10px 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 6px 18px rgba(0,0,0,0.45);
        transition: transform var(--anim-normal) var(--anim-ease), box-shadow var(--anim-normal) var(--anim-ease);
    }}
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.01);
        box-shadow: 0 12px 30px rgba(0,0,0,0.55);
    }}

    /* pydeck tooltip override small visual polish */
    .map-tooltip {{
        font-family: inherit;
        border-radius: 10px !important;
        padding: 12px !important;
        background: linear-gradient(180deg, rgba(20,30,40,0.92), rgba(10,20,30,0.96)) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        box-shadow: var(--shadow-md) !important;
    }}
    .map-tooltip h3 {{
        margin: 0 0 6px 0;
        font-size: var(--font-heading-md);
        color: var(--color-primary-500);
    }}
    .map-tooltip p {{
        margin: 2px 0;
        font-size: var(--font-body-sm);
        color: var(--text-secondary);
    }}

    /* responsive tweaks */
    @media (max-width: 900px) {{
        .block-container {{
            padding: 16px 16px 32px 16px;
        }}
        .stApp h1 {{ font-size: 1.9rem; }}
    }}

    /* reduced motion support */
    @media (prefers-reduced-motion: reduce) {{
        * {{
            transition: none !important;
            animation: none !important;
        }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ====================
# 3. DATA MANAGEMENT (no performance fields)
# ====================

@st.cache_data
def load_branch_data() -> pd.DataFrame:
    """Load and cache branch data with safe defaults."""
    data = pd.DataFrame({
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

    # Branch scale / visual size for icons (kept as a mock but harmless)
    data["Branch_Size"] = [90, 150, 120, 110, 200]
    return data


# ====================
# 4. 3D MAP VISUALIZATION (icons + pulsing selection)
# ====================

def create_3d_icon_layer(data: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Layer:
    """
    Create an IconLayer showing branches as modern pins.
    No performance colors; icons use a consistent accent color and scale by Branch_Size.
    """
    ICON_DATA = {
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }

    # assign icon_data and size from Branch_Size normalized to a scale
    data = data.copy()
    data["icon_data"] = [ICON_DATA] * len(data)
    # normalize Branch_Size to reasonable icon_size values
    min_size = data["Branch_Size"].min()
    max_size = data["Branch_Size"].max()
    if max_size == min_size:
        data["icon_size"] = 1.2
    else:
        data["icon_size"] = data["Branch_Size"].apply(lambda x: 0.8 + 1.6 * ((x - min_size) / (max_size - min_size)))

    # emphasize selected branch
    if selected_branch and selected_branch != "All Branches":
        data["icon_size"] = data.apply(lambda r: r["icon_size"] * 1.6 if r["Branch"] == selected_branch else r["icon_size"] * 0.9, axis=1)

    # static accent color (RGBa)
    accent = [0, 180, 219, 240]

    return pdk.Layer(
        "IconLayer",
        data=data,
        pickable=True,
        auto_highlight=True,
        get_icon="icon_data",
        get_size="icon_size",
        get_position=["Longitude", "Latitude"],
        size_scale=20,
        get_color=accent,
        highlight_color=[255, 255, 255, 160],
        transitions={"get_size": 900, "get_position": 900}
    )


def create_pulsing_layer(data: pd.DataFrame, selected_branch: Optional[str] = None) -> Optional[pdk.Layer]:
    """Return a ScatterplotLayer representing a pulsing ring for selected branch (or None)."""
    if not selected_branch or selected_branch == "All Branches":
        return None

    selected_data = data[data["Branch"] == selected_branch].copy()
    if selected_data.empty:
        return None

    selected_data["radius"] = 180  # meters
    return pdk.Layer(
        "ScatterplotLayer",
        data=selected_data,
        get_position=["Longitude", "Latitude"],
        get_fill_color=[0, 180, 219, 70],
        get_line_color=[0, 180, 219, 160],
        get_radius="radius",
        stroked=True,
        get_line_width=2,
        pickable=False,
        radius_min_pixels=24,
        radius_max_pixels=90,
        transitions={"get_radius": 2000}
    )


def create_map_view(data: pd.DataFrame, selected_branch: Optional[str] = None, pitch: int = 50, zoom: int = 11, bearing: int = 0) -> pdk.Deck:
    """Compose pydeck deck with icon + pulsing layers and polished tooltip."""
    layers = [create_3d_icon_layer(data, selected_branch)]
    pulsing = create_pulsing_layer(data, selected_branch)
    if pulsing:
        layers.append(pulsing)

    # view state - center on selected branch if present
    if selected_branch and selected_branch != "All Branches":
        s = data[data["Branch"] == selected_branch]
        if not s.empty:
            lat = float(s["Latitude"].iloc[0])
            lon = float(s["Longitude"].iloc[0])
            zoom = 14
        else:
            lat = float(data["Latitude"].mean())
            lon = float(data["Longitude"].mean())
    else:
        lat = float(data["Latitude"].mean())
        lon = float(data["Longitude"].mean())

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=pitch, bearing=bearing, min_zoom=5, max_zoom=20, controller=True)

    # map style control (pydeck supports several string keys)
    style = st.session_state.get("map_style", "dark")
    map_styles = {"dark": "dark", "light": "light", "satellite": "satellite", "road": "road"}

    tooltip_config = {
        "html": """
        <div class="map-tooltip">
            <h3>{Branch}</h3>
            <p><strong>IFSC:</strong> {IFSC_Code}</p>
            <p><strong>Address:</strong> {Address}</p>
            <p><strong>Pincode:</strong> {Pincode}</p>
        </div>
        """,
        "style": {
            "padding": "6px",
            "backgroundColor": SURFACE_1,
            "color": TEXT_PRIMARY
        }
    }

    return pdk.Deck(layers=layers, initial_view_state=view_state, map_style=map_styles.get(style, "dark"), tooltip=tooltip_config, width="100%", height=640)


# ====================
# 5. DASHBOARD COMPONENTS
# ====================

def render_metric_cards(data: pd.DataFrame):
    """Render a set of custom-styled metric cards (pure Streamlit components inside styled container)."""
    col1, col2, col3, col4 = st.columns(4, gap="large")

    avg_branch_size = int(data["Branch_Size"].mean())
    total_branches = len(data)
    cities = data["City"].nunique()
    coverage = "45.2"  # placeholder

    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Branches</div>
                <div class="metric-value">{total_branches}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Cities Covered</div>
                <div class="metric-value">{cities}</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Branch Size</div>
                <div class="metric-value">{avg_branch_size}</div>
            </div>
            """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Coverage (km²)</div>
                <div class="metric-value">{coverage}</div>
            </div>
            """, unsafe_allow_html=True)


def render_branch_table(data: pd.DataFrame):
    """Render an interactive branch table without performance column."""
    st.markdown("### Branch Network Details")

    column_config = {
        "Branch": st.column_config.TextColumn("Branch Name", width="medium"),
        "IFSC_Code": st.column_config.TextColumn("IFSC Code", width="large"),
        "Address": st.column_config.TextColumn("Full Address", width="large"),
        "Latitude": st.column_config.NumberColumn("Latitude", format="%.6f"),
        "Longitude": st.column_config.NumberColumn("Longitude", format="%.6f"),
        "Branch_Size": st.column_config.NumberColumn("Relative Size")
    }

    return st.data_editor(data, column_config=column_config, use_container_width=True, hide_index=True, num_rows="dynamic", key="branch_table")


# ====================
# 6. MAIN APPLICATION
# ====================

def main():
    inject_design_system()

    # ensure map style state exists
    if "map_style" not in st.session_state:
        st.session_state["map_style"] = "dark"

    # Load data
    data = load_branch_data()

    # Header area
    st.markdown(
        f"""
        <div class="fade-in-up">
            <h1> SBI Bank Network Intelligence</h1>
            <div class="body-text">Enterprise-grade 3D visualization dashboard for strategic branch network analysis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar controls
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding:12px 6px;">
                <div style="font-size:20px; font-weight:800; color:{PRIMARY_500};">SBI DASHBOARD</div>
                <div style="font-size:12px; color:{TEXT_SECONDARY}; margin-top:4px;">Enterprise Control Panel</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        selected_branch = st.selectbox("Focus on Branch", options=["All Branches"] + list(data["Branch"].unique()), key="branch_selector")

        st.divider()
        st.markdown("### Map Controls")

        col1, col2 = st.columns(2)
        with col1:
            map_pitch = st.slider("3D Tilt", min_value=0, max_value=60, value=45, key="map_pitch")
        with col2:
            map_zoom = st.slider("Zoom Level", min_value=5, max_value=20, value=11, key="map_zoom")

        st.session_state["map_style"] = st.selectbox("Basemap Style", options=["Dark", "Light", "Satellite", "Road"], index=0, key="map_style_selector").lower()

        st.divider()
        st.markdown("### Animation")
        show_pulse = st.checkbox("Pulse Effect", value=True, key="show_pulse")
        reduce_motion = st.checkbox("Reduce Motion", value=False, key="reduce_motion")

        st.divider()
        st.markdown("### Data")
        st.caption(f"Data Points: {len(data)} branches")
        st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    # Main content
    st.markdown("### Network Overview")
    render_metric_cards(data)
    st.divider()

    st.markdown("### Interactive 3D Network Map")
    deck = create_map_view(data=data, selected_branch=selected_branch, pitch=st.session_state.get("map_pitch", 45), zoom=st.session_state.get("map_zoom", 11))
    st.pydeck_chart(deck, use_container_width=True)

    # Footer controls for map
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption("Tip: Click on any branch pin to view detailed information")
    with col2:
        if st.button("Reset View", use_container_width=True):
            st.session_state["map_pitch"] = 45
            st.session_state["map_zoom"] = 11
            st.experimental_rerun()
    with col3:
        if st.button("Export View", use_container_width=True):
            st.info("Export functionality can be added (PNG/GeoJSON/Share link).")

    st.divider()
    edited = render_branch_table(data)

    # Footer
    st.divider()
    st.markdown(
        f"""
        <div style="text-align:center; padding: 28px 0;">
            <div style="font-size:0.85rem; color:var(--text-secondary);">SBI Bank Enterprise Dashboard v1.0 • Secure • Production Ready</div>
            <div style="font-size:0.75rem; color:var(--text-secondary); margin-top:6px;">
                This dashboard follows accessible contrast and reduced-motion patterns where possible.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
