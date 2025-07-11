# pages/CPV_Dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm
from utils import generate_cpv_data

st.set_page_config(
    page_title="CPV Dashboard | Grifols",
    layout="wide"
)

st.title("📊 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of the commercial Reagent Filling process for a key NAT product.")

with st.expander("🌐 My Role as Manager: Ensuring a Continued State of Control", expanded=True):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that our commercial manufacturing processes remain in a state of control. As the Senior Manager, I am accountable for this program. This dashboard is how I **"manage...activities to ensure processes remain compliant with cGMP and regulatory requirements through monitoring [and] trending."**

    - **FDA Process Validation Guidance (Stage 3):** This guidance requires an ongoing program to collect and analyze product and process data. This dashboard is our direct fulfillment of that requirement.
    - **Proactive Oversight:** I use this tool to monitor our Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) to detect any unforeseen process variability or drift *before* it results in a product failure.
    - **Audit & Review Readiness:** This dashboard provides the data package for our Annual Product Quality Reviews (APQRs) and is a key exhibit used to "describe and defend" our program during regulatory inspections.
    - **Driving Improvements:** The insights gained here (e.g., a process with marginal capability) are direct inputs for projects on our **Operational Excellence Dashboard**.
    """)

# --- Data Generation ---
cpv_df = generate_cpv_data()

# --- Select Parameter to Analyze ---
st.header("Process Parameter Analysis")
st.caption("Select a parameter to view its control chart and process capability analysis.")

# Define spec limits for each parameter
spec_limits = {
    'Final Potency (%)': (90.0, 110.0),
    'Fill Volume (mL)': (9.90, 10.10)
}
parameter_to_plot = st.selectbox(
    "Select a Critical Quality Attribute (CQA) or Critical Process Parameter (CPP):",
    cpv_df.columns.drop('Batch ID').tolist()
)
st.divider()

# --- SPC Chart and Capability Analysis ---
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader(f"Control Chart for: **{parameter_to_plot}**")

    # SPC Chart Logic
    mean = cpv_df[parameter_to_plot].mean()
    std = cpv_df[parameter_to_plot].std()
    ucl = mean + 3 * std
    lcl = mean - 3 * std

    fig_spc = go.Figure()
    fig_spc.add_hline(y=mean, line_dash="solid", line_color="green", annotation_text="Mean")
    fig_spc.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL (+3σ)")
    fig_spc.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL (-3σ)")
    fig_spc.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter_to_plot], mode='lines+markers', name=parameter_to_plot))

    # Highlight trends using Nelson Rules (Rule 2: 9 points in a row on same side of mean)
    points_on_one_side = 0
    for i in range(len(cpv_df)):
        if cpv_df[parameter_to_plot][i] < mean:
            points_on_one_side += 1
        else:
            points_on_one_side = 0
        if points_on_one_side >= 9:
            fig_spc.add_vrect(x0=cpv_df['Batch ID'][i-8], x1=cpv_df['Batch ID'][i], fillcolor="orange", opacity=0.2, line_width=0, annotation_text="Trend Detected", annotation_position="top left")
            break

    fig_spc.update_layout(height=500, title=f"I-Chart for {parameter_to_plot}", xaxis_title="Batch ID", yaxis_title=parameter_to_plot, xaxis={'type': 'category'})
    st.plotly_chart(fig_spc, use_container_width=True)

with col2:
    st.subheader("Process Capability Analysis (Ppk)")
    lsl, usl = spec_limits.get(parameter_to_plot, (None, None))

    if lsl is not None:
        def calculate_ppk(data_series, usl, lsl):
            mean = data_series.mean()
            std_dev = data_series.std()
            if std_dev == 0: return np.inf
            ppu = (usl - mean) / (3 * std_dev)
            ppl = (mean - lsl) / (3 * std_dev)
            return min(ppu, ppl)

        ppk_value = calculate_ppk(cpv_df[parameter_to_plot], usl, lsl)

        st.metric(f"Process Performance Index (Ppk)", f"{ppk_value:.2f}")
        if ppk_value < 1.0: st.error("NOT CAPABLE")
        elif ppk_value < 1.33: st.warning("MARGINALLY CAPABLE")
        else: st.success("CAPABLE (Target ≥ 1.33)")
        
        st.markdown(f"**Specification Limits:** {lsl} – {usl}")

        fig_hist = px.histogram(cpv_df, x=parameter_to_plot, nbins=15, histnorm='probability density', marginal='rug')
        fig_hist.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
        fig_hist.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
        fig_hist.update_layout(title="Process Distribution vs. Specs", height=380)
        st.plotly_chart(fig_hist, use_container_width=True)
    else:
        st.info(f"Process Capability is not applicable for '{parameter_to_plot}' as it has no defined upper/lower specification limits.")


with st.expander("📝 My Role as Manager: Interpreting CPV Data for Action"):
    st.markdown("""
    This dashboard provides me with the objective evidence needed to effectively manage our commercial processes.

    #### Analysis of `Final Potency (%)`:
    - **Control Chart:** The I-Chart shows a clear and concerning **downward trend** starting around batch M24-1020, flagged by the orange shaded region (violating a Nelson rule). While no single point has failed the control limits, this sustained drift indicates a systemic change in the process.
    - **Process Capability:** The **Ppk of 0.85** is a direct result of this drift. It quantitatively confirms that the process is **not capable** of reliably meeting its specification and is at high risk of producing an Out-of-Specification (OOS) batch.

    #### My Actions as Senior Manager:
    1.  **Immediate Investigation:** I will immediately charter a cross-functional investigation with Manufacturing, MTS, and QA. The data from this dashboard will be the centerpiece of our first meeting. My primary responsibility is to ensure this trend is understood and corrected.
    2.  **Leading the Discussion:** I will use these charts to "lead discussions of data with peers." The discussion will focus on potential root causes for a slow degradation in potency. Are we seeing instability in a key raw material? Is there an equipment issue, like a temperature controller drifting on a storage unit?
    3.  **Driving Improvement:** This is a clear-cut case where I must "drive and validate process improvements." Once the root cause is identified, my team will lead the effort to design and validate the necessary corrective actions (e.g., qualifying a new supplier, updating a maintenance procedure).
    4.  **Regulatory Reporting:** This trend and the resulting investigation will be a key topic in our next Annual Product Quality Review (APQR), demonstrating to health authorities that our CPV program is effective at detecting issues and that we are taking appropriate action.
    """)
