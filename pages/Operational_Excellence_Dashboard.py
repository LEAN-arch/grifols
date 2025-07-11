# pages/Operational_Excellence_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_opex_data

st.set_page_config(
    page_title="OpEx Dashboard | Grifols",
    layout="wide"
)

st.title("🏆 Operational Excellence (OpEx) Dashboard")
st.markdown("### Directing and tracking process improvement initiatives using Lean, 5S, and Standardization methodologies.")

with st.expander("🌐 My Role as Manager: Driving Continuous Improvement", expanded=True):
    st.markdown("""
    A core part of my responsibility as Senior Manager is to **"drive and validate process improvements in manufacturing"** and to demonstrate expertise with **"Lean, 5S, [and] Operational Excellence."** This dashboard serves as the central hub for managing my department's OpEx program.

    - **Strategic Focus:** It allows me to translate strategic goals (e.g., "reduce validation cycle time") into specific, actionable initiatives for my team.
    - **Visibility & Accountability:** This platform provides clear visibility into the progress of each initiative and holds the project leads accountable for their timelines and deliverables.
    - **Demonstrating Value:** It helps me showcase the tangible benefits of our improvement efforts to senior leadership, linking our projects to key business metrics like efficiency, compliance, and cost savings.
    - **Fostering Culture:** By actively managing and celebrating these projects, I help to build a "creative, organized, self-motivated, perceptive and innovative" culture within my team, as required by my role.
    """)

# --- Data Generation ---
opex_df = generate_opex_data()

# --- OpEx Program KPIs ---
st.header("Operational Excellence Program KPIs")
total_initiatives = len(opex_df)
completed_initiatives = opex_df[opex_df['Status'] == 'Complete'].shape[0]
inprogress_initiatives = opex_df[opex_df['Status'] == 'In Progress'].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Active Initiatives", total_initiatives)
col2.metric("Completed Initiatives (YTD)", completed_initiatives)
col3.metric("Initiatives In Progress", inprogress_initiatives)

st.divider()

# --- Initiative Kanban Board ---
st.header("Initiative Status Kanban Board")
st.caption("A visual overview of all OpEx initiatives, categorized by their current status.")

# Separate initiatives by status for the Kanban view
not_started_df = pd.DataFrame() # Add if needed
in_progress_df = opex_df[opex_df['Status'] == 'In Progress']
complete_df = opex_df[opex_df['Status'] == 'Complete']

k_col1, k_col2, k_col3 = st.columns(3)

with k_col1:
    st.subheader("📝 Not Started")
    st.info("No initiatives currently in this stage.")
    # Example of how to populate:
    # for index, row in not_started_df.iterrows():
    #     st.info(f"**{row['Initiative Name']}**\n\n*Lead: {row['Lead']}*")

with k_col2:
    st.subheader("🚀 In Progress")
    for index, row in in_progress_df.iterrows():
        st.warning(f"**{row['Initiative Name']}**\n\n*Type: {row['Type']} | Lead: {row['Lead']}*")

with k_col3:
    st.subheader("✅ Complete")
    for index, row in complete_df.iterrows():
        st.success(f"**{row['Initiative Name']}**\n\n*Type: {row['Type']} | Lead: {row['Lead']}*")

st.divider()

# --- Detailed Initiative Tracker ---
st.header("Detailed Initiative Tracker")
st.caption("A comprehensive list of all operational excellence projects, their scope, and status.")

st.dataframe(
    opex_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Target Completion": st.column_config.DateColumn("Target Date", format="YYYY-MM-DD")
    }
)

with st.expander("📝 My Role as Manager: Directing OpEx Activities"):
    st.markdown("""
    This dashboard provides me with the necessary tools to effectively lead our continuous improvement program.

    1.  **Project Oversight:** I can quickly see that our two "In Progress" initiatives are the `Reduce Re-work in Doc Review` and `Standardize Tech Transfer Template` projects. I will follow up with the leads, David L. and Anna K., during our next 1-on-1 meetings to check on their progress against the target completion dates.

    2.  **Strategic Alignment:** The `Reduce Re-work` project is a Lean initiative aimed at reducing waste, a core principle of operational excellence. The `Standardize Tech Transfer Template` project is a crucial standardization effort that will improve the efficiency and consistency of all future tech transfer projects my team undertakes. Both are perfectly aligned with our strategic goals.

    3.  **Celebrating Success:** The `5S Implementation` led by Maria S. is complete. It's my responsibility as a manager to recognize and celebrate this achievement with the team and to communicate its positive impact (improved lab audit scores) to leadership. This reinforces the value of our OpEx program and motivates the team.

    4.  **Future Initiatives:** By analyzing data from our other dashboards (e.g., a long cycle time for deviations in the **CPV Dashboard**), I can identify opportunities for new OpEx projects and add them to our pipeline, ensuring our improvement efforts are always focused on the most impactful areas.
    """)
