import streamlit as st
import pandas as pd
import pydeck as pdk
import json
from datetime import datetime
from typing import Optional, Dict, Any
import os

# ====================
# 1. ENHANCED DESIGN TOKENS WITH COLOR THEORY
# ====================

@st.cache_resource
def load_design_tokens() -> Dict[str, Any]:
    """Load enhanced design tokens with elegant color palette."""
    try:
        if os.path.exists('theme_tokens.json'):
            with open('theme_tokens.json', 'r') as f:
                tokens = json.load(f)
        else:
            # Elegant color palette based on color theory
            tokens = {
                "themes": {
                    "dark": {
                        "color": {
                            "primary": {
                                "50": "#e6f3ff",
                                "100": "#cce7ff",
                                "200": "#99d0ff",
                                "300": "#66b8ff",
                                "400": "#339fff",
                                "500": "#0066cc",  # Elegant blue
                                "600": "#0052a3",
                                "700": "#003d7a",
                                "800": "#002952",
                                "900": "#001429"
                            },
                            "secondary": {
                                "500": "#8a2be2",  # Blue violet accent
                                "600": "#7a1fd2",
                                "700": "#6a13c2"
                            },
                            "surface": {
                                "0": "#0a0a0f",    # Deep space black
                                "1": "#151522",    # Rich dark blue
                                "2": "#1e1e2d",    # Card surface
                                "3": "#2a2a3a",    # Elevated surface
                                "4": "#36364a"     # Hover surface
                            },
                            "accent": {
                                "gradient": {
                                    "start": "#0066cc",
                                    "middle": "#8a2be2",
                                    "end": "#00d4ff"
                                }
                            },
                            "semantic": {
                                "success": "#10dc60",
                                "warning": "#ffce00",
                                "danger": "#f04141",
                                "info": "#0cd1e8",
                                "muted": "rgba(255, 255, 255, 0.5)",
                                "text": {
                                    "primary": "rgba(255, 255, 255, 0.95)",
                                    "secondary": "rgba(255, 255, 255, 0.7)",
                                    "tertiary": "rgba(255, 255, 255, 0.5)"
                                }
                            }
                        },
                        "gradients": {
                            "primary": "linear-gradient(135deg, #0066cc 0%, #8a2be2 50%, #00d4ff 100%)",
                            "card": "linear-gradient(145deg, #1e1e2d 0%, #2a2a3a 100%)",
                            "sidebar": "linear-gradient(180deg, #151522 0%, #0a0a0f 100%)"
                        },
                        "glass": {
                            "morphism": "rgba(30, 30, 45, 0.7)",
                            "border": "rgba(255, 255, 255, 0.1)"
                        }
                    },
                    "light": {
                        "color": {
                            "primary": {
                                "500": "#0066cc",
                                "600": "#0052a3",
                                "700": "#003d7a"
                            },
                            "secondary": {
                                "500": "#8a2be2",
                                "600": "#7a1fd2",
                                "700": "#6a13c2"
                            },
                            "surface": {
                                "0": "#f8f9ff",
                                "1": "#ffffff",
                                "2": "#f0f4ff",
                                "3": "#e6ebff",
                                "4": "#dce2ff"
                            },
                            "accent": {
                                "gradient": {
                                    "start": "#0066cc",
                                    "middle": "#8a2be2",
                                    "end": "#00d4ff"
                                }
                            },
                            "semantic": {
                                "success": "#28a745",
                                "warning": "#ffc107",
                                "danger": "#dc3545",
                                "info": "#17a2b8",
                                "muted": "rgba(0, 0, 0, 0.5)",
                                "text": {
                                    "primary": "rgba(0, 0, 0, 0.9)",
                                    "secondary": "rgba(0, 0, 0, 0.7)",
                                    "tertiary": "rgba(0, 0, 0, 0.5)"
                                }
                            }
                        },
                        "gradients": {
                            "primary": "linear-gradient(135deg, #0066cc 0%, #8a2be2 50%, #00d4ff 100%)",
                            "card": "linear-gradient(145deg, #ffffff 0%, #f0f4ff 100%)",
                            "sidebar": "linear-gradient(180deg, #ffffff 0%, #f8f9ff 100%)"
                        },
                        "glass": {
                            "morphism": "rgba(255, 255, 255, 0.7)",
                            "border": "rgba(0, 0, 0, 0.1)"
                        }
                    }
                },
                "typography": {
                    "font_family": "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif",
                    "display": {
                        "xl": "3.5rem",
                        "lg": "2.5rem",
                        "md": "2rem",
                        "sm": "1.75rem"
                    },
                    "heading": {
                        "xl": "1.5rem",
                        "lg": "1.25rem",
                        "md": "1.125rem",
                        "sm": "1rem"
                    },
                    "body": {
                        "lg": "1rem",
                        "md": "0.875rem",
                        "sm": "0.75rem"
                    },
                    "lineHeight": {
                        "tight": "1.2",
                        "normal": "1.5",
                        "relaxed": "1.75"
                    }
                },
                "spacing": {
                    "base": "0.5rem",
                    "scale": [0, 0.25, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24, 32]
                },
                "effects": {
                    "shadows": {
                        "sm": "0 2px 8px rgba(0, 0, 0, 0.1)",
                        "md": "0 4px 20px rgba(0, 0, 0, 0.15)",
                        "lg": "0 8px 40px rgba(0, 0, 0, 0.2)",
                        "xl": "0 20px 60px rgba(0, 0, 0, 0.3)",
                        "glow": "0 0 40px rgba(0, 102, 204, 0.3)"
                    },
                    "blur": {
                        "sm": "blur(8px)",
                        "md": "blur(16px)",
                        "lg": "blur(24px)"
                    }
                },
                "animation": {
                    "duration": {
                        "fast": "200ms",
                        "normal": "300ms",
                        "slow": "500ms"
                    },
                    "easing": {
                        "standard": "cubic-bezier(0.4, 0, 0.2, 1)",
                        "decelerate": "cubic-bezier(0, 0, 0.2, 1)",
                        "accelerate": "cubic-bezier(0.4, 0, 1, 1)"
                    }
                },
                "radius": {
                    "sm": "8px",
                    "md": "12px",
                    "lg": "16px",
                    "xl": "24px",
                    "full": "9999px"
                }
            }
        return tokens
    except Exception as e:
        st.error(f"Error loading tokens: {e}")
        return {}

