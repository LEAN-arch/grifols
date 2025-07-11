# pages/Travel_Vendor_Management.py

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.set_page_config(
    page_title="Travel & Vendor Mgmt | Grifols",
    layout="wide"
)

st.title("✈️ Travel & Vendor Management Hub")
st.markdown("### Planning and tracking essential on-site travel and managing key vendor relationships.")

with st.expander("🌐 My Role as Manager: On-Site Oversight and Partnership", expanded=True):
    st.markdown("""
    While data provides a powerful overview, effective management of external partners and critical projects often requires on-site presence. My role states I **"may require travel up to 10% to vendors or other Grifols sites."** This dashboard is my tool for managing this responsibility strategically.

    - **Purposeful Travel:** I use this to plan and justify all travel, ensuring it is targeted and provides value. This includes "person-in-plant" oversight during critical validation batches, supplier audits, and strategic partnership meetings.
    - **Vendor Management:** A significant portion of our work relies on external vendors for services, testing, and materials. This hub provides a centralized place to track our key partners, their status, and performance notes.
    - **Budgetary Control:** All travel and external services have budgetary implications. This tool helps me to plan for these expenses and track them against the departmental budget managed in the **Budget Tracker**.
    - **Cross-Functional Visibility:** It provides visibility to my leadership and cross-functional partners on my engagement with external sites, reinforcing our commitment to strong partnerships.
    """)

# --- Mock Data Generation ---
def generate_travel_plan_data():
    data = {
        'Trip ID': ['TVL-24-005', 'TVL-24-006', 'TVL-24-007'],
        'Lead Traveler': ['David L.', 'Sr. Manager', 'Anna K.'],
        'Destination': ['Grifols - Clayton, NC', 'Supplier HQ - Germany', 'Grifols - Emeryville, CA'],
        'Purpose': ['Person-in-plant for PV Batch #1', 'Key Supplier Audit & QBR', 'Tech Transfer Kick-off Meeting'],
        'Project': ['New Antigen Tech Transfer', 'All', 'New Reagent Development'],
        'Status': ['Complete', 'Planned', 'Planned'],
        'Dates': ['2024-08-12 to 2024-08-16', '2024-10-21 to 2024-10-25', '2024-11-04 to 2024-11-05']
    }
    return pd.DataFrame(data)

def generate_vendor_list_data():
    data = {
        'Vendor Name': ['Pharma-Validate Inc.', 'Bio-Assay Labs', 'GMP Consumables Co.'],
        'Service / Product': ['Validation Protocol Authoring', 'External Potency Testing', 'Sterile Vials & Stoppers'],
        'Status': ['Active MSA', 'Active MSA', 'Approved Supplier'],
        'Last Audit Date': [pd.to_datetime('2023-11-15'), pd.to_datetime('2024-02-20'), pd.to_datetime('2023-09-01')],
        'Notes': ['Primary partner for protocol writing support.', 'Used for release testing of development lots.', 'Sole supplier for DG Gel Card vials - High Risk.']
    }
    return pd.DataFrame(data)

travel_df = generate_travel_plan_data()
vendor_df = generate_vendor_list_data()


# --- Travel Plan Section ---
st.header("Departmental Travel Plan & History")
st.caption("A log of all planned and completed travel to Grifols sites and external vendors.")

st.dataframe(
    travel_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Dates": st.column_config.TextColumn("Planned Dates")
    }
)

# --- Vendor Management Section ---
st.divider()
st.header("Key Vendor & Supplier Management")
st.caption("A list of critical vendors for services and materials, including their status and key notes.")

st.dataframe(
    vendor_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Last Audit Date": st.column_config.DateColumn("Last Audit", format="YYYY-MM-DD")
    }
)

with st.expander("📝 My Role as Manager: Strategic Use of This Data"):
    st.markdown("""
    This dashboard allows me to manage the external-facing aspects of my role with structure and foresight.

    1.  **Planning & Justification:** The travel plan is not just a schedule; it's a justification tool. For the upcoming trip to Germany, I can clearly articulate to my leadership that the purpose is a strategic audit of a key supplier, which is critical for de-risking our supply chain.

    2.  **Resource Allocation:** I can see that David L. recently completed a "person-in-plant" trip. In his next 1-on-1, I will debrief with him to gather insights that can only be obtained by being on the manufacturing floor. This ensures we get maximum value from the travel budget.

    3.  **Risk Management:** The vendor list immediately flags that **GMP Consumables Co.** is a high-risk, sole supplier. This data point is a direct input to our program's risk register and justifies initiating a project to qualify a second supplier, which I can then add to my team's portfolio in the main **Command Center**.

    4.  **Budgeting:** The planned trips and active vendor services are tangible items with real costs. I use this information to build an accurate forecast for the 'Travel' and 'External Testing/Consulting' categories in my **Budget Tracker**, ensuring there are no financial surprises.
    """)
