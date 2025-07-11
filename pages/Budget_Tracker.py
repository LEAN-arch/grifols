# pages/Budget_Tracker.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_budget_data

st.set_page_config(
    page_title="Budget Tracker | Grifols",
    layout="wide"
)

st.title("💰 Departmental Budget Tracker")
st.markdown("### Managing the financial resources for the Process Transfer, Development, and Validation program.")

# --- Data Generation ---
budget_df = generate_budget_data()

# --- High-Level KPIs ---
st.header("Overall Fiscal Year Budget Status")
total_budget = budget_df['FY Budget ($K)'].sum()
total_actuals = budget_df['Actuals YTD ($K)'].sum()
total_variance = total_budget - total_actuals
percent_spent = (total_actuals / total_budget) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total FY Budget", f"${total_budget:,.0f}K")
col2.metric("Actuals YTD", f"${total_actuals:,.0f}K")
col3.metric("Remaining Budget", f"${total_variance:,.0f}K")
col4.metric("Total Budget Spent", f"{percent_spent:.1f}%")

st.progress(int(percent_spent))
st.divider()

# --- Upgraded Visualization and Detailed Data ---
col_detail, col_viz = st.columns(2)

with col_detail:
    st.header("Detailed Budget by Category")
    st.caption("A line-item view of the budget, actuals, and variance for each spending category.")
    
    def style_variance(val):
        if val < 0:
            return 'background-color: #F8D7DA; color: #721C24' # Over budget
        return ''
        
    st.dataframe(
        budget_df.style.map(lambda v: style_variance(v), subset=['Variance ($K)']),
        use_container_width=True,
        hide_index=True,
        column_config={
            "FY Budget ($K)": st.column_config.NumberColumn(format="$%dK"),
            "Actuals YTD ($K)": st.column_config.NumberColumn(format="$%dK"),
            "Variance ($K)": st.column_config.NumberColumn(format="$%dK"),
            "% Spent": st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=100)
        },
        height=480
    )

with col_viz:
    st.header("Budget Waterfall Analysis")
    st.caption("Visualizing how spending in each category contributes to the remaining budget.")

    # Prepare data for waterfall chart
    waterfall_data = [
        go.Waterfall(
            name="Budget Analysis",
            orientation="v",
            measure=["absolute"] + ["relative"] * len(budget_df) + ["total"],
            x=["Total Budget"] + budget_df['Category'].tolist() + ["Remaining Budget"],
            textposition="outside",
            text=[f"{total_budget}K"] + [f"{-val}K" for val in budget_df['Actuals YTD ($K)']] + [f"{total_variance}K"],
            y=[total_budget] + (-budget_df['Actuals YTD ($K)']).tolist() + [total_variance],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "#DA291C"}}, # Red for spending
            increasing={"marker": {"color": "#007A33"}}, # Green for additions (none here)
            totals={"marker": {"color": "#0033A0"}} # Blue for totals
        )
    ]

    fig = go.Figure(waterfall_data)
    fig.update_layout(
        title="Fiscal Year Budget Flow",
        yaxis_title="Amount ($K)",
        height=450,
        margin=dict(t=50, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)

with st.container(border=True):
    st.header("Managerial Analysis & Action Plan")
    st.markdown("""
    - **Financial Health:** The waterfall chart provides a powerful and intuitive story for financial reviews. It clearly shows our starting budget of **$2,180K** being drawn down by each spending category, with a final remaining balance of **$475K**. The overall budget consumption of **78%** is on track for this point in the fiscal year.

    - **Area of Concern:** The chart immediately draws the eye to the largest red bar, **Salaries & Benefits**, which is our biggest expenditure, as expected. However, the detailed table highlights the primary issue: the **External Testing/Consulting** category is **$30K over budget**. This variance requires immediate management attention.

    - **Strategic Decision-Making:**
        1.  **Investigate Variance:** My first action is to determine the driver for the consulting overspend. Was it due to an unforeseen technical challenge on a project that required specialized support? Or was it poor initial scoping?
        2.  **Budget Re-forecasting:** I see a significant positive variance in the **Capital Equipment** budget. If the planned equipment purchase can be deferred to the next fiscal year without impacting our strategic goals, I will work with Finance to re-allocate these funds to cover the consulting overage.
        3.  **Future State:** This analysis demonstrates a need for tighter controls around the scoping of external work. I will implement a more rigorous review process for all statements of work (SOWs) before they are approved to ensure our budget estimates are more robust in the future. This is a key process improvement for my department.
    """)
