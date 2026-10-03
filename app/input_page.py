"""
AgriPredict — New Prediction Dashboard
Run with:  streamlit run agripredict_app.py
Requires:  pip install streamlit plotly
"""

import base64
import os
import sys
from pathlib import Path
import streamlit as st
import plotly.graph_objects as go

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from utils.wather_api import get_weather
from models.crop_recomendation import crop_recomendation
from models.crop_yeild import predict_yield

LOGO_PATH = ROOT_DIR / "assets" / "logo.png"
if not LOGO_PATH.is_file():
    LOGO_PATH = Path(r"C:\Users\Yash\DataScienceCode\agripredict-ai\assets\logo.png")
LOGO_BASE64 = base64.b64encode(LOGO_PATH.read_bytes()).decode() if LOGO_PATH.is_file() else None

st.set_page_config(page_title="AgriPredict — New Prediction", page_icon="🌱", layout="wide")

# ----------------------------------------------------------------------
# DATA — Indian states -> districts -> (lat, lon)
# ----------------------------------------------------------------------
STATE_DISTRICTS = {

    "Andaman and Nicobar Islands": {
        "NICOBARS": (9.2648, 93.0130),
        "NORTH AND MIDDLE ANDAMAN": (12.6110, 92.8317),
        "SOUTH ANDAMANS": (11.7401, 92.6586),
    },

    "Andhra Pradesh": {
        "ANANTAPUR": (14.6819, 77.6006),
        "CHITTOOR": (13.2172, 79.1003),
        "EAST GODAVARI": (16.9891, 82.2475),
        "GUNTUR": (16.3067, 80.4365),
        "KADAPA": (14.4673, 78.8242),
        "KRISHNA": (16.6100, 80.7214),
        "KURNOOL": (15.8281, 78.0373),
        "PRAKASAM": (15.5057, 80.0499),
        "SPSR NELLORE": (14.4426, 79.9865),
        "SRIKAKULAM": (18.2969, 83.8968),
        "VISAKHAPATNAM": (17.6868, 83.2185),
        "VIZIANAGARAM": (18.1067, 83.3956),
        "WEST GODAVARI": (16.9174, 81.3399),
    },

    "Arunachal Pradesh": {
        "ANJAW": (28.0706, 96.3666),
        "CHANGLANG": (27.1130, 96.7275),
        "DIBANG VALLEY": (28.7406, 95.9697),
        "EAST KAMENG": (27.2646, 93.0466),
        "EAST SIANG": (28.0660, 95.3268),
        "KURUNG KUMEY": (27.5000, 93.6000),
        "LOHIT": (27.9497, 96.1663),
        "LONGDING": (26.8720, 95.3077),
        "LOWER DIBANG VALLEY": (28.1548, 95.7846),
        "LOWER SUBANSIRI": (27.5285, 93.8316),
        "NAMSAI": (27.6698, 95.8597),
        "PAPUM PARE": (27.0844, 93.6053),
        "TAWANG": (27.5861, 91.8594),
        "TIRAP": (27.0192, 95.5635),
        "UPPER SIANG": (28.9833, 94.8167),
        "UPPER SUBANSIRI": (28.3000, 94.0000),
        "WEST KAMENG": (27.0000, 92.4000),
        "WEST SIANG": (28.0600, 94.7800),
    },

    "Assam": {
        "BAKSA": (26.7000, 91.0000),
        "BARPETA": (26.3226, 91.0063),
        "BONGAIGAON": (26.4785, 90.5583),
        "CACHAR": (24.8333, 92.7833),
        "CHIRANG": (26.5000, 90.7000),
        "DARRANG": (26.4500, 92.0300),
        "DHEMAJI": (27.4833, 94.5833),
        "DHUBRI": (26.0207, 89.9743),
        "DIBRUGARH": (27.4728, 94.9120),
        "DIMA HASAO": (25.5000, 93.0000),
        "GOALPARA": (26.1667, 90.6167),
        "GOLAGHAT": (26.5117, 93.9617),
        "HAILAKANDI": (24.6833, 92.5667),
        "JORHAT": (26.7500, 94.2167),
        "KAMRUP": (26.1500, 91.6000),
        "KAMRUP METRO": (26.1445, 91.7362),
        "KARBI ANGLONG": (26.0000, 93.0000),
        "KARIMGANJ": (24.8667, 92.3500),
        "KOKRAJHAR": (26.4000, 90.2667),
        "LAKHIMPUR": (27.2333, 94.1000),
        "MARIGAON": (26.2500, 92.3333),
        "NAGAON": (26.3500, 92.6833),
        "NALBARI": (26.4500, 91.4333),
        "SIVASAGAR": (26.9833, 94.6333),
        "SONITPUR": (26.6333, 92.8000),
        "TINSUKIA": (27.5000, 95.3500),
        "UDALGURI": (26.7500, 92.1000),
    },

    "Bihar": {
        "ARARIA": (26.1500, 87.4667),
        "ARWAL": (25.2500, 84.6833),
        "AURANGABAD": (24.7500, 84.3667),
        "BANKA": (24.8833, 86.9167),
        "BEGUSARAI": (25.4167, 86.1333),
        "BHAGALPUR": (25.2500, 87.0000),
        "BHOJPUR": (25.5667, 84.6667),
        "BUXAR": (25.5667, 83.9833),
        "DARBHANGA": (26.1667, 85.9000),
        "GAYA": (24.7969, 85.0039),
        "GOPALGANJ": (26.4667, 84.4333),
        "JAMUI": (24.9167, 86.2167),
        "JEHANABAD": (25.2167, 84.9833),
        "KAIMUR (BHABUA)": (25.0500, 83.6167),
        "KATIHAR": (25.5333, 87.5833),
        "KHAGARIA": (25.5000, 86.4833),
        "KISHANGANJ": (26.1000, 87.9500),
        "LAKHISARAI": (25.1667, 86.1000),
        "MADHEPURA": (25.9167, 86.7833),
        "MADHUBANI": (26.3500, 86.0667),
        "MUNGER": (25.3833, 86.4667),
        "MUZAFFARPUR": (26.1167, 85.3833),
        "NALANDA": (25.1333, 85.4500),
        "NAWADA": (24.8833, 85.5333),
        "PASHCHIM CHAMPARAN": (27.1000, 84.3500),
        "PATNA": (25.5941, 85.1376),
        "PURBI CHAMPARAN": (26.6500, 84.9167),
        "PURNIA": (25.7833, 87.4667),
        "ROHTAS": (24.9500, 84.0333),
        "SAHARSA": (25.8833, 86.6000),
        "SAMASTIPUR": (25.8500, 85.7833),
        "SARAN": (25.8500, 84.7500),
        "SHEIKHPURA": (25.1333, 85.8500),
        "SHEOHAR": (26.5167, 85.3000),
        "SITAMARHI": (26.6000, 85.4833),
        "SIWAN": (26.2167, 84.3667),
        "SUPAUL": (26.1167, 86.6000),
        "VAISHALI": (25.6833, 85.2167),
    },

    "Chhattisgarh": {
        "BALOD": (20.7333, 81.2000),
        "BALODA BAZAR": (21.6500, 82.1600),
        "BALRAMPUR": (23.1667, 83.3167),
        "BASTAR": (19.1000, 81.9500),
        "BEMETARA": (21.7167, 81.5333),
        "BIJAPUR": (18.8500, 80.8333),
        "BILASPUR": (22.0797, 82.1409),
        "DANTEWADA": (18.9000, 81.3500),
        "DHAMTARI": (20.7074, 81.5497),
        "DURG": (21.1904, 81.2849),
        "GARIYABAND": (20.6333, 82.0667),
        "JANJGIR-CHAMPA": (21.9667, 82.5833),
    },

    "Punjab": {
        "CHANDIGARH": (30.7333, 76.7794),
    },
}

