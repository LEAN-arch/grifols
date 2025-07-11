# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_validation_portfolio_data, generate_program_risk_data

# --- Page Configuration ---
st.set_page_config(
    page_title="Validation & Transfer Command Center | Grifols",
    page_icon="https://www.grifols.com/o/grifols-theme/images/favicon.ico",
    layout="wide"
)

# --- Data Loading ---
portfolio_df = generate_validation_portfolio_data()
risks_df = generate_program_risk_data()

# --- Page Title and Header ---
st.image("https://www.grifols.com/o/grifols-theme/images/logos/logo-grifols.svg", width=250)
st.title("Validation & Transfer Program Command Center")
st.markdown("### Strategic Management of Process Transfer, Development, and Validation for Grifols' NAT & BTS Diagnostic Products.")

# --- Upgraded KPIs with Visual Context ---
st.header("Strategic Program Health: Visual KPIs")

completed_projects_df = portfolio_df[portfolio_df['Status'].str.contains('Complete')]
on_time_completion_pct = (completed_projects_df[completed_projects_df['Status'] == 'Complete - On Time'].shape[0] / len(completed_projects_df)) * 100 if not completed_projects_df.empty else 100.0
projects_at_risk = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
high_priority_risks = risks_df[risks_df['Risk Score'] >= 15].shape[0]
budget_variance_pct = -12.5 # Example: 12.5% over budget

# Helper function for bullet charts
def create_bullet_chart(value, target, title, suffix, invert_colors=False):
    fig = go.Figure(go.Indicator(
        mode="number+gauge",
        gauge={'shape': "bullet", 'axis': {'range': [None, 120 if not invert_colors else 20]},
               'threshold': {'line': {'color': "red", 'width': 2}, 'thickness': 0.75, 'value': target},
               'bar': {'color': "green" if (value >= target and not invert_colors) or (value <= target and invert_colors) else "orange"}},
        value=value,
        domain={'x': [0.1, 1], 'y': [0, 1]},
        title={'text': title, 'font': dict(size=14)},
        number={'suffix': suffix}
    ))
    fig.update_layout(height=100, margin=dict(l=10, r=10, t=30, b=10, pad=0))
    return fig

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.plotly_chart(create_bullet_chart(on_time_completion_pct, 95, "On-Time Completion Rate", "%"), use_container_width=True)
with col2:
    st.plotly_chart(create_bullet_chart(projects_at_risk, 0, "Projects At-Risk", "", invert_colors=True), use_container_width=True)
with col3:
    st.plotly_chart(create_bullet_chart(high_priority_risks, 0, "High-Priority Risks", "", invert_colors=True), use_container_width=True)
with col4:
    st.plotly_chart(create_bullet_chart(abs(budget_variance_pct), 5, "Budget Variance", "%", invert_colors=True), use_container_width=True)

st.divider()

# --- Main Content Area: Portfolio and Resource Management ---
col1, col2 = st.columns(2)

with col1:
    st.header("Portfolio Timeline & Resource Allocation")
    st.caption("Gantt chart overview grouped by project lead to visualize team workload and project timelines.")
    
    # Sort by lead for grouping
    portfolio_df_sorted = portfolio_df.sort_values(by='Project Lead')
    
    fig = px.timeline(
        portfolio_df_sorted,
        x_start="Start Date",
        x_end="End Date",
        y="Project Name",
        color="Status",
        facet_row="Project Lead",
        title="Active Projects by Lead Engineer",
        hover_name="Project Name",
        color_discrete_map={
            'In Progress': '#007A33', 'At Risk': '#DA291C',
            'On Hold': '#6C6F70', 'Complete - On Time': '#0033A0'
        }
    )
    fig.update_yaxes(autorange="reversed") # Keep consistent order
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Program Risk Heatmap")
    st.caption("Prioritizing risks to compliance and timelines based on impact and probability.")
    
    # Create a pivot table for the heatmap
    risk_pivot = risks_df.pivot_table(index='Impact', columns='Probability', values='Risk Score', aggfunc='count').fillna(0)
    risk_text = risks_df.pivot_table(index='Impact', columns='Probability', values='Risk ID', aggfunc=lambda x: '<br>'.join(x)).fillna('')

    fig_risk = go.Figure(data=go.Heatmap(
        z=risk_pivot.values,
        x=risk_pivot.columns,
        y=risk_pivot.index,
        colorscale='YlOrRd',
        text=risk_text,
        hovertemplate='<b>Risk IDs:</b><br>%{text}<br><b>Impact:</b> %{y}<br><b>Probability:</b> %{x}<extra></extra>'
    ))
    fig_risk.update_layout(
        title="Risk Heatmap (Count of Risks per Category)",
        xaxis_title="Probability",
        yaxis_title="Impact",
        height=600,
        xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5], ticktext=['Remote', 'Unlikely', 'Possible', 'Likely', 'Certain']),
        yaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5], ticktext=['Negligible', 'Minor', 'Moderate', 'Major', 'Critical'], autorange="reversed")
    )
    st.plotly_chart(fig_risk, use_container_width=True)

st.divider()

with st.container(border=True):
    st.header("Managerial Analysis & Action Items")
    st.markdown("""
    - **Performance Analysis:** The visual KPIs immediately draw attention to the **12.5% budget variance**, which exceeds our 5% target. The **On-Time Completion Rate** is slightly below our 95% goal. These are the top two metrics to address in my next leadership update.

    - **Resource Allocation Insights:** The timeline, now faceted by lead, clearly shows that **Anna K.** is managing two large, overlapping projects. While she is a top performer, this represents a **resource bottleneck** and a key-person dependency risk. This data supports a discussion about reassigning a smaller project or providing her with junior support.

    - **Risk Mitigation Focus:** The heatmap instantly focuses our attention on the top-right quadrant. We have a high-impact, high-probability risk related to resource bottlenecking, which directly corroborates the Gantt chart's story. Our primary risk mitigation efforts must be directed here.

    - **Strategic Action Plan:**
        1.  **Budget:** Drill down into the **Budget Tracker** to identify the source of the variance and formulate a correction plan.
        2.  **Resources:** In my next 1-on-1 with Anna K., I will use the timeline visual to discuss her workload and explore options for delegation to "manage and develop" other team members like Maria S.
        3.  **Risk:** The resource bottleneck risk (RISK-RES-01) will be the top agenda item for our next team meeting, where we will brainstorm and assign mitigation actions.
    """)
