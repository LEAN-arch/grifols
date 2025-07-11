# utils.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import date, timedelta

# --- Custom Plotly Template for Grifols ---
grifols_template = {
    "layout": {
        "font": {"family": "Arial, sans-serif", "size": 12, "color": "#333333"},
        "title": {"font": {"family": "Arial, sans-serif", "size": 18, "color": "#DA291C"}, "x": 0.05},
        "plot_bgcolor": "#FFFFFF",
        "paper_bgcolor": "#FFFFFF",
        "colorway": ["#DA291C", "#007A33", "#0033A0", "#FFC72C", "#6C6F70", "#A2AAAD"],
        "xaxis": {"gridcolor": "#EAEAEA", "linecolor": "#B0B0B0", "zerolinecolor": "#EAEAEA", "title_font": {"size": 14}},
        "yaxis": {"gridcolor": "#EAEAEA", "linecolor": "#B0B0B0", "zerolinecolor": "#EAEAEA", "title_font": {"size": 14}},
        "legend": {"bgcolor": "rgba(255,255,255,0.85)", "bordercolor": "#CCCCCC", "borderwidth": 1}
    }
}
pio.templates["grifols"] = grifols_template
pio.templates.default = "grifols"

# === CORE DATA GENERATION (Validation Program Management) ===

def generate_validation_portfolio_data():
    """Generates portfolio data for a manager overseeing various validation projects."""
    data = {
        'Project Name': [
            'Procleix Panther System Reagent Re-validation',
            'New Antigen Test Tech Transfer',
            'DG Gel Card Filling Process Validation',
            'Eluate Buffer Formulation Process Improvement',
            'Q1 2025 Requalification Activities',
            'Automate CPV Data Trending'
        ],
        'Project Type': ['Re-validation', 'Tech Transfer', 'Process Validation', 'Process Improvement', 'Requalification', 'Automation/Efficiency'],
        'Product Line': ['NAT', 'BTS', 'BTS', 'NAT', 'All', 'All'],
        'Project Lead': ['Anna K.', 'David L.', 'Maria S.', 'Anna K.', 'David L.', 'Maria S.'],
        'Status': ['In Progress', 'At Risk', 'Complete - On Time', 'In Progress', 'On Hold', 'Not Started'],
        'Start Date': [date(2024, 7, 1), date(2024, 5, 15), date(2024, 4, 1), date(2024, 8, 1), date(2025, 1, 1), date(2025, 1, 15)],
        'End Date': [date(2024, 11, 30), date(2024, 10, 31), date(2024, 7, 30), date(2024, 12, 15), date(2025, 3, 31), date(2025, 6, 30)],
        'Target Completion': [pd.to_datetime(d) for d in ['2024-11-30', '2024-10-15', '2024-07-30', '2024-12-15', '2025-03-31', '2025-06-30']],
        # NEW: Added effort metric for scenario planning
        'Effort (Person-Months)': [4.0, 5.5, 3.0, 4.5, 3.0, 6.0]
    }
    df = pd.DataFrame(data)
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    return df

def generate_program_risk_data():
    """Generates program-level risks relevant to a validation manager."""
    data = {
        'Risk ID': ['RISK-RES-01', 'RISK-COMP-01', 'RISK-SUP-01', 'RISK-TRANS-01'],
        'Project': ['All', 'Panther Re-validation', 'DG Gel Card PV', 'New Antigen Transfer'],
        'Risk Description': [
            'Key validation SME (Anna K.) has high workload, creating a resource bottleneck.',
            'New FDA guidance on data integrity may require updates to existing validation packages.',
            'Single-source supplier for a critical raw material has quality system issues.',
            'CDMO partner for new antigen test has limited experience with the specific technology.'
        ],
        'Impact': [4, 5, 4, 3], 'Probability': [4, 2, 3, 4],
        'Owner': ['Sr. Manager', 'QA/RA', 'Supply Chain', 'Sr. Manager'],
        'Status': ['Mitigating', 'Evaluating', 'Action Plan Open', 'Mitigating']
    }
    df = pd.DataFrame(data)
    df['Risk Score'] = df['Impact'] * df['Probability']
    return df.sort_values(by='Risk Score', ascending=False)

# === STAFF MANAGEMENT & BUDGET DATA ===

def generate_staff_performance_data():
    """Generates data for managing staff goals and performance."""
    data = {
        'Team Member': ['Anna K.', 'David L.', 'Maria S.', 'New Hire'],
        'Role': ['Principal Engineer', 'Senior Engineer', 'Engineer II', 'Engineer I'],
        'Utilization (%)': [110, 90, 75, 50],
        'Q3 Goals Completed (%)': [100, 85, 95, 100],
        'Required Training Complete (%)': [100, 100, 90, 75],
        'Performance Review Status': ['Complete', 'Scheduled', 'Complete', 'Due'],
        'Development Goal': ['Lead cross-functional OpEx team', 'Mentor new hire on PV', 'Gain expertise in DOE', 'Complete GMP training module']
    }
    return pd.DataFrame(data)

def generate_budget_data():
    """Generates departmental budget data for a manager."""
    data = {
        'Category': ['Salaries & Benefits', 'Capital Equipment', 'Validation Consumables', 'External Testing/Consulting', 'Travel', 'Training & Development'],
        'FY Budget ($K)': [1200, 500, 250, 150, 50, 30],
        'Actuals YTD ($K)': [950, 300, 225, 180, 25, 15],
    }
    df = pd.DataFrame(data)
    df['Variance ($K)'] = df['FY Budget ($K)'] - df['Actuals YTD ($K)']
    df['% Spent'] = (df['Actuals YTD ($K)'] / df['FY Budget ($K)']) * 100
    return df