SEASONS = [
    "Autumn",
    "Kharif",
    "Rabi",
    "Summer",
    "Whole Year",
    "Winter"
]

SEASON_INFO = {
    "Autumn": {
        "desc": "Crops grown during the autumn season, generally benefiting from moderate temperatures and available soil moisture.",
        "crops": ["Maize", "Groundnut", "Vegetables", "Pulses"],
    },

    "Kharif": {
        "desc": "Monsoon-season crops sown with the onset of rains and harvested after the monsoon. They depend heavily on adequate rainfall.",
        "crops": ["Rice", "Cotton", "Soybean", "Maize"],
    },

    "Rabi": {
        "desc": "Winter-season crops sown after the monsoon and harvested in spring. They generally require cooler temperatures and rely on irrigation and residual soil moisture.",
        "crops": ["Wheat", "Mustard", "Gram", "Barley"],
    },

    "Summer": {
        "desc": "Summer crops grown during the hot season. These crops generally require irrigation because rainfall is limited.",
        "crops": ["Watermelon", "Cucumber", "Moong", "Fodder"],
    },

    "Whole Year": {
        "desc": "Crops that can be cultivated throughout the year under suitable temperature, water availability, and management conditions.",
        "crops": ["Banana", "Coconut", "Sugarcane", "Papaya"],
    },

    "Winter": {
        "desc": "Crops grown during the cooler winter months, generally requiring moderate temperatures and suitable irrigation.",
        "crops": ["Wheat", "Peas", "Potato", "Mustard"],
    },
}

