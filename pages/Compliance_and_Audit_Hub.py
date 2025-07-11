# pages/Compliance_and_Audit_Hub.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

st.set_page_config(
    page_title="Compliance & Audit Hub | Grifols",
    layout="wide"
)

st.title("🛡️ Compliance & Audit Readiness Hub")
st.markdown("### A strategic dashboard for monitoring compliance status and preparing for regulatory and internal audits.")

with st.expander("🌐 My Role as Manager: Ensuring Inspection Readiness", expanded=True):
    st.markdown("""
    As the Senior Manager, I am ultimately accountable for the compliance of our entire validation program. It is my responsibility to **"describe and defend [our] process transfer, development and validation program during audits and inspections."** This dashboard is my primary tool for maintaining a constant state of inspection readiness.

    - **Proactive Risk Identification:** I use this hub to analyze historical audit findings and identify recurring themes or "hot spots." This allows me to proactively strengthen these areas before the next audit.
    - **Documentation Readiness:** It helps me ensure that our most critical validation packages and master documents are current, complete, and readily accessible.
    - **Team Preparation:** This serves as a central point for preparing my team for an audit. We can review our program's strengths and weaknesses and ensure everyone is aligned on our strategies and justifications.
    - **Compliance Oversight:** This provides a high-level view of our compliance posture, ensuring that our activities are consistently performed in accordance with cGMPs, corporate policies, and regulatory requirements.
    """)

# --- Mock Data Generation ---
def generate_audit_findings_data():
    data = {
        'Finding Source': [
            'Data Integrity & ALCOA+', 'Justification of Acceptance Criteria',
            'Investigation & Deviation Handling', 'Training Records & Effectiveness',
            'Validation Master Plan (VMP) Adherence', 'Supplier Qualification',
            'CPV Program Execution'
        ],
        'Count': [8, 5, 4, 3, 2, 2, 1]
    }
    return pd.DataFrame(data).sort_values('Count', ascending=False)

def generate_key_documents_data():
    data = {
        'Document ID': ['VMP-001', 'SOP-VAL-001', 'PV-NAT-FORM-001', 'SOP-CPV-001', 'SOP-TT-001'],
        'Document Title': ['Site Validation Master Plan', 'SOP for Process Validation', 'NAT Reagent Formulation PV Report', 'SOP for Continued Process Verification', 'SOP for Technology Transfer'],
        'Status': ['Current', 'Current', 'Current', 'Current', 'Current'],
        'Last Review': [date(2024, 1, 15), date(2024, 3, 10), date(2023, 11, 20), date(2024, 5, 5), date(2024, 6, 1)]
    }
    return pd.DataFrame(data)

audit_df = generate_audit_findings_data()
docs_df = generate_key_documents_data()


# --- Audit Readiness KPIs ---
st.header("Audit Readiness & Compliance KPIs")
high_risk_findings = audit_df.iloc[0]['Finding Source']
overdue_revalidations = 2 # From Validation Lifecycle dashboard
open_capas = 5 # This would be linked from a CAPA system

col1, col2, col3 = st.columns(3)
col1.metric("Top Historical Finding Area", high_risk_findings)
col2.metric("Overdue Revalidations", overdue_revalidations, delta=f"{overdue_revalidations} to prioritize", delta_color="inverse")
col3.metric("Open Validation-Related CAPAs", open_capas)
st.divider()


# --- Visual Analysis of Audit Hot Spots ---
st.header("Analysis of Historical Audit Findings (Internal & External)")
st.caption("A Pareto analysis of past audit observations to identify systemic weaknesses and focus preparation efforts.")

audit_df['Cumulative %'] = (audit_df['Count'].cumsum() / audit_df['Count'].sum()) * 100
fig_pareto = go.Figure()
fig_pareto.add_trace(go.Bar(
    x=audit_df['Finding Source'], y=audit_df['Count'], name='Finding Count',
    marker_color='#DA291C'
))
fig_pareto.add_trace(go.Scatter(
    x=audit_df['Finding Source'], y=audit_df['Cumulative %'], name='Cumulative %',
    yaxis='y2', line=dict(color='#0033A0')
))
fig_pareto.update_layout(
    title_text="Pareto Chart of Historical Audit Finding Categories",
    height=500,
    yaxis2=dict(title='Cumulative Percentage (%)', overlaying='y', side='right', range=[0, 101])
)
st.plotly_chart(fig_pareto, use_container_width=True)
st.divider()


# --- Key Document Status ---
st.header("Key Audit Document Readiness")
st.caption("A checklist of our most frequently requested master documents and validation packages.")
st.dataframe(docs_df, use_container_width=True, hide_index=True)

with st.container(border=True):
    st.header("Managerial Analysis & Audit Preparation Strategy")
    st.markdown("""
    - **Focus Area Identified:** The **Pareto Chart** provides a powerful, data-driven insight. It clearly shows that **'Data Integrity & ALCOA+'** and **'Justification of Acceptance Criteria'** are our two biggest historical weaknesses, accounting for over 50% of past findings. This tells me exactly where to focus my team's preparation efforts.

    - **Proactive Remediation:** Based on this analysis, I will direct my team to perform a gap assessment of our recent validation packages specifically against current data integrity standards. I will also task a senior engineer to develop a more robust template for justifying acceptance criteria in our validation protocols, directly addressing a known vulnerability.

    - **"Front Room" Preparation:** The Key Documents list serves as my checklist for the audit "front room." I will ensure that the latest, approved versions of these documents are immediately available. For the `NAT Reagent Formulation PV Report`, I will have my project lead, Anna K., prepare a presentation to walk auditors through the study, using the **Validation Project Drilldown** dashboard as a visual aid.

    - **Team Briefing:** In my pre-audit briefing with my team, I will present the Pareto chart. This ensures everyone is aware of our historical "hot spots" and is prepared to speak confidently about how our current procedures and recent improvements have addressed these areas. This is how I "provide leadership" and ensure the team is aligned and ready to "describe and defend" our work.
    """)
