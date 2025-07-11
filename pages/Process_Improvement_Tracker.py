# pages/Process_Improvement_Tracker.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_opex_data # Renamed to generate_improvement_data in memory

# Renaming for clarity in this context
def generate_improvement_data():
    """Generates data for tracking process improvement initiatives."""
    data = {
        'Initiative ID': ['PI-24-001', 'PI-24-002', 'PI-24-003', 'PI-24-004'],
        'Initiative Name': ['Standardize Tech Transfer Template', 'Reduce Re-work in Doc Review', '5S Implementation in Validation Lab', 'Automate CPV Data Trending'],
        'Lead': ['Anna K.', 'David L.', 'Maria S.', 'Anna K.'],
        'Improvement Type': ['Standardization', 'Lean (Waste Reduction)', '5S', 'Automation/Efficiency'],
        'Business Driver': ['Reduce Transfer Time', 'Improve Cycle Time', 'Enhance Safety & Compliance', 'Improve Data Integrity'],
        'Status': ['In Progress', 'In Progress', 'Complete', 'Not Started'],
        'Target Completion': [pd.to_datetime('2024-12-31'), pd.to_datetime('2024-09-30'), pd.to_datetime('2024-06-30'), pd.to_datetime('2025-03-31')]
    }
    return pd.DataFrame(data)

improvement_df = generate_improvement_data()


st.set_page_config(
    page_title="Process Improvement | Grifols",
    layout="wide"
)

st.title("🚀 Process Improvement Tracker")
st.markdown("### Directing and tracking initiatives to enhance the efficiency, compliance, and robustness of our validation and manufacturing processes.")

with st.expander("🌐 My Role as Manager: Driving Continuous Improvement", expanded=True):
    st.markdown("""
    A core part of my responsibility as Senior Manager is to **"drive and validate process improvements in manufacturing"** and to demonstrate expertise with methodologies like **"Lean, 5S, [and] Operational Excellence."** This dashboard is the central management tool for this program.

    - **Strategic Direction:** I use this platform to translate high-level goals (e.g., "increase efficiency") into a portfolio of specific, actionable projects for my team. The "Business Driver" for each initiative ensures alignment with Grifols' objectives.
    - **Resource Management:** By assigning leads and tracking status, I can manage my team's bandwidth and ensure these important, non-routine projects receive the appropriate focus without jeopardizing our core validation and transfer work.
    - **Fostering Innovation:** This dashboard makes process improvement a formal and visible part of our team's responsibilities. It empowers my staff to be "creative... and innovative" by providing a structured way to propose, execute, and get recognition for projects that challenge the status quo.
    - **Demonstrating Value:** This provides a clear overview of our improvement efforts, which I can present to leadership to showcase my department's proactive contributions to the business beyond just maintaining compliance.
    """)

# --- OpEx Program KPIs ---
st.header("Process Improvement Program KPIs")
total_initiatives = len(improvement_df)
completed_initiatives = improvement_df[improvement_df['Status'] == 'Complete'].shape[0]
inprogress_initiatives = improvement_df[improvement_df['Status'] == 'In Progress'].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Active Initiatives", total_initiatives)
col2.metric("Completed Initiatives (YTD)", completed_initiatives)
col3.metric("Initiatives In Progress", inprogress_initiatives)

st.divider()

# --- Initiative Kanban Board ---
st.header("Initiative Status Kanban Board")
st.caption("A visual overview of all improvement initiatives, categorized by their current status.")

not_started_df = improvement_df[improvement_df['Status'] == 'Not Started']
in_progress_df = improvement_df[improvement_df['Status'] == 'In Progress']
complete_df = improvement_df[improvement_df['Status'] == 'Complete']

k_col1, k_col2, k_col3 = st.columns(3)

with k_col1:
    st.subheader("📝 Not Started / Planned")
    if not_started_df.empty:
        st.info("No initiatives currently in this stage.")
    else:
        for index, row in not_started_df.iterrows():
            st.info(f"**{row['Initiative Name']}**\n\n*Type: {row['Improvement Type']} | Lead: {row['Lead']}*")

with k_col2:
    st.subheader("🚀 In Progress")
    if in_progress_df.empty:
        st.info("No initiatives currently in this stage.")
    else:
        for index, row in in_progress_df.iterrows():
            st.warning(f"**{row['Initiative Name']}**\n\n*Type: {row['Improvement Type']} | Lead: {row['Lead']}*")

with k_col3:
    st.subheader("✅ Complete")
    if complete_df.empty:
        st.info("No initiatives currently in this stage.")
    else:
        for index, row in complete_df.iterrows():
            st.success(f"**{row['Initiative Name']}**\n\n*Type: {row['Improvement Type']} | Lead: {row['Lead']}*")

st.divider()

# --- Detailed Initiative Tracker ---
st.header("Detailed Initiative Tracker")
st.caption("A comprehensive list of all process improvement projects, their business driver, and status.")

st.dataframe(
    improvement_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Target Completion": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")
    }
)

with st.expander("📝 My Role as Manager: Directing These Initiatives"):
    st.markdown("""
    This dashboard provides me with the necessary tools to effectively lead our continuous improvement program.

    1.  **Project Oversight & Prioritization:** I can quickly see that our two "In Progress" initiatives are critical to our department's efficiency. The **Standardized Tech Transfer Template** will reduce errors and speed up future projects, while the **Reduce Re-work in Doc Review** project directly addresses a known bottleneck. I will follow up with the leads, Anna and David, to ensure they have the support they need.

    2.  **Strategic Planning:** The `Automate CPV Data Trending` project is currently "Not Started." This is a high-value project that will save significant engineering time. After reviewing the team's workload on the main **Command Center**, I will schedule a kick-off for this project for the next quarter.

    3.  **Performance Management:** I use this dashboard in my 1-on-1s. For example, I can praise Maria S. for successfully completing the 5S project. I can also work with Anna K., whose development goal is leadership, to ensure she is effectively managing the cross-functional aspects of the template standardization project. This helps me "manage and develop staff" in a practical, hands-on way.
    """)
