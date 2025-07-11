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

# --- Upgraded KPIs with Superior Visuals: "Metric Card" Approach ---
st.header("Strategic Program Health: Key Performance Indicators")

# --- Custom CSS for Metric Cards ---
st.markdown("""
<style>
.metric-card {
    background-color: #F8F8F8;
    border-radius: 10px;
    padding: 15px;
    border: 1px solid #EAEAEA;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
.metric-title {
    font-size: 16px;
    font-weight: bold;
    color: #333333;
    margin-bottom: 5px;
}
.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #DA291C;
}
.metric-target {
    font-size: 12px;
    color: #6C6F70;
}
</style>
""", unsafe_allow_html=True)

# Calculate Managerial KPIs
completed_projects_df = portfolio_df[portfolio_df['Status'].str.contains('Complete')]
on_time_completion_pct = (completed_projects_df[completed_projects_df['Status'] == 'Complete - On Time'].shape[0] / len(completed_projects_df)) * 100 if not completed_projects_df.empty else 100.0
projects_at_risk = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
high_priority_risks = risks_df[risks_df['Risk Score'] >= 15].shape[0]
revals_due = 2

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=False):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Portfolio On-Time Completion</div>
            <div class="metric-value">{on_time_completion_pct:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(on_time_completion_pct))
        st.markdown("<div class='metric-target'>Target: > 95%</div>", unsafe_allow_html=True)

with col2:
    with st.container(border=False):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Projects Currently At-Risk</div>
            <div class="metric-value">{projects_at_risk}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(projects_at_risk / 5 * 100) if projects_at_risk > 0 else 0) # Scale progress bar
        st.markdown("<div class='metric-target'>Target: 0</div>", unsafe_allow_html=True)


with col3:
    with st.container(border=False):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Open High-Priority Risks</div>
            <div class="metric-value">{high_priority_risks}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(high_priority_risks / 5 * 100) if high_priority_risks > 0 else 0)
        st.markdown("<div class='metric-target'>Target: 0</div>", unsafe_allow_html=True)

with col4:
    with st.container(border=False):
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Revalidations Overdue</div>
            <div class="metric-value">{revals_due}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(int(revals_due / 5 * 100) if revals_due > 0 else 0)
        st.markdown("<div class='metric-target'>Target: 0</div>", unsafe_allow_html=True)

st.divider()

# --- Main Content Area: Portfolio and Resource Management ---
col_gantt, col_risk = st.columns(2)

