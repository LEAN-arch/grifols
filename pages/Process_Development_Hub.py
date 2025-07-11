# pages/Process_Development_Hub.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import generate_doe_data

st.set_page_config(
    page_title="Process Development | Grifols",
    layout="wide"
)

st.title("🔬 Process Development & Characterization Hub")
st.markdown("### Analyzing data from development studies to establish robust and well-understood manufacturing processes.")

# --- Data Generation ---
doe_df = generate_doe_data()

# --- 1. Experimental Design & Data ---
st.header("1. DOE Study: Reagent Formulation Robustness")
st.caption("A Design of Experiments (DOE) study was executed to understand the impact of Temperature and pH on the long-term stability of a critical NAT reagent.")

with st.expander("🔬 The Experiment & Methodology"):
    st.markdown("""
    #### The Goal
    To efficiently map the relationship between two critical formulation parameters (**Temperature** and **pH**) and a key quality attribute (**Stability**). The goal is to identify an operating window where the reagent is robust and maintains its potency over time, even with minor variations in the manufacturing environment. This is a foundational step to **"drive and validate process improvements."**

    #### The Method: Response Surface Methodology (RSM)
    A quadratic statistical model is built from the DOE data to create a "map" of the process. This model allows us to visualize the response (Stability) across the entire design space and identify the optimal operating region. This scientific approach is critical to **"ensure appropriate acceptance criteria are applied and justified"** for our processes.
    """)
    st.dataframe(doe_df, use_container_width=True)

# --- 2. Interactive Analysis of the Design Space ---
st.header("2. Interactive Visualization of the Process Design Space")
st.markdown("Use the slider to define the minimum acceptable stability. The highlighted green area on the 2D contour plot represents the **Proven Acceptable Range (PAR)**—the operating window where this criterion is met.")

# --- Interactive Control ---
stability_spec = st.slider(
    "Minimum Acceptable Stability (% of Initial Potency)",
    min_value=90.0, max_value=100.0, value=95.0, step=0.5
)

# --- Generate Contour Data & Model (Simulated for this mockup) ---
temp_range = np.linspace(doe_df['Temperature (°C)'].min(), doe_df['Temperature (°C)'].max(), 50)
ph_range = np.linspace(doe_df['pH'].min(), doe_df['pH'].max(), 50)
temp_grid, ph_grid = np.meshgrid(temp_range, ph_range)
stability_pred = 99 - 0.05 * (temp_grid - 25)**2 - 150 * (ph_grid - 7.4)**2
opt_temp, opt_ph, max_stability = 25.0, 7.4, 99.0

# --- Upgraded Combined 3D Surface and 2D Contour Plot ---
fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'contour'}]],
    subplot_titles=('3D Response Surface', '2D Contour Map with PAR')
)

# 3D Surface Plot
fig.add_trace(go.Surface(
    z=stability_pred, x=temp_range, y=ph_range, colorscale='Viridis', showscale=False,
    name='Response Surface'
), row=1, col=1)
fig.add_trace(go.Scatter3d(
    x=doe_df['Temperature (°C)'], y=doe_df['pH'], z=doe_df['Stability (% Initial)'],
    mode='markers', marker=dict(size=5, color='black', symbol='diamond'), name='DOE Points'
), row=1, col=1)
fig.add_trace(go.Scatter3d(
    x=[opt_temp], y=[opt_ph], z=[max_stability],
    mode='markers', marker=dict(size=10, color='red', symbol='cross'), name='Predicted Optimum'
), row=1, col=1)

# 2D Contour Plot
fig.add_trace(go.Contour(
    z=stability_pred, x=temp_range, y=ph_range, colorscale='Viridis', showscale=False,
    contours=dict(coloring='lines', showlabels=True), line=dict(width=1)
), row=1, col=2)
# Highlight the Proven Acceptable Range (PAR)
par_mask = (stability_pred >= stability_spec)
fig.add_trace(go.Contour(
    z=par_mask.astype(int), x=temp_range, y=ph_range, showscale=False,
    contours_coloring='lines', line_width=0,
    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0, 122, 51, 0.4)']],
    hoverinfo='none', name='PAR'
), row=1, col=2)
fig.add_trace(go.Scatter(
    x=doe_df['Temperature (°C)'], y=doe_df['pH'],
    mode='markers', marker=dict(color='black', symbol='diamond-open', size=8), name='DOE Points'
), row=1, col=2)


# --- START: Corrected fig.update_layout block ---
fig.update_layout(
    height=700,
    title_text="Process Robustness: Stability as a Function of Temperature and pH",
    # Use nested dictionaries for scene axis titles
    scene=dict(
        xaxis=dict(title='Temperature (°C)'),
        yaxis=dict(title='Formulation pH'),
        zaxis=dict(title='Stability (%)')
    ),
    # Use nested dictionaries for 2D subplot axis titles
    xaxis2=dict(title='Temperature (°C)'),
    yaxis2=dict(title='Formulation pH'),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
# --- END: Corrected fig.update_layout block ---

st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    st.header("Managerial Analysis & Decision")
    st.markdown(f"""
    - **Process Understanding:** The 3D surface plot provides an intuitive "map" of our process, making it an excellent tool for communicating with our cross-functional partners in Manufacturing and QA. It clearly shows the "peak" of stability.
    
    - **Control Strategy Definition:** The 2D contour plot is where we make our key decisions. The analysis shows that our process is far more sensitive to changes in **pH** than it is to **Temperature**. The green "sweet spot" (Proven Acceptable Range) is very narrow along the pH axis. This is a critical insight.
    
    - **Data-Driven Decision:** Based on this data, I will direct the team to implement a tight control limit for pH (e.g., 7.40 ± 0.05) in the Master Batch Record. The acceptable range for temperature can be wider (e.g., 20-30°C), which provides operational flexibility to the manufacturing team without compromising product quality.
    
    - **Audit Defense:** In a regulatory inspection, I can use this interactive plot to **"describe and defend"** our control strategy. I can show the auditor our design space and use the slider to demonstrate how our chosen operating ranges ensure we consistently meet our stability specification of **{stability_spec:.1f}%**. This provides clear, objective evidence of a well-characterized and robust process.
    """)
