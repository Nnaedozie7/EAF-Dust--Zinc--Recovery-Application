#  EAF Dust (Zinc) Recovery Decision Tool (Streamlit)

A lightweight, **rule-based** Streamlit app (no dataset needed) to help choose a practical zinc recovery route for EAF dust (EAFD).

## Inputs (MVP)
1. Zn content (%)
2. Halide level (Cl/F): Low / Medium / High
3. Pb/Cd level: Low / Medium / High
4. Moisture/Oil contamination: Low / High
5. Waelz available? (Yes/No)
6. Hydromet available? (Yes/No)

## Outputs
- Ranked routes:
  - Waelz (pyrometallurgy)
  - Hydromet (leaching + purification)
  - Stabilization + Landfill (fallback)
- Transparent explanation (“why”) + pros/cons

## Run locally

streamlit run app.py
