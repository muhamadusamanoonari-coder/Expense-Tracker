import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="QUANTUM | Ledger Terminal",
    page_icon="⚡",
    layout="wide"
)

# --- THE "COBALT NEON" UI ENGINE ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050a18;
        background-image: radial-gradient(circle at 50% 50%, #0a1931 0%, #050a18 100%);
        color: #e0e6ed;
    }
    
    /* Global Text Color Fix */
    p, span, label, .stMarkdown {
        color: #cbd5e0 !important;
    }

    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background: rgba(16, 23, 42, 0.8);
        border: 1px solid #1e293b;
        border-left: 4px solid #38bdf8;
        padding: 1rem;
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 800;
    }

    /* THE LEDGER FIX: Ensuring table text is bright and clear */
    .stTable, [data-testid="stTable"] {
        background-color: #0f172a;
        color: #ffffff !important;
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Targeting the specific data cells for visibility */
    td, th {
        color: #ffffff !important;
        border-bottom: 1px solid #1e293b !important;
        font-family: 'Inter', sans-serif;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        transition: 0.2s all ease-in-out;
    }
    .stButton>button:hover {
        opacity: 0.9;
        box-shadow: 0px 0px 15px rgba(59, 130, 246, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

EXPENSE_FILE = "expenses.txt"

def load_data():
    if os.path.exists(EXPENSE_FILE):
        try:
            # Matches original notebook: amount, category, note
            df = pd.read_csv(EXPENSE_FILE, names=["Amount", "Category", "Note"])
            return df
        except:
            return pd.DataFrame(columns=["Amount", "Category", "Note"])
    return pd.DataFrame(columns=["Amount", "Category", "Note"])

def save_expense(amount, category, note):
    with open(EXPENSE_FILE, "a") as f:
        f.write(f"{amount},{category},{note}\n")

# --- HEADER SECTION ---
st.markdown("<h1 style='color: white; margin-bottom: 0;'>QUANTUM LEDGER</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b;'>VIRTUAL ASSET TRACKING ENGINE // STABLE RELEASE</p>", unsafe_allow_html=True)

df = load_data()

# --- TOP STATS ---
m1, m2, m3 = st.columns(3)
if not df.empty:
    total = df["Amount"].sum()
    m1.metric("TOTAL DEPLOYED", f"${total:,.2f}")
    m2.metric("ENTRY COUNT", f"{len(df)}")
    m3.metric("MAX OUTFLOW", f"${df['Amount'].max():,.2f}")
else:
    m1.metric("TOTAL DEPLOYED", "$0.00")
    m2.metric("ENTRY COUNT", "0")
    m3.metric("MAX OUTFLOW", "$0.00")

st.markdown("---")

# --- INTERACTIVE CONTENT ---
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📝 Record Entry")
    with st.form("input_form"):
        val = st.number_input("Amount", min_value=0.0, format="%.2f")
        cat = st.selectbox("Category", ["Food", "Work", "Transport", "Subscriptions", "Other"])
        note = st.text_input("Transaction Note")
        if st.form_submit_button("SYNC TO CLOUD"):
            if val > 0:
                save_expense(val, cat, note)
                st.rerun()

with col_right:
    st.subheader("📈 Distribution Analytics")
    if not df.empty:
        fig = px.area(df, x=df.index, y="Amount", 
                      line_shape="spline",
                      color_discrete_sequence=["#38bdf8"])
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_visible=False,
            yaxis_gridcolor='#1e293b',
            margin=dict(l=0, r=0, t=10, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Awaiting data input for visualization.")

# --- THE LEDGER SECTION ---
st.markdown("### 📜 System Ledger")
if not df.empty:
    # We use a styled dataframe display which is more readable in Streamlit
    st.dataframe(
        df.sort_index(ascending=False), 
        use_container_width=True,
        hide_index=True
    )
else:
    st.write("Ledger empty.")