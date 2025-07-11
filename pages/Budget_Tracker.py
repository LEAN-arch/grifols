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

with st.expander("🌐 My Role as Manager: Fiscal Responsibility", expanded=True):
    st.markdown("""
    As the Senior Manager, a key part of my role is to **"manage and set department budgets as necessary."** This involves not only planning for future needs but also ensuring we are responsible stewards of the resources allocated to us. This dashboard is my primary tool for financial oversight.

    - **Strategic Planning:** It allows me to track spending against our annual plan, ensuring that our highest priority projects, as defined in the **Command Center**, are adequately funded.
    - **Resource Justification:** When requesting headcount or capital equipment, I use the data here to build a data-driven business case for senior management.
    - **Cross-Functional Communication:** This provides a clear summary of our financial status, which is essential when discussing project scope and resources with partners in Manufacturing, Engineering, and Finance.
    - **Proactive Management:** By monitoring the variance and percent spent, I can identify potential overruns early and take corrective action, or identify areas of savings that can be re-allocated to other critical priorities.
    """)

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

# --- Detailed Budget Breakdown ---
col_detail, col_viz = st.columns(2)

with col_detail:
    st.header("Detailed Budget by Category")
    st.caption("A line-item view of the budget, actuals, and variance for each spending category.")
    
    def style_variance(val):
        if val < 0:
            return 'background-color: #F8D7DA; color: #721C24' # Over budget
        return ''
        
    st.dataframe(
        budget_df.style.apply(lambda x: x.map(lambda v: style_variance(v)) if x.name == 'Variance ($K)' else ['']*len(x), axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={
            "FY Budget ($K)": st.column_config.NumberColumn(format="$%dK"),
            "Actuals YTD ($K)": st.column_config.NumberColumn(format="$%dK"),
            "Variance ($K)": st.column_config.NumberColumn(format="$%dK"),
            "% Spent": st.column_config.ProgressColumn(
                format="%.1f%%",
                min_value=0,
                max_value=100
            )
        }
    )

with col_viz:
    st.header("Budget Allocation vs. Actual Spending")
    st.caption("Visualizing the distribution of our budget and how our actual spending compares.")
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=budget_df['Category'],
        x=budget_df['FY Budget ($K)'],
        name='FY Budget',
        orientation='h',
        marker_color='#A2AAAD'
    ))
    fig.add_trace(go.Bar(
        y=budget_df['Category'],
        x=budget_df['Actuals YTD ($K)'],
        name='Actuals YTD',
        orientation='h',
        marker_color='#DA291C'
    ))
    fig.update_layout(
        barmode='group',
        title="Budget vs. Actuals by Category",
        xaxis_title="Amount ($K)",
        yaxis_title=None,
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)

with st.expander("📝 Manager's Analysis and Action Plan"):
    st.markdown("""
    This dashboard provides an immediate and clear picture of my department's financial health.

    - **Area of Concern:** The `External Testing/Consulting` category is significantly **over budget** (Variance of -$30K). This is a critical flag that requires immediate attention.
    - **Investigation:** My first step is to understand the driver for this overspend. Was it an unplanned series of characterization studies? Did a complex investigation require more external lab support than anticipated? I will review the project expenses associated with this line item.
    - **Corrective Action:** To offset this, I see that our `Capital Equipment` spending is currently under budget. If the planned equipment purchase is no longer necessary this fiscal year, I can work with Finance to re-forecast and potentially re-allocate funds. If not, I may need to de-prioritize other, less critical external activities for the remainder of the year.
    - **Strategic Planning:** Seeing the high spend on `Validation Consumables` reinforces the need for accurate planning during the initial phases of our validation projects. For future projects, I will ensure my team provides more detailed estimates for consumable usage to build a more robust budget.
    """)
