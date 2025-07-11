# pages/C_Action_Log.py

import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Action Log | Grifols", layout="wide")

st.title("📋 Manager's Action Log")
st.markdown("### A centralized and persistent log to track action items, owners, and due dates derived from dashboard analyses.")

# --- Initialize session state if it's missing (for direct navigation) ---
if 'action_log' not in st.session_state:
    st.session_state.action_log = pd.DataFrame(columns=[
        "Action Item", "Source Dashboard", "Owner", "Due Date", "Status", "Notes"
    ])

# --- Filtering Options ---
st.sidebar.header("Filter Actions")
status_filter = st.sidebar.multiselect(
    "Filter by Status",
    options=st.session_state.action_log['Status'].unique(),
    default=st.session_state.action_log['Status'].unique()
)
owner_filter = st.sidebar.multiselect(
    "Filter by Owner",
    options=st.session_state.action_log['Owner'].unique(),
    default=st.session_state.action_log['Owner'].unique()
)

# Apply filters
if not st.session_state.action_log.empty:
    filtered_log = st.session_state.action_log[
        st.session_state.action_log['Status'].isin(status_filter) &
        st.session_state.action_log['Owner'].isin(owner_filter)
    ]
else:
    filtered_log = st.session_state.action_log.copy()


st.info(f"Displaying {len(filtered_log)} of {len(st.session_state.action_log)} total actions.")

# --- Display and Edit the Action Log ---
edited_log = st.data_editor(
    filtered_log,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Action Item": st.column_config.TextColumn(width="large", required=True),
        "Source Dashboard": st.column_config.TextColumn(disabled=True),
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Open", "In Progress", "Blocked", "Complete"],
            required=True
        ),
        "Owner": st.column_config.TextColumn(required=True),
        "Due Date": st.column_config.DateColumn(required=True),
    },
    key="action_log_editor"
)

# --- Logic to Update the Main Log from the Editor ---
# When the user edits the filtered view, we need to update the original, unfiltered dataframe
if st.button("Save Changes to Log"):
    # This is a simplified update logic. For production apps, a more careful merge/update is needed.
    st.session_state.action_log = pd.DataFrame(edited_log)
    st.success("Action log updated successfully!")
    st.rerun()