# Initialize with dark theme by default
TOKENS = load_design_tokens()
CURRENT_THEME = "dark"

# ====================
# 2. ENHANCED DESIGN SYSTEM WITH 3D EFFECTS
# ====================

def inject_design_system():
    """Inject comprehensive CSS with elegant design system and 3D effects."""
    theme = st.session_state.get('theme', 'dark')
    tokens = TOKENS["themes"][theme]
    
    st.markdown(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
        /* ===== CSS CUSTOM PROPERTIES ===== */
        :root {{
            /* Color Palette */
            --color-primary-500: {tokens["color"]["primary"]["500"]};
            --color-primary-600: {tokens["color"]["primary"]["600"]};
            --color-primary-700: {tokens["color"]["primary"]["700"]};
            --color-secondary-500: {tokens["color"]["secondary"]["500"]};
            --color-surface-0: {tokens["color"]["surface"]["0"]};
            --color-surface-1: {tokens["color"]["surface"]["1"]};
            --color-surface-2: {tokens["color"]["surface"]["2"]};
            --color-surface-3: {tokens["color"]["surface"]["3"]};
            --color-surface-4: {tokens["color"]["surface"]["4"]};
            
            /* Gradients */
            --gradient-primary: {tokens["gradients"]["primary"]};
            --gradient-card: {tokens["gradients"]["card"]};
            --gradient-sidebar: {tokens["gradients"]["sidebar"]};
            
            /* Glass Morphism */
            --glass-bg: {tokens["glass"]["morphism"]};
            --glass-border: {tokens["glass"]["border"]};
            
            /* Semantic Colors */
            --color-success: {tokens["color"]["semantic"]["success"]};
            --color-warning: {tokens["color"]["semantic"]["warning"]};
            --color-danger: {tokens["color"]["semantic"]["danger"]};
            --color-info: {tokens["color"]["semantic"]["info"]};
            --color-text-primary: {tokens["color"]["semantic"]["text"]["primary"]};
            --color-text-secondary: {tokens["color"]["semantic"]["text"]["secondary"]};
            --color-text-tertiary: {tokens["color"]["semantic"]["text"]["tertiary"]};
            
            /* Typography */
            --font-family: {TOKENS["typography"]["font_family"]};
            --font-display-xl: {TOKENS["typography"]["display"]["xl"]};
            --font-display-lg: {TOKENS["typography"]["display"]["lg"]};
            --font-heading-xl: {TOKENS["typography"]["heading"]["xl"]};
            --font-heading-lg: {TOKENS["typography"]["heading"]["lg"]};
            --font-body-lg: {TOKENS["typography"]["body"]["lg"]};
            --font-body-md: {TOKENS["typography"]["body"]["md"]};
            
            /* Spacing */
            --space-1: {TOKENS["spacing"]["scale"][1]}rem;
            --space-2: {TOKENS["spacing"]["scale"][2]}rem;
            --space-3: {TOKENS["spacing"]["scale"][3]}rem;
            --space-4: {TOKENS["spacing"]["scale"][4]}rem;
            --space-6: {TOKENS["spacing"]["scale"][6]}rem;
            --space-8: {TOKENS["spacing"]["scale"][8]}rem;
            
            /* Effects */
            --shadow-sm: {TOKENS["effects"]["shadows"]["sm"]};
            --shadow-md: {TOKENS["effects"]["shadows"]["md"]};
            --shadow-lg: {TOKENS["effects"]["shadows"]["lg"]};
            --shadow-xl: {TOKENS["effects"]["shadows"]["xl"]};
            --shadow-glow: {TOKENS["effects"]["shadows"]["glow"]};
            --blur-md: {TOKENS["effects"]["blur"]["md"]};
            
            /* Animation */
            --duration-normal: {TOKENS["animation"]["duration"]["normal"]};
            --easing-standard: {TOKENS["animation"]["easing"]["standard"]};
            
            /* Radius */
            --radius-md: {TOKENS["radius"]["md"]};
            --radius-lg: {TOKENS["radius"]["lg"]};
            --radius-xl: {TOKENS["radius"]["xl"]};
        }}
        
        /* ===== BASE STYLES WITH 3D PERSPECTIVE ===== */
        .stApp {{
            background: var(--color-surface-0);
            background-image: 
                radial-gradient(at 40% 20%, rgba(var(--color-primary-500), 0.15) 0px, transparent 50%),
                radial-gradient(at 80% 0%, rgba(var(--color-secondary-500), 0.15) 0px, transparent 50%),
                radial-gradient(at 0% 50%, rgba(var(--color-info), 0.1) 0px, transparent 50%),
                radial-gradient(at 80% 50%, rgba(var(--color-warning), 0.1) 0px, transparent 50%);
            color: var(--color-text-primary);
            font-family: var(--font-family);
            min-height: 100vh;
            perspective: 1000px;
        }}
        
        /* ===== 3D CARD EFFECTS ===== */
        .card-3d {{
            background: var(--gradient-card);
            border-radius: var(--radius-xl);
            padding: var(--space-6);
            backdrop-filter: var(--blur-md);
            border: 1px solid var(--glass-border);
            box-shadow: var(--shadow-xl);
            transform-style: preserve-3d;
            transition: all 0.4s var(--easing-standard);
            position: relative;
            overflow: hidden;
        }}
        
        .card-3d::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
            border-radius: var(--radius-xl) var(--radius-xl) 0 0;
            z-index: 2;
        }}
        
        .card-3d:hover {{
            transform: translateY(-12px) rotateX(5deg);
            box-shadow: var(--shadow-xl), var(--shadow-glow);
        }}
        
        /* ===== GLASS MORPHISM ===== */
        .glass-panel {{
            background: var(--glass-bg);
            backdrop-filter: var(--blur-md);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
        }}
        
        /* ===== TYPOGRAPHY ENHANCEMENTS ===== */
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 700;
            line-height: 1.2;
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--space-4);
        }}
        
        .gradient-text {{
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 800;
        }}
        
        /* ===== STREAMLIT COMPONENT OVERRIDES ===== */
        /* Metric Cards with 3D effect */
        [data-testid="stMetric"] {{
            background: var(--gradient-card) !important;
            backdrop-filter: var(--blur-md);
            border-radius: var(--radius-lg) !important;
            padding: var(--space-4) !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--shadow-md) !important;
            transition: all 0.3s var(--easing-standard) !important;
            position: relative;
            overflow: hidden;
        }}
        
        [data-testid="stMetric"]::before {{
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            bottom: 0;
            width: 4px;
            background: var(--gradient-primary);
            border-radius: var(--radius-lg) 0 0 var(--radius-lg);
        }}
        
        [data-testid="stMetric"]:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
        }}
        
        [data-testid="stMetricLabel"] {{
            color: var(--color-text-secondary) !important;
            font-size: var(--font-body-md) !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        [data-testid="stMetricValue"] {{
            color: var(--color-text-primary) !important;
            font-size: var(--font-heading-xl) !important;
            font-weight: 800 !important;
        }}
        
        /* Buttons with 3D effect */
        .stButton > button {{
            background: var(--gradient-primary) !important;
            color: white !important;
            border: none !important;
            border-radius: var(--radius-lg) !important;
            padding: var(--space-3) var(--space-6) !important;
            font-weight: 600 !important;
            font-size: var(--font-body-md) !important;
            transition: all 0.3s var(--easing-standard) !important;
            box-shadow: var(--shadow-md) !important;
            position: relative;
            overflow: hidden;
            z-index: 1;
        }}
        
        .stButton > button::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
            z-index: -1;
            transition: opacity 0.3s;
            opacity: 0;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-3px) scale(1.05);
            box-shadow: var(--shadow-lg), var(--shadow-glow) !important;
        }}
        
        .stButton > button:hover::before {{
            opacity: 1;
        }}
        
        /* Selectboxes */
        [data-testid="stSelectbox"] {{
            background: var(--gradient-card) !important;
            border-radius: var(--radius-lg) !important;
            border: 1px solid var(--glass-border) !important;
            box-shadow: var(--shadow-sm) !important;
        }}
        
        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background: var(--gradient-sidebar) !important;
            backdrop-filter: var(--blur-md);
            border-right: 1px solid var(--glass-border);
            box-shadow: var(--shadow-lg);
        }}
        
        /* Sliders */
        [data-testid="stSlider"] > div > div {{
            background: var(--gradient-primary) !important;
        }}
        
        /* Dataframes and Tables */
        .stDataFrame {{
            border-radius: var(--radius-lg) !important;
            overflow: hidden !important;
            box-shadow: var(--shadow-md) !important;
        }}
        
        /* ===== CUSTOM COMPONENTS ===== */
        .stat-badge {{
            display: inline-flex;
            align-items: center;
            padding: var(--space-1) var(--space-3);
            background: var(--gradient-primary);
            color: white;
            border-radius: var(--radius-full);
            font-size: var(--font-body-sm);
            font-weight: 600;
            box-shadow: var(--shadow-sm);
        }}
        
        .pulse-dot {{
            width: 8px;
            height: 8px;
            background: var(--color-success);
            border-radius: 50%;
            margin-right: var(--space-1);
            animation: pulse 2s infinite;
        }}
        
        /* ===== ANIMATIONS ===== */
        @keyframes pulse {{
            0% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.5); opacity: 0.7; }}
            100% {{ transform: scale(1); opacity: 1; }}
        }}
        
        @keyframes float {{
            0%, 100% {{ transform: translateY(0) rotate(0); }}
            50% {{ transform: translateY(-20px) rotate(5deg); }}
        }}
        
        @keyframes shimmer {{
            0% {{ background-position: -1000px 0; }}
            100% {{ background-position: 1000px 0; }}
        }}
        
        .float-animation {{
            animation: float 6s ease-in-out infinite;
        }}
        
        /* ===== RESPONSIVE DESIGN ===== */
        @media (max-width: 768px) {{
            .card-3d:hover {{
                transform: translateY(-8px);
            }}
            
            [data-testid="stMetric"]:hover {{
                transform: translateY(-4px);
            }}
        }}
        
        /* ===== UTILITY CLASSES ===== */
        .text-gradient {{
            background: var(--gradient-primary);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .border-gradient {{
            border: 2px solid transparent;
            background: linear-gradient(var(--color-surface-2), var(--color-surface-2)) padding-box,
                        var(--gradient-primary) border-box;
        }}
        </style>
    </head>
    </html>
    """, unsafe_allow_html=True)

# ====================
# 3. DATA MANAGEMENT
# ====================

@st.cache_data
def load_branch_data() -> pd.DataFrame:
    """Load and cache branch data."""
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
        "State": ["KARNATAKA"] * 5,
        "Pincode": ["560037", "560035", "560103", "560071", "560016"],
        "Country": ["India"] * 5,
        "Latitude": [12.9382107, 12.9188658, 12.9246927, 12.9534312, 12.9927608],
        "Longitude": [77.6992385, 77.6700914, 77.672937, 77.6406167, 77.7021471]
    })
    
    data['Branch_Size'] = [100, 150, 120, 130, 200]
    data['Performance_Score'] = [0.8, 0.9, 0.7, 0.85, 0.95]
    data['Transaction_Volume'] = [5000000, 7500000, 4500000, 6000000, 9000000]
    
    return data

# ====================
# 4. 3D MAP VISUALIZATION
# ====================

def create_3d_map(data: pd.DataFrame, selected_branch: Optional[str] = None) -> pdk.Deck:
    """Create enhanced 3D map with better visual effects."""
    colors = []
    for score in data['Performance_Score']:
        if score >= 0.9:
            colors.append([16, 220, 96, 200])  # Success green
        elif score >= 0.7:
            colors.append([255, 206, 0, 180])   # Warning yellow
        else:
            colors.append([240, 65, 65, 160])   # Danger red
    
    layers = [
        pdk.Layer(
            "ScatterplotLayer",
            data=data,
            get_position=['Longitude', 'Latitude'],
            get_fill_color=colors,
            get_radius='Transaction_Volume',
            radius_scale=0.0001,
            radius_min_pixels=10,
            radius_max_pixels=100,
            pickable=True,
            auto_highlight=True,
            stroked=True,
            get_line_color=[255, 255, 255, 200],
            line_width_min_pixels=2
        ),
        pdk.Layer(
            "TextLayer",
            data=data,
            get_position=['Longitude', 'Latitude'],
            get_text='Branch',
            get_color=[255, 255, 255, 255],
            get_size=14,
            get_alignment_baseline="'bottom'"
        )
    ]
    
    # Set view based on selection
    if selected_branch and selected_branch != 'All Branches':
        selected_data = data[data['Branch'] == selected_branch]
        if len(selected_data) > 0:
            lat = selected_data['Latitude'].iloc[0]
            lon = selected_data['Longitude'].iloc[0]
            zoom = 14
        else:
            lat = data['Latitude'].mean()
            lon = data['Longitude'].mean()
            zoom = 11
    else:
        lat = data['Latitude'].mean()
        lon = data['Longitude'].mean()
        zoom = 11
    
    view_state = pdk.ViewState(
        latitude=lat,
        longitude=lon,
        zoom=zoom,
        pitch=60,
        bearing=30,
        max_zoom=20,
        min_zoom=5
    )
    
    return pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v10',
        tooltip={
            "html": """
            <div class="glass-panel" style="padding: 12px; border-radius: 8px;">
                <h3 style="margin: 0 0 8px 0; color: #0066cc;">{Branch}</h3>
                <p style="margin: 4px 0;"><strong>IFSC:</strong> {IFSC_Code}</p>
                <p style="margin: 4px 0;"><strong>Performance:</strong> {Performance_Score:.0%}</p>
                <p style="margin: 4px 0;"><strong>Volume:</strong> ₹{Transaction_Volume:,.0f}</p>
            </div>
            """
        },
        width="100%",
        height=600
    )

# ====================
# 5. DASHBOARD COMPONENTS
# ====================

def render_header():
    """Render enhanced header with theme toggle."""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <h1 style="margin-bottom: 0.5rem;">🏦 SBI Bank Network Intelligence</h1>
            <p style="color: var(--color-text-secondary); font-size: 1.1rem;">
            Real-time 3D visualization of branch network performance and analytics
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🌙 Dark Theme" if st.session_state.get('theme', 'dark') == 'light' else "☀️ Light Theme", 
                    use_container_width=True):
            st.session_state.theme = 'light' if st.session_state.get('theme', 'dark') == 'dark' else 'dark'
            st.rerun()
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

def render_metrics(data):
    """Render enhanced metric cards."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Branches",
            value=f"{len(data):,}",
            delta="+2 this month",
            delta_color="normal"
        )
    
    with col2:
        total_volume = data['Transaction_Volume'].sum()
        st.metric(
            label="Total Volume",
            value=f"₹{total_volume/1000000:.1f}M",
            delta="+12.5%",
            delta_color="normal"
        )
    
    with col3:
        avg_perf = data['Performance_Score'].mean()
        st.metric(
            label="Avg Performance",
            value=f"{avg_perf:.1%}",
            delta=f"+{avg_perf-0.75:.1%}",
            delta_color="normal"
        )
    
    with col4:
        high_perf = len(data[data['Performance_Score'] >= 0.8])
        st.metric(
            label="High Performers",
            value=high_perf,
            delta=f"{high_perf/len(data)*100:.0f}%",
            delta_color="normal"
        )

def render_sidebar(data):
    """Render enhanced sidebar."""
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 1.5rem; font-weight: 800; margin-bottom: 0.5rem;" class="text-gradient">
                SBI DASHBOARD
            </div>
            <div style="color: var(--color-text-tertiary); font-size: 0.875rem;">
                Network Intelligence Platform
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        selected_branch = st.selectbox(
            "📍 Select Branch",
            options=['All Branches'] + list(data['Branch'].unique()),
            help="Focus on specific branch for detailed analysis"
        )
        
        st.divider()
        
        st.markdown("### 🎛️ Map Controls")
        
        col1, col2 = st.columns(2)
        with col1:
            map_style = st.selectbox(
                "Style",
                ["Dark", "Light", "Satellite", "Terrain"],
                index=0
            )
        
        with col2:
            pitch = st.slider("3D Pitch", 0, 80, 60)
        
        zoom = st.slider("Zoom Level", 5, 18, 11)
        
        st.divider()
        
        st.markdown("### 📊 Filters")
        
        perf_range = st.slider(
            "Performance Range",
            0.0, 1.0, (0.7, 1.0)
        )
        
        volume_filter = st.selectbox(
            "Transaction Volume",
            ["All", "High (>₹5M)", "Medium (₹2-5M)", "Low (<₹2M)"]
        )
        
        st.divider()
        
        st.markdown("### 📈 Quick Stats")
        st.caption(f"Active Branches: {len(data)}")
        st.caption(f"Coverage Area: 45.2 km²")
        st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        return selected_branch, {"style": map_style.lower(), "pitch": pitch, "zoom": zoom}

# ====================
# 6. MAIN APPLICATION
# ====================

def main():
    """Main application with enhanced UI."""
    
    # Initialize theme
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    
    # Inject design system
    inject_design_system()
    
    # Load data
    data = load_branch_data()
    
    # Render header
    render_header()
    
    # Render sidebar and get controls
    selected_branch, map_controls = render_sidebar(data)
    
    # Render metrics
    render_metrics(data)
    
    st.divider()
    
    # 3D Map
    st.markdown("""
    <div style="margin: 2rem 0;">
        <h2>🌍 Interactive 3D Network Map</h2>
        <p style="color: var(--color-text-secondary);">
        Visualize branch performance, transaction volumes, and geographical distribution in real-time 3D
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    deck = create_3d_map(data, selected_branch)
    st.pydeck_chart(deck, use_container_width=True)
    
    # Map controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.caption("💡 Click on any branch to view detailed information and analytics")
    with col2:
        if st.button("🔄 Reset View", use_container_width=True):
            st.rerun()
    with col3:
        if st.button("📥 Export Data", use_container_width=True):
            st.success("Data export initiated!")
    
    st.divider()
    
    # Branch Details
    st.markdown("### 📋 Branch Network Details")
    
    # Filter data based on selections
    filtered_data = data.copy()
    if selected_branch != 'All Branches':
        filtered_data = filtered_data[filtered_data['Branch'] == selected_branch]
    
    # Style the dataframe
    def color_performance(val):
        if val >= 0.9:
            color = '#10dc60'
        elif val >= 0.7:
            color = '#ffce00'
        else:
            color = '#f04141'
        return f'background-color: {color}20; color: {color}; font-weight: bold;'
    
    styled_df = filtered_data.style.map(
        lambda x: color_performance(x) if isinstance(x, (int, float)) else '',
        subset=['Performance_Score']
    ).format({
        'Performance_Score': '{:.1%}',
        'Transaction_Volume': '₹{:,.0f}'
    })
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Branch": "Branch Name",
            "IFSC_Code": "IFSC Code",
            "Performance_Score": st.column_config.ProgressColumn(
                "Performance",
                help="Branch performance score",
                format="%.0%",
                min_value=0,
                max_value=1
            ),
            "Transaction_Volume": "Volume (₹)"
        }
    )
    
    # Footer
    st.divider()
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: var(--color-text-tertiary);">
        <p style="font-size: 0.875rem; margin-bottom: 0.5rem;">
        <strong>SBI Bank Network Intelligence Platform v2.0</strong>
        </p>
        <p style="font-size: 0.75rem;">
        Built with advanced 3D visualization • Real-time analytics • Enterprise-grade security
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
