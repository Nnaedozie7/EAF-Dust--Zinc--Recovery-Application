import streamlit as st

st.set_page_config(
    page_title="EAF Dust (Zinc) Recovery Decision Tool",
    layout="wide",
)

st.title(" EAF Dust (Zinc) Recovery Decision Tool")
st.caption(
    "Rule-based, no dataset required. Enter dust characteristics + local availability "
    "to get ranked recovery routes with pros/cons and clear reasoning."
)


with st.sidebar:
    st.header("Inputs (MVP)")

    zn_pct = st.number_input("Zn content (%)", min_value=0.0, max_value=60.0, value=18.0, step=0.5)

    halides = st.selectbox("Halide level (Cl/F)", ["Low", "Medium", "High"], index=1)
    pbcd = st.selectbox("Pb/Cd level", ["Low", "Medium", "High"], index=1)
    moisture = st.selectbox("Moisture / Oil contamination", ["Low", "High"], index=0)

    waelz_available = st.toggle("Waelz available?", value=True)
    hydromet_available = st.toggle("Hydromet available?", value=False)

    st.divider()
    st.subheader("How this tool works")
    st.write(
        "- Scores routes using practical feasibility rules.\n"
        "- Ranks: **Recommended**, **Alternative**, **Not advised**.\n"
        "- Provides transparent reasons + pros/cons."
    )


def score_waelz(zn, hal, pbcd_lvl, moist, available):
    score = 0
    reasons = []

    if available:
        score += 3
        reasons.append("Waelz route is locally available.")
    else:
        score -= 6
        reasons.append("No Waelz option available locally (major feasibility barrier).")

    
    if zn >= 20:
        score += 4
        reasons.append("High Zn supports recovery economics.")
    elif zn >= 15:
        score += 2
        reasons.append("Moderate Zn supports recovery potential.")
    elif zn >= 10:
        score += 0
        reasons.append("Low-moderate Zn: recovery may be marginal.")
    else:
        score -= 3
        reasons.append("Very low Zn makes recovery less attractive.")

    
    if hal == "High":
        score -= 2
        reasons.append("High halides increase operational complexity/corrosion/handling needs.")
    elif hal == "Medium":
        score -= 0
        reasons.append("Medium halides: manageable with proper handling.")
    else:
        score += 1
        reasons.append("Low halides: fewer handling constraints.")

    
    if pbcd_lvl == "High":
        score -= 1
        reasons.append("High Pb/Cd increases hazardous handling requirements.")
    elif pbcd_lvl == "Medium":
        score += 0
    else:
        score += 1
        reasons.append("Low Pb/Cd reduces hazardous handling burden.")

    
    if moist == "High":
        score -= 1
        reasons.append("High moisture/oil may require drying/pre-treatment.")
    else:
        score += 0

    return score, reasons

def score_hydromet(zn, hal, pbcd_lvl, moist, available):
    score = 0
    reasons = []

    if available:
        score += 3
        reasons.append("Hydromet route is locally available.")
    else:
        score -= 6
        reasons.append("No hydromet option available locally (major feasibility barrier).")

    
    if zn >= 25:
        score += 4
        reasons.append("High Zn is favorable for hydromet recovery.")
    elif zn >= 20:
        score += 2
        reasons.append("Moderate-high Zn supports hydromet feasibility.")
    elif zn >= 15:
        score += 0
        reasons.append("Moderate Zn: hydromet may be marginal depending on costs.")
    else:
        score -= 3
        reasons.append("Low Zn is typically unattractive for hydromet processing.")

    
    if hal == "High":
        score -= 5
        reasons.append("High halides strongly penalize hydromet (chemistry, corrosion, purification load).")
    elif hal == "Medium":
        score -= 2
        reasons.append("Medium halides add purification complexity.")
    else:
        score += 2
        reasons.append("Low halides are favorable for leaching/purification.")

    
    if pbcd_lvl == "High":
        score -= 4
        reasons.append("High Pb/Cd strongly penalizes hydromet (purification + hazardous streams).")
    elif pbcd_lvl == "Medium":
        score -= 1
        reasons.append("Medium Pb/Cd adds purification load.")
    else:
        score += 1
        reasons.append("Low Pb/Cd improves hydromet simplicity.")

    
    if moist == "High":
        score -= 2
        reasons.append("High moisture/oil can complicate leaching/solid-liquid separation.")
    else:
        score += 0

    return score, reasons

