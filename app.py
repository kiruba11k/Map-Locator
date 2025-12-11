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
    """Load design tokens with comprehensive dual-theme system."""
    try:
        if os.path.exists('theme_tokens.json'):
            with open('theme_tokens.json', 'r') as f:
                tokens = json.load(f)
        else:
            # Sophisticated dual-theme system based on color theory
            # Primary: Indigo (#6366F1) for trust & professionalism
            # Accent: Teal (#14B8A6) for energy & modern feel
            # Neutrals: Warm grays for elegance
            tokens = {
                "color": {
                    "dark": {
                        "primary": {
                            "50": "#e0e7ff", "100": "#c7d2fe", "200": "#a5b4fc",
                            "300": "#818cf8", "400": "#6366f1", "500": "#4f46e5",
                            "600": "#4338ca", "700": "#3730a3", "800": "#312e81",
                            "900": "#1e1b4b"
                        },
                        "accent": {
                            "50": "#f0fdfa", "100": "#ccfbf1", "200": "#99f6e4",
                            "300": "#5eead4", "400": "#2dd4bf", "500": "#14b8a6",
                            "600": "#0d9488", "700": "#0f766e", "800": "#115e59",
                            "900": "#134e4a"
                        },
                        "surface": {
                            "0": "#0a0a0a",    # Base background
                            "1": "#1a1a1a",    # Card background
                            "2": "#262626",    # Elevated surfaces
                            "3": "#404040"     # Borders & dividers
                        },
                        "text": {
                            "primary": "#fafafa",
                            "secondary": "#d4d4d4",
                            "tertiary": "#a3a3a3"
                        },
                        "semantic": {
                            "success": "#10b981",
                            "warning": "#f59e0b",
                            "error": "#ef4444",
                            "info": "#3b82f6"
                        }
                    },
                    "light": {
                        "primary": {
                            "50": "#eef2ff", "100": "#e0e7ff", "200": "#c7d2fe",
                            "300": "#a5b4fc", "400": "#818cf8", "500": "#6366f1",
                            "600": "#4f46e5", "700": "#4338ca", "800": "#3730a3",
                            "900": "#1e1b4b"
                        },
                        "accent": {
                            "50": "#f0fdfa", "100": "#ccfbf1", "200": "#99f6e4",
                            "300": "#5eead4", "400": "#2dd4bf", "500": "#14b8a6",
                            "600": "#0d9488", "700": "#0f766e", "800": "#115e59",
                            "900": "#134e4a"
                        },
                        "surface": {
                            "0": "#ffffff",    # Base background
                            "1": "#fafafa",    # Card background
                            "2": "#f5f5f5",    # Elevated surfaces
                            "3": "#e5e5e5"     # Borders & dividers
                        },
                        "text": {
                            "primary": "#171717",
                            "secondary": "#525252",
                            "tertiary": "#737373"
                        },
                        "semantic": {
                            "success": "#10b981",
                            "warning": "#f59e0b",
                            "error": "#dc2626",
                            "info": "#2563eb"
                        }
                    }
                },
                "typography": {
                    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
                    "font_mono": "'JetBrains Mono', 'SF Mono', Monaco, monospace",
                    "scale": {
                        "display": { "xl": "3.75rem", "lg": "3rem", "md": "2.25rem" },
                        "heading": { "xl": "1.875rem", "lg": "1.5rem", "md": "1.25rem", "sm": "1.125rem" },
                        "body": { "lg": "1.125rem", "md": "1rem", "sm": "0.875rem" },
                        "caption": "0.75rem"
                    },
                    "weight": {
                        "light": "300",
                        "regular": "400",
                        "medium": "500",
                        "semibold": "600",
                        "bold": "700",
                        "extrabold": "800"
                    }
                },
                "spacing": {
                    "scale": [0, 4, 8, 12, 16, 20, 24, 32, 40, 48, 56, 64, 80, 96, 128],
                    "radius": {
                        "sm": "6px",
                        "md": "12px",
                        "lg": "16px",
                        "xl": "24px",
                        "full": "9999px"
                    }
                },
                "elevation": {
                    "levels": {
                        "0": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                        "1": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
                        "2": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
                        "3": "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)"
                    },
                    "blur": {
                        "sm": "blur(4px)",
                        "md": "blur(8px)",
                        "lg": "blur(16px)"
                    }
                },
                "animation": {
                    "timing": {
                        "fast": "150ms",
                        "normal": "300ms",
                        "slow": "500ms"
                    },
                    "easing": {
                        "default": "cubic-bezier(0.4, 0, 0.2, 1)",
                        "emphasized": "cubic-bezier(0.2, 0, 0, 1)",
                        "decelerate": "cubic-bezier(0, 0, 0.2, 1)"
                    }
                }
            }
        
        return tokens
    except Exception:
        return {}

