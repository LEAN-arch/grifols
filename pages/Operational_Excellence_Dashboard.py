# pages/Operational_Excellence_Dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_improvement_data

st.set_page_config(
    page_title="OpEx Dashboard | Grifols",
    layout="wide"
)

st.title("🚀 Process Improvement Tracker")
st.markdown("### Directing and tracking initiatives to enhance the efficiency, compliance, and robustness of our validation and manufacturing processes.")

with st.expander("🌐 Managerial Focus: Driving Continuous Improvement"):
    st.markdown("""
    A core part of my responsibility as Senior Manager is to **"drive and validate process improvements in manufacturing"** and to demonstrate expertise with methodologies like **"Lean, 5S, [and] Operational Excellence."** This dashboard serves as the central hub for managing my department's OpEx program.
    - **Strategic Focus:** It allows me to translate strategic goals (e.g., "reduce validation cycle time") into a portfolio of specific, actionable initiatives for my team.
    - **Visibility & Accountability:** This platform provides clear visibility into the progress of each initiative and holds the project leads accountable for their timelines and deliverables.
    - **Demonstrating Value:** It helps me showcase the tangible benefits of our improvement efforts to senior leadership, linking our projects to key business metrics.
    """)

# --- Data Generation ---
improvement_df = generate_improvement_data()

# --- OpEx Program KPIs ---
st.header("Process Improvement Program KPIs")
total_initiatives = len(improvement_df)
completed_initiatives = improvement_df[improvement_df['Status'] == 'Complete'].shape[0]
inprogress_initiatives = improvement_df[improvement_df['Status'] == 'In Progress'].shape[0]
total_budget_allocated = improvement_df['Budget ($K)'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Active Initiatives", total_initiatives)
col2.metric("Completed Initiatives (YTD)", completed_initiatives)
col3.metric("Initiatives In Progress", inprogress_initiatives)
col4.metric("Total Budget Allocated", f"${total_budget_allocated}K")

st.divider()

# --- Enhanced Visualization: Impact vs. Effort Matrix ---
st.header("Initiative Prioritization Matrix")
st.caption("Visualizing all initiatives on an Impact vs. Effort matrix to strategically focus resources.")

impact_map = {'Low': 1, 'Medium': 2, 'High': 3}
effort_map = {'Low': 1, 'Medium': 2, 'High': 3}
plot_df = improvement_df.copy()
plot_df['Impact_Num'] = plot_df['Impact'].map(impact_map)
plot_df['Effort_Num'] = plot_df['Effort'].map(effort_map)

fig = px.scatter(
    plot_df, x='Effort_Num', y='Impact_Num', size='Budget ($K)', color='Status',
    hover_name='Initiative Name', text='Initiative ID', size_max=60,
    color_discrete_map={
        'In Progress': '#007A33', 'Complete': '#0033A0',
        'Planned': '#6C6F70', 'At Risk': '#DA291C'
    }
)

fig.add_vline(x=2.5, line_dash="dash")
fig.add_hline(y=2.5, line_dash="dash")
fig.add_annotation(x=1.5, y=3.2, text="<b>Quick Wins</b>", showarrow=False, font_size=14, font_color="green")
fig.add_annotation(x=1.5, y=1.8, text="Fill-Ins", showarrow=False)
fig.add_annotation(x=3.2, y=3.2, text="<b>Strategic Initiatives</b>", showarrow=False, font_size=14, font_color="blue")
fig.add_annotation(x=3.2, y=1.8, text="Thankless Tasks", showarrow=False)

fig.update_layout(
    height=500, title='Impact vs. Effort Portfolio View',
    xaxis_title='Effort Required', yaxis_title='Strategic Impact',
    xaxis=dict(tickvals=list(effort_map.values()), ticktext=list(effort_map.keys())),
    yaxis=dict(tickvals=list(impact_map.values()), ticktext=list(impact_map.keys()))
)
fig.update_traces(textposition='top center')
st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- Detailed Initiative Tracker ---
st.header("Detailed Initiative Tracker")
st.caption("A comprehensive list of all process improvement projects, their drivers, and progress.")

st.dataframe(
    improvement_df,
    use_container_width=True, hide_index=True,
    column_config={
        "Progress (%)": st.column_config.ProgressColumn("Progress", min_value=0, max_value=100, format="%d%%"),
        "Budget ($K)": st.column_config.NumberColumn("Budget", format="$%dK")
    }
)

with st.container(border=True):
    st.header("Managerial Analysis & Action Plan")
    st.markdown("""
    - **Strategic Prioritization:** The **Impact vs. Effort Matrix** is my primary tool for strategic planning. It immediately shows that the **'Reduce Re-work in Doc Review'** project is a high-impact, medium-effort initiative, making it a key focus. The **'5S Implementation'** was a perfect "Quick Win" and its completion is a success story to share.
    
    - **Resource Planning:** The **'Automate CPV Data Trending'** is a high-impact, high-effort "Strategic Initiative." Its large bubble indicates a significant budget, which I have already secured. Knowing its high effort, I will ensure Anna K. has protected time and the necessary support from IT to ensure its success when we kick it off.
    
    - **Performance Monitoring:** In the detailed tracker, I can see the **'Standardize Tech Transfer Template'** is only at 40% progress, while the doc review project is at 75%. In my next 1-on-1 with Anna K., I will use this data to discuss any potential roadblocks or resource needs for the template project to ensure it stays on track.
    """)
