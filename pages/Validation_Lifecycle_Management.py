# pages/Validation_Lifecycle_Management.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
from utils import generate_revalidation_data

st.set_page_config(
    page_title="Validation Lifecycle Mgmt | Grifols",
    layout="wide"
)

st.title("🔄 Validation Lifecycle Management Dashboard")
st.markdown("### Overseeing the revalidation and requalification schedule for all validated processes and equipment to ensure continuous compliance.")

with st.expander("🌐 My Role as Manager: Ensuring Ongoing Compliance", expanded=True):
    st.markdown("""
    A validation is not a one-time event; it is a lifecycle. As the Senior Manager, it is my responsibility to direct a program that ensures our entire portfolio of validated processes remains in a compliant state. This is a key expectation of health authorities (e.g., FDA, EMA) and is outlined in cGMP regulations (**21 CFR 211**) and our internal Grifols policies.

    - **Evaluating Existing Packages & Justifying Intervals:** My team periodically reviews validation packages against current industry guidance. We use a **risk-based approach (per ICH Q9)** to justify the revalidation interval for each system. A high-risk, complex process like NAT reagent formulation requires a more frequent review than a simple, robust utility.
    - **Proactive Scheduling & Resource Management:** This dashboard is my primary tool for foreseeing upcoming revalidation activities. This allows me to "manage and develop staff" by assigning projects based on their development goals, "prioritize" work for my team, and "manage and set department budgets" to ensure resources are available.
    - **Audit Readiness:** This dashboard is designed to be presented during an audit. It allows me to "describe and defend" our validation program by clearly showing how we track our systems, justify our revalidation schedule, and maintain a continuous state of control.
    """)

# --- Data Generation and Correction ---
revalidation_df = generate_revalidation_data()

# FIX: Ensure date columns are in the correct pandas datetime format before any operations
revalidation_df['Last Validation Date'] = pd.to_datetime(revalidation_df['Last Validation Date'])
revalidation_df['Next Assessment Due'] = pd.to_datetime(revalidation_df['Next Assessment Due'])


# --- KPIs for Lifecycle Management ---
st.header("Program Compliance Status")
total_packages = len(revalidation_df)
due_for_reval = revalidation_df[revalidation_df['Status'] == 'Due'].shape[0]
high_risk_due = revalidation_df[(revalidation_df['Status'] == 'Due') & (revalidation_df['Risk Score'] >= 8)].shape[0]
due_next_90_days = revalidation_df[
    (revalidation_df['Next Assessment Due'] > pd.to_datetime(date.today())) &
    (revalidation_df['Next Assessment Due'] < pd.to_datetime(date.today()) + pd.DateOffset(days=90))
].shape[0]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Validated Systems", total_packages)
col2.metric("Systems Currently Due", due_for_reval)
col3.metric("High-Risk Systems Due", high_risk_due, delta="High Priority", delta_color="inverse")
col4.metric("Due in Next 90 Days", due_next_90_days, help="For resource planning")

st.divider()

# --- Revalidation Master List ---
st.header("Validation Master List & Status")
st.caption("A comprehensive, risk-ranked list of all validated systems. Select a row for a detailed drill-down view.")

# Create a styled dataframe for a better visual experience
def highlight_status(row):
    style = ''
    if row['Status'] == 'Due':
        style = 'background-color: #F8D7DA; color: #721C24'
    elif (row['Next Assessment Due'] - pd.to_datetime(date.today())).days < 90:
        style = 'background-color: #FFF3CD'
    return [style] * len(row)

# FIX: The buggy tz_localize lines that caused the error have been removed,
# as the columns are now correctly formatted as timezone-naive datetimes above.

# Use st.data_editor to get selected rows
selection = st.data_editor(
    revalidation_df.style.apply(highlight_status, axis=1),
    hide_index=True,
    use_container_width=True,
    column_config={
        "Risk Score": st.column_config.ProgressColumn(
            "Risk Score", help="Risk score based on complexity and impact (higher is more critical)",
            min_value=0, max_value=10, format="%d 🔥"
        ),
        "Last Validation Date": st.column_config.DateColumn("Last Validation", format="YYYY-MM-DD"),
        "Next Assessment Due": st.column_config.DateColumn("Next Due Date", format="YYYY-MM-DD"),
    },
    key="selection_table"
)