# ----------------------------------------------------------------------
# ICONS — crisp inline SVGs (no emoji)
# ----------------------------------------------------------------------
def icon(name, size=20, color="#14532d", stroke=2):
    if name == "leaf" and LOGO_BASE64:
        return (f'<img src="data:image/png;base64,{LOGO_BASE64}" alt="AgriPredict logo" '
                f'width="{size}" height="{size}" style="object-fit:contain;vertical-align:-4px"/>')

    paths = {
        "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/>'
                '<path d="M2 21c0-3 1.85-5.36 5.08-6C9.87 14.13 12 13 13 12"/>',
        "sprout": '<path d="M7 20h10"/><path d="M10 20c0-4.4-2.7-8-6-8"/>'
                  '<path d="M14 20c0-4.4 2.7-8 6-8"/><path d="M12 20v-7"/>'
                  '<path d="M12 13a4 4 0 0 1-4-4V7h2a4 4 0 0 1 4 4v2Z"/>'
                  '<path d="M12 13a4 4 0 0 0 4-4V7h-2a4 4 0 0 0-4 4v2Z"/>',
        "pin": '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/>',
        "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/>'
                '<line x1="12" y1="8" x2="12.01" y2="8"/>',
        "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/>'
                    '<line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
        "home": '<path d="M3 9.5 12 3l9 6.5V21a1 1 0 0 1-1 1h-5v-7H9v7H4a1 1 0 0 1-1-1Z"/>',
        "doc": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/>'
               '<line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/>',
        "insights": '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/>'
                    '<line x1="6" y1="20" x2="6" y2="14"/>',
    }
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'fill="none" stroke="{color}" stroke-width="{stroke}" stroke-linecap="round" '
            f'stroke-linejoin="round" style="vertical-align:-4px">{paths.get(name, "")}</svg>')


def icon_b64(name, color="#ffffff"):
    svg = icon(name, 18, color).replace('style="vertical-align:-4px"', "")
    return base64.b64encode(svg.encode()).decode()


