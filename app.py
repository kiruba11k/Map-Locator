# sbi_dashboard_ui.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os

# ====================
# 1. TOKEN LOADING & SAFE FALLBACKS
# ====================

@st.cache_resource
def load_design_tokens_from_file(path: str = "theme_tokens.json") -> Dict[str, Any]:
    """
    Load tokens from path if present. Provide a robust fallback object for everything
    used in the UI. This avoids KeyError and ensures CSS can reference tokens safely.
    """
    try:
        tokens = {}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    tokens = json.load(f)
                # No success banner here: UI will show uploaded token status in sidebar.
            except Exception as e:
                st.warning(f"Failed to parse {path}: {e}")
                tokens = {}
        # Ensure full fallbacks
        tokens.setdefault("color", {})
        tokens["color"].setdefault("primary", {
            "50": "#eaf9ff", "100": "#cdefff", "200": "#9fe3ff",
            "300": "#6fd8ff", "400": "#3fcdfb", "500": "#00b4db",
            "600": "#00a0c6", "700": "#0083b0", "800": "#006d94", "900": "#005778"
        })
        tokens["color"].setdefault("surface", {
            "0": "#0f1720", "1": "#12202a", "2": "#172a36", "3": "#1e3340"
        })
        tokens["color"].setdefault("background", {
            "light": "#f6f9fb",
            "dark": "#071127"
        })
        tokens["color"].setdefault("semantic", {
            "success": "#10b981", "warning": "#f59e0b", "danger": "#ef4444",
            "muted": "rgba(255,255,255,0.65)",
            "text": {"primary": "rgba(255,255,255,0.96)", "secondary": "rgba(255,255,255,0.78)"}
        })

        tokens.setdefault("typography", {})
        tokens["typography"].setdefault("display", {"xl": "2.75rem"})
        tokens["typography"].setdefault("heading", {"lg": "1.5rem", "md": "1.125rem"})
        tokens["typography"].setdefault("body", {"md": "1rem", "sm": "0.9rem"})
        tokens["typography"].setdefault("caption", "0.75rem")
        tokens["typography"].setdefault("lineHeight", {"tight": "1.1", "normal": "1.4", "relaxed": "1.6"})
        tokens["typography"].setdefault("letterSpacing", {"tight": "-0.5px", "normal": "0px", "wide": "0.8px"})

        tokens.setdefault("spacing", {"base": "8px"})
        tokens.setdefault("animation", {"duration": {"normal": "0.35s"}, "easing": {"standard": "cubic-bezier(0.2,0.9,0.2,1)"}})
        tokens.setdefault("elevation", {
            "shadow": {"md": "0 8px 22px rgba(2,6,23,0.45)", "lg": "0 16px 48px rgba(2,6,23,0.6)"},
            "blur": {"md": "12px"}
        })

        return tokens
    except Exception as e:
        # Super-safe minimal fallback
        st.error(f"Design token loader error: {e}")
        return {
            "color": {
                "primary": {"500": "#00b4db", "700": "#0083b0"},
                "surface": {"0": "#0f1720", "1": "#12202a"},
                "background": {"light": "#f6f9fb", "dark": "#071127"},
                "semantic": {"text": {"primary": "rgba(255,255,255,0.96)", "secondary": "rgba(255,255,255,0.78)"}}
            },
            "typography": {"display": {"xl": "2.75rem"}, "heading": {"lg": "1.5rem"}, "body": {"md": "1rem"}, "caption": "0.75rem"},
            "spacing": {"base": "8px"},
            "animation": {"duration": {"normal": "0.35s"}, "easing": {"standard": "ease-in-out"}},
            "elevation": {"shadow": {"md": "0 8px 22px rgba(2,6,23,0.45)", "lg": "0 16px 48px rgba(2,6,23,0.6)"}}
        }

# Load default tokens (will be replaced if user uploads)
TOKENS = load_design_tokens_from_file()

# Helper to safely get nested path from TOKENS
def get_token(path: str, default=None):
    cur = TOKENS
    for key in path.split("."):
        if isinstance(cur, dict) and key in cur:
            cur = cur[key]
        else:
            return default
    return cur

