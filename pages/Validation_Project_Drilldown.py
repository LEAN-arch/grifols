# pages/Validation_Project_Drilldown.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_validation_portfolio_data, generate_pv_data

st.set_page_config(
    page_title="Validation Project Drilldown | Grifols",
    layout="wide"
)

st.title("📑 Validation Project Drilldown")
st.markdown("### A detailed view of a specific validation project, including its protocol, acceptance criteria, results, and final disposition.")

# --- Data Generation and Project Selection ---
portfolio_df = generate_validation_portfolio_data()
pv_projects = portfolio_df[portfolio_df['Project Type'].isin(['Process Validation', 'Re-validation'])]['Project Name'].tolist()

if not pv_projects:
    st.warning("No Process Validation or Re-validation projects found in the portfolio.")
    st.stop()

project_name = st.selectbox(
    "Select a Process Validation project to view its details:",
    pv_projects,
    index=1 # Default to the DG Gel Card project for a better example
)
st.header(f"Drilldown for: **{project_name}**")
st.divider()

# --- Project Summary ---
project_details = portfolio_df[portfolio_df['Project Name'] == project_name].iloc[0]
pv_data = generate_pv_data()

st.subheader("Project Overview & Final Disposition")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Project Lead", project_details['Project Lead'])
col2.metric("Product Line", project_details['Product Line'])
col3.metric("Protocol ID", "VP-BTS-FILL-005")

# Determine final status and display with an icon
final_status = "PASS" if not "FAIL" in pv_data['Result'].unique() else "FAIL - DEVIATION REQUIRED"
if final_status == "PASS":
    col4.success(f"✔️ Final Status: {final_status}")
else:
    col4.error(f"❌ Final Status: {final_status}")

st.info(f"**Validation Objective:** To demonstrate that the DG Gel Card filling process consistently produces product meeting all pre-defined specifications and quality attributes across three consecutive, successful production-scale batches.")
st.divider()

# --- Upgraded Visualization: Results Heatmap ---
st.header("Acceptance Criteria & Batch Results")
st.caption("Results from the three Process Validation batches are compared against the pre-approved acceptance criteria. Red cells indicate a failure.")

# Create a pivot table for the heatmap
pivot_values = pv_data.pivot(index='Parameter', columns='Batch', values='Value')
pivot_results = pv_data.pivot(index='Parameter', columns='Batch', values='Result')
spec_map = pv_data[['Parameter', 'Spec']].drop_duplicates().set_index('Parameter')
pivot_values = pivot_values.join(spec_map)

# Create annotations for the heatmap
annotations = []
for r, row in enumerate(pivot_values.index):
    for c, col in enumerate(pivot_values.columns):
        if col != 'Spec':
            value = pivot_values.loc[row, col]
            result = pivot_results.loc[row, col]
            annotations.append(dict(
                text=f"{value:.2f}<br>({result})",
                x=col, y=row,
                xref='x1', yref='y1',
                showarrow=False,
                font=dict(color="white" if result == "FAIL" else "black")
            ))

# Create the heatmap
fig = go.Figure(data=go.Heatmap(
    z=(pivot_results != 'PASS').astype(int), # 1 for FAIL, 0 for PASS
    x=pivot_values.columns.drop('Spec'),
    y=pivot_values.index,
    colorscale=[[0, '#D4EDDA'], [1, '#DA291C']], # Green for PASS, Red for FAIL
    showscale=False,
    hovertemplate="<b>Parameter:</b> %{y}<br><b>Batch:</b> %{x}<br><b>Result:</b> %{text}<extra></extra>",
    text=pivot_values.drop(columns='Spec').applymap(lambda x: f"{x:.2f}")
))
fig.update_layout(
    title="Process Validation Results Summary",
    height=400,
    annotations=annotations
)
st.plotly_chart(fig, use_container_width=True)

# Display specs table for reference
st.caption("Reference: Acceptance Criteria")
st.dataframe(spec_map, use_container_width=True)


with st.container(border=True):
    st.header("Managerial Analysis & Decision")
    st.markdown("""
    - **Data-Driven Conclusion:** The results heatmap provides an immediate, unambiguous summary of the validation outcome. The bright red cell instantly draws attention to the single failure point. This is a powerful tool for leading a technical review.
    
    - **Clear Failure:** The project has a **FAIL** status. While most parameters for all three batches passed, the **`Final Potency Assay` for `PV-Batch-02` was 88%**, which is outside the acceptance criterion of 90-110%. Per our validation protocol, this means the campaign did not meet its primary objective.
    
    - **Action Plan:**
        1.  **Direct Investigation:** The "FAIL" status requires a formal deviation to be initiated. I will direct the project lead, **Maria S.**, to take ownership of this deviation and to lead a thorough root cause investigation. My role is to provide her with the resources and support she needs to be successful.
        2.  **Ensure Compliant Follow-up:** I am accountable for ensuring the investigation is robust and scientifically sound. I will "work closely with cross-functional partners" from QC and Manufacturing to ensure all potential causes are explored.
        3.  **Strategic Next Steps:** Once a root cause is confirmed and a corrective action is implemented, my team will draft a protocol to execute a new, replacement PV batch. We cannot "describe and defend" this process as validated until we have three consecutive, successful batches. This entire, documented process demonstrates a compliant and robust validation program to regulatory authorities.
    """)