def score_landfill_surrogate(zn, hal, pbcd_lvl, moist, waelz_avail, hydro_avail):
    """
    We include landfill as a 'fallback option' in the ranking even though it isn't a toggle input in the MVP.
    It's helpful for the decision tool: if recovery routes are infeasible, landfill becomes likely.
    """
    score = 0
    reasons = []

    
    if (not waelz_avail) and (not hydro_avail):
        score += 6
        reasons.append("No recovery infrastructure available → landfill/stabilization becomes the practical fallback.")
    else:
        score += 1
        reasons.append("Recovery options exist; landfill typically becomes a last resort.")

    
    if zn < 10:
        score += 3
        reasons.append("Low Zn makes recovery less attractive → disposal more likely.")
    elif zn < 15:
        score += 1
        reasons.append("Moderate-low Zn can make recovery marginal.")
    else:
        score -= 2
        reasons.append("Higher Zn usually favors recovery over disposal.")

    
    if pbcd_lvl == "High":
        score += 3
        reasons.append("High Pb/Cd increases hazardous handling → controlled disposal may be chosen if recovery is limited.")
    elif pbcd_lvl == "Medium":
        score += 1
    else:
        score += 0

    
    if hal == "High":
        score += 1
        reasons.append("High halides increase processing complexity; disposal may be considered if treatment is unavailable.")

    
    if moist == "High":
        score += 1
        reasons.append("High moisture/oil increases pre-treatment needs; disposal may be selected if not economical.")

    return score, reasons


waelz_score, waelz_reasons = score_waelz(zn_pct, halides, pbcd, moisture, waelz_available)
hydro_score, hydro_reasons = score_hydromet(zn_pct, halides, pbcd, moisture, hydromet_available)
landfill_score, landfill_reasons = score_landfill_surrogate(zn_pct, halides, pbcd, moisture, waelz_available, hydromet_available)

routes = [
    {
        "Route": "Waelz (pyrometallurgy)",
        "Score": waelz_score,
        "Why": waelz_reasons,
        "Pros": [
            "Mature industrial route for EAF dust in many regions",
            "Handles mixed dust streams comparatively well",
            "Produces a Zn-rich oxide stream (product depends on plant)"
        ],
        "Cons": [
            "Energy-intensive",
            "Impurities/halides can raise operating complexity",
            "Requires specialized operator and logistics"
        ]
    },
    {
        "Route": "Hydromet (leaching + purification)",
        "Score": hydro_score,
        "Why": hydro_reasons,
        "Pros": [
            "Potential for high-purity zinc products (route-dependent)",
            "Can be attractive when halides and impurities are low",
            "Often good for controlled chemistry and product specs"
        ],
        "Cons": [
            "Sensitive to halides and Pb/Cd (purification load)",
            "More complex chemistry/solid-liquid handling",
            "Requires specialized facility and reagent management"
        ]
    },
    {
        "Route": "Stabilization + Landfill (fallback)",
        "Score": landfill_score,
        "Why": landfill_reasons,
        "Pros": [
            "Simplest operationally when recovery is infeasible",
            "Predictable logistics if permitted",
            "Can be appropriate for very low Zn or problematic impurities"
        ],
        "Cons": [
            "Loses resource value (Zn not recovered)",
            "Long-term liability/permit constraints",
            "Not aligned with circular economy targets"
        ]
    },
]


routes_sorted = sorted(routes, key=lambda x: x["Score"], reverse=True)


st.subheader("Ranked recommendation")

c1, c2, c3 = st.columns(3)
c1.metric("Recommended", routes_sorted[0]["Route"])
c2.metric("Alternative", routes_sorted[1]["Route"])
c3.metric("Other option", routes_sorted[2]["Route"])

st.divider()

# Explain in expandable sections
st.subheader("Why these recommendations?")

for i, r in enumerate(routes_sorted):
    label = "✅ Recommended" if i == 0 else ("🟡 Alternative" if i == 1 else "⚪ Other")
    with st.expander(f"{label}: {r['Route']}  (Score: {r['Score']})", expanded=(i == 0)):
        st.markdown("**Key reasons (from your inputs):**")
        for reason in r["Why"]:
            st.write(f"- {reason}")

        st.markdown("**Pros:**")
        for p in r["Pros"]:
            st.write(f"- {p}")

        st.markdown("**Cons:**")
        for c in r["Cons"]:
            st.write(f"- {c}")

st.divider()

st.subheader("Quick notes / flags")
if zn_pct < 10:
    st.warning("Zn% is very low — recovery economics may be weak in many cases.")
if halides == "High":
    st.warning("Halides are high — expect higher complexity/cost, especially for hydromet.")
if pbcd == "High":
    st.warning("Pb/Cd is high — hazardous handling and purification/disposal constraints become important.")
if (not waelz_available) and (not hydromet_available):
    st.error("No recovery routes are available locally (Waelz OFF + Hydromet OFF). The tool will tend to select landfill fallback.")