with col_gantt:
    st.header("Portfolio Timeline & Resource Allocation")
    st.caption("Gantt chart overview grouped by project lead to visualize team workload and project timelines.")
    
    portfolio_df_sorted = portfolio_df.sort_values(by='Project Lead')
    
    fig = px.timeline(
        portfolio_df_sorted, x_start="Start Date", x_end="End Date", y="Project Name",
        color="Status", facet_row="Project Lead", title="Active Projects by Lead Engineer",
        hover_name="Project Name", color_discrete_map={
            'In Progress': '#007A33', 'At Risk': '#DA291C', 'On Hold': '#6C6F70', 'Complete - On Time': '#0033A0'
        }
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- START: Updated and Corrected Risk Visualization Block ---
with col_risk:
    st.header("Program Risk Bubble Matrix")
    st.caption("Prioritizing risks based on impact and probability. Color indicates max severity; size indicates volume.")

    # 1. Aggregate risk data for the bubble matrix
    # Added include_groups=False to address the FutureWarning
    risk_agg = risks_df.groupby(['Impact', 'Probability']).apply(lambda g: pd.Series({
        'Risk Count': len(g),
        'Max Risk Score': g['Risk Score'].max(),
        'Risk Details': '<br>'.join(f"<b>{row['Risk ID']}</b> (Score: {row['Risk Score']}): {row['Risk Description']}"
                                    for _, row in g.iterrows())
    }), include_groups=False).reset_index()

    # 2. Create the advanced bubble matrix plot
    fig_risk = go.Figure()

    # Add background color shapes for risk levels
    fig_risk.add_shape(type="rect", xref="x", yref="y", x0=0.5, y0=0.5, x1=3.5, y1=3.5,
                      fillcolor="rgba(0, 122, 51, 0.1)", line_color="rgba(0, 122, 51, 0.3)")
    fig_risk.add_shape(type="rect", xref="x", yref="y", x0=3.5, y0=0.5, x1=5.5, y1=3.5,
                      fillcolor="rgba(255, 199, 44, 0.1)", line_color="rgba(255, 199, 44, 0.3)")
    fig_risk.add_shape(type="rect", xref="x", yref="y", x0=0.5, y0=3.5, x1=3.5, y1=5.5,
                      fillcolor="rgba(255, 199, 44, 0.1)", line_color="rgba(255, 199, 44, 0.3)")
    fig_risk.add_shape(type="rect", xref="x", yref="y", x0=3.5, y0=3.5, x1=5.5, y1=5.5,
                      fillcolor="rgba(218, 41, 28, 0.15)", line_color="rgba(218, 41, 28, 0.4)")

    # Add the scatter plot trace (the bubbles)
    fig_risk.add_trace(go.Scatter(
        x=risk_agg['Probability'],
        y=risk_agg['Impact'],
        mode='markers+text',
        marker=dict(
            color=risk_agg['Max Risk Score'],
            colorscale='YlOrRd',
            size=risk_agg['Risk Count'] * 20,
            sizemin=15,
            showscale=True,
            colorbar=dict(title='Max Risk Score', x=1.15),
            line=dict(width=1, color='DarkSlateGrey')
        ),
        text=risk_agg['Risk Count'],
        textfont=dict(color='black', size=14),
        # FIX: Use customdata to hold the original risk count for the hovertemplate
        customdata=risk_agg['Risk Count'],
        hovertext=risk_agg['Risk Details'],
        hovertemplate=(
            "<b>Impact:</b> %{y}<br>"
            "<b>Probability:</b> %{x}<br>"
            # FIX: Reference customdata instead of the scaled marker.size
            "<b>Risk Count:</b> %{customdata}<br>"
            "<hr><b>Risks in this Category:</b><br>%{hovertext}<extra></extra>"
        )
    ))
    
    # 3. Final layout styling
    fig_risk.update_layout(
        title="Risk Matrix: Severity (Color), Volume (Size), and Impact",
        xaxis_title="Probability",
        yaxis_title="Impact",
        height=600,
        plot_bgcolor='#FFFFFF',
        xaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Remote', 'Unlikely', 'Possible', 'Likely', 'Certain'],
            range=[0.5, 5.5],
            showgrid=True, gridcolor='rgba(0,0,0,0.1)'
        ),
        yaxis=dict(
            tickmode='array',
            tickvals=[1, 2, 3, 4, 5],
            ticktext=['Negligible', 'Minor', 'Moderate', 'Major', 'Critical'],
            autorange="reversed",
            range=[5.5, 0.5],
            showgrid=True, gridcolor='rgba(0,0,0,0.1)'
        ),
        showlegend=False,
        margin=dict(t=50, l=50, r=50, b=50)
    )

    st.plotly_chart(fig_risk, use_container_width=True)
# --- END: Updated and Corrected Risk Visualization Block ---
    
st.divider()

with st.container(border=True):
    st.header("Managerial Analysis & Action Plan")
    st.markdown("""
    - **Performance Analysis:** The visual KPIs provide an instant health check. While our **On-Time Completion Rate** is slightly below target, the more pressing issues are the **2 Projects At-Risk** and **2 Overdue Revalidations**. These represent immediate compliance and timeline risks.
    - **Resource Allocation Insights:** The timeline, faceted by lead, clearly shows that **Anna K.** is managing two large, overlapping projects. This represents a **resource bottleneck** and a key-person dependency risk, which is also flagged as our single highest-priority risk on the risk matrix.
    - **Risk Mitigation Focus:** The risk matrix instantly focuses our attention on the top-right, red quadrant. Our primary risk mitigation efforts must be directed at the resource bottleneck.
    - **Strategic Action Plan:**
        1. **At-Risk Projects:** My top priority is to drill down into the two at-risk items using the dedicated dashboards to formulate mitigation plans with the team leads.
        2. **Resource Balancing:** I will meet with Anna K. to review her workload. The data strongly supports re-assigning one of her upcoming projects (e.g., the CPV Automation) to another team member, like Maria S., as a development opportunity. This addresses the risk and develops my team.
    """)