# Shortcuts
PRIMARY_500 = get_token("color.primary.500", "#00b4db")
PRIMARY_700 = get_token("color.primary.700", "#0083b0")
BG_LIGHT = get_token("color.background.light", "#f6f9fb")
BG_DARK = get_token("color.background.dark", "#071127")
SURFACE_0 = get_token("color.surface.0", "#0f1720")
SURFACE_1 = get_token("color.surface.1", "#12202a")
TEXT_PRIMARY = get_token("color.semantic.text.primary", "rgba(255,255,255,0.96)")
TEXT_SECONDARY = get_token("color.semantic.text.secondary", "rgba(255,255,255,0.78)")
FONT_DISPLAY_XL = get_token("typography.display.xl", "2.75rem")
FONT_HEADING_LG = get_token("typography.heading.lg", "1.5rem")
FONT_HEADING_MD = get_token("typography.heading.md", "1.125rem")
FONT_BODY_MD = get_token("typography.body.md", "1rem")
FONT_BODY_SM = get_token("typography.body.sm", "0.9rem")
FONT_CAPTION = get_token("typography.caption", "0.75rem")
SPACE_BASE = get_token("spacing.base", "8px")
ANIM_NORMAL = get_token("animation.duration.normal", "0.35s")
ANIM_EASE = get_token("animation.easing.standard", "cubic-bezier(0.2,0.9,0.2,1)")
SHADOW_MD = get_token("elevation.shadow.md", "0 8px 22px rgba(2,6,23,0.45)")
SHADOW_LG = get_token("elevation.shadow.lg", "0 16px 48px rgba(2,6,23,0.6)")
BLUR_MD = get_token("elevation.blur.md", "12px")

# Page config
st.set_page_config(page_title="SBI Bank Network Intelligence", layout="wide", initial_sidebar_state="expanded")


# ====================
# 2. INJECT THE MODERN THEME CSS (ADAPTIVE)
# ====================

