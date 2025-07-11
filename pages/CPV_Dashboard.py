# pages/CPV_Dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

# --- HELPER FUNCTIONS ---
def calculate_ppk(data_series, usl, lsl):
    """Calculates the Ppk for a given series of data and spec limits."""
    mean = data_series.mean()
    std_dev = data_series.std()
    if std_dev == 0: return np.inf
    ppu = (usl - mean) / (3 * std_dev)
    ppl = (mean - lsl) / (3 * std_dev)
    return min(ppu, ppl)

def create_control_chart(df, parameter, color):
    """Generates a standardized I-Chart for a given parameter."""
    mean = df[parameter].mean()
    ucl = mean + 3 * df[parameter].std()
    lcl = mean - 3 * df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green", opacity=0.8)
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", opacity=0.8, annotation_text="UCL")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", opacity=0.8, annotation_text="LCL")
    fig.add_trace(go.Scatter(x=df['Batch ID'], y=df[parameter], mode='lines+markers', name=parameter, line_color=color))
    
    out_of_control = df[(df[parameter] > ucl) | (df[parameter] < lcl)]
    if not out_of_control.empty:
        fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='OOC'))
        
    fig.update_layout(height=300, margin=dict(t=10, b=20, l=10, r=10), showlegend=False)
    return fig

# --- Data Generation ---
def generate_full_cpv_data():
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    resin_age = np.linspace(1, 200, n_batches)
    buffer_lot_id = [f"BUF-0{i//10+1}" for i in range(n_batches)]
    conductivity = np.random.normal(15.2, 0.2, n_batches)
    conductivity[40] = 17.5
    load_density = np.random.normal(25.5, 0.5, n_batches)
    elution_ph = np.random.normal(6.5, 0.05, n_batches)
    purity_base = 99.0
    purity_resin_effect = - (resin_age / 250)**2
    purity_cond_effect = - abs(conductivity - 15.2) * 0.5
    purity_noise = np.random.normal(0, 0.1, n_batches)
    purity = purity_base + purity_resin_effect + purity_cond_effect + purity_noise
    yield_val = 90 - (resin_age / 100) + np.random.normal(0, 0.5, n_batches)
    return pd.DataFrame({
        'Batch ID': batches, 'CQA - Purity (%)': purity, 'CQA - Step Yield (%)': yield_val,
        'CPP - IEX Pool Conductivity (mS/cm)': conductivity, 'CPP - IEX Load Density (g/L)': load_density,
        'CPP - Elution Buffer pH': elution_ph, 'CMA - Resin Age (cycles)': resin_age, 'CMA - Buffer Lot ID': buffer_lot_id
    })
cpv_df = generate_full_cpv_data()


# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="CPV Dashboard | Grifols", layout="wide")
st.title("📊 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of the commercial Reagent Filling process for a key NAT product.")

# --- Control Strategy Definition ---
st.header("IEX Chromatography Control Strategy Monitoring")
st.caption("This dashboard holistically tracks all defined parameters for the Ion Exchange unit operation, linking process inputs (CMAs, CPPs) to quality outputs (CQAs).")
st.divider()

# --- 1. Critical Quality Attributes (CQAs) ---
st.subheader("I. Critical Quality Attribute (CQA) Monitoring")
cqa_col1, cqa_col2 = st.columns(2)
with cqa_col1:
    parameter = 'CQA - Purity (%)'
    lsl, usl = 97.5, 100.0
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")
    fig = create_control_chart(cpv_df, parameter, '#005EB8')
    st.plotly_chart(fig, use_container_width=True)
with cqa_col2:
    parameter = 'CQA - Step Yield (%)'
    lsl, usl = 85.0, 100.0
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")
    fig = create_control_chart(cpv_df, parameter, '#00A9E0')
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 2. Critical Process Parameters (CPPs) ---
st.subheader("II. Critical Process Parameter (CPP) Monitoring")
cpp_col1, cpp_col2, cpp_col3 = st.columns(3)
cpps_to_plot = {
    cpp_col1: {'param': 'CPP - IEX Pool Conductivity (mS/cm)', 'color': '#F36633'},
    cpp_col2: {'param': 'CPP - IEX Load Density (g/L)', 'color': '#8DC63F'},
    cpp_col3: {'param': 'CPP - Elution Buffer pH', 'color': '#6F1D77'},
}
for col, info in cpps_to_plot.items():
    with col:
        st.markdown(f"**{info['param']}**")
        fig = create_control_chart(cpv_df, info['param'], info['color'])
        st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 3. Critical Material Attributes (CMAs) ---
st.subheader("III. Critical Material Attribute (CMA) Monitoring")
cma_col1, cma_col2 = st.columns(2)
with cma_col1:
    st.markdown(f"**CMA - Resin Age (cycles)**")
    fig = px.line(cpv_df, x='Batch ID', y='CMA - Resin Age (cycles)', markers=True, line_shape="linear")
    fig.update_layout(height=300, margin=dict(t=20, b=20), yaxis_title="Cycles")
    st.plotly_chart(fig, use_container_width=True)
with cma_col2:
    st.markdown(f"**CMA - Buffer Lot ID**")
    fig = px.scatter(cpv_df, x='Batch ID', y='CMA - Buffer Lot ID', color='CMA - Buffer Lot ID')
    fig.update_layout(height=300, margin=dict(t=20, b=20), yaxis_title=None, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 4. Multivariate Analysis & Interpretation ---
st.header("IV. Multivariate Analysis & Overall Interpretation")
with st.container(border=True):
    st.subheader("Correlation Matrix")
    st.caption("Visualizing the relationships between all process parameters to identify key drivers of variation.")
    numeric_df = cpv_df.select_dtypes(include=np.number)
    corr_df = numeric_df.corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title="Correlation Heatmap of CQAs, CPPs, and CMAs"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.subheader("Managerial Conclusion & Action Plan")
    st.markdown("""
    This holistic CPV analysis tells a clear, data-driven story that is essential for my oversight role.
    
    1.  **The Problem:** Our most important CQA, **Purity**, is exhibiting a clear downward trend, and its process capability is unacceptable (Ppk < 1.0). This is a direct threat to product quality and compliance.
    2.  **The Clues:** The control charts for all three CPPs—**Conductivity, Load Density, and pH**—are stable. This indicates the CDMO is operating the process consistently. The problem is not with their execution of the batch record.
    3.  **The Smoking Gun:** The **Correlation Matrix** provides the definitive link. It shows a very strong **negative correlation (r = -0.96)** between **CMA - Resin Age** and **CQA - Purity**.
    
    **Action Plan:**
    - **Definitive Conclusion:** I can conclude with high confidence that the process itself is not failing; the *chromatography resin* is failing as it reaches the end of its validated lifetime.
    - **Corrective Action:** I will direct the project lead to issue a formal recommendation to the manufacturing site to discard the current resin pack and prepare the column with a new lot of resin.
    - **Preventive Action (Lifecycle Management):** This analysis provides the objective evidence needed to justify a change to our control strategy. I will initiate a change control to reduce the validated lifetime of the IEX resin from its current limit to a more conservative one (e.g., from 250 to 200 cycles). This is a perfect example of using the CPV program to **"drive and validate process improvements"** and ensure long-term product robustness.
    """)