def footer_leaves_svg(size=46):
    return (
        f'<svg width="{size}" height="{int(size * 0.85)}" viewBox="0 0 48 40" fill="none" xmlns="http://www.w3.org/2000/svg" style="display:inline-block;">'
        '<path d="M24 34C24 34 11 32 7 21C3 10 12 5 18 7C24 9 24 22 24 34Z" fill="#34d399"/>'
        '<path d="M24 34C19 25 16 16 18 7" stroke="#059669" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M24 34C24 34 37 32 41 21C45 10 36 5 30 7C24 9 24 22 24 34Z" fill="#22c55e"/>'
        '<path d="M24 34C29 25 32 16 30 7" stroke="#15803d" stroke-width="2" stroke-linecap="round"/>'
        '<path d="M24 34V38" stroke="#16a34a" stroke-width="2.5" stroke-linecap="round"/>'
        '</svg>'
    )



def head(icon_name, title, sub, size=24, color="#14532d"):
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:10px;">{icon(icon_name, size, color)}'
        f'<span class="card-head">{title}</span></div>'
        f'<p class="card-sub">{sub}</p>',
        unsafe_allow_html=True,
    )


def note(icon_name, text, kind="green"):
    cls = "note-box" if kind == "green" else "note-box-blue"
    color = "#16a34a" if kind == "green" else "#2563eb"
    st.markdown(
        f'<div class="{cls}"><span style="margin-right:8px">{icon(icon_name, 18, color)}</span>{text}</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------
# CSS
# ----------------------------------------------------------------------
st.markdown("""
<style>
    /* Header and Toolbar: Transparent background */
    header[data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background: transparent !important;
    }

    /* Hide Streamlit default hamburger menu, footer, deploy button and status widget */
    #MainMenu,
    footer,
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    [data-testid="manage-app-button"] {
        display: none !important;
        visibility: hidden !important;
    }

    /* Reopen/Expand Button (Streamlit 1.51 stExpandSidebarButton & legacy stSidebarCollapsedControl) */
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: inline-flex !important;
        background-color: #053b2a !important;
        border: 1.5px solid #22c55e !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        margin: 6px 12px !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        cursor: pointer !important;
        z-index: 1000000 !important;
        transition: all 0.2s ease-in-out !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    [data-testid="stSidebarCollapsedControl"]:hover {
        background-color: #00874e !important;
        border-color: #4ade80 !important;
        transform: scale(1.05);
    }

    [data-testid="stExpandSidebarButton"] svg,
    [data-testid="stExpandSidebarButton"] span,
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="stSidebarCollapsedControl"] span {
        fill: #ffffff !important;
        color: #ffffff !important;
    }

    /* Sidebar Close/Collapse Button (inside the sidebar) */
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: inline-flex !important;
        cursor: pointer !important;
    }

    [data-testid="stSidebarCollapseButton"] button {
        color: #eafaf1 !important;
        background: transparent !important;
    }

    [data-testid="stSidebarCollapseButton"] svg {
        fill: #eafaf1 !important;
        stroke: #eafaf1 !important;
    }

    .block-container {padding-top: 2.8rem; padding-bottom: 2rem; max-width: 1400px;}

    /* Sidebar Background & Spacing */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #053b2a 0%, #022319 100%) !important;
    }
    [data-testid="stSidebar"] * {
        color: #eafaf1 !important;
    }
    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding-top: 1.5rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }

    /* Sidebar Buttons Base */
    [data-testid="stSidebar"] div.stButton {
        margin-bottom: 6px !important;
    }
    [data-testid="stSidebar"] div.stButton > button {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        justify-content: flex-start !important;
        width: 100% !important;
        padding: 11px 16px !important;
        border-radius: 12px !important;
        border: none !important;
        font-size: 1.05rem !important;
        gap: 14px !important;
        cursor: pointer !important;
        transition: all 0.15s ease-in-out !important;
        text-align: left !important;
    }

    /* Active Sidebar Button (Primary) */
    [data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"],
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {
        background: #00874e !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25) !important;
    }
    [data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-primary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {
        background: #007744 !important;
        color: #ffffff !important;
    }

    /* Inactive Sidebar Buttons (Secondary) */
    [data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-secondary"],
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        box-shadow: none !important;
    }
    [data-testid="stSidebar"] div.stButton > button[data-testid="stBaseButton-secondary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
    }

    /* Icons inside Sidebar Buttons */
    [data-testid="stSidebar"] div.stButton button span[data-testid="stIconMaterial"] {
        font-size: 24px !important;
        color: #ffffff !important;
        line-height: 1 !important;
    }
    [data-testid="stSidebar"] div.stButton button p {
        color: #ffffff !important;
        margin: 0 !important;
        font-size: 1.05rem !important;
        line-height: 1.2 !important;
    }

    .page-title {font-size: 2.2rem; font-weight: 800; color: #14532d; margin-bottom: 0; display:flex; align-items:center; gap:12px;}
    .page-title span {color: #16a34a;}
    .page-sub {color: #667; font-size: 1rem; margin-top: 2px; margin-left: 40px;}

    .info-banner {background: #eafaf1; border: 1px solid #bbf0d3; border-radius: 14px; padding: 14px 18px; display: flex; gap: 10px; align-items: flex-start;}
    .info-banner b {color: #14532d;}
    .info-banner p {margin: 0; color: #4a6a5a; font-size: 0.85rem;}

    /* Card Container Layout — Auto-expand to content, prevent vertical clipping */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px !important;
        border: 1px solid #e6ece8 !important;
        background: #ffffff !important;
        height: auto !important;
        min-height: auto !important;
        max-height: none !important;
        overflow: visible !important;
        display: flex !important;
        flex-direction: column !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] > div,
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"] {
        height: auto !important;
        min-height: auto !important;
        max-height: none !important;
        overflow: visible !important;
        flex: 1 1 auto !important;
    }

    /* Target columns and inner vertical blocks to ensure full content visibility without cutoffs */
    [data-testid="column"] > div,
    [data-testid="stColumn"] > div,
    [data-testid="column"] div[data-testid="stVerticalBlock"],
    [data-testid="stColumn"] div[data-testid="stVerticalBlock"] {
        height: 100% !important;
        min-height: auto !important;
        max-height: none !important;
        overflow: visible !important;
    }

    /* Prevent clipping on inner markdown or element wrappers */
    div[data-testid="stVerticalBlockBorderWrapper"] .element-container,
    div[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stMarkdownContainer"] {
        overflow: visible !important;
        height: auto !important;
    }
    /* Equal height for Row 2 cards */
    [data-testid="column"] {
        display: flex !important;
    }

    [data-testid="column"] > div {
        width: 100% !important;
    }

    [data-testid="column"] > div > div[data-testid="stVerticalBlockBorderWrapper"] {
        height: 100% !important;
    }

    
    .card-head {font-size: 1.2rem; font-weight: 700; color: #14532d;}
    .card-sub {color: #7a8a80; font-size: 0.82rem; margin: 2px 0 12px 34px;}

    .unit-box {background: #f1f4f2; border: 1px solid #d1dcd4; border-radius: 8px; padding: 9px 10px; text-align: center; color: #14532d; font-weight: 600; font-size: 0.88rem; margin-top: 27px;}

    .note-box {background: #eafaf1; border-radius: 10px; padding: 10px 12px; font-size: 0.85rem; color: #365d47; display:flex; align-items:flex-start;}
    .note-box-blue {background: #eaf3fb; border-radius: 10px; padding: 10px 12px; font-size: 0.85rem; color: #2c4a63; display:flex; align-items:flex-start;}

    .season-box {background: #f7faf8; border: 1px dashed #cfe6d8; border-radius: 12px; padding: 12px 14px; margin-top: 14px;}
    .season-box b {color: #14532d;}
    .season-box p {color: #56695f; font-size: 0.85rem; margin: 6px 0 8px 0;}
    .chip {display:inline-block; background:#e6f6ec; color:#166534; border-radius:20px; padding:3px 11px; font-size:0.78rem; margin:2px 4px 2px 0; font-weight:600;}

    .loc-tag {display:flex; align-items:center; gap:8px; font-size:1.02rem; color:#14532d; font-weight:700; margin: 10px 0 10px 0;}
    .loc-tag small {display:block; color:#7a8a80; font-weight:500; font-size:0.8rem;}

    /* Main Content Generate Button */
    section.main div.stButton > button,
    [data-testid="stMain"] div.stButton > button {
        background: #14532d !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.7rem 1.6rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        display:flex !important;
        align-items:center !important;
        justify-content:center !important;
        gap:10px !important;
    }
    section.main div.stButton > button:hover,
    [data-testid="stMain"] div.stButton > button:hover {
        background: #0f3d21 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "New Prediction"

with st.sidebar:
    logo_html = (
        f'<div style="display: flex; justify-content: center; margin-bottom: 12px;">'
        f'<img src="data:image/png;base64,{LOGO_BASE64}" alt="AgriPredict Logo" '
        f'style="width: 80px; height: 80px; object-fit: contain; filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.35));"/>'
        f'</div>'
    ) if LOGO_BASE64 else ""

    st.markdown(
        f"""
        <div style="text-align: center; padding: 0.2rem 0 1.6rem 0;">
            {logo_html}
            <h1 style="color: #ffffff; font-size: 1.95rem; font-weight: 800; margin: 0; letter-spacing: -0.5px; line-height: 1.2;">
                Agri<span style="color: #22c55e;">Predict</span>
            </h1>
            <p style="color: #a7d9c4; font-size: 0.95rem; font-weight: 500; line-height: 1.35; margin: 6px 0 0 0;">
                Grow Smarter<br>Farm Better
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    nav_pages = [
        ("Home", ":material/home:"),
        ("New Prediction", ":material/description:"),
        ("Model Insights", ":material/bar_chart:"),
        ("About", ":material/info:"),
    ]

    for name, icon_id in nav_pages:
        is_active = (st.session_state.current_page == name)
        btn_type = "primary" if is_active else "secondary"
        if st.button(name, icon=icon_id, key=f"nav_btn_{name}", use_container_width=True, type=btn_type):
            if not is_active:
                st.session_state.current_page = name
                st.rerun()

    # Footer matching Image 2
    st.markdown("<div style='margin-top: 5rem;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align: center; padding-bottom: 1.2rem;">
            {footer_leaves_svg(46)}
            <p style="color: #eafaf1; font-size: 0.95rem; font-weight: 500; line-height: 1.35; margin: 10px 0 0 0;">
                For a Sustainable<br>Tomorrow
            </p>
            <div style="width: 44px; height: 3.5px; background: #22c55e; border-radius: 4px; margin: 12px auto 0 auto;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

page = st.session_state.current_page

# ----------------------------------------------------------------------
# MAIN
# ----------------------------------------------------------------------
if page != "New Prediction":
    st.markdown(f'<p class="page-title">{icon("leaf", 30, "#16a34a")} {page}</p>', unsafe_allow_html=True)
    if page == "Home":
        st.markdown('<p class="page-sub">Welcome to AgriPredict AI — Empowering farmers with intelligent crop advisory</p>', unsafe_allow_html=True)
        st.info("The Home dashboard is under development. Select **New Prediction** from the sidebar to test predictions.")
    elif page == "Model Insights":
        st.markdown('<p class="page-sub">Explore performance metrics and feature importances of our models</p>', unsafe_allow_html=True)
        st.info("Model metrics and analytics are under development. Select **New Prediction** from the sidebar to test predictions.")
    elif page == "About":
        st.markdown('<p class="page-sub">About the AgriPredict AI project & system</p>', unsafe_allow_html=True)
        st.info("AgriPredict AI is an agricultural decision-support tool. Select **New Prediction** from the sidebar to test predictions.")
    st.stop()

head_col, banner_col = st.columns([2.2, 1])
with head_col:
    st.markdown(f'<p class="page-title">{icon("leaf", 30, "#16a34a")} New <span>Prediction</span></p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter your farm details to get AI-powered insights</p>', unsafe_allow_html=True)
with banner_col:
    st.markdown(
        f'<div class="info-banner">{icon("leaf", 22, "#16a34a")}<div><b>Accurate inputs lead to better recommendations</b>'
        f'<p>Provide correct information for more reliable results.</p></div></div>',
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Row 1: Location Details (full width, horizontal) ----------------
with st.container(border=True):
    head("pin", "Location Details", "Select your state and district", color="#14532d")

    left, right = st.columns([1, 1.35])
    with left:
        state = st.selectbox("State", list(STATE_DISTRICTS.keys()), index=0)
        district = st.selectbox("District", list(STATE_DISTRICTS[state].keys()), index=0)
        lat, lon = STATE_DISTRICTS[state][district]

        st.markdown(
            f'<div class="loc-tag">{icon("pin", 18, "#16a34a")} {district}<br><small style="margin-left:26px">{state}, India</small></div>',
            unsafe_allow_html=True,
        )
        note("leaf", "Selected location will be used to fetch weather data")

    with right:
        fig = go.Figure(go.Scattergeo(
            lat=[lat], lon=[lon], mode="markers+text",
            marker=dict(size=15, color="#16a34a", line=dict(width=2, color="white")),
            text=[district], textposition="top center",
            textfont=dict(color="#14532d", size=13, family="Arial Black"),
        ))
        fig.update_geos(
            scope="asia", resolution=50,
            showcountries=True, countrycolor="#8fc9a8",
            showland=True, landcolor="#eafaf1",
            showocean=True, oceancolor="#e6f0fa",
            showlakes=False, showcoastlines=True, coastlinecolor="#8fc9a8",
            lataxis_range=[6, 38], lonaxis_range=[66, 98],
            visible=False,
        )
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=300, paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Row 2: Soil Information | Farm Details (equal ratio) ----------------
col_soil, col_farm = st.columns(2)

with col_soil:
    with st.container(border=True):
        head("sprout", "Soil Information", "Enter soil nutrient values and pH")

        def field_with_unit(label, default, unit=None, step=1.0, fmt=None):
            if unit and str(unit).strip():
                c1, c2 = st.columns([3, 1])
                with c1:
                    val = st.number_input(label, value=default, step=step, format=fmt)
                with c2:
                    st.markdown(f'<div class="unit-box">{unit}</div>', unsafe_allow_html=True)
                return val
            else:
                return st.number_input(label, value=default, step=step, format=fmt)

        nitrogen = field_with_unit("Nitrogen (N)", 120.0, "kg/ha")
        phosphorus = field_with_unit("Phosphorus (P)", 50.0, "kg/ha")
        potassium = field_with_unit("Potassium (K)", 90.0, "kg/ha")
        soil_ph = field_with_unit("Soil pH", 6.5, "pH", step=0.1, fmt="%.1f")

        note("info", "Enter values from your soil test report (or use estimated values).", kind="blue")



with col_farm:
    with st.container(border=True):
        head("leaf", "Farm Details", "Select season and area")

        season = st.selectbox("Season", SEASONS, index=0)

        ac1, ac2 = st.columns([3, 1])
        with ac1:
            area = st.number_input("Area", value=2.5, step=0.1, format="%.1f")
        with ac2:
            st.markdown('<div class="unit-box">hectares</div>', unsafe_allow_html=True)

        note("leaf", "Provide accurate details for better prediction results.")

        info = SEASON_INFO[season]
        chips = "".join(f'<span class="chip">{c}</span>' for c in info["crops"])
        st.markdown(
            f'<div class="season-box"><b>{icon("calendar", 16, "#14532d")} About {season.split(" (")[0]} season</b>'
            f'<p>{info["desc"]}</p>{chips}</div>',
            unsafe_allow_html=True,
        )

# ---------------- Generate Prediction ----------------
st.markdown("<br>", unsafe_allow_html=True)
btn_icon_css = f"""
<style>
div.stButton > button::before {{
    content: ""; display:inline-block; width:18px; height:18px;
    background-image: url("data:image/svg+xml;base64,{icon_b64('insights')}");
    background-size: contain; background-repeat: no-repeat;
}}
</style>
"""
st.markdown(btn_icon_css, unsafe_allow_html=True)

btn_col1, btn_col2 = st.columns([4, 1])
with btn_col2:
    generate = st.button("Generate Prediction  →", use_container_width=True)

if generate:
    with st.spinner("Fetching weather data and generating predictions..."):
        try:
            # 1. Fetch weather data from Open-Meteo via wather_api
            rainfall_30_days, temperature_2m, relative_humidity_1000hpa, relative_humidity_100hpa = get_weather(
                state=state,
                district=district,
                season=season
            )

            # 2. Crop Recommendation Model
            crop_preds = crop_recomendation(
                n=nitrogen,
                p=phosphorus,
                k=potassium,
                ph=soil_ph,
                temp=temperature_2m,
                humidity=relative_humidity_1000hpa,
                rainfall=rainfall_30_days
            )
            recommended_crop = str(crop_preds[0])

            # 3. Crop Yield Prediction Model
            # Format crop title to match yield training dataset conventions
            yield_crop_input = recommended_crop.strip().title()
            predicted_yield, predicted_production = predict_yield(
                state=state,
                district=district,
                season=season,
                crop=yield_crop_input,
                temperature=temperature_2m,
                humidity=relative_humidity_100hpa,
                area=area
            )

            # 4. Display Results
            st.markdown("<br>", unsafe_allow_html=True)
            with st.container(border=True):
                head("insights", "Prediction Results", f"Generated for {district}, {state} ({season} season)")

                res_col1, res_col2 = st.columns(2)
                with res_col1:
                    st.markdown(
                        f"""
                        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:18px; height:100%;">
                            <span style="font-size:0.8rem; color:#15803d; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">Recommended Crop</span>
                            <h2 style="color:#14532d; margin:8px 0 4px 0; font-size:2rem; font-weight:800;">{recommended_crop.title()}</h2>
                            <p style="color:#4a6a5a; font-size:0.85rem; margin:0;">Optimal crop matched for soil parameters (N-P-K: {int(nitrogen)}-{int(phosphorus)}-{int(potassium)}, pH: {soil_ph}) and local weather conditions.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with res_col2:
                    st.markdown(
                        f"""
                        <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:12px; padding:18px; height:100%;">
                            <span style="font-size:0.8rem; color:#15803d; font-weight:700; text-transform:uppercase; letter-spacing:0.5px;">Estimated Yield & Production</span>
                            <h2 style="color:#14532d; margin:8px 0 4px 0; font-size:2rem; font-weight:800;">{predicted_yield:.2f} <span style="font-size:1rem; font-weight:500; color:#56695f;">tonnes / ha</span></h2>
                            <p style="color:#4a6a5a; font-size:0.85rem; margin:0;">Total estimated harvest: <b>{predicted_production:.2f} tonnes</b> over <b>{area:.1f} hectares</b>.</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                # Weather Summary Box
                st.markdown(
                    f"""
                    <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:10px; padding:14px 18px;">
                        <span style="font-size:0.85rem; font-weight:700; color:#1e293b;">Live Weather Parameters Used in Prediction:</span>
                        <div style="display:flex; flex-wrap:wrap; gap:20px; margin-top:10px; font-size:0.88rem; color:#475569;">
                            <div>🌡️ <b>Temperature:</b> {temperature_2m:.2f} °C</div>
                            <div>🌧️ <b>Rainfall (30 days):</b> {rainfall_30_days:.2f} mm</div>
                            <div>💧 <b>Humidity (1000 hPa):</b> {relative_humidity_1000hpa:.2f} %</div>
                            <div>☁️ <b>Humidity (100 hPa):</b> {relative_humidity_100hpa:.2f} %</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
