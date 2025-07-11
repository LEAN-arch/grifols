# pages/Technology_Transfer_Hub.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from utils import generate_validation_portfolio_data # Re-using for project selection

st.set_page_config(
    page_title="Tech Transfer Hub | Grifols",
    layout="wide"
)

st.title("✈️ Technology Transfer Hub")
st.markdown("### Directing the end-to-end transfer of new or improved processes into GMP manufacturing.")

with st.expander("🌐 My Role as Manager: Directing Technology Transfer", expanded=True):
    st.markdown("""
    Technology transfer is a complex, cross-functional endeavor that requires meticulous planning and coordination. As the Senior Manager, I am responsible for **"directing the process transfer...activities to support GMP manufacturing in accordance with appropriate regulatory requirements."**

    - **Strategic Coordination:** I use this hub to establish the strategy and timeline for the transfer, ensuring it aligns with our overall business objectives.
    - **Cross-Functional Partnership:** This dashboard serves as the "single source of truth" during our weekly tech transfer meetings with R&D, Manufacturing, MTS, QC, and QA. It ensures all parties are aligned on status, responsibilities, and next steps.
    - **Risk Management:** By tracking the completion of key deliverables, we proactively identify and mitigate risks that could delay the project or compromise the receiving site's ability to manufacture a quality product.
    - **Audit Readiness:** This provides a clear, documented history of the transfer process, which is critical for "describing and defending" our program during a regulatory inspection.
    """)

# --- Mock data for the checklist ---
def generate_tech_transfer_checklist_data():
    data = {
        'Phase': [
            "1. Planning & Initiation", "1. Planning & Initiation",
            "2. Knowledge Transfer", "2. Knowledge Transfer", "2. Knowledge Transfer",
            "3. Facility Fit & Engineering", "3. Facility Fit & Engineering", "3. Facility Fit & Engineering",
            "4. Validation & Closeout", "4. Validation & Closeout", "4. Validation & Closeout"
        ],
        'Deliverable / Task': [
            'Tech Transfer Plan & Protocol (Approved)',
            'Form Cross-Functional Transfer Team',
            'Transfer Process Description & Flow Diagrams',
            'Transfer Bill of Materials (BOM)',
            'Execute Lab-Scale Demonstration Runs',
            'Gap Analysis & Facility Fit Assessment',
            'Raw Material & Consumable Qualification',
            'Execute Engineering / Feasibility Batch',
            'Execute Process Validation (PV) Batches',
            'Complete Process Validation Summary Report',
            'Update Master Batch Record (Approved)'
        ],
        'Lead Department': ['Validation', 'Sr. Manager', 'R&D/MTS', 'Supply Chain', 'R&D', 'Engineering/MTS', 'Validation/QC', 'Manufacturing', 'Manufacturing', 'Validation', 'QA/Mfg'],
        'Status': ['Complete', 'Complete', 'Complete', 'Complete', 'In Progress', 'In Progress', 'At Risk', 'Not Started', 'Not Started', 'Not Started', 'Not Started']
    }
    return pd.DataFrame(data)

# --- Select Project to View ---
portfolio_df = generate_validation_portfolio_data()
transfer_projects = portfolio_df[portfolio_df['Project Type'] == 'Tech Transfer']['Project Name'].tolist()

if not transfer_projects:
    st.warning("No active Technology Transfer projects found in the portfolio.")
    st.stop()

project_name = st.selectbox(
    "Select an active Technology Transfer project to view its status:",
    transfer_projects
)
st.header(f"Status for: **{project_name}**")
st.divider()

# --- Kanban Board for Major Phases ---
st.subheader("High-Level Phase Status")
checklist_df = generate_tech_transfer_checklist_data()

# Logic to determine phase status
phase_status = {}
for phase_name in checklist_df['Phase'].unique():
    phase_tasks = checklist_df[checklist_df['Phase'] == phase_name]
    if 'At Risk' in phase_tasks['Status'].values:
        phase_status[phase_name] = 'At Risk'
    elif all(phase_tasks['Status'] == 'Complete'):
        phase_status[phase_name] = 'Complete'
    elif 'In Progress' in phase_tasks['Status'].values:
        phase_status[phase_name] = 'In Progress'
    else:
        phase_status[phase_name] = 'Not Started'

k_cols = st.columns(len(phase_status))
for i, (phase, status) in enumerate(phase_status.items()):
    with k_cols[i]:
        if status == 'Complete':
            st.success(f"**{phase}**\n\nStatus: {status}")
        elif status == 'At Risk':
            st.error(f"**{phase}**\n\nStatus: {status}")
        elif status == 'In Progress':
            st.warning(f"**{phase}**\n\nStatus: {status}")
        else:
            st.info(f"**{phase}**\n\nStatus: {status}")
st.divider()

# --- Detailed Deliverable Checklist ---
st.subheader("Detailed Deliverable & Task Checklist")
st.caption("A granular, auditable checklist of all required tasks for the selected project. As a manager, I review this weekly with the project team.")

def style_status(val):
    if val == 'Complete': return 'background-color: #D4EDDA; color: #155724'
    if val == 'In Progress': return 'background-color: #FFF3CD'
    if val == 'At Risk': return 'background-color: #F8D7DA; color: #721C24'
    return ''

st.dataframe(
    checklist_df.style.apply(lambda x: x.map(style_status) if x.name == 'Status' else ['']*len(x), axis=1),
    use_container_width=True,
    hide_index=True
)

with st.expander("📝 My Role as Manager: Directing This Transfer Project"):
    st.markdown("""
    This dashboard provides the structure and visibility needed to successfully direct a complex technology transfer.

    1.  **Prioritization & Risk Management:** The checklist immediately highlights that the **Raw Material & Consumable Qualification** task is **'At Risk'**. This is a common bottleneck and a major risk to the project timeline. My immediate action is to schedule a meeting with the Supply Chain and QC leads to understand the cause of the delay (e.g., supplier delays, failed testing) and develop a mitigation plan.

    2.  **Coordination & Delegation:** The "Lead Department" column clearly defines accountability. I can see that the "At Risk" item falls under Validation/QC. I will work with the leads in those departments to ensure they have the resources and support they need to resolve the issue.

    3.  **Leading Cross-Functional Meetings:** In my weekly tech transfer meeting, I will project this dashboard. We will walk through the checklist item by item, focusing on the "In Progress" and "At Risk" items. This ensures the entire cross-functional team (R&D, MTS, Manufacturing, QA) is aligned on status and that all dependencies are being managed.

    4.  **Strategic Decision-Making:** Seeing the delay in material qualification, I must make a strategic decision. Do we delay the engineering batch, or do we proceed using existing, qualified materials with the plan to switch post-validation? This dashboard provides the context needed to weigh the risks and make an informed decision with the team.
    """)
