# pages/Process_Development_Hub.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import generate_doe_data

st.set_page_config(
    page_title="Process Development | Grifols",
    layout="wide"
)

st.title("🔬 Process Development & Characterization Hub")
st.markdown("### Analyzing data from development studies to establish robust and well-understood manufacturing processes.")

with st.expander("🌐 My Role as SME: From Data to Defensible Processes", expanded=True):
    st.markdown("""
    As the Senior Manager, I must **"participate as subject matter expert"** and ensure our processes are built on a foundation of sound science. This hub is where we analyze the data from our process development and characterization studies. The work done here is critical for:

    - **Driving Process Improvements:** Using statistical tools like Design of Experiments (DOE) to scientifically optimize our processes for better performance and robustness.
    - **Establishing Control Strategies:** The data from these studies is used to define the Normal Operating Ranges (NOR) and Proven Acceptable Ranges (PAR) for our Critical Process Parameters (CPPs).
    - **Justifying Acceptance Criteria:** The performance observed in these studies helps us to "ensure appropriate acceptance criteria are applied and justified" for our validation protocols.
    - **Defending the Process:** During an audit, I use the data and visualizations from these studies to "describe and defend" our process understanding and the rationale for our control strategy, demonstrating compliance with FDA and ICH Q8 (Quality by Design) principles.
    """)

# --- Data Generation ---
doe_df = generate_doe_data()

# --- 1. Experimental Design & Data ---
st.header("1. DOE Study: Reagent Formulation Robustness")
st.caption("A Design of Experiments (DOE) study was executed to understand the impact of Temperature and pH on the long-term stability of a critical NAT reagent.")

with st.expander("🔬 The Experiment & Methodology"):
    st.markdown("""
    #### The Goal
    To efficiently map the relationship between two critical formulation parameters (**Temperature** and **pH**) and a key quality attribute (**Stability**). The goal is to identify an operating window where the reagent is robust and maintains its potency over time, even with minor variations in the manufacturing environment.

    #### The Method: Response Surface Methodology (RSM)
    A quadratic statistical model is built from the DOE data to create a "map" of the process. This model allows us to visualize the response (Stability) across the entire design space and identify the optimal operating region. The model takes the form:
    """)
    st.latex(r'''
    Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_{11} X_1^2 + \beta_{22} X_2^2 + \beta_{12} X_1 X_2
    ''')
    st.markdown("Where Y is Stability, and X₁ and X₂ are Temperature and pH.")
    st.dataframe(doe_df, use_container_width=True)

# --- 2. Interactive Analysis of the Design Space ---
st.header("2. Interactive Visualization of the Process Design Space")
st.markdown("Use the slider to define the minimum acceptable stability. The highlighted green area on the plot represents the **Proven Acceptable Range (PAR)**—the operating window where this criterion is met.")

# --- Interactive Control ---
stability_spec = st.slider(
    "Minimum Acceptable Stability (% of Initial Potency)",
    min_value=90.0, max_value=100.0, value=95.0, step=0.5
)

# --- Generate Contour Data (Simulated for this mockup) ---
temp_range = np.linspace(doe_df['Temperature (°C)'].min(), doe_df['Temperature (°C)'].max(), 50)
ph_range = np.linspace(doe_df['pH'].min(), doe_df['pH'].max(), 50)
temp_grid, ph_grid = np.meshgrid(temp_range, ph_range)

# Mock response surface based on the DOE data's known center
stability_pred = 99 - 0.05 * (temp_grid - 25)**2 - 150 * (ph_grid - 7.4)**2

# --- Contour Plot ---
fig = go.Figure()

# Add Stability Contour lines
fig.add_trace(go.Contour(
    z=stability_pred, x=temp_range, y=ph_range,
    name='Stability (%)',
    contours_coloring='lines',
    line_color='#0033A0',
    showscale=False,
    contours=dict(showlabels=True, labelfont=dict(color='#0033A0'))
))

# Highlight the Proven Acceptable Range (PAR)
par_mask = (stability_pred >= stability_spec)
fig.add_trace(go.Contour(
    z=par_mask.astype(int),
    x=temp_range, y=ph_range,
    contours_coloring='lines',
    line_width=0,
    showscale=False,
    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0, 122, 51, 0.4)']], # Transparent and Green
    hoverinfo='none',
    name='PAR'
))

# Add DOE points
fig.add_trace(go.Scatter(
    x=doe_df['Temperature (°C)'], y=doe_df['pH'],
    mode='markers', marker=dict(color='black', symbol='diamond-open', size=10),
    name='DOE Design Points'
))

fig.update_layout(
    title="Process Robustness: Stability as a Function of Temperature and pH",
    height=700,
    xaxis_title="Temperature (°C)",
    yaxis_title="Formulation pH",
    legend=dict(x=1.05, y=1)
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📝 My Role as SME: Interpreting the Data for Action"):
    st.markdown(f"""
    This plot is the key output of our process development work. In a cross-functional meeting with R&D and Manufacturing, I would use this visualization to lead the discussion and make a data-driven decision.

    #### Analysis of the Design Space
    - **Optimal Region:** The model clearly shows that peak stability is achieved at a pH of **7.4** and a temperature of **25°C**.
    - **Process Robustness:** The green shaded area shows the Proven Acceptable Range (PAR) where we can expect to achieve at least **{stability_spec:.1f}%** stability. We can see the process is much more sensitive to changes in pH than it is to temperature; the oval shape is narrow along the pH axis but wide along the temperature axis. This is a critical insight for our control strategy.
    
    #### My Decision and Path Forward
    1.  **Define Control Strategy:** Based on this data, I will direct the team to set the manufacturing target for pH at **7.40**. To ensure robustness, I will propose a tight Normal Operating Range (NOR) of 7.38 - 7.42, which sits comfortably in the middle of the PAR. The NOR for temperature can be wider, for example 20-30°C.
    2.  **Justify Acceptance Criteria:** This study provides the scientific data to justify the pH specification of 7.40 ± 0.05 in our validation protocols and batch records. I can now confidently "ensure appropriate acceptance criteria are applied and justified."
    3.  **Defend in Audits:** If an auditor questions our pH controls, I can present this plot as objective evidence, demonstrating that we have a deep, scientific understanding of our process and have set our limits to ensure product quality. This is how we "describe and defend" our program.
    """)
