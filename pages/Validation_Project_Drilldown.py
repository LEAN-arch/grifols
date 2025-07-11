# pages/Validation_Project_Drilldown.py

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import generate_validation_portfolio_data, generate_pv_data

st.set_page_config(
    page_title="Validation Project Drilldown | Grifols",
    layout="wide"
)

st.title("📑 Validation Project Drilldown")
st.markdown("### A detailed view of a specific validation project, including its protocol, acceptance criteria, results, and final disposition.")

with st.expander("🌐 My Role as SME: Ensuring Defensible Validation", expanded=True):
    st.markdown("""
    While the Command Center provides a high-level program overview, this dashboard allows me, as the Senior Manager and subject matter expert, to drill into the specifics of any single validation project. This is crucial for several of my core responsibilities:

    - **Ensuring Appropriate Acceptance Criteria:** This view explicitly lists the pre-approved acceptance criteria from the validation protocol. I use this to confirm that our criteria are scientifically sound, justified, and meet regulatory expectations before we even begin the study.
    - **Describing and Defending the Program:** During an audit or inspection, I can pull up this page for any given project and clearly walk the inspector through the protocol's intent, the pre-defined criteria, the results obtained, and the final conclusion. This provides a clear, concise, and defensible summary of the validation activity.
    - **Leading Technical Discussions:** In meetings with my team or cross-functional partners, this dashboard serves as the focal point for discussing results, analyzing any deviations, and reaching a final conclusion on the success of the validation.
    """)

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

# Determine final status based on results
final_status = "PASS" if not "FAIL" in pv_data['Result'].unique() else "FAIL - DEVIATION REQUIRED"
if final_status == "PASS":
    col4.success(f"**Final Status: {final_status}**")
else:
    col4.error(f"**Final Status: {final_status}**")

st.info(f"**Validation Objective:** To demonstrate that the DG Gel Card filling process consistently produces product meeting all pre-defined specifications and quality attributes across three consecutive, successful production-scale batches.")

st.divider()

# --- Acceptance Criteria & Results ---
st.header("Acceptance Criteria & Batch Results")
st.caption("Results from the three Process Validation batches are compared against the pre-approved acceptance criteria from the validation protocol.")

# Create a pivot table to show batches vs. parameters
pivot_df = pv_data.pivot(index='Parameter', columns='Batch', values='Value').reset_index()

# Add the spec column
spec_map = pv_data[['Parameter', 'Spec']].drop_duplicates().set_index('Parameter')
pivot_df = pivot_df.join(spec_map, on='Parameter')

# Add pass/fail styling
def style_results(df):
    styled_df = df.copy()
    for batch in ['PV-Batch-01', 'PV-Batch-02', 'PV-Batch-03']:
        pass_fail_series = pv_data[pv_data['Batch'] == batch].set_index('Parameter')['Result']
        styled_df[batch] = styled_df[batch].astype(str) + " (" + pass_fail_series.reindex(styled_df['Parameter']).values + ")"
    return styled_df

# For now, just show the data clearly
st.dataframe(
    pivot_df[['Parameter', 'Spec', 'PV-Batch-01', 'PV-Batch-02', 'PV-Batch-03']],
    use_container_width=True,
    hide_index=True
)


with st.expander("📝 My Role as Manager: Analysis and Conclusion"):
    st.markdown(f"""
    This drilldown view is precisely what I need to lead a technical review of a completed validation project.

    #### Analysis of Results
    - **Overall Outcome:** The project has a **FAIL** status. While most parameters for all three batches passed successfully, the `Final Potency Assay` for `PV-Batch-02` was 88%, which is outside the acceptance criterion of 90-110%.
    - **Compliance Check:** This single failure means the process validation campaign, as a whole, did not meet its primary objective. A passing result requires three consecutive, successful batches.

    #### My Actions as Senior Manager
    1.  **Direct Investigation:** The "FAIL" status automatically triggers a formal deviation. I will direct the project lead, **Maria S.**, to lead the investigation into the root cause of the potency failure for the second batch. Was it a raw material issue? An operator error? An equipment malfunction?
    2.  **Cross-Functional Collaboration:** I will convene a meeting with my partners in QC (who run the potency assay) and Manufacturing (who executed the batch) to ensure the investigation is thorough and scientifically sound.
    3.  **Path Forward:** Once a root cause is confirmed and a corrective action is implemented (e.g., additional operator training, a change in a raw material specification), I will direct the team to draft a protocol to execute a new, replacement PV batch.
    4.  **Defending the Program:** This entire process—identifying the failure, investigating, correcting, and re-validating—demonstrates a robust and compliant validation program. When I "describe and defend" this project to an auditor, I can show that our system worked as intended: it detected a failure and we took appropriate, documented action.
    """)
