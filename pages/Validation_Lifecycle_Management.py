# pages/Validation_Lifecycle_Management.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from utils import generate_revalidation_data

st.set_page_config(
    page_title="Validation Lifecycle Mgmt | Grifols",
    layout="wide"
)

st.title("🔄 Validation Lifecycle Management Dashboard")
st.markdown("### Overseeing the revalidation and requalification schedule for all validated processes and equipment to ensure continuous compliance.")

with st.expander("🌐 My Role as Manager: Ensuring Ongoing Compliance", expanded=True):
    st.markdown("""
    A validation is not a one-time event; it is a lifecycle. As the Senior Manager, it is my responsibility to ensure that our entire validation program remains in a compliant state throughout the product lifecycle. This includes:

    - **Evaluating Existing Packages:** Regularly reviewing our historical validation packages to ensure they meet the latest FDA guidance and internal Grifols guidelines.
    - **Defining Revalidation Requirements:** Ensuring our Validation Master Plan (VMP) adequately defines the requirements and intervals for periodic revalidation or requalification of processes and equipment.
    - **Proactive Scheduling & Budgeting:** Using this dashboard to foresee upcoming revalidation activities, allowing me to plan resources, prioritize work for my team, and allocate budget effectively.
    - **Audit Readiness:** This dashboard provides a clear, immediate answer to an auditor's question: "How do you ensure your validated processes remain in a state of control over time?" It demonstrates a proactive, risk-based approach to lifecycle management.
    """)

# --- Data Generation ---
revalidation_df = generate_revalidation_data()

# --- KPIs for Lifecycle Management ---
st.header("Program Compliance Status")
total_packages = len(revalidation_df)
due_for_reval = revalidation_df[revalidation_df['Status'] == 'Due'].shape[0]
due_next_90_days = revalidation_df[
    (revalidation_df['Next Assessment Due'] > pd.to_datetime(date.today())) &
    (revalidation_df['Next Assessment Due'] < pd.to_datetime(date.today()) + pd.DateOffset(days=90))
].shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Validated Processes/Systems", total_packages)
col2.metric("Packages Currently Due for Revalidation", due_for_reval, delta=f"{due_for_reval} Overdue", delta_color="inverse")
col3.metric("Revalidations Due in Next 90 Days", due_next_90_days)

st.divider()

# --- Revalidation Schedule Timeline ---
st.header("Revalidation & Requalification Schedule")
st.caption("A forward-looking timeline of all required periodic review and revalidation activities.")

# Make dates timezone-unaware for compatibility with Plotly
revalidation_df['Last Validation Date'] = revalidation_df['Last Validation Date'].dt.tz_localize(None)
revalidation_df['Next Assessment Due'] = revalidation_df['Next Assessment Due'].dt.tz_localize(None)

fig = px.timeline(
    revalidation_df,
    x_start="Last Validation Date",
    x_end="Next Assessment Due",
    y="Process/System",
    color="Status",
    title="Validation Status & Next Due Dates",
    hover_name="Validation Package ID",
    color_discrete_map={
        'OK': '#007A33',
        'Due': '#DA291C'
    }
)

# Add a vertical line for today's date
today_date = pd.to_datetime(date.today()).tz_localize(None)
fig.add_vline(x=today_date, line_width=3, line_dash="dash", line_color="black",
              annotation_text="Today", annotation_position="bottom right")

fig.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Detailed Revalidation Table ---
st.header("Actionable Revalidation List")
st.caption("A filtered list of all validation packages that are currently due or coming due soon, allowing for proactive planning.")

# Create a styled dataframe
def style_status(df):
    style = pd.DataFrame('', index=df.index, columns=df.columns)
    style.loc[df['Status'] == 'Due', :] = 'background-color: #F8D7DA; color: #721C24'
    return style

st.dataframe(
    revalidation_df.style.apply(style_status, axis=None),
    use_container_width=True,
    hide_index=True,
    column_config={
        "Last Validation Date": st.column_config.DateColumn("Last Validation", format="YYYY-MM-DD"),
        "Next Assessment Due": st.column_config.DateColumn("Next Due Date", format="YYYY-MM-DD"),
        "Revalidation Interval (Years)": st.column_config.NumberColumn("Interval (Yrs)")
    }
)

with st.expander("📝 My Role as Manager: Taking Action on This Data"):
    st.markdown("""
    This dashboard provides me with the critical information needed to manage my program effectively.

    1.  **Prioritization:** The table immediately identifies the two systems that are **Due** for revalidation: `NAT Reagent Formulation` and the `Procleix Panther System`. These become my team's highest priority validation projects.
    2.  **Resource Allocation:** I know I need to assign validation staff to these projects immediately. I can refer to the **Staff Management Hub** to see who has the right expertise and current bandwidth to lead these activities.
    3.  **Budgeting:** Revalidating a major process like NAT Formulation requires significant resources (consumables, QC testing, personnel time). This data gives me the justification I need to request and allocate funds in the departmental budget, which I manage in the **Budget Tracker**.
    4.  **Cross-Functional Kick-off:** For the Panther System revalidation, I will use this data to initiate a cross-functional kick-off meeting with Manufacturing, MTS, and QA to align on the scope, strategy, and timeline for the upcoming project.
    """)
