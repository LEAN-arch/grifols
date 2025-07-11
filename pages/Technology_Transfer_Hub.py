# pages/Technology_Transfer_Hub.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_validation_portfolio_data

st.set_page_config(
    page_title="Tech Transfer Hub | Grifols",
    layout="wide"
)

st.title("✈️ Technology Transfer Hub")
st.markdown("### Directing the end-to-end transfer of new or improved processes into GMP manufacturing.")

# --- Mock data for the checklist ---
def generate_tech_transfer_checklist_data():
    """Generates a more detailed dataframe for Gantt chart plotting."""
    data = {
        'Task': [
            'Tech Transfer Plan & Protocol (Approved)', 'Form Cross-Functional Transfer Team',
            'Transfer Process Description & Flow Diagrams', 'Transfer Bill of Materials (BOM)',
            'Execute Lab-Scale Demonstration Runs', 'Gap Analysis & Facility Fit Assessment',
            'Raw Material & Consumable Qualification', 'Execute Engineering / Feasibility Batch',
            'Execute Process Validation (PV) Batches', 'Complete PV Summary Report', 'Update Master Batch Record (Approved)'
        ],
        'Start': pd.to_datetime([
            '2024-05-01', '2024-05-05', '2024-05-15', '2024-05-20', '2024-06-01',
            '2024-06-15', '2024-06-20', '2024-08-01', '2024-09-01', '2024-10-15', '2024-11-01'
        ]),
        'Finish': pd.to_datetime([
            '2024-05-14', '2024-05-10', '2024-06-14', '2024-06-20', '2024-06-30',
            '2024-07-15', '2024-09-30', '2024-08-15', '2024-10-14', '2024-10-31', '2024-11-15'
        ]),
        'Phase': ["Planning", "Planning", "Knowledge Transfer", "Knowledge Transfer", "Knowledge Transfer",
                  "Facility Fit", "Facility Fit", "Engineering", "Validation", "Validation", "Closeout"],
        'Lead Department': ['Validation', 'Sr. Manager', 'R&D/MTS', 'Supply Chain', 'R&D',
                          'Engineering/MTS', 'Validation/QC', 'Manufacturing', 'Manufacturing', 'Validation', 'QA/Mfg'],
        'Status': ['Complete', 'Complete', 'Complete', 'Complete', 'Complete',
                   'In Progress', 'At Risk', 'Planned', 'Planned', 'Planned', 'Planned']
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

# --- Upgraded Visualizations ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Project Health Funnel")
    st.caption("Visualizing progress through the phase-gate process.")
    
    checklist_df = generate_tech_transfer_checklist_data()
    phase_counts = checklist_df['Phase'].value_counts().reindex(["Planning", "Knowledge Transfer", "Facility Fit", "Engineering", "Validation", "Closeout"])
    
    fig_funnel = go.Figure(go.Funnel(
        y=phase_counts.index,
        x=phase_counts.values,
        textinfo="value+percent initial",
        marker={"color": ["#0033A0", "#007A33", "#FFC72C", "#6C6F70", "#A2AAAD", "#DA291C"]},
    ))
    fig_funnel.update_layout(title_text="Deliverables per Project Phase", height=500, margin=dict(t=50, b=0))
    st.plotly_chart(fig_funnel, use_container_width=True)

with col2:
    st.subheader("Detailed Project Gantt Chart")
    st.caption("An interactive timeline of all project tasks and deliverables.")
    
    fig_gantt = px.timeline(
        checklist_df,
        x_start="Start",
        x_end="Finish",
        y="Task",
        color="Lead Department",
        title="Interactive Project Timeline",
        hover_name="Task",
        hover_data={"Status": True}
    )
    fig_gantt.update_yaxes(categoryorder="total descending")
    fig_gantt.update_layout(height=500, margin=dict(t=50, b=0))
    st.plotly_chart(fig_gantt, use_container_width=True)

st.divider()

# --- Detailed Deliverable Checklist ---
st.header("Detailed Deliverable & Task Status")
st.caption("A granular, auditable checklist of all required tasks for the selected project.")

def style_status(val):
    if val == 'Complete': return 'background-color: #D4EDDA; color: #155724'
    if val == 'In Progress': return 'background-color: #FFF3CD'
    if val == 'At Risk': return 'background-color: #F8D7DA; color: #721C24'
    if val == 'Planned': return 'background-color: #EAEAEA'
    return ''

st.dataframe(
    checklist_df.style.apply(lambda x: x.map(style_status) if x.name == 'Status' else ['']*len(x), axis=1),
    use_container_width=True,
    hide_index=True
)

with st.container(border=True):
    st.header("Managerial Analysis & Action Plan")
    st.markdown("""
    - **High-Level Status:** The **Project Health Funnel** shows that we are through the initial planning and knowledge transfer phases, but now entering the more complex 'Facility Fit' phase. This is a known point of risk in any tech transfer.
    
    - **Critical Path Identified:** The **Gantt Chart** and the detailed table immediately highlight the **'At Risk'** item: **Raw Material & Consumable Qualification**. Its long duration on the Gantt chart shows it is a critical path activity. A delay here will have a direct, cascading impact on the start of the Engineering and Validation batches.
    
    - **Leading Cross-Functional Action:** As the Senior Manager, my immediate action is to call a focused meeting with the leads of this task: **Validation, QC, and Supply Chain**. The purpose is not to assign blame, but to understand the specific blockers (e.g., supplier lead time, QC lab capacity, unexpected test results) and to use my authority to remove those roadblocks.
    
    - **Strategic Coordination:** I will use this data to clearly communicate the project status to our leadership and to the receiving manufacturing site. We must be transparent about the potential timeline impact and the mitigation plan we are putting in place. This is a core function of my role in coordinating these complex projects.
    """)