def inject_modern_css():
    """
    Injects CSS for:
      - Adaptive background (light/dark)
      - Premium fonts (Inter + Poppins fallback)
      - Glass cards, 3D gradients, responsive typography
      - Accessibility: reduced-motion
    The CSS uses values from TOKENS safely.
    """
    # Use safe CSS color values; ensure strings are quoted
    css = f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&family=Poppins:wght@400;600;700&display=swap');

    :root {{
        --primary-500: {PRIMARY_500};
        --primary-700: {PRIMARY_700};
        --bg-light: {BG_LIGHT};
        --bg-dark: {BG_DARK};
        --surface-0: {SURFACE_0};
        --surface-1: {SURFACE_1};
        --text-primary: {TEXT_PRIMARY};
        --text-secondary: {TEXT_SECONDARY};
        --font-display-xl: {FONT_DISPLAY_XL};
        --font-heading-lg: {FONT_HEADING_LG};
        --font-heading-md: {FONT_HEADING_MD};
        --font-body-md: {FONT_BODY_MD};
        --font-body-sm: {FONT_BODY_SM};
        --font-caption: {FONT_CAPTION};
        --space-base: {SPACE_BASE};
        --anim-normal: {ANIM_NORMAL};
        --anim-ease: {ANIM_EASE};
        --shadow-md: {SHADOW_MD};
        --shadow-lg: {SHADOW_LG};
        --blur-md: {BLUR_MD};
    }}

    /* Choose bg according to user color scheme preference */
    body, html, .stApp {{
        min-height: 100vh;
        margin: 0;
        padding: 0;
        font-family: 'Inter', 'Poppins', system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}

    /* Light mode defaults */
    .stApp {{
        background-color: var(--bg-light);
        background-image:
            radial-gradient(circle at 10% 10%, rgba(59,130,246,0.06), transparent 15%),
            radial-gradient(circle at 90% 80%, rgba(99,102,241,0.04), transparent 25%),
            linear-gradient(160deg, rgba(255,255,255,0.95), rgba(245,248,255,0.98));
        color: #0b2540;
    }}

    /* Dark mode */
    @media (prefers-color-scheme: dark) {{
        .stApp {{
            background-color: var(--bg-dark);
            background-image:
                radial-gradient(circle at 15% 10%, rgba(0,186,219,0.06), transparent 12%),
                radial-gradient(circle at 85% 80%, rgba(3,105,161,0.05), transparent 20%),
                linear-gradient(160deg, rgba(7,17,39,1), rgba(2,28,48,0.95));
            color: var(--text-primary);
        }}
    }}

    /* Main container sizing like an app website */
    .block-container {{
        max-width: 1400px;
        padding: 28px 36px 48px 36px;
        margin: 0 auto;
    }}

    /* Header */
    .app-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        margin-bottom: 14px;
    }}
    .brand {{
        display:flex;
        align-items:center;
        gap:12px;
    }}
    .brand .logo {{
        width:42px;
        height:42px;
        border-radius:10px;
        background: linear-gradient(135deg, var(--primary-500), var(--primary-700));
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-weight:800;
        box-shadow: var(--shadow-md);
    }}
    .brand h1 {{
        margin:0;
        font-size: var(--font-display-xl);
        font-weight:800;
        line-height:1;
        color:inherit;
    }}
    .brand p {{
        margin:0;
        font-size: var(--font-body-sm);
        color:var(--text-secondary);
    }}

    /* Topbar controls (search / profile) */
    .top-controls {{
        display:flex;
        gap:12px;
        align-items:center;
    }}
    .search-box input {{
        padding: 10px 12px;
        width:340px;
        border-radius: 12px;
        border: 1px solid rgba(0,0,0,0.06);
        background: rgba(255,255,255,0.9);
        outline:none;
        box-shadow: 0 6px 20px rgba(2,6,23,0.06);
    }}
    @media (prefers-color-scheme: dark) {{
        .search-box input {{
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.05);
            color: var(--text-primary);
        }}
    }}

    .profile-pill {{
        display:flex;
        gap:10px;
        align-items:center;
        padding:8px 12px;
        border-radius: 999px;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.04);
    }}
    .profile-pill img {{
        width:36px;
        height:36px;
        border-radius:50%;
    }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        width: 320px;
        padding: 18px;
    }}
    .sidebar-section {{
        padding: 12px;
        border-radius: 12px;
        margin-bottom: 12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.03);
        backdrop-filter: blur(var(--blur-md));
    }}

    /* Metric cards */
    .metrics-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
        margin-bottom: 20px;
    }}
    .metric-card {{
        border-radius: 14px;
        padding: 18px;
        background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.03);
        box-shadow: var(--shadow-md);
        transition: transform var(--anim-normal) var(--anim-ease), box-shadow var(--anim-normal) var(--anim-ease);
    }}
    .metric-card:hover {{
        transform: translateY(-6px);
        box-shadow: var(--shadow-lg);
    }}
    .metric-label {{ color: var(--text-secondary); font-size: var(--font-body-sm); margin-bottom:6px; }}
    .metric-value {{ font-size: var(--font-heading-md); font-weight:700; color:inherit; }}

    /* Map container */
    .map-container {{
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.04);
        box-shadow: var(--shadow-md);
    }}

    /* Table wrapper */
    .table-card {{
        margin-top: 18px;
        border-radius: 12px;
        padding: 12px;
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border: 1px solid rgba(255,255,255,0.03);
    }}

    /* Tooltip override for pydeck */
    .map-tooltip {{
        border-radius: 10px !important;
        padding: 10px !important;
        background: linear-gradient(180deg, rgba(10,20,30,0.95), rgba(7,14,25,0.98)) !important;
        color: var(--text-primary) !important;
        border: 1px solid rgba(255,255,255,0.04) !important;
        box-shadow: var(--shadow-md) !important;
        font-size: var(--font-body-sm) !important;
    }}
    .map-tooltip h3 {{ margin:0 0 6px 0; font-size: var(--font-heading-md); color: var(--primary-500); }}
    .map-tooltip p {{ margin:0; color: var(--text-secondary); font-size: var(--font-body-sm); }}

    /* Reduced motion support */
    @media (prefers-reduced-motion: reduce) {{
        * {{ transition: none !important; animation: none !important; }}
    }}

    /* Responsive adjustments */
    @media (max-width: 1100px) {{
        .metrics-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .search-box input {{ width: 180px; }}
    }}
    @media (max-width: 700px) {{
        .metrics-grid {{ grid-template-columns: 1fr; }}
        .brand h1 {{ font-size: 1.6rem; }}
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ====================
# 3. DATA LAYER (branch data, safe)
# ====================

@st.cache_data
def load_branch_data() -> pd.DataFrame:
    """Return sample branch data. Replace with DB/CSV/API as needed."""
    df = pd.DataFrame({
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
        "Branch_Size": [90, 150, 120, 110, 200]
    })
    return df


# ====================
# 4. MAP LAYERS (icons + pulsing selection)
# ====================

def create_icon_layer(df: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Layer:
    ICON = {
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }
    data = df.copy()
    data["icon_data"] = [ICON] * len(data)
    min_size = data["Branch_Size"].min()
    max_size = data["Branch_Size"].max()
    if max_size == min_size:
        data["icon_size"] = 1.2
    else:
        data["icon_size"] = data["Branch_Size"].apply(lambda x: 0.8 + 1.6 * ((x - min_size) / (max_size - min_size)))

    if selected_branch and selected_branch != "All Branches":
        data["icon_size"] = data.apply(lambda r: r["icon_size"] * 1.6 if r["Branch"] == selected_branch else r["icon_size"] * 0.9, axis=1)

    accent_rgba = [0, 180, 219, 240]  # consistent accent color

    return pdk.Layer(
        "IconLayer",
        data=data,
        pickable=True,
        auto_highlight=True,
        get_icon="icon_data",
        get_size="icon_size",
        get_color=accent_rgba,
        get_position=["Longitude", "Latitude"],
        size_scale=20,
        highlight_color=[255,255,255,180],
        transitions={"get_size": 900, "get_position": 900},
    )


def create_pulse_layer(df: pd.DataFrame, selected_branch: Optional[str] = None) -> Optional[pdk.Layer]:
    if not selected_branch or selected_branch == "All Branches":
        return None
    sel = df[df["Branch"] == selected_branch].copy()
    if sel.empty:
        return None
    sel["radius"] = 180
    return pdk.Layer(
        "ScatterplotLayer",
        data=sel,
        get_position=["Longitude", "Latitude"],
        get_radius="radius",
        get_fill_color=[0,180,219,60],
        get_line_color=[0,180,219,160],
        stroked=True,
        get_line_width=2,
        pickable=False,
        radius_min_pixels=24,
        radius_max_pixels=90,
        transitions={"get_radius": 2000}
    )


def create_deck(df: pd.DataFrame, selected_branch: Optional[str] = None, pitch: int = 50, zoom: int = 11) -> pdk.Deck:
    layers = [create_icon_layer(df, selected_branch)]
    pulse = create_pulse_layer(df, selected_branch)
    if pulse:
        layers.append(pulse)

    if selected_branch and selected_branch != "All Branches":
        s = df[df["Branch"] == selected_branch]
        if not s.empty:
            lat = float(s["Latitude"].iloc[0])
            lon = float(s["Longitude"].iloc[0])
            zoom = 14
        else:
            lat = float(df["Latitude"].mean())
            lon = float(df["Longitude"].mean())
    else:
        lat = float(df["Latitude"].mean())
        lon = float(df["Longitude"].mean())

    view_state = pdk.ViewState(latitude=lat, longitude=lon, zoom=zoom, pitch=pitch, bearing=0, min_zoom=5, max_zoom=20, controller=True)

    tooltip = {
        "html": """
        <div class="map-tooltip">
            <h3>{Branch}</h3>
            <p><strong>IFSC:</strong> {IFSC_Code}</p>
            <p><strong>Address:</strong> {Address}</p>
            <p><strong>Pincode:</strong> {Pincode}</p>
        </div>""",
        "style": {"padding":"6px"}
    }

    style_choice = st.session_state.get("map_style", "dark")
    map_styles = {"dark":"dark","light":"light","satellite":"satellite","road":"road"}

    return pdk.Deck(layers=layers, initial_view_state=view_state, map_style=map_styles.get(style_choice,"dark"), tooltip=tooltip, height=640, width="100%")


# ====================
# 5. UI COMPONENTS (metrics, table)
# ====================

def render_header():
    # Use HTML blocks styled by CSS injected earlier
    st.markdown("""
    <div class="app-header">
        <div class="brand">
            <div class="logo">S</div>
            <div>
                <h1>SBI Bank Network Intelligence</h1>
                <p>Enterprise branch network analysis</p>
            </div>
        </div>
        <div class="top-controls">
            <div class="search-box">
                <input placeholder="Search branch, IFSC, city..." id="global-search" />
            </div>
            <div class="profile-pill">
                <img src="https://avatars.dicebear.com/api/identicon/admin.svg" alt="profile" />
                <div style="font-size:0.9rem;">Admin</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics(df: pd.DataFrame):
    total = len(df)
    cities = df["City"].nunique()
    avg_size = int(df["Branch_Size"].mean()) if "Branch_Size" in df.columns else "-"
    coverage = "45.2"

    st.markdown('<div class="metrics-grid">', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Branches</div>
            <div class="metric-value">{total}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Cities Covered</div>
            <div class="metric-value">{cities}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Branch Size</div>
            <div class="metric-value">{avg_size}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Total Coverage (km²)</div>
            <div class="metric-value">{coverage}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_branch_table(df: pd.DataFrame):
    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.markdown("### Branch Network Details")
    column_config = {
        "Branch": st.column_config.TextColumn("Branch Name", width="medium"),
        "IFSC_Code": st.column_config.TextColumn("IFSC Code", width="large"),
        "Address": st.column_config.TextColumn("Full Address", width="large"),
        "Latitude": st.column_config.NumberColumn("Latitude", format="%.6f"),
        "Longitude": st.column_config.NumberColumn("Longitude", format="%.6f"),
        "Branch_Size": st.column_config.NumberColumn("Relative Size")
    }
    editor = st.data_editor(df, column_config=column_config, use_container_width=True, hide_index=True, num_rows="dynamic", key="branch_table_editor")
    st.markdown('</div>', unsafe_allow_html=True)
    return editor


# ====================
# 6. MAIN APP FLOW
# ====================

def main():
    inject_modern_css()

    # Sidebar with navigation and token upload
    with st.sidebar:
        st.markdown("<div style='font-weight:800; font-size:1rem; margin-bottom:8px;'>Navigation</div>", unsafe_allow_html=True)

        nav = st.radio("", ("Overview", "Branches", "Map", "Settings"))
        st.divider()

        st.markdown("<div class='sidebar-section'><strong>Theme</strong></div>", unsafe_allow_html=True)
        theme_opt = st.selectbox("Choose Theme Preset", ("Dark (default)", "Light", "Oceanic", "Neutral"))
        # Map style selection for pydeck
        st.session_state["map_style"] = st.selectbox("Map Style", ("Dark","Light","Satellite","Road"), index=0).lower()

        st.markdown("<div class='sidebar-section'><strong>Design tokens</strong></div>", unsafe_allow_html=True)
        uploaded = st.file_uploader("Upload theme_tokens.json (optional)", type=["json"])
        if uploaded:
            try:
                t = json.load(uploaded)
                # Write uploaded tokens to a local file and reload tokens
                with open("theme_tokens.json", "w", encoding="utf-8") as f:
                    json.dump(t, f, indent=2)
                st.success("theme_tokens.json uploaded and saved. Reloading tokens...")
                # Reload tokens (and refresh)
                global TOKENS
                TOKENS = load_design_tokens_from_file("theme_tokens.json")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to load uploaded file: {e}")

        st.markdown("<div style='margin-top:12px; font-size:0.9rem; color: rgba(0,0,0,0.6)'>Controls</div>", unsafe_allow_html=True)
        if st.button("Reset Tokens"):
            try:
                if os.path.exists("theme_tokens.json"):
                    os.remove("theme_tokens.json")
                TOKENS = load_design_tokens_from_file()
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Reset failed: {e}")

        st.divider()
        st.markdown("<div style='font-size:0.9rem; color: rgba(0,0,0,0.6)'>About</div>", unsafe_allow_html=True)
        st.markdown("SBI Enterprise Dashboard • Modern UI • Built for demos and prototypes", unsafe_allow_html=True)

    # --- Main header & content
    render_header()

    df = load_branch_data()

    # Navigation routing
    if st.session_state.get("map_style") is None:
        st.session_state["map_style"] = "dark"

    if nav == "Overview":
        render_metrics(df)
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown("### Interactive 3D Network Map")
        # quick controls
        col1, col2 = st.columns([3,1])
        with col2:
            if st.button("Export View"):
                st.info("Export not implemented in demo. Add PNG/GeoJSON export as needed.")

        deck = create_deck(df, selected_branch=st.session_state.get("branch_selector", "All Branches"), pitch=45, zoom=11)
        st.pydeck_chart(deck, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.divider()
        render_branch_table(df)

    elif nav == "Branches":
        st.markdown("### Branch Explorer")
        render_metrics(df)
        st.divider()
        render_branch_table(df)

    elif nav == "Map":
        st.markdown("### Full Screen Map")
        selection = st.selectbox("Focus on Branch", options=["All Branches"] + list(df["Branch"].unique()), key="branch_selector_map")
        deck = create_deck(df, selected_branch=selection, pitch=st.session_state.get("map_pitch", 45), zoom=st.session_state.get("map_zoom", 11))
        st.pydeck_chart(deck, use_container_width=True)

    else:  # Settings
        st.markdown("### Settings")
        st.markdown("Adjust application settings, upload design tokens, or change themes.")
        if st.button("Show Current Token Sample"):
            st.json(TOKENS)

    # Footer
    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; padding:18px 0 40px 0; color: rgba(0,0,0,0.5);">
        <small>© {datetime.now().year} SBI Bank Network Intelligence • Demo UI</small>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
