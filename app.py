import streamlit as st
import plotly.graph_objects as go

# =============================
# Planet presets
# =============================
PLANET_PRESETS = {
    "Custom": None,

    "Earth-like": {
        "distance": 1.0,
        "star": "Sun-like",
        "water": True,
        "atmosphere": {
            "O2": 21,
            "CO2": 1,
            "N2": 78,
            "H2O": 1,
            "CH4": 0
        }
    },

    "Mars-like": {
        "distance": 1.52,
        "star": "Sun-like",
        "water": False,
        "atmosphere": {
            "O2": 0,
            "CO2": 15,
            "N2": 85,
            "H2O": 0,
            "CH4": 0
        }
    },

    "Venus-like": {
        "distance": 0.72,
        "star": "Sun-like",
        "water": False,
        "atmosphere": {
            "O2": 0,
            "CO2": 20,
            "N2": 80,
            "H2O": 0,
            "CH4": 0
        }
    },

    "Titan-like": {
        "distance": 9.5,
        "star": "Sun-like",
        "water": False,
        "atmosphere": {
            "O2": 0,
            "CO2": 2,
            "N2": 95,
            "H2O": 0,
            "CH4": 5
        }
    }
}

# =============================
# Page configuration
# =============================
st.set_page_config(
    page_title="Biospace | Planetary Habitability Simulator",
    page_icon="🪐",
    layout="centered"
)

# =============================
# Language selector (base)
# =============================
language = st.selectbox("Language / Idioma", ["English", "Português"])

TEXT = {
    "English": {
        "title": "🪐 Planetary Habitability Simulator",
        "subtitle": "Explore how planetary and atmospheric chemistry influence habitability.",
        "preset": "Preset planets",
        "planet_params": "Planet Parameters",
        "atmosphere": "Atmospheric Composition (%)",
        "assessment": "Habitability Assessment",
        "habitable": "🟢 Potentially habitable",
        "marginal": "🟡 Marginal habitability",
        "hostile": "🔴 Hostile to life as we know it",
        "interpretation": "Scientific Interpretation",
        "caption": "This model is qualitative and intended for educational purposes."
    },
    "Português": {
        "title": "🪐 Simulador de Habitabilidade Planetária",
        "subtitle": "Explore como a química planetária e atmosférica influencia a habitabilidade.",
        "preset": "Planetas pré-definidos",
        "planet_params": "Parâmetros do Planeta",
        "atmosphere": "Composição Atmosférica (%)",
        "assessment": "Avaliação de Habitabilidade",
        "habitable": "🟢 Potencialmente habitável",
        "marginal": "🟡 Habitabilidade marginal",
        "hostile": "🔴 Hostil à vida como conhecemos",
        "interpretation": "Interpretação Científica",
        "caption": "Este modelo é qualitativo e educacional."
    }
}

t = TEXT[language]

# =============================
# Header
# =============================
st.title(t["title"])
st.markdown(t["subtitle"])
st.divider()

# =============================
# Preset selector
# =============================
preset_name = st.selectbox(
    t["preset"],
    list(PLANET_PRESETS.keys())
)

preset = PLANET_PRESETS[preset_name]

# =============================
# Default / preset values
# =============================
if preset:
    distance = preset["distance"]
    star_type = preset["star"]
    water = preset["water"]

    o2 = preset["atmosphere"]["O2"]
    co2 = preset["atmosphere"]["CO2"]
    n2 = preset["atmosphere"]["N2"]
    h2o = preset["atmosphere"]["H2O"]
    ch4 = preset["atmosphere"]["CH4"]
else:
    distance = 1.0
    star_type = "Sun-like"
    water = True
    o2, co2, n2, h2o, ch4 = 21, 1, 78, 1, 0

# =============================
# Planet parameters
# =============================
st.subheader(t["planet_params"])

water = st.checkbox("Liquid water present", value=water)

distance = st.slider(
    "Distance from the star (AU)",
    0.1, 10.0, distance, 0.05
)

star_type = st.selectbox(
    "Star type",
    ["Red dwarf", "Sun-like", "Hot star"],
    index=["Red dwarf", "Sun-like", "Hot star"].index(star_type)
)

st.divider()

# =============================
# Atmospheric composition
# =============================
st.subheader(t["atmosphere"])

col1, col2 = st.columns(2)

with col1:
    o2 = st.slider("O₂ (Oxygen)", 0, 30, o2)
    co2 = st.slider("CO₂ (Carbon dioxide)", 0, 20, co2)
    n2 = st.slider("N₂ (Nitrogen)", 0, 100, n2)

with col2:
    h2o = st.slider("H₂O vapor", 0, 10, h2o)
    ch4 = st.slider("CH₄ (Methane)", 0, 10, ch4)

# =============================
# Habitability logic
# =============================
score = 0

if water and h2o >= 1:
    score += 2

if 10 <= o2 <= 25:
    score += 2
elif o2 > 0:
    score += 1

if co2 <= 5 and ch4 <= 3:
    score += 2
elif co2 <= 10:
    score += 1
else:
    score -= 1

if 0.7 <= distance <= 1.5:
    score += 2

if star_type == "Sun-like":
    score += 2
elif star_type == "Red dwarf":
    score += 1

# =============================
# Assessment
# =============================
st.subheader(t["assessment"])

if score >= 7:
    st.success(t["habitable"])
elif score >= 4:
    st.warning(t["marginal"])
else:
    st.error(t["hostile"])

# =============================
# Radar chart
# =============================
radar_labels = ["Water", "Oxygen", "Greenhouse", "Orbit", "Star"]

radar_values = [
    2 if water and h2o >= 1 else 0,
    2 if 10 <= o2 <= 25 else 1 if o2 > 0 else 0,
    2 if co2 <= 5 else 1 if co2 <= 10 else 0,
    2 if 0.7 <= distance <= 1.5 else 0,
    2 if star_type == "Sun-like" else 1,
]

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=radar_values + [radar_values[0]],
        theta=radar_labels + [radar_labels[0]],
        fill="toself",
        line=dict(color="#5DADE2"),
        fillcolor="rgba(93,173,226,0.4)"
    )
)

fig.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 2])),
    height=450,
    showlegend=False,
    title="Habitability Balance"
)

st.plotly_chart(fig, use_container_width=True)

# =============================
# Interpretation
# =============================
st.subheader(t["interpretation"])

if h2o < 1:
    st.info("Low atmospheric water vapor reduces surface habitability.")

if co2 > 10:
    st.warning("High CO₂ levels may trigger runaway greenhouse effects.")

if o2 > 0 and ch4 > 0:
    st.success(
        "The coexistence of O₂ and CH₄ suggests chemical disequilibrium, "
        "often discussed as a potential biosignature."
    )

st.caption(t["caption"])
