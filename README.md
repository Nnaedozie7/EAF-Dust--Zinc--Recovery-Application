# Zinc Recovery from EAF Dust Decision Tool

## Overview

Electric Arc Furnace Dust (EAFD) is a hazardous by-product generated during EAF steelmaking. However, it also contains significant amounts of **recoverable zinc**, making it an important secondary resource.

This application evaluates **potential zinc recovery routes from EAF dust** based on dust composition and processing constraints.

The tool recommends the most suitable recovery method using a **rule-based decision model**.

---

## Problem Description

EAF dust forms when metal vapors and fine particles are carried in the furnace off-gas and captured by baghouse filters.

Typical EAF dust generation rates:

10–20 kg per ton of steel produced.

Because galvanized scrap is widely used in steel recycling, EAF dust often contains significant zinc concentrations.

However, the dust also contains hazardous elements such as:

- lead
- cadmium
- halides

This complicates disposal and recycling.

The tool helps determine **whether zinc recovery is viable and which process route is most suitable**.

---

## Metallurgical Background

During EAF steelmaking, zinc coatings on scrap vaporize:

Zn → Zn(g)

The vapor then oxidizes in the off-gas stream:

Zn(g) + O₂ → ZnO

This zinc oxide is captured in the baghouse as part of EAF dust.

Typical EAF dust composition:

| Component | Typical Range |
|--------|--------|
| Zn | 10 – 35 % |
| Fe | 20 – 40 % |
| Pb | trace |
| Cd | trace |
| Cl/F | variable |

Because of its heavy metal content, EAF dust is often classified as **hazardous waste**.

---

## Methodology

The application uses a **rule-based decision framework**.

Users provide inputs including:

- Zinc concentration
- Halide level
- Pb/Cd risk level
- Moisture level
- Availability of Waelz processing
- Availability of hydrometallurgical processing

The tool evaluates these parameters and recommends one of the following routes:

### Waelz Process

A high-temperature rotary kiln process that reduces zinc oxide:

ZnO + C → Zn(g)

The zinc vapor is re-oxidized to produce **Waelz oxide**, which typically contains:

50–70 % Zn

### Hydrometallurgical Recovery

A chemical process involving:

- leaching
- purification
- electrowinning

This route can produce high-purity zinc but requires stricter impurity control.

### Landfill (Fallback)

If recovery is not feasible, controlled landfill disposal may be required.

---

## Results

The tool provides:

- Recommended zinc recovery route
- Alternative processing options
- Explanation of the decision logic
- Environmental considerations

This supports **decision-making for EAF dust management**.

---

## Code Structure

The application consists of:

1. User input interface
2. Rule-based evaluation engine
3. Process route scoring system
4. Recommendation output

The interface is implemented using **Streamlit**.

---

## How to Run

Install dependencies:

```bash
pip install streamlit
