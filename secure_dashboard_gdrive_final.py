"""
Restaurant Sales Analytics Dashboard - Secure Google Drive Version
Password protected with data loaded from Google Drive
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import hashlib
import requests
from io import BytesIO

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Restaurant Sales Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============== GOOGLE DRIVE FILE IDs ==============
# Google Sheets file IDs (configured and ready)
GDRIVE_FILES = {
    '2025-01': {
        'id': '18iJOJtBo_haJLsZlFVknuap9xN4HLUa0',
        'name': 'January 2025'
    },
    '2025-02': {
        'id': '1t6MOUvRrixczqQZu0T_DwhJyhF5XTtnK',
        'name': 'February 2025'
    },
    '2025-03': {
        'id': '1te1qlRUqA5QSxu6xBcE0S4mWBuoLTzpI',
        'name': 'March 2025'
    },
    '2025-04': {
        'id': '1ElaQO46HeNdWLTw0MTeqJl6ecXrujAg2',
        'name': 'April 2025'
    },
    '2025-05': {
        'id': '1SV8ilwhzRtIpwublxCUQTCuVLeqbwRSi',
        'name': 'May 2025'
    },
    '2025-06': {
        'id': '1goGzbaFuS_A0OnEsT_EBV5AsXTrQxMeN',
        'name': 'June 2025'
    },
    '2025-07': {
        'id': '1we0cbjX2UMsgLHLGzxtnAtGHcJXUlZDY',
        'name': 'July 2025'
    },
    '2025-08': {
        'id': '17XHQw7ZD_dV6-_8wJqHkMvoFgZcv3Mvm',
        'name': 'August 2025'
    }
}

def check_password():
    """Returns True if user entered correct password"""
    
    # Password hash for: !nnow!2014kiosk$
    CORRECT_PASSWORD_HASH = "93e9a50971b9b0735252b9edb6ad4839b3f2d159d957479351957977d5b4ae1f"
    
    def password_entered():
        """Checks whether entered password is correct."""
        if hashlib.sha256(st.session_state["password"].encode()).hexdigest() == CORRECT_PASSWORD_HASH:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["password_correct"] = False

    # First run, show input
    if "password_correct" not in st.session_state:
        st.markdown("## 🔐 Restaurant Sales Analytics Dashboard")
        st.text_input(
            "Please enter password to access the dashboard:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.info("💡 Contact your administrator for access credentials")
        return False
    
    # Password incorrect, show error
    elif not st.session_state["password_correct"]:
        st.markdown("## 🔐 Restaurant Sales Analytics Dashboard")
        st.text_input(
            "Please enter password to access the dashboard:", 
            type="password", 
            on_change=password_entered, 
            key="password"
        )
        st.error("❌ Incorrect password. Please try again.")
        return False
    
    # Password correct
    else:
        return True

# Only show dashboard if password is correct
if not check_password():
    st.stop()

# ============== MAIN DASHBOARD CODE STARTS HERE ==============

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(90deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2E8B57;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🍽️ Restaurant Sales Analytics Dashboard</h1>', unsafe_allow_html=True)

# Add logout button in sidebar
with st.sidebar:
    if st.button("🚪 Logout"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()
    st.markdown("---")

# Function to load data from Google Drive
@st.cache_data(show_spinner=False)
def load_from_gdrive(file_id, month_year, month_name):
    """Load Excel file from Google Sheets"""
    # Export Google Sheets as Excel format
    url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=xlsx"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            df = pd.read_excel(BytesIO(response.content))
            
            # Rename columns for consistency
            column_mapping = {
                'Restaurant Name': 'Restaurant_Name',
                'Amount Collected': 'Amount_Collected',
                'POS Revenue%': 'POS_Revenue_PCT',
                'KIOSK Revenue%': 'KIOSK_Revenue_PCT',
                'ONLINE Revenue%': 'ONLINE_Revenue_PCT'
            }
            
            df = df.rename(columns=column_mapping)
            
            # Add month column
            df['Month_Year'] = month_year
            
            # Clean percentage columns
            for col in ['POS_Revenue_PCT', 'KIOSK_Revenue_PCT', 'ONLINE_Revenue_PCT']:
                if col in df.columns:
                    # Handle percentage values that might be strings with %
                    df[col] = pd.to_numeric(
                        df[col].astype(str).str.replace('%', ''), 
                        errors='coerce'
                    ).fillna(0)
            
            # Calculate revenue amounts
            df['Amount_Collected'] = pd.to_numeric(df['Amount_Collected'], errors='coerce').fillna(0)
            df['POS_Revenue_Amount'] = df['Amount_Collected'] * df['POS_Revenue_PCT'] / 100
            df['KIOSK_Revenue_Amount'] = df['Amount_Collected'] * df['KIOSK_Revenue_PCT'] / 100
            df['ONLINE_Revenue_Amount'] = df['Amount_Collected'] * df['ONLINE_Revenue_PCT'] / 100
            
            return df, None
        else:
            return None, f"Failed to download {month_name} data (Status: {response.status_code})"
    except Exception as e:
        return None, f"Error loading {month_name}: {str(e)}"

# Load all data with progress bar
@st.cache_data(show_spinner=False)
def load_all_data():
    """Load all Excel files from Google Drive"""
    all_data = []
    errors = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, (month_year, file_info) in enumerate(GDRIVE_FILES.items()):
        status_text.text(f"Loading {file_info['name']} data...")
        
        if not file_info['id'].startswith('REPLACE'):  # Only load if ID is set
            df, error = load_from_gdrive(file_info['id'], month_year, file_info['name'])
            if df is not None:
                all_data.append(df)
            elif error:
                errors.append(error)
        else:
            errors.append(f"⚠️ {file_info['name']}: File ID not configured")
        
        progress_bar.progress((idx + 1) / len(GDRIVE_FILES))
    
    progress_bar.empty()
    status_text.empty()
    
    if errors:
        with st.expander("⚠️ Data Loading Issues", expanded=False):
            for error in errors:
                st.warning(error)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame()

# Load data
st.info("📊 Loading data from Google Drive...")
df = load_all_data()

if df.empty:
    st.error("""
    ❌ No data could be loaded. Please ensure:
    1. Google Drive file IDs are correctly set in the code
    2. Files are shared with 'Anyone with the link can view'
    3. Your internet connection is stable
    """)
    st.stop()

# Success message
st.success(f"✅ Loaded {len(df):,} records from {df['Month_Year'].nunique()} months")

# Sidebar for filtering
with st.sidebar:
    st.header("📊 Dashboard Controls")
    
    # Data Overview
    st.metric("Total Records", f"{len(df):,}")
    st.metric("Unique Restaurants", f"{df['Restaurant_Name'].nunique():,}")
    
    st.markdown("---")
    
    # Period Selection
    st.subheader("📅 Time Period")
    available_months = sorted(df['Month_Year'].unique())
    
    period_type = st.radio(
        "Select Period",
        ["All Time", "Last 6 Months", "Last 3 Months", "Last Month", "Custom Range"]
    )
    
    if period_type == "Custom Range":
        selected_months = st.multiselect(
            "Select Months",
            available_months,
            default=available_months[-3:] if len(available_months) >= 3 else available_months
        )
    elif period_type == "All Time":
        selected_months = available_months
    elif period_type == "Last 6 Months":
        selected_months = available_months[-6:] if len(available_months) >= 6 else available_months
    elif period_type == "Last 3 Months":
        selected_months = available_months[-3:] if len(available_months) >= 3 else available_months
    else:  # Last Month
        selected_months = [available_months[-1]] if available_months else []
    
    # Restaurant filter
    st.markdown("---")
    st.subheader("🏪 Restaurant Filter")
    filter_restaurants = st.checkbox("Filter Specific Restaurants")
    
    if filter_restaurants:
        selected_restaurants = st.multiselect(
            "Select Restaurants",
            sorted(df['Restaurant_Name'].unique()),
            default=[]
        )
    else:
        selected_restaurants = df['Restaurant_Name'].unique()

# Filter data
filtered_df = df[
    (df['Month_Year'].isin(selected_months)) & 
    (df['Restaurant_Name'].isin(selected_restaurants))
]

if filtered_df.empty:
    st.warning("No data available for selected filters")
    st.stop()

# Display KPIs
st.markdown("## 📊 Key Performance Indicators")
time_period_text = f" ({selected_months[0]} to {selected_months[-1]})" if len(selected_months) > 1 else f" ({selected_months[0]})" if selected_months else ""

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = filtered_df['Amount_Collected'].sum()
    st.metric(
        f"Total Revenue{time_period_text}", 
        f"${total_revenue/1_000_000:.2f}M" if total_revenue >= 1_000_000 else f"${total_revenue:,.0f}"
    )

with col2:
    unique_restaurants = filtered_df['Restaurant_Name'].nunique()
    st.metric("Active Restaurants", f"{unique_restaurants:,}")

with col3:
    avg_revenue = filtered_df.groupby('Restaurant_Name')['Amount_Collected'].sum().mean()
    st.metric(
        "Avg Revenue/Restaurant",
        f"${avg_revenue:,.0f}"
    )

with col4:
    pos_revenue = filtered_df['POS_Revenue_Amount'].sum()
    st.metric(
        "POS Revenue",
        f"${pos_revenue/1_000_000:.2f}M" if pos_revenue >= 1_000_000 else f"${pos_revenue:,.0f}"
    )

with col5:
    online_revenue = filtered_df['ONLINE_Revenue_Amount'].sum()
    st.metric(
        "Online Revenue",
        f"${online_revenue/1_000_000:.2f}M" if online_revenue >= 1_000_000 else f"${online_revenue:,.0f}"
    )

# Add visualization tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Revenue Trends", "🏆 Top Performers", "📊 Channel Analysis", "📥 Data Export"])

with tab1:
    # Monthly revenue trend
    monthly_revenue = filtered_df.groupby('Month_Year')['Amount_Collected'].sum().reset_index()
    monthly_revenue = monthly_revenue.sort_values('Month_Year')
    
    fig_trend = px.line(
        monthly_revenue,
        x='Month_Year',
        y='Amount_Collected',
        title='Monthly Revenue Trend',
        markers=True
    )
    fig_trend.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    # Top 20 restaurants
    top_restaurants = (
        filtered_df.groupby('Restaurant_Name')['Amount_Collected']
        .sum()
        .sort_values(ascending=False)
        .head(20)
    )
    
    fig_top = px.bar(
        x=top_restaurants.values,
        y=top_restaurants.index,
        orientation='h',
        title='Top 20 Restaurants by Revenue',
        labels={'x': 'Revenue ($)', 'y': 'Restaurant'}
    )
    fig_top.update_layout(height=600)
    st.plotly_chart(fig_top, use_container_width=True)

with tab3:
    # Channel distribution
    col1, col2 = st.columns(2)
    
    with col1:
        channel_totals = {
            'POS': filtered_df['POS_Revenue_Amount'].sum(),
            'Kiosk': filtered_df['KIOSK_Revenue_Amount'].sum(),
            'Online': filtered_df['ONLINE_Revenue_Amount'].sum()
        }
        
        fig_pie = px.pie(
            values=list(channel_totals.values()),
            names=list(channel_totals.keys()),
            title='Revenue by Channel'
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Channel trends over time
        channel_trends = filtered_df.groupby('Month_Year').agg({
            'POS_Revenue_Amount': 'sum',
            'KIOSK_Revenue_Amount': 'sum',
            'ONLINE_Revenue_Amount': 'sum'
        }).reset_index()
        channel_trends = channel_trends.sort_values('Month_Year')
        
        fig_channel_trend = go.Figure()
        fig_channel_trend.add_trace(go.Scatter(
            x=channel_trends['Month_Year'],
            y=channel_trends['POS_Revenue_Amount'],
            name='POS',
            mode='lines+markers'
        ))
        fig_channel_trend.add_trace(go.Scatter(
            x=channel_trends['Month_Year'],
            y=channel_trends['KIOSK_Revenue_Amount'],
            name='Kiosk',
            mode='lines+markers'
        ))
        fig_channel_trend.add_trace(go.Scatter(
            x=channel_trends['Month_Year'],
            y=channel_trends['ONLINE_Revenue_Amount'],
            name='Online',
            mode='lines+markers'
        ))
        
        fig_channel_trend.update_layout(
            title='Channel Revenue Trends',
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_channel_trend, use_container_width=True)

with tab4:
    st.markdown("### 📥 Export Data")
    
    # Prepare export data
    export_df = filtered_df[[
        'Restaurant_Name', 'Amount_Collected', 
        'POS_Revenue_PCT', 'KIOSK_Revenue_PCT', 'ONLINE_Revenue_PCT',
        'Month_Year'
    ]]
    
    # Convert to CSV
    csv = export_df.to_csv(index=False)
    
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"restaurant_sales_export_{selected_months[0]}_to_{selected_months[-1]}.csv",
        mime="text/csv"
    )
    
    st.info(f"Export contains {len(export_df):,} records from {export_df['Month_Year'].nunique()} months")

# Footer
st.markdown("---")
st.markdown("*🔒 Secure Dashboard - Data loaded from Google Drive*")