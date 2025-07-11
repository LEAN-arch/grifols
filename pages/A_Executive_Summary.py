# pages/A_Executive_Summary.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils import (
    generate_validation_portfolio_data,
    generate_program_risk_data,
    generate_budget_data,
    generate_revalidation_data
)
import streamlit.components.v1 as components

st.set_page_config(page_title="Executive Summary | Grifols", layout="wide")

# --- Custom CSS for printing ---
st.markdown("""
<style>
@media print {
    .stDeployButton, .stSidebar {
        display: none !important;
    }
    .main > div {
        padding-top: 0;
    }
    .stExpander, .stTextArea {
        page-break-inside: avoid;
    }
}
.report-container {
    border: 1px solid #EAEAEA;
    border-radius: 10px;
    padding: 25px;
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

# --- Data Loading ---
portfolio_df = generate_validation_portfolio_data()
risks_df = generate_program_risk_data()
budget_df = generate_budget_data()
revalidation_df = generate_revalidation_data()

# --- Page Header ---
st.title("Monthly Executive Summary")
st.markdown(f"**Report Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}")

# --- Print Button ---
if st.button("🖨️ Generate Print View / PDF"):
    components.html("<script>window.print()</script>", height=0)

with st.container(border=True):
    st.header("1. Manager's Narrative")
    st.text_area(
        "Narrative",
        "Overall, the program is tracking to plan with key strategic initiatives underway. On-time completion is slightly below target due to a technical issue on one project, which is now resolved. The primary focus for the upcoming month is to mitigate the resource bottleneck risk associated with Anna K. by re-assigning the 'Automate CPV' project. The budget is on track, with the exception of an overspend in consulting that is being actively managed by reallocating funds from deferred CapEx. Two systems are overdue for revalidation and are our top priority for the validation team.",
        height=200,
        label_visibility="collapsed"
    )

    st.header("2. Key Program Health Metrics")

    # --- Calculate KPIs ---
    on_time_completion_pct = (portfolio_df[portfolio_df['Status'] == 'Complete - On Time'].shape[0] / portfolio_df[portfolio_df['Status'].str.contains('Complete')].shape[0]) * 100
    projects_at_risk = portfolio_df[portfolio_df['Status'] == 'At Risk'].shape[0]
    high_priority_risks = risks_df[risks_df['Risk Score'] >= 15].shape[0]
    revals_due = revalidation_df[revalidation_df['Status'] == 'Due'].shape[0]
    total_budget = budget_df['FY Budget ($K)'].sum()
    percent_spent = (budget_df['Actuals YTD ($K)'].sum() / total_budget) * 100

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("On-Time Completion", f"{on_time_completion_pct:.1f}%")
    kpi2.metric("Projects At-Risk", projects_at_risk)
    kpi3.metric("High-Priority Risks", high_priority_risks)
    kpi4.metric("Revalidations Due", revals_due)
    kpi5.metric("FY Budget Spent", f"{percent_spent:.1f}%")

    st.header("3. Strategic Overview")
    col_risk, col_budget = st.columns(2)

    with col_risk:
        st.subheader("Program Risk Matrix")
        # --- Risk Matrix Logic (copied from app.py) ---
        risk_agg = risks_df.groupby(['Impact', 'Probability']).apply(lambda g: pd.Series({
            'Risk Count': len(g), 'Max Risk Score': g['Risk Score'].max()
        }), include_groups=False).reset_index()

        fig_risk = go.Figure()
        fig_risk.add_shape(type="rect", xref="x", yref="y", x0=0.5, y0=0.5, x1=3.5, y1=3.5, fillcolor="rgba(0, 122, 51, 0.1)", line_color="rgba(0, 122, 51, 0.3)")
        fig_risk.add_shape(type="rect", xref="x", yref="y", x0=3.5, y0=0.5, x1=5.5, y1=3.5, fillcolor="rgba(255, 199, 44, 0.1)", line_color="rgba(255, 199, 44, 0.3)")
        fig_risk.add_shape(type="rect", xref="x", yref="y", x0=0.5, y0=3.5, x1=3.5, y1=5.5, fillcolor="rgba(255, 199, 44, 0.1)", line_color="rgba(255, 199, 44, 0.3)")
        fig_risk.add_shape(type="rect", xref="x", yref="y", x0=3.5, y0=3.5, x1=5.5, y1=5.5, fillcolor="rgba(218, 41, 28, 0.15)", line_color="rgba(218, 41, 28, 0.4)")
        fig_risk.add_trace(go.Scatter(
            x=risk_agg['Probability'], y=risk_agg['Impact'], mode='markers+text',
            marker=dict(color=risk_agg['Max Risk Score'], colorscale='YlOrRd', size=risk_agg['Risk Count'] * 20, sizemin=15, showscale=False, line=dict(width=1, color='DarkSlateGrey')),
            text=risk_agg['Risk Count'], textfont=dict(color='black', size=14), hoverinfo='none'
        ))
        fig_risk.update_layout(
            xaxis_title="Probability", yaxis_title="Impact", height=400,
            xaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5], ticktext=['Remote', 'Unlikely', 'Possible', 'Likely', 'Certain'], range=[0.5, 5.5]),
            yaxis=dict(tickmode='array', tickvals=[1, 2, 3, 4, 5], ticktext=['Negligible', 'Minor', 'Moderate', 'Major', 'Critical'], autorange="reversed", range=[5.5, 0.5]),
            margin=dict(t=20, b=20, l=20, r=20)
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col_budget:
        st.subheader("Budget vs. Actuals")
        fig_budget = go.Figure(go.Indicator(
            mode = "number+gauge",
            gauge = {'shape': "bullet",
                     'axis': {'range': [None, total_budget]},
                     'threshold': {
                         'line': {'color': "red", 'width': 2},
                         'thickness': 0.75,
                         'value': total_budget},
                     'bar': {'color': "#0033A0"},
                    },
            value = budget_df['Actuals YTD ($K)'].sum(),
            delta = {'reference': total_budget},
            number= {'prefix': "$", 'suffix': "K"},
            title = {"text": "Total Spend (YTD)"}))
        fig_budget.update_layout(height=400, margin=dict(t=50, b=40, l=20, r=20))
        st.plotly_chart(fig_budget, use_container_width=True)
