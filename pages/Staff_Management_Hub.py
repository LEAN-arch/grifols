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

with st.expander("🌐 My Role as Manager: Leading and Developing the Team", expanded=True):
    st.markdown("""
    As the Senior Manager, one of my most important responsibilities is to **"provide leadership for the group"** and **"manage and develop staff by setting individual and group goals and manage performance based on Grifols guidelines."** This dashboard is my primary tool for fulfilling that duty.

    - **Performance Management:** It provides a centralized, data-driven view of my team's performance against their quarterly goals, enabling objective and constructive feedback during performance reviews.
    - **Training & Compliance:** It allows me to "evaluate the effectiveness of training" by monitoring the completion status of required GMP and technical training for each team member, ensuring our group remains compliant and skilled.
    - **Professional Development:** By tracking development goals, I can actively "manage diverse groups of technical a