# === VALIDATION & PROCESS DATA ===

def generate_pv_data():
    """Generates Process Validation data for a reagent formulation process."""
    np.random.seed(1)
    batches = ['PV-Batch-01', 'PV-Batch-02', 'PV-Batch-03']
    data = []
    for batch in batches:
        data.append({'Batch': batch, 'Parameter': 'Mixing Speed (RPM)', 'Value': np.random.normal(505, 5), 'Spec': '450-550 RPM', 'Result': 'PASS'})
        data.append({'Batch': batch, 'Parameter': 'Mixing Time (min)', 'Value': np.random.normal(62, 2), 'Spec': '60±5 min', 'Result': 'PASS'})
        data.append({'Batch': batch, 'Parameter': 'Final pH', 'Value': np.random.normal(7.41, 0.02), 'Spec': '7.40±0.05', 'Result': 'PASS'})
        data.append({'Batch': batch, 'Parameter': 'Final Potency Assay', 'Value': np.random.normal(103, 2), 'Spec': '90-110%', 'Result': 'PASS'})
    # Simulate one failure
    data[7]['Value'] = 88
    data[7]['Result'] = 'FAIL'
    return pd.DataFrame(data)

def generate_cpv_data():
    """Generates data for a Continued Process Verification program."""
    np.random.seed(101)
    n_batches = 30
    df = pd.DataFrame({
        'Batch ID': [f'M24-{1000+i}' for i in range(n_batches)],
        'Final Potency (%)': np.random.normal(102, 1.5, n_batches),
        'Fill Volume (mL)': np.random.normal(10.02, 0.05, n_batches),
    })
    # Introduce a process drift
    df.loc[20:, 'Final Potency (%)'] -= np.linspace(0, 2.5, 10)
    return df

def generate_doe_data():
    """Generates DOE data for a formulation robustness study."""
    np.random.seed(42)
    temp_levels = np.array([-1, 1, -1, 1, 0, 0])
    ph_levels = np.array([-1, -1, 1, 1, 0, 0])
    temp_real = temp_levels * 5 + 25
    ph_real = ph_levels * 0.1 + 7.4
    true_stability = 98 - (2 * ph_levels**2) - (1 * temp_levels**2)
    measured_stability = true_stability + np.random.normal(0, 0.5, len(temp_real))
    return pd.DataFrame({'Temperature (°C)': temp_real, 'pH': ph_real, 'Stability (% Initial)': measured_stability})

# === OPERATIONAL EXCELLENCE DATA ===
def generate_improvement_data():
    """Generates data for tracking process improvement initiatives."""
    data = {
        'Initiative ID': ['PI-24-001', 'PI-24-002', 'PI-24-003', 'PI-24-004'],
        'Initiative Name': ['Standardize Tech Transfer Template', 'Reduce Re-work in Doc Review', '5S Implementation in Validation Lab', 'Automate CPV Data Trending'],
        'Lead': ['Anna K.', 'David L.', 'Maria S.', 'Anna K.'],
        'Improvement Type': ['Standardization', 'Lean', '5S', 'Automation'],
        'Business Driver': ['Reduce Transfer Time', 'Improve Cycle Time', 'Enhance Safety & Compliance', 'Improve Data Integrity'],
        'Status': ['In Progress', 'In Progress', 'Complete', 'Planned'],
        'Progress (%)': [40, 75, 100, 0],
        'Impact': ['High', 'High', 'Medium', 'High'], # High, Medium, Low
        'Effort': ['High', 'Medium', 'Low', 'High'], # High, Medium, Low
        'Budget ($K)': [25, 15, 5, 50],
        'Target Completion': [pd.to_datetime('2024-12-31'), pd.to_datetime('2024-09-30'), pd.to_datetime('2024-06-30'), pd.to_datetime('2025-03-31')]
    }
    return pd.DataFrame(data)


# === REVALIDATION TRACKER DATA ===
def generate_revalidation_data():
    """Generates data for tracking the lifecycle of validated processes."""
    today = date.today()
    data = {
        'Process/System': ['NAT Reagent Formulation', 'BTS Gel Card Filling Line', 'Autoclave AC-101', 'Procleix Panther System'],
        'Validation Package ID': ['PV-NAT-FORM-001', 'PV-BTS-FILL-005', 'PQ-AC101-008', 'PV-PANT-002'],
        'Last Validation Date': [today - timedelta(days=3*365), today - timedelta(days=2*365), today - timedelta(days=300), today - timedelta(days=5*365)],
        'Revalidation Interval (Years)': [3, 2, 1, 5],
        'Status': ['Due', 'OK', 'OK', 'Due'],
        'Risk Score': [9, 7, 5, 8],
        'Complexity': ['High', 'High', 'Low', 'High'],
        'Next Assessment Due': [(pd.to_datetime(d) + pd.DateOffset(years=i)) for d, i in zip(
            [today - timedelta(days=3*365), today - timedelta(days=2*365), today - timedelta(days=300), today - timedelta(days=5*365)],
            [3, 2, 1, 5]
        )]
    }
    return pd.DataFrame(data)
