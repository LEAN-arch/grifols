# pages/B_Scenario_Planner.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_staff_performance_data, generate_validation_portfolio_data, generate_budget_data

st.set_page_config(page_title="Scenario Planner | Grifols", layout="wide")

st.title("⚖️ Resource & Scenario Planner")
st.markdown("### A proactive tool to simulate project assignments and budget changes to foresee impacts on team workload and financials.")

# --- Data Loading ---
staff_df = generate_staff_performance_data().set_index('Team Member')
portfolio_df = generate_validation_portfolio_data()
budget_df = generate_budget_data()
team_members = staff_df.index.tolist()

# --- 1. Resource Planning Scenario ---
st.header("I. Resource Planning: Simulate Project Assignments")
st.caption("Assign 'Not Started' projects to team members and instantly see the impact on their total workload utilization.")

# Filter for unassigned projects
unassigned_projects = portfolio_df[portfolio_df['Status'] == 'Not Started'].copy()
unassigned_projects['Assigned To'] = 'Unassigned'

if 'assignments' not in st.session_state:
    st.session_state.assignments = unassigned_projects

# Create the editable table for assignments
st.write("##### Assign Projects:")
edited_assignments = st.data_editor(
    unassigned_projects,
    column_config={
        "Assigned To": st.column_config.SelectboxColumn("Assign To", options=['Unassigned'] + team_members, required=True),
        "Project Name": st.column_config.TextColumn(disabled=True),
        "Effort (Person-Months)": st.column_config.NumberColumn(disabled=True),
        "Start Date": st.column_config.DateColumn(disabled=True),
    },
    hide_index=True,
    use_container_width=True,
    key='project_assignment_editor'
)

# --- Calculate and Display Simulated Utilization ---
st.write("##### Simulated Team Utilization:")
base_utilization = staff_df[['Utilization (%)']].copy()

# Calculate added workload
# Assuming 1 Person-Month of effort = 1/12 FTE ~ 8.3% utilization for the year
# This is a simplification; a real model would be more complex.
effort_to_util_factor = 100 / 12 
assigned_effort = edited_assignments[edited_assignments['Assigned To'] != 'Unassigned'].groupby('Assigned To')['Effort (Person-Months)'].sum()
added_utilization = (assigned_effort * effort_to_util_factor).rename('Added Utilization (%)').round(0)

# Combine and calculate simulated utilization
simulated_df = base_utilization.join(added_utilization).fillna(0)
simulated_df['Simulated Utilization (%)'] = simulated_df['Utilization (%)'] + simulated_df['Added Utilization (%)']

# Display heatmap
fig_heatmap = px.imshow(
    simulated_df[['Simulated Utilization (%)']].T,
    text_auto=True,
    aspect="auto",
    color_continuous_scale='RdYlGn_r',
    range_color=[50, 150],
    title="Simulated Team Workload with New Assignments"
)
fig_heatmap.update_layout(xaxis_title="", yaxis_title="")
st.plotly_chart(fig_heatmap, use_container_width=True)

st.divider()

# --- 2. Budget Planning Scenario ---
st.header("II. Budget Planning: Simulate New Initiatives")
st.caption("Add a hypothetical new initiative and cost to see the immediate impact on the departmental budget.")

col1, col2 = st.columns([1, 2])

with col1:
    with st.form("new_initiative_form"):
        st.write("##### Add a Hypothetical Initiative:")
        initiative_name = st.text_input("Initiative Name", "e.g., New Lab Instrument")
        initiative_cost = st.number_input("Estimated Cost ($K)", min_value=0, value=100)
        submitted = st.form_submit_button("Simulate Impact")

with col2:
    st.write("##### Simulated Budget Waterfall:")
    
    # Create a copy of the budget for simulation
    simulated_budget_df = budget_df.copy()
    
    if submitted and initiative_name and initiative_cost > 0:
        new_row = pd.DataFrame([{'Category': initiative_name, 'Actuals YTD ($K)': initiative_cost}])
        simulated_budget_df = pd.concat([simulated_budget_df, new_row], ignore_index=True)

    # --- Waterfall Chart Logic (from Budget_Tracker.py) ---
    total_budget = budget_df['FY Budget ($K)'].sum()
    sim_actuals = simulated_budget_df['Actuals YTD ($K)'].sum()
    sim_variance = total_budget - sim_actuals

    waterfall_data = [
        go.Waterfall(
            name="Budget Analysis", orientation="v",
            measure=["absolute"] + ["relative"] * len(simulated_budget_df) + ["total"],
            x=["Total Budget"] + simulated_budget_df['Category'].tolist() + ["Remaining Budget"],
            textposition="outside",
            text=[f"{total_budget}K"] + [f"{-val}K" for val in simulated_budget_df['Actuals YTD ($K)']] + [f"{sim_variance}K"],
            y=[total_budget] + (-simulated_budget_df['Actuals YTD ($K)']).tolist() + [sim_variance],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#DA291C"}},
            totals={"marker": {"color": "#0033A0"}}
        )
    ]
    fig_waterfall = go.Figure(waterfall_data)
    fig_waterfall.update_layout(
        title="Fiscal Year Budget Flow (Simulated)", yaxis_title="Amount ($K)", height=450,
        margin=dict(t=50, b=10)
    )
    st.plotly_chart(fig_waterfall, use_container_width=True)
