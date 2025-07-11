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

completed_projects_df = portfolio_df[portfolio_df['Status'].str.contains('Complete')]
if not completed_projects_df.empty:
    on_time_completion_pct = (completed_projects_df[completed_projects_df['Status'] == 'Complete - On Time'].shape[0] / len(completed_projects_df)) * 100
else:
    on_time_completion_pct = 100.0
projects_at_risk = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
fy_budget_spent_pct = 78
revals_due = 2 # Pulled from revalidation tracker

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Projects Portfolio", f"{len(portfolio_df)}")
col2.metric("Portfolio On-Time Completion", f"{on_time_completion_pct:.1f}%")
col3.metric("Projects At-Risk", f"{projects_at_risk}", delta=f"{projects_at_risk} requiring attention", delta_color="inverse")
col4.metric("Revalidations Due", f"{revals_due}", help="See Validation Lifecycle for details")

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
        color="Project Lead",
        title="Portfolio Timeline by Project Lead",
        hover_name="Project Name",
        hover_data={"Project Type": True, "Status": True}
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
    use_container_width=True, hide_index=True
)

st.divider()
with st.expander("🌐 My Role as Senior Manager: How This Dashboard Empowers Me", expanded=True):
    st.markdown("""
    As the Senior Manager of Process Transfer, Development, and Validation, my primary responsibility is to **direct a comprehensive program** that ensures our NAT and BTS diagnostic products are manufactured in a robust, compliant, and efficient manner. This Command Center is my central tool for setting strategic objectives, managing resources, and defending our program during audits and inspections, directly addressing my core duties.

    ---
    
    #### **Directing the Program & Establishing Strategic Goals:**
    *   **How:** The **KPIs** and **Portfolio Timeline** on this home page provide the high-level view I need to direct activities, prioritize projects, and coordinate their completion in line with Grifols' organizational objectives.
    
    #### **Managing & Developing Staff:**
    *   **How:** The Gantt chart, colored by **Project Lead**, gives me an immediate visual on resource allocation. I use this to "manage diverse groups" and "delegate appropriately." The dedicated **Staff Management Hub** provides the platform for me to "set individual and group goals," track training effectiveness, and "manage performance."

    #### **Managing Budgets:**
    *   **How:** The **Budget Tracker** dashboard provides the detailed tools I need to "manage and set department budgets as necessary," ensuring financial responsibility for all validation and development activities.

    #### **Driving Process Improvements & Operational Excellence:**
    *   **How:** The **Operational Excellence Dashboard** is my tool for tracking our Lean, 5S, and other improvement initiatives. The **Process Development Hub** houses the scientific data (like DOEs) that I use to "drive and validate process improvements in manufacturing."

    #### **Ensuring Compliance & Defending in Audits:**
    *   **How:** I use the **Validation Lifecycle Management** dashboard to "evaluate existing processes" and ensure revalidation occurs at appropriate intervals. The entire suite, especially the **Validation Project Drilldown** and **CPV Dashboard**, is designed to be presented in audits, allowing me to "describe and defend [our] process transfer, development and validation program" with clear, data-driven evidence.

    #### **Working with Cross-Functional Partners:**
    *   **How:** This platform serves as the "single source of truth." I use it in cross-functional meetings with Manufacturing, MTS, Engineering, R&D, and QA to "lead discussions of data" and ensure strategic alignment on all projects.
    
    #### **Managing Technology Transfers:**
    *   **How:** The dedicated **Technology Transfer Hub** provides a structured, checklist-driven approach to "manage...process transfer...activities," ensuring a robust handover to manufacturing or a partner site.

    This integrated system ensures that every aspect of my role is supported by data, fostering a culture of excellence, compliance, and strategic leadership.
    """)
