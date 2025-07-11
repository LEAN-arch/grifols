# pages/Staff_Management_Hub.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_staff_performance_data

st.set_page_config(
    page_title="Staff Management Hub | Grifols",
    layout="wide"
)

st.title("👥 Staff Management & Development Hub")
st.markdown("### A dedicated dashboard for setting team objectives, tracking performance, and managing professional development.")

# --- Data Generation ---
staff_df = generate_staff_performance_data()

# --- Team-Level KPIs ---
st.header("Team Performance & Utilization Overview")
avg_goals_complete = staff_df['Q3 Goals Completed (%)'].mean()
avg_training_complete = staff_df['Required Training Complete (%)'].mean()
team_utilization = staff_df['Utilization (%)'].mean()
over_utilized_count = staff_df[staff_df['Utilization (%)'] > 100].shape[0]


col1, col2, col3, col4 = st.columns(4)
col1.metric("Team Utilization", f"{team_utilization:.0f}%", help="Average workload across all team members.")
col2.metric("Over-Utilized Staff", over_utilized_count, delta=f"{over_utilized_count} at risk", delta_color="inverse", help="Staff with >100% assigned project load.")
col3.metric("Avg. Quarterly Goal Completion", f"{avg_goals_complete:.1f}%")
col4.metric("Avg. Training Compliance", f"{avg_training_complete:.1f}%")

st.divider()

# --- Enhanced Visualization Section ---
col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.header("Team Utilization Heatmap")
    st.caption("Visualizing current workload distribution to manage bandwidth and prevent burnout.")
    
    # Create a DataFrame suitable for a heatmap
    heatmap_df = staff_df.set_index('Team Member')[['Utilization (%)']]
    
    fig_heatmap = px.imshow(
        heatmap_df.T,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdYlGn_r', # Red-Yellow-Green (reversed)
        range_color=[50, 120],
        title="Current Team Workload Utilization"
    )
    fig_heatmap.update_layout(xaxis_title="", yaxis_title="")
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col_viz2:
    st.header("Performance & Compliance Matrix")
    st.caption("Mapping team members by goal achievement and training status to tailor management focus.")
    
    fig_quad = px.scatter(
        staff_df,
        x="Q3 Goals Completed (%)",
        y="Required Training Complete (%)",
        color="Role",
        size=[20]*len(staff_df), # Use a constant size for clarity
        text="Team Member",
        title="Goal Achievement vs. Training Compliance"
    )
    fig_quad.add_vline(x=90, line_dash="dash")
    fig_quad.add_hline(y=90, line_dash="dash")
    fig_quad.update_traces(textposition='top center')
    fig_quad.update_layout(xaxis_range=[70,105], yaxis_range=[70,105])
    st.plotly_chart(fig_quad, use_container_width=True)

st.divider()

# --- Detailed Data & Action Plan ---
st.header("Individual Performance & Development Tracker")
st.caption("A comprehensive, editable overview of each team member's goals, training status, and development focus.")

st.data_editor(
    staff_df,
    column_config={
        "Utilization (%)": st.column_config.ProgressColumn("Utilization", min_value=0, max_value=120, format="%d%%"),
        "Q3 Goals Completed (%)": st.column_config.ProgressColumn("Q3 Goal Completion", min_value=0, max_value=100, format="%d%%"),
        "Required Training Complete (%)": st.column_config.ProgressColumn("Training Compliance", min_value=0, max_value=100, format="%d%%"),
        "Performance Review Status": st.column_config.SelectboxColumn("Perf. Review Status", options=["Complete", "Scheduled", "Due"]),
        "Development Goal": st.column_config.TextColumn("Current Development Goal", width="large")
    },
    use_container_width=True, hide_index=True
)

with st.container(border=True):
    st.header("Managerial Analysis & Action Plan")
    st.markdown("""
    - **Performance Analysis:** The **Performance Matrix** provides a clear snapshot of my team. **Anna K.** and **Maria S.** are in the top-right "High Performer" quadrant. **David L.** is a solid performer but slightly behind on his goals. The **New Hire** is a clear outlier in the bottom-right, indicating they are meeting goals but are behind on training—a typical and manageable situation.
    
    - **Workload & Burnout Risk:** The **Utilization Heatmap** immediately flags **Anna K.** as a critical concern. At 110% utilization, she is over-burdened, which poses a risk to both her projects and her well-being. This directly contradicts my goal of having her lead a new OpEx team.
    
    - **Strategic Action Plan:**
        1.  **Delegate:** To free up Anna's capacity, I will "delegate appropriately." The `Automate CPV Data Trending` project, currently assigned to her, is a perfect development opportunity for **Maria S.**, whose goal is to gain expertise in new areas. I will re-assign this project.
        2.  **Onboarding Focus:** I will work with David L. (the designated mentor) and the New Hire to create a 30-day plan to close the 25% training gap, moving them into the "High Performer" quadrant.
        3.  **Performance Coaching:** In my upcoming 1-on-1 with David L., we will focus on the 15% gap in his quarterly goals to understand the blockers and create a plan to ensure he hits 100% next quarter.
    """)