st.divider()

# --- Detailed Drill-Down View ---
st.header("Detailed System View")

# Check if a row is selected
if len(selection) > 0:
    # Get the data for the first selected row
    selected_system_data = pd.DataFrame(selection).iloc[0]
    st.subheader(f"System: **{selected_system_data['Process/System']}**")

    # Mock data for the selected system's history
    history_df = pd.DataFrame({
        'Date': pd.to_datetime([
            selected_system_data['Last Validation Date'] - pd.DateOffset(years=selected_system_data['Revalidation Interval (Years)']),
            selected_system_data['Last Validation Date'] - pd.DateOffset(days=300),
            selected_system_data['Last Validation Date'] - pd.DateOffset(days=150),
            selected_system_data['Last Validation Date']
        ]),
        'Event': ['Initial Validation', 'Change Control CC-21-045', 'Minor Review', 'Last Revalidation'],
        'Description': ['Initial process validation completed', 'Replaced primary filling nozzle', 'Annual product review, no changes', 'Full revalidation package approved'],
        'Type': ['Validation', 'Change', 'Review', 'Validation']
    })

    drill_col1, drill_col2 = st.columns([1, 1])
    with drill_col1:
        st.markdown("#### Key Information")
        st.metric("Current Status", selected_system_data['Status'])
        st.metric("Next Assessment Due", selected_system_data['Next Assessment Due'].strftime('%Y-%m-%d'))
        st.metric("Validation Package ID", selected_system_data['Validation Package ID'])
        st.metric("Revalidation Interval", f"{selected_system_data['Revalidation Interval (Years)']} Years")
        st.markdown(f"**Justification:** The **{selected_system_data['Revalidation Interval (Years)']} year** interval is justified based on the system's **{selected_system_data['Complexity']}** complexity and its extensive history of stable performance, as documented in the CPV program.")

    with drill_col2:
        st.markdown("#### System Validation History")
        fig_hist = px.scatter(
            history_df, x='Date', y='Event', color='Type',
            title=f"Validation & Change History for {selected_system_data['Process/System']}",
            size_max=10, symbol='Type',
            hover_data=['Description'],
            color_discrete_map={'Validation': '#007A33', 'Change': '#DA291C', 'Review': '#0033A0'}
        )
        fig_hist.update_traces(marker_size=15)
        fig_hist.update_layout(yaxis_title=None)
        st.plotly_chart(fig_hist, use_container_width=True)

else:
    st.info("Select a row from the master list above to see a detailed drill-down view.")

with st.expander("📝 My Role as Manager: Taking Action on This Data", expanded=True):
    st.markdown("""
    This dashboard provides me with the critical, risk-based information needed to direct my program.

    1.  **Risk-Based Prioritization:** The table is ranked by risk. My immediate attention is drawn to the two **Due** systems. Of those, the `Procleix Panther System` has a higher risk score (8) than `NAT Reagent Formulation` (9, typo fixed to be higher), making it the top priority for resource allocation, even though NAT Formulation is also critical. *[Self-correction: The prompt had 9 for NAT, I will use that as the higher priority]*. The `NAT Reagent Formulation` with a risk score of 9 is the absolute top priority.
    2.  **Resource Allocation & Delegation:** I will assign my most experienced engineer, **Anna K.**, to lead the high-risk NAT Revalidation. I will assign **David L.** to the Panther System project, as this aligns with his development goals. This demonstrates how I "manage diverse groups" and "delegate appropriately."
    3.  **Justifying Budgets:** The upcoming revalidations, especially for high-complexity systems, require significant financial resources. This dashboard provides the clear, data-driven justification I need when I "manage and set department budgets" for the next fiscal year.
    4.  **Leading Technical Discussions:** In a cross-functional meeting, I can use the "Detailed System View" to walk QA, MTS, and Manufacturing through the validation history of a specific process, providing context for the upcoming revalidation and ensuring alignment on the project scope. This showcases my ability to "lead discussions of data with peers."
    """)
