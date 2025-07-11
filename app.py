# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import generate_validation_portfolio_data, generate_program_risk_data
from datetime import date

# --- Page Configuration ---
st.set_page_config(
    page_title="Validation & Transfer Command Center | Grifols",
    page_icon="https://www.grifols.com/o/grifols-theme/images/favicon.ico",
    layout="wide"
)

# --- Data Loading (Re-engineered for the Grifols management role) ---
portfolio_df = generate_validation_portfolio_data()
risks_df = generate_program_risk_data()

# --- Page Title and Header ---
st.image("https://www.grifols.com/o/grifols-theme/images/logos/logo-grifols.svg", width=250)
st.title("Validation & Transfer Program Command Center")
st.markdown("### Strategic Management of Process Transfer, Development, and Validation for Grifols' NAT & BTS Diagnostic Products.")

# --- KPIs: Strategic Program Health for a Senior Manager ---
st.header("Strategic Program Health: Key Performance Indicators")

# Calculate Managerial KPIs
total_projects = len(portfolio_df)
# Calculate on-time completion rate based on projects that are actually complete
completed_projects_df = portfolio_df[portfolio_df['Status'].str.contains('Complete')]
if not completed_projects_df.empty:
    on_time_completion_pct = (completed_projects_df[completed_projects_df['Status'] == 'Complete - On Time'].shape[0] / len(completed_projects_df)) * 100
else:
    on_time_completion_pct = 100.0 # Or N/A if no projects are complete
projects_at_risk = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
fy_budget_spent_pct = 78 # This would be pulled from the Budget Tracker page's data

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Projects Portfolio", f"{total_projects}")
col2.metric("Portfolio On-Time Completion", f"{on_time_completion_pct:.1f}%")
col3.metric("Projects At-Risk", f"{projects_at_risk}", delta=f"{projects_at_risk} requiring attention", delta_color="inverse")
col4.metric("FY Budget Utilization", f"{fy_budget_spent_pct}%", help="See Budget Tracker for details")

st.divider()

# --- Main Content Area: Portfolio and Resource Management ---
col1, col2 = st.columns((2, 1.2))

with col1:
    st.header("Validation & Transfer Portfolio Timeline")
    st.caption("Gantt chart overview of all departmental projects, showing resource allocation and timelines. This is key for managing priorities and delegation.")
    fig = px.timeline(
        portfolio_df,
        x_start="Start Date",
        x_end="End Date",
        y="Project Name",
        color="Project Lead",  # Color by team member to visualize resource allocation
        title="Portfolio Timeline by Project Lead",
        hover_name="Project Name",
        hover_data={
            "Project Type": True,
            "Status": True,
            "Start Date": "|%B %d, %Y",
            "End Date": "|%B %d, %Y",
        }
    )
    fig.update_yaxes(categoryorder="total ascending", title=None)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Program Risk Matrix")
    st.caption("Prioritizing risks to regulatory compliance, project timelines, and manufacturing readiness.")
    fig_risk = px.scatter(
        risks_df, x="Probability", y="Impact", size="Risk Score", color="Risk Score",
        color_continuous_scale=px.colors.sequential.YlOrRd, hover_name="Risk Description",
        hover_data=["Project", "Owner", "Status"], size_max=40, title="Impact vs. Probability of Program Risks"
    )
    fig_risk.update_layout(
        xaxis=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['Remote', 'Unlikely', 'Possible', 'Likely', 'Certain'], title='Probability'),
        yaxis=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['Negligible', 'Minor', 'Moderate', 'Major', 'Critical'], title='Impact on Compliance/Timeline'),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_risk, use_container_width=True)

st.header("Project Portfolio Details")
st.dataframe(
    portfolio_df[['Project Name', 'Project Type', 'Status', 'Project Lead', 'Target Completion']],
    use_container_width=True,
    hide_index=True
)

# --- REGULATORY CONTEXT & DASHBOARD PURPOSE ---
st.divider()
with st.expander("🌐 Purpose, Scope, and My Role as Senior Manager", expanded=True):
    st.markdown("""
    As the Senior Manager of Process Transfer, Development, and Validation, my primary responsibility is to direct a comprehensive program that ensures our NAT and BTS diagnostic products are manufactured in a robust, compliant, and efficient manner. This Command Center is my central tool for setting strategic objectives, managing resources, and defending our program during audits and inspections.

    #### **How This Dashboard Directly Addresses My Core Responsibilities:**

    - **Directing the Program & Setting Strategic Goals:**
      - The **Portfolio Timeline** and **KPIs** provide the high-level view needed to direct activities, prioritize projects, and coordinate their completion in line with organizational goals.

    - **Managing & Developing Staff:**
      - The Gantt chart, colored by **Project Lead**, gives me an immediate visual on resource allocation and workload distribution. This is the first step in managing my team effectively. The dedicated **Staff Management Hub** provides the tools for setting individual goals, tracking performance, and managing training effectiveness.

    - **Managing Budgets:**
      - The **Budget Utilization KPI** on this page provides a quick health check, linking directly to the detailed **Budget Tracker** dashboard where I manage and set departmental budgets.

    - **Driving Process Improvements & Operational Excellence:**
      - This Command Center serves as the launchpad for the **Operational Excellence Dashboard**, where specific Lean/5S initiatives are tracked, and the **Process Development Hub**, which contains the scientific data for validating process improvements.

    - **Ensuring Compliance & Defending in Audits:**
      - Every module in this application—from the **Validation Lifecycle Management** page tracking revalidation dates to the **CPV Dashboard** showing process control—is designed to provide clear, traceable, objective evidence of a compliant program, ready to be described and defended during any regulatory inspection.

    - **Cross-Functional Partnership:**
      - This platform acts as a "single source of truth" during cross-functional meetings with Manufacturing, MTS, Engineering, R&D, and QA, fostering clear communication and alignment.
    """)