# Initialize with dark theme as default
TOKENS = load_design_tokens()
CURRENT_THEME = "dark"  # Will be togglable
THEME_TOKENS = TOKENS.get("color", {}).get(CURRENT_THEME, {})

st.set_page_config(
    page_title="SBI Network Intelligence",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====================
# 2. ENHANCED DUAL-THEME DESIGN SYSTEM
# ====================

def inject_enhanced_design_system(theme: str = "dark"):
    """Inject sophisticated CSS with dual-theme support and color theory."""
    theme_tokens = TOKENS.get("color", {}).get(theme, {})
    typo = TOKENS.get("typography", {})
    spacing = TOKENS.get("spacing", {})
    elevation = TOKENS.get("elevation", {})
    animation = TOKENS.get("animation", {})
    
    primary = theme_tokens.get("primary", {})
    accent = theme_tokens.get("accent", {})
    surface = theme_tokens.get("surface", {})
    text = theme_tokens.get("text", {})
    semantic = theme_tokens.get("semantic", {})
    
    st.markdown(f"""
    <style>
    /* ===== DUAL-THEME CSS CUSTOM PROPERTIES ===== */
    :root {{
        /* Color System - Primary & Accent */
        --color-primary-50: {primary.get('50', '#eef2ff')};
        --color-primary-500: {primary.get('500', '#6366f1')};
        --color-primary-700: {primary.get('700', '#4338ca')};
        --color-accent-500: {accent.get('500', '#14b8a6')};
        --color-accent-300: {accent.get('300', '#5eead4')};
        
        /* Surface Colors */
        --color-surface-0: {surface.get('0', '#0a0a0a')};
        --color-surface-1: {surface.get('1', '#1a1a1a')};
        --color-surface-2: {surface.get('2', '#262626')};
        --color-surface-3: {surface.get('3', '#404040')};
        
        /* Text Colors */
        --color-text-primary: {text.get('primary', '#fafafa')};
        --color-text-secondary: {text.get('secondary', '#d4d4d4')};
        --color-text-tertiary: {text.get('tertiary', '#a3a3a3')};
        
        /* Semantic Colors */
        --color-success: {semantic.get('success', '#10b981')};
        --color-warning: {semantic.get('warning', '#f59e0b')};
        --color-error: {semantic.get('error', '#ef4444')};
        --color-info: {semantic.get('info', '#3b82f6')};
        
        /* Typography System */
        --font-family: {typo.get('font_family', "'Inter', sans-serif")};
        --font-mono: {typo.get('font_mono', "'JetBrains Mono', monospace")};
        --font-display-lg: {typo.get('scale', {}).get('display', {}).get('lg', '3rem')};
        --font-heading-md: {typo.get('scale', {}).get('heading', {}).get('md', '1.25rem')};
        --font-body-md: {typo.get('scale', {}).get('body', {}).get('md', '1rem')};
        --font-caption: {typo.get('scale', {}).get('caption', '0.75rem')};
        
        /* Spacing & Layout */
        --radius-md: {spacing.get('radius', {}).get('md', '12px')};
        --radius-lg: {spacing.get('radius', {}).get('lg', '16px')};
        --space-3: {spacing.get('scale', [0,4,8,12,16,20,24,32,40,48,56,64,80,96,128])[3]}px;
        --space-4: {spacing.get('scale', [0,4,8,12,16,20,24,32,40,48,56,64,80,96,128])[4]}px;
        --space-6: {spacing.get('scale', [0,4,8,12,16,20,24,32,40,48,56,64,80,96,128])[6]}px;
        
        /* Elevation & Depth */
        --shadow-1: {elevation.get('levels', {}).get('1', '0 4px 6px -1px rgb(0 0 0 / 0.1)')};
        --shadow-2: {elevation.get('levels', {}).get('2', '0 10px 15px -3px rgb(0 0 0 / 0.1)')};
        --shadow-3: {elevation.get('levels', {}).get('3', '0 20px 25px -5px rgb(0 0 0 / 0.1)')};
        --blur-md: {elevation.get('blur', {}).get('md', 'blur(8px)')};
        
        /* Animation */
        --timing-normal: {animation.get('timing', {}).get('normal', '300ms')};
        --easing-default: {animation.get('easing', {}).get('default', 'cubic-bezier(0.4, 0, 0.2, 1)')};
    }}
    
    /* ===== BASE RESET & THEME APPLICATIONS ===== */
    .stApp {{
        background: var(--color-surface-0) !important;
        color: var(--color-text-primary) !important;
        font-family: var(--font-family) !important;
        font-weight: 400;
        line-height: 1.6;
        letter-spacing: -0.01em;
    }}
    
    /* ===== ELEGANT TYPOGRAPHY HIERARCHY ===== */
    h1, h2, h3, h4, h5, h6 {{
        font-weight: 600;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }}
    
    .stMarkdown h1 {{
        font-size: var(--font-display-lg) !important;
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem !important;
    }}
    
    .stMarkdown h2 {{
        font-size: var(--font-heading-md) !important;
        color: var(--color-text-primary) !important;
        margin-top: 2rem !important;
        margin-bottom: 1rem !important;
    }}
    
    /* ===== REFINED CARD SYSTEM ===== */
    .glass-card {{
        background: linear-gradient(
            145deg,
            rgba(255, 255, 255, 0.05),
            rgba(255, 255, 255, 0.02)
        ) !important;
        backdrop-filter: var(--blur-md);
        border-radius: var(--radius-lg) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: var(--shadow-1) !important;
        transition: all var(--timing-normal) var(--easing-default) !important;
    }}
    
    .glass-card:hover {{
        transform: translateY(-4px) scale(1.01);
        box-shadow: var(--shadow-3) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
    }}
    
    /* ===== STREAMLIT COMPONENT OVERHAUL ===== */
    
    /* Metric Cards - Elegant Redesign */
    [data-testid="stMetric"] {{
        background: var(--color-surface-1) !important;
        border-radius: var(--radius-lg) !important;
        padding: var(--space-6) var(--space-4) !important;
        border-left: 4px solid var(--color-accent-500) !important;
        box-shadow: var(--shadow-1) !important;
        transition: all var(--timing-normal) var(--easing-default) !important;
    }}
    
    [data-testid="stMetric"]:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-2) !important;
        border-left-color: var(--color-accent-300) !important;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: var(--color-text-secondary) !important;
        font-size: var(--font-caption) !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    [data-testid="stMetricValue"] {{
        color: var(--color-text-primary) !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        line-height: 1.1 !important;
    }}
    
    [data-testid="stMetricDelta"] {{
        font-weight: 600 !important;
    }}
    
    /* Sidebar - Minimal & Elegant */
    [data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            var(--color-surface-1),
            var(--color-surface-0)
        ) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    
    /* Form Controls - Modern */
    .stSelectbox, .stSlider, .stTextInput {{
        background: var(--color-surface-2) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 200ms ease !important;
    }}
    
    .stSelectbox:hover, .stSlider:hover {{
        border-color: var(--color-primary-500) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1) !important;
    }}
    
    /* Buttons - Sophisticated */
    .stButton > button {{
        background: linear-gradient(
            135deg,
            var(--color-primary-500),
            var(--color-primary-700)
        ) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.025em;
        transition: all var(--timing-normal) var(--easing-default) !important;
        box-shadow: var(--shadow-1) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-2) !important;
        background: linear-gradient(
            135deg,
            var(--color-primary-400),
            var(--color-primary-600)
        ) !important;
    }}
    
    /* Data Table - Clean */
    .stDataFrame {{
        border-radius: var(--radius-lg) !important;
        overflow: hidden !important;
    }}
    
    /* Divider - Subtle */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.1),
            transparent
        ) !important;
        margin: 2rem 0 !important;
    }}
    
    /* Tooltip - Elegant */
    .map-tooltip {{
        background: var(--color-surface-1) !important;
        backdrop-filter: var(--blur-md) !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: var(--shadow-3) !important;
        padding: 1rem !important;
        max-width: 280px !important;
    }}
    
    .map-tooltip h3 {{
        color: var(--color-accent-500) !important;
        margin: 0 0 0.5rem 0 !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }}
    
    .map-tooltip p {{
        color: var(--color-text-secondary) !important;
        margin: 0.25rem 0 !important;
        font-size: 0.875rem !important;
        line-height: 1.4 !important;
    }}
    
    /* ===== ANIMATIONS & MICRO-INTERACTIONS ===== */
    @keyframes fadeSlideUp {{
        from {{ opacity: 0; transform: translateY(12px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}
    
    .animate-fade-up {{
        animation: fadeSlideUp 0.6s var(--easing-default) forwards;
    }}
    
    .animate-float {{
        animation: float 3s var(--easing-default) infinite;
    }}
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {{
        :root {{
            --font-display-lg: 2.25rem;
            --font-heading-md: 1.25rem;
        }}
        
        .stMetricValue {{
            font-size: 1.75rem !important;
        }}
    }}
    
    /* ===== UTILITY CLASSES ===== */
    .text-gradient {{
        background: linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .border-gradient {{
        border: double 2px transparent;
        background-image: linear-gradient(var(--color-surface-1), var(--color-surface-1)), 
                          linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500));
        background-origin: border-box;
        background-clip: padding-box, border-box;
    }}
    </style>
    """, unsafe_allow_html=True)

# ====================
# 3. SIMPLIFIED DATA MANAGEMENT
# ====================

@st.cache_data
def load_branch_data() -> pd.DataFrame:
    """Load optimized branch data."""
    data = pd.DataFrame({
        "Branch": ["PANATHUR", "BELLANDUR", "BELLANDUR", "PANATHUR", "BRIGADE METROPOLIS"],
        "IFSC_Code": ["SBIN0017040", "SBIN0015647", "SBIN0041171", "SBIN0016877", "SBIN0015034"],
        "Address": [
            "SBI BANK,NO.132 BY 8,PANATHUR JUNCTION,PANATHUR,MARATHAHALLI",
            "SBI BANK, SURAJPUR MAIN ROAD, KAIKONDRAHALLI, BELANDUR WARD",
            "SBI BANK,THANUSH ARCADE, BELLANDUR OUTER RING ROAD,NEXT TO COFFEE DAY",
            "SBI BANK,NO. 535, GURMUKH SINGH COMMERCIAL COMPLEX, AMARJYOTHI H.B.C.S. LAYOUT, DOMLUR",
            "SBI BANK,MS BRIGADE ENTERPRISES, WHITEFIELD ROAD"
        ],
        "City": ["BANGALORE"] * 5,
        "Pincode": ["560037", "560035", "560103", "560071", "560016"],
        "Latitude": [12.9382107, 12.9188658, 12.9246927, 12.9534312, 12.9927608],
        "Longitude": [77.6992385, 77.6700914, 77.672937, 77.6406167, 77.7021471],
        "Performance_Score": [0.85, 0.92, 0.78, 0.88, 0.95]
    })
    return data

# ====================
# 4. ENHANCED 3D MAP VISUALIZATION
# ====================

def create_3d_icon_layer(data: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Layer:
    """Create elegant 3D icon layer with color theory."""
    # Performance-based colors
    colors = []
    for score in data['Performance_Score']:
        if score >= 0.9:
            colors.append([16, 185, 129, 230])  # Emerald
        elif score >= 0.8:
            colors.append([59, 130, 246, 210])  # Blue
        elif score >= 0.7:
            colors.append([245, 158, 11, 190])  # Amber
        else:
            colors.append([239, 68, 68, 170])   # Red
    
    ICON_DATA = {
        "url": "https://cdn-icons-png.flaticon.com/512/684/684908.png",
        "width": 128,
        "height": 128,
        "anchorY": 128
    }
    
    data = data.copy()
    data['icon_data'] = [ICON_DATA] * len(data)
    data['icon_size'] = 1.0
    
    if selected_branch and selected_branch != 'All Branches':
        data.loc[data['Branch'] == selected_branch, 'icon_size'] = 1.8
    
    return pdk.Layer(
        "IconLayer",
        data=data,
        get_icon="icon_data",
        get_size="icon_size",
        get_position=['Longitude', 'Latitude'],
        pickable=True,
        auto_highlight=True,
        highlight_color=[255, 255, 255, 150],
        size_scale=18,
        get_color=colors,
        transitions={'get_size': 800, 'get_color': 800}
    )

def create_map_view(data: pd.DataFrame, selected_branch: Optional[str] = None,
                   pitch: int = 50, zoom: int = 11, bearing: int = 0) -> pdk.Deck:
    """Create immersive 3D map with rotation controls."""
    layers = [create_3d_icon_layer(data, selected_branch)]
    
    # Calculate view state
    if selected_branch and selected_branch != 'All Branches':
        selected = data[data['Branch'] == selected_branch]
        if len(selected) > 0:
            lat, lon = selected[['Latitude', 'Longitude']].iloc[0]
            zoom = 14
        else:
            lat, lon = data[['Latitude', 'Longitude']].mean()
    else:
        lat, lon = data[['Latitude', 'Longitude']].mean()
    
    view_state = pdk.ViewState(
        latitude=float(lat),
        longitude=float(lon),
        zoom=zoom,
        pitch=pitch,
        bearing=bearing
    )
    
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style='dark' if CURRENT_THEME == 'dark' else 'light',
        tooltip={
            "html": """
            <div class="map-tooltip">
                <h3>{Branch}</h3>
                <p><strong>IFSC:</strong> {IFSC_Code}</p>
                <p><strong>Area:</strong> {Address.split(',')[0]}</p>
                <p><strong>Pincode:</strong> {Pincode}</p>
                <p><strong>Performance:</strong> <span style="color:{'#10b981' if Performance_Score >= 0.8 else '#f59e0b'}">{Performance_Score:.0%}</span></p>
            </div>
            """,
            "style": {
                "backgroundColor": THEME_TOKENS.get("surface", {}).get("1", "#1a1a1a"),
                "color": THEME_TOKENS.get("text", {}).get("primary", "#fafafa")
            }
        },
        width="100%",
        height=550
    )

# ====================
# 5. REFINED DASHBOARD COMPONENTS
# ====================

def render_minimal_metrics(data: pd.DataFrame):
    """Render elegant, minimal metric cards."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.container():
            st.markdown("####  **Network**")
            st.markdown(f"### {len(data)}")
            st.caption("Total Branches")
    
    with col2:
        with st.container():
            st.markdown("####  **Coverage**")
            st.markdown(f"### {data['City'].nunique()}")
            st.caption("Cities")
    
    with col3:
        with st.container():
            st.markdown("####  **Performance**")
            avg_perf = data['Performance_Score'].mean()
            st.markdown(f"### {avg_perf:.1%}")
            st.caption("Average Score")

def render_simplified_table(data: pd.DataFrame):
    """Render clean, focused data table."""
    # Show only essential columns
    display_data = data[['Branch', 'IFSC_Code', 'City', 'Pincode', 'Performance_Score']].copy()
    display_data['Performance'] = display_data['Performance_Score'].apply(
        lambda x: f"{x:.0%}"
    )
    
    column_config = {
        "Branch": st.column_config.TextColumn("Branch", width="medium"),
        "IFSC_Code": st.column_config.TextColumn("IFSC", width="medium"),
        "City": st.column_config.TextColumn("City", width="small"),
        "Pincode": st.column_config.TextColumn("Pincode", width="small"),
        "Performance": st.column_config.ProgressColumn(
            "Performance",
            format="%f",
            min_value=0,
            max_value=1,
            width="medium"
        )
    }
    
    st.dataframe(
        display_data[['Branch', 'IFSC_Code', 'City', 'Pincode', 'Performance']],
        column_config=column_config,
        use_container_width=True,
        hide_index=True
    )

# ====================
# 6. REFINED MAIN APPLICATION
# ====================

def main():
    """Main application with refined UI."""
    
    # Initialize theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Inject design system
    inject_enhanced_design_system(st.session_state.theme)
    
    # Load data
    data = load_branch_data()
    
    # ===== ELEGANT HEADER =====
    st.markdown("""
    <div class="animate-fade-up" style="margin-bottom: 3rem;">
        <h1> SBI Network Intelligence</h1>
        <p style="color: var(--color-text-secondary); font-size: 1.1rem; margin-top: 0.5rem;">
            Immersive 3D visualization of branch network performance
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # ===== REFINED SIDEBAR =====
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; margin-bottom: 2.5rem;">
            <div style="
                font-size: 1.5rem;
                font-weight: 700;
                background: linear-gradient(135deg, var(--color-primary-500), var(--color-accent-500));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 0.5rem;
            ">
                SBI 3D
            </div>
            <div style="color: var(--color-text-tertiary); font-size: 0.875rem;">
                Interactive Dashboard
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Theme Toggle
        st.session_state.theme = st.radio(
            "Theme",
            ["Dark", "Light"],
            horizontal=True,
            label_visibility="collapsed"
        ).lower()
        
        st.divider()
        
        # Map Controls
        st.markdown("####  **Controls**")
        
        selected_branch = st.selectbox(
            "Branch Focus",
            ['All Branches'] + sorted(data['Branch'].unique()),
            key="branch_select"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            map_pitch = st.slider("Tilt", 0, 60, 45)
        with col2:
            map_zoom = st.slider("Zoom", 5, 20, 11)
        
        map_style = st.selectbox(
            "Map Style",
            ["Dark", "Light", "Satellite"],
            index=0 if st.session_state.theme == 'dark' else 1
        )
        
        st.divider()
        
        # Visual Effects
        st.markdown("####  **Effects**")
        show_animations = st.toggle("Animations", True)
        
        st.divider()
        
        # Info
        st.caption(f"**Data:** {len(data)} locations")
        st.caption(f"**Updated:** {datetime.now().strftime('%b %d, %Y')}")
    
    # ===== MAIN CONTENT =====
    
    # Minimal Metrics
    render_minimal_metrics(data)
    
    st.divider()
    
    # 3D Map
    st.markdown("####  **Interactive 3D Map**")
    st.caption("Hold Shift + drag to rotate • Scroll to zoom • Click pins for details")
    
    deck = create_map_view(
        data=data,
        selected_branch=selected_branch,
        pitch=map_pitch,
        zoom=map_zoom
    )
    st.pydeck_chart(deck, use_container_width=True)
    
    # Map Controls
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button(" Reset View", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Simplified Data
    st.markdown("####  **Branch Details**")
    render_simplified_table(data)
    
    # Elegant Footer
    st.markdown("""
    <div style="
        text-align: center;
        margin-top: 3rem;
        padding-top: 2rem;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        color: var(--color-text-tertiary);
        font-size: 0.875rem;
    ">
        <div>SBI Network Intelligence Dashboard v2.0</div>
        <div style="margin-top: 0.5rem; font-size: 0.75rem;">
            Professional 3D Visualization • Color Theory Design System
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
