"""
Restaurant Sales Analytics Dashboard - Complete Secure Google Drive Version
Version: 2.0.0 - Full Feature Set with Google Sheets Integration
Password protected with all advanced features from the original dashboard
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
from datetime import datetime
from scipy import stats

warnings.filterwarnings('ignore')

# Version Information
__version__ = "2.0.0"
__release_date__ = "2025-09-03"

# Page configuration
st.set_page_config(
    page_title="Restaurant Sales Analytics Dashboard",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="collapsed"
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
    
    # Password hash (SHA-256)
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
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    [data-testid="metric-container"] {
        width: 100%;
        min-height: 120px;
    }
    [data-testid="metric-container"] > div {
        width: 100%;
        white-space: nowrap;
        overflow: visible;
    }
    /* Hide sidebar toggle button */
    [data-testid="collapsedControl"] {
        display: none;
    }
    /* Style logout button */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
    }
    div[data-testid="column"]:nth-child(2) button:hover {
        background-color: #ff3333;
        color: white;
    }
    [data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 1rem !important;
        line-height: 1.2 !important;
        word-wrap: break-word !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        max-width: none !important;
    }
    [data-testid="metric-container"] [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        white-space: normal;
        word-wrap: break-word;
    }
    h1 {
        color: #1f77b4;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
# Header with logout button
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🍽️ Restaurant Sales Analytics Dashboard")
    st.markdown("### Comprehensive analysis of restaurant performance across multiple revenue channels")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)  # Add some spacing
    if st.button("🚪 Logout", key="logout_btn"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

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
            df['Month'] = month_name
            
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
            
            # Add revenue tier categorization
            df['Revenue_Tier'] = df['Amount_Collected'].apply(categorize_revenue_tier)
            
            return df, None
        else:
            return None, f"Failed to download {month_name} data (Status: {response.status_code})"
    except Exception as e:
        return None, f"Error loading {month_name}: {str(e)}"

def categorize_revenue_tier(amount):
    """Categorize amount into revenue tiers"""
    if pd.isna(amount) or amount <= 0:
        return 'Zero'
    elif amount <= 1000:
        return '1K'
    elif amount <= 10000:
        return '10K'
    elif amount <= 20000:
        return '20K'
    elif amount <= 50000:
        return '50K'
    elif amount <= 100000:
        return '100K'
    else:
        return '100K+'

# Period Selection
st.markdown("#### 📅 Select Analysis Period")
col1, col2, col3 = st.columns([2, 2, 6])

with col1:
    period_option = st.selectbox(
        "Analysis Period",
        ["All Months", "Last 6 Months", "Last 3 Months", "Last 2 Months", "Single Month", "Custom Range"],
        index=0,
        help="Choose which months to include in the analysis"
    )

with col2:
    if period_option == "Single Month":
        month_options = list(GDRIVE_FILES.keys())
        selected_month_key = st.selectbox(
            "Select Month",
            month_options,
            index=len(month_options)-1,  # Default to latest
            format_func=lambda x: GDRIVE_FILES[x]['name']
        )
    elif period_option == "Custom Range":
        available_months = [GDRIVE_FILES[key]['name'] for key in GDRIVE_FILES.keys()]
        selected_months_range = st.multiselect(
            "Select Months",
            available_months,
            default=available_months[-3:]  # Default to last 3 months
        )
    else:
        selected_month_key = None
        selected_months_range = None

with col3:
    # Display selected period info
    if period_option == "All Months":
        st.info("📊 Analyzing: All 8 months (January to August 2025)")
    elif period_option == "Last 6 Months":
        st.info("📊 Analyzing: Last 6 months (March to August 2025)")
    elif period_option == "Last 3 Months":
        st.info("📊 Analyzing: Last 3 months (June to August 2025)")
    elif period_option == "Last 2 Months":
        st.info("📊 Analyzing: Last 2 months (July to August 2025)")
    elif period_option == "Custom Range":
        if selected_months_range:
            st.info(f"📊 Analyzing: {', '.join(selected_months_range)}")
        else:
            st.warning("Please select months to analyze")
    else:
        st.info(f"📊 Analyzing: {GDRIVE_FILES[selected_month_key]['name']} only")

st.markdown("---")

# Load all data with progress bar
@st.cache_data(show_spinner=False)
def load_all_data(period_selection, selected_key=None, selected_range=None):
    """Load Excel files from Google Drive based on period selection"""
    all_data = []
    errors = []
    
    # Determine which files to load
    if period_selection == "All Months":
        files_to_load = list(GDRIVE_FILES.keys())
    elif period_selection == "Last 6 Months":
        files_to_load = list(GDRIVE_FILES.keys())[-6:]
    elif period_selection == "Last 3 Months":
        files_to_load = list(GDRIVE_FILES.keys())[-3:]
    elif period_selection == "Last 2 Months":
        files_to_load = list(GDRIVE_FILES.keys())[-2:]
    elif period_selection == "Single Month":
        files_to_load = [selected_key] if selected_key else []
    elif period_selection == "Custom Range":
        if selected_range:
            files_to_load = []
            for key, info in GDRIVE_FILES.items():
                if info['name'] in selected_range:
                    files_to_load.append(key)
        else:
            files_to_load = []
    else:
        files_to_load = []
    
    if not files_to_load:
        return pd.DataFrame(), ["No files selected for loading"]
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, file_key in enumerate(files_to_load):
        file_info = GDRIVE_FILES[file_key]
        status_text.text(f"Loading {file_info['name']} data...")
        
        df, error = load_from_gdrive(file_info['id'], file_key, file_info['name'])
        if df is not None:
            df['Source_File'] = f"{file_info['name']}.xlsx"  # Add source file tracking
            all_data.append(df)
        elif error:
            errors.append(error)
        
        progress_bar.progress((idx + 1) / len(files_to_load))
    
    progress_bar.empty()
    status_text.empty()
    
    if errors:
        with st.expander("⚠️ Data Loading Issues", expanded=False):
            for error in errors:
                st.warning(error)
    
    if all_data:
        return pd.concat(all_data, ignore_index=True), errors
    else:
        return pd.DataFrame(), errors

# Load data
st.info("📊 Loading data from Google Sheets...")
df, load_errors = load_all_data(
    period_option, 
    selected_month_key if period_option == "Single Month" else None,
    selected_months_range if period_option == "Custom Range" else None
)

if df.empty:
    st.error("""
    ❌ No data could be loaded. Please ensure:
    1. Google Drive file IDs are correctly set in the code
    2. Files are shared with 'Anyone with the link can view'
    3. Your internet connection is stable
    """)
    st.stop()

# Success message
st.success(f"✅ Loaded {len(df):,} records from {df['Month'].nunique()} months")

# Data Summary
if 'Month' in df.columns:
    months_included = sorted(df['Month'].unique())
    data_summary = f"**Current Analysis**: {', '.join(months_included)} | **Total Records**: {len(df):,} | **Unique Restaurants**: {df['Restaurant_Name'].nunique():,}"
    st.markdown(f"<div style='background-color: #e8f4f8; padding: 10px; border-radius: 5px; margin-bottom: 20px;'>{data_summary}</div>", unsafe_allow_html=True)

# Month-over-Month Analysis Functions
def calculate_mom_metrics(df):
    """Calculate month-over-month metrics for all restaurants"""
    if 'Month' not in df.columns or df['Month'].nunique() < 2:
        return None
    
    # Create pivot table with months as columns
    pivot_df = df.pivot_table(
        values='Amount_Collected',
        index='Restaurant_Name',
        columns='Month',
        aggfunc='sum',
        fill_value=0
    )
    
    # Sort columns chronologically
    month_order = ['January 2025', 'February 2025', 'March 2025', 'April 2025', 
                   'May 2025', 'June 2025', 'July 2025', 'August 2025']
    available_months = [m for m in month_order if m in pivot_df.columns]
    pivot_df = pivot_df[available_months]
    
    # Calculate MoM changes
    mom_changes = {}
    for i in range(1, len(available_months)):
        prev_month = available_months[i-1]
        curr_month = available_months[i]
        
        # Calculate absolute and percentage changes
        absolute_change = pivot_df[curr_month] - pivot_df[prev_month]
        
        # Avoid division by zero
        percentage_change = np.where(
            pivot_df[prev_month] != 0,
            (absolute_change / pivot_df[prev_month]) * 100,
            np.where(pivot_df[curr_month] > 0, 100, 0)
        )
        
        mom_changes[f"{prev_month} to {curr_month}"] = {
            'absolute': absolute_change,
            'percentage': percentage_change,
            'prev_month': pivot_df[prev_month],
            'curr_month': pivot_df[curr_month]
        }
    
    return pivot_df, mom_changes

def categorize_restaurant_performance(pivot_df, mom_changes):
    """Categorize restaurants based on performance trends"""
    if not mom_changes:
        return {}
    
    categories = {
        'Rising Stars': [],
        'Declining': [],
        'Stable Performers': [],
        'New Entrants': [],
        'Churned': [],
        'Volatile': []
    }
    
    # Get the most recent month comparison
    latest_comparison = list(mom_changes.keys())[-1]
    latest_data = mom_changes[latest_comparison]
    
    # Convert Series to dict for easier access
    prev_month_dict = latest_data['prev_month'].to_dict() if hasattr(latest_data['prev_month'], 'to_dict') else dict(latest_data['prev_month'])
    curr_month_dict = latest_data['curr_month'].to_dict() if hasattr(latest_data['curr_month'], 'to_dict') else dict(latest_data['curr_month'])
    
    # Handle percentage data properly
    if hasattr(latest_data['percentage'], 'to_dict'):
        percentage_dict = latest_data['percentage'].to_dict()
    else:
        percentage_dict = dict(zip(pivot_df.index, latest_data['percentage']))
    
    for restaurant in pivot_df.index:
        prev_val = prev_month_dict.get(restaurant, 0)
        curr_val = curr_month_dict.get(restaurant, 0)
        pct_change = percentage_dict.get(restaurant, 0)
        
        # Categorize based on performance
        if prev_val == 0 and curr_val > 0:
            categories['New Entrants'].append(restaurant)
        elif prev_val > 0 and curr_val == 0:
            categories['Churned'].append(restaurant)
        elif pct_change > 20:
            categories['Rising Stars'].append(restaurant)
        elif pct_change < -20:
            categories['Declining'].append(restaurant)
        elif abs(pct_change) <= 10:
            categories['Stable Performers'].append(restaurant)
        else:
            # Check volatility across all months
            restaurant_values = pivot_df.loc[restaurant].values
            cv = np.std(restaurant_values) / np.mean(restaurant_values) if np.mean(restaurant_values) > 0 else 0
            if cv > 0.5:
                categories['Volatile'].append(restaurant)
            else:
                categories['Stable Performers'].append(restaurant)
    
    return categories

def generate_insights(df, mom_changes, categories):
    """Generate AI insights based on data analysis"""
    insights = []
    
    if not mom_changes:
        return ["Insufficient data for month-over-month analysis. Need at least 2 months of data."]
    
    # Get latest comparison
    latest_comparison = list(mom_changes.keys())[-1]
    latest_data = mom_changes[latest_comparison]
    
    # Overall revenue trend
    total_prev = latest_data['prev_month'].sum()
    total_curr = latest_data['curr_month'].sum()
    total_change_pct = ((total_curr - total_prev) / total_prev * 100) if total_prev > 0 else 0
    
    if total_change_pct > 0:
        insights.append(f"📈 Total revenue increased by {total_change_pct:.1f}% in {latest_comparison.split(' to ')[1]}")
    else:
        insights.append(f"📉 Total revenue decreased by {abs(total_change_pct):.1f}% in {latest_comparison.split(' to ')[1]}")
    
    # Category insights
    if categories['Rising Stars']:
        insights.append(f"🌟 {len(categories['Rising Stars'])} restaurants showing strong growth (>20%)")
    
    if categories['Declining']:
        insights.append(f"⚠️ {len(categories['Declining'])} restaurants need attention (>20% decline)")
    
    if categories['New Entrants']:
        insights.append(f"🆕 {len(categories['New Entrants'])} new restaurants started generating revenue")
    
    if categories['Churned']:
        insights.append(f"🔴 {len(categories['Churned'])} restaurants stopped generating revenue")
    
    # Channel insights if available
    if 'ONLINE_Revenue_Amount' in df.columns:
        online_growth = df.groupby('Month')['ONLINE_Revenue_Amount'].sum()
        if len(online_growth) > 1:
            online_change = (online_growth.iloc[-1] - online_growth.iloc[-2]) / online_growth.iloc[-2] * 100 if online_growth.iloc[-2] > 0 else 0
            if online_change > 10:
                insights.append(f"💻 Online channel growing rapidly at {online_change:.1f}%")
    
    # Top performer
    if hasattr(latest_data['absolute'], 'max') and latest_data['absolute'].max() > 0:
        top_gainer_idx = latest_data['absolute'].idxmax()
        top_gain = latest_data['absolute'].max()
        insights.append(f"🏆 {top_gainer_idx} had the highest growth: +${top_gain:,.0f}")
    
    # Biggest decline  
    if hasattr(latest_data['absolute'], 'min') and latest_data['absolute'].min() < 0:
        top_decliner_idx = latest_data['absolute'].idxmin()
        top_decline = abs(latest_data['absolute'].min())
        insights.append(f"📊 {top_decliner_idx} had the largest decline: -${top_decline:,.0f}")
    
    return insights

# Search Bar and AI Insights Section
st.markdown("## 🔍 Search & Insights")

search_col1, search_col2 = st.columns([2, 3])

with search_col1:
    # Restaurant search
    search_term = st.text_input(
        "🔍 Search Restaurants",
        placeholder="Type restaurant name...",
        help="Search for specific restaurants by name"
    )
    
    if search_term:
        # Filter dataframe based on search
        filtered_restaurants = df[df['Restaurant_Name'].str.contains(search_term, case=False, na=False)]['Restaurant_Name'].unique()
        st.info(f"Found {len(filtered_restaurants)} restaurants matching '{search_term}'")
        
        # Apply filter to main dataframe
        df_filtered = df[df['Restaurant_Name'].isin(filtered_restaurants)]
    else:
        df_filtered = df.copy()

with search_col2:
    # AI Insights
    st.markdown("### 🤖 AI-Generated Insights")
    
    # Calculate insights if multiple months available
    if 'Month' in df.columns and df['Month'].nunique() > 1:
        mom_result = calculate_mom_metrics(df)
        if mom_result:
            pivot_df, mom_changes = mom_result
            categories = categorize_restaurant_performance(pivot_df, mom_changes)
            insights = generate_insights(df, mom_changes, categories)
            
            # Get latest comparison data for detailed views
            latest_comparison = list(mom_changes.keys())[-1]
            comparison_data = mom_changes[latest_comparison]
            prev_month, curr_month = latest_comparison.split(' to ')
            
            # Display insights in expandable format
            with st.expander("View Key Insights", expanded=True):
                for insight in insights[:5]:  # Show top 5 insights
                    st.markdown(f"• {insight}")
            
            # Interactive detailed insights
            st.markdown("#### 🔍 Detailed Restaurant Lists")
            
            insight_tabs = st.tabs(["🌟 Rising Stars", "⚠️ Declining", "🆕 New Entrants", "🔴 Churned"])
            
            with insight_tabs[0]:  # Rising Stars
                if categories['Rising Stars']:
                    st.markdown(f"**{len(categories['Rising Stars'])} restaurants showing >20% growth:**")
                    
                    # Create detailed dataframe for rising stars
                    pct_dict = dict(zip(pivot_df.index, comparison_data['percentage']))
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    prev_dict = comparison_data['prev_month'].to_dict() if hasattr(comparison_data['prev_month'], 'to_dict') else dict(comparison_data['prev_month'])
                    abs_dict = dict(zip(pivot_df.index, comparison_data['absolute']))
                    
                    rising_data = []
                    for restaurant in categories['Rising Stars']:
                        rising_data.append({
                            'Restaurant': restaurant,
                            f'{prev_month} Revenue': prev_dict.get(restaurant, 0),
                            f'{curr_month} Revenue': curr_dict.get(restaurant, 0),
                            'Growth %': pct_dict.get(restaurant, 0),
                            'Growth $': abs_dict.get(restaurant, 0)
                        })
                    
                    rising_df = pd.DataFrame(rising_data).sort_values('Growth $', ascending=False)
                    
                    st.dataframe(
                        rising_df.style.format({
                            f'{prev_month} Revenue': '${:,.0f}',
                            f'{curr_month} Revenue': '${:,.0f}',
                            'Growth %': '{:+.1f}%',
                            'Growth $': '${:+,.0f}'
                        }).background_gradient(subset=['Growth %'], cmap='Greens'),
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.info("No rising star restaurants in this period")
            
            with insight_tabs[1]:  # Declining
                if categories['Declining']:
                    st.markdown(f"**{len(categories['Declining'])} restaurants showing >20% decline:**")
                    
                    # Create detailed dataframe for declining restaurants
                    pct_dict = dict(zip(pivot_df.index, comparison_data['percentage']))
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    prev_dict = comparison_data['prev_month'].to_dict() if hasattr(comparison_data['prev_month'], 'to_dict') else dict(comparison_data['prev_month'])
                    abs_dict = dict(zip(pivot_df.index, comparison_data['absolute']))
                    
                    declining_data = []
                    for restaurant in categories['Declining']:
                        declining_data.append({
                            'Restaurant': restaurant,
                            f'{prev_month} Revenue': prev_dict.get(restaurant, 0),
                            f'{curr_month} Revenue': curr_dict.get(restaurant, 0),
                            'Decline %': pct_dict.get(restaurant, 0),
                            'Decline $': abs_dict.get(restaurant, 0)
                        })
                    
                    declining_df = pd.DataFrame(declining_data).sort_values('Decline $', ascending=True)
                    
                    st.dataframe(
                        declining_df.style.format({
                            f'{prev_month} Revenue': '${:,.0f}',
                            f'{curr_month} Revenue': '${:,.0f}',
                            'Decline %': '{:+.1f}%',
                            'Decline $': '${:+,.0f}'
                        }).background_gradient(subset=['Decline %'], cmap='Reds_r'),
                        use_container_width=True,
                        height=300
                    )
                    
                    # Alert for biggest decliners
                    biggest_decliners = declining_df.head(3)
                    st.error(f"⚠️ **Urgent Attention Needed:**")
                    for _, row in biggest_decliners.iterrows():
                        st.markdown(f"• **{row['Restaurant']}**: {row['Decline %']:+.1f}% (${row['Decline $']:+,.0f})")
                else:
                    st.success("No declining restaurants in this period")
            
            with insight_tabs[2]:  # New Entrants
                if categories['New Entrants']:
                    st.markdown(f"**{len(categories['New Entrants'])} new restaurants started generating revenue:**")
                    
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    
                    new_data = []
                    for restaurant in categories['New Entrants']:
                        new_data.append({
                            'Restaurant': restaurant,
                            f'{curr_month} Revenue': curr_dict.get(restaurant, 0)
                        })
                    
                    new_df = pd.DataFrame(new_data).sort_values(f'{curr_month} Revenue', ascending=False)
                    
                    st.dataframe(
                        new_df.style.format({
                            f'{curr_month} Revenue': '${:,.0f}'
                        }).background_gradient(subset=[f'{curr_month} Revenue'], cmap='Blues'),
                        use_container_width=True,
                        height=200
                    )
                    
                    # Highlight top new performers
                    if len(new_df) > 0:
                        top_new = new_df.iloc[0]
                        st.success(f"🏆 **Top New Performer**: {top_new['Restaurant']} - ${top_new[f'{curr_month} Revenue']:,.0f}")
                else:
                    st.info("No new restaurants started generating revenue")
            
            with insight_tabs[3]:  # Churned
                if categories['Churned']:
                    st.markdown(f"**{len(categories['Churned'])} restaurants stopped generating revenue:**")
                    
                    prev_dict = comparison_data['prev_month'].to_dict() if hasattr(comparison_data['prev_month'], 'to_dict') else dict(comparison_data['prev_month'])
                    
                    churned_data = []
                    for restaurant in categories['Churned']:
                        churned_data.append({
                            'Restaurant': restaurant,
                            f'{prev_month} Revenue (Lost)': prev_dict.get(restaurant, 0)
                        })
                    
                    churned_df = pd.DataFrame(churned_data).sort_values(f'{prev_month} Revenue (Lost)', ascending=False)
                    
                    st.dataframe(
                        churned_df.style.format({
                            f'{prev_month} Revenue (Lost)': '${:,.0f}'
                        }).background_gradient(subset=[f'{prev_month} Revenue (Lost)'], cmap='Reds'),
                        use_container_width=True,
                        height=200
                    )
                    
                    # Calculate total lost revenue
                    total_lost = churned_df[f'{prev_month} Revenue (Lost)'].sum()
                    st.warning(f"💰 **Total Revenue Lost**: ${total_lost:,.0f}")
                else:
                    st.success("No restaurants churned in this period")
        else:
            st.info("Add more months of data to see month-over-month insights")
    else:
        st.info("Month-over-month insights require multiple months of data")

st.markdown("---")

# Use filtered dataframe for rest of dashboard
df = df_filtered

# Determine time period text based on selection
if period_option == "All Months":
    period_text = "January 2025 to August 2025"
elif period_option == "Last 6 Months":
    period_text = "March 2025 to August 2025"
elif period_option == "Last 3 Months":
    period_text = "June 2025 to August 2025"
elif period_option == "Last 2 Months":
    period_text = "July 2025 to August 2025"
elif period_option == "Single Month":
    period_text = f"{GDRIVE_FILES[selected_month_key]['name']}"
else:  # Custom Range
    if selected_months_range and len(selected_months_range) > 0:
        if len(selected_months_range) == 1:
            period_text = selected_months_range[0]
        else:
            sorted_months = sorted(selected_months_range)
            period_text = f"{sorted_months[0]} to {sorted_months[-1]}"
    else:
        period_text = "Custom Range"

# Key Metrics Row
st.markdown(f"## 📊 Key Performance Indicators ({period_text})")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    total_revenue = df['Amount_Collected'].sum() if 'Amount_Collected' in df.columns else 0
    # Format large numbers with K/M suffixes if needed, or show full number
    if total_revenue >= 1_000_000:
        display_revenue = f"${total_revenue/1_000_000:.2f}M"
    else:
        display_revenue = f"${total_revenue:,.0f}"
    st.metric("Total Revenue", display_revenue)

with col2:
    num_restaurants = df['Restaurant_Name'].nunique() if 'Restaurant_Name' in df.columns else 0
    st.metric("Total Restaurants", f"{num_restaurants:,}")

with col3:
    avg_revenue = df['Amount_Collected'].mean() if 'Amount_Collected' in df.columns else 0
    st.metric("Avg Revenue/Restaurant", f"${avg_revenue:,.0f}")

with col4:
    pos_revenue = df['POS_Revenue_Amount'].sum() if 'POS_Revenue_Amount' in df.columns else 0
    if pos_revenue >= 1_000_000:
        pos_display = f"${pos_revenue/1_000_000:.2f}M"
    else:
        pos_display = f"${pos_revenue:,.0f}"
    st.metric("POS Revenue", pos_display)

with col5:
    online_revenue = df['ONLINE_Revenue_Amount'].sum() if 'ONLINE_Revenue_Amount' in df.columns else 0
    if online_revenue >= 1_000_000:
        online_display = f"${online_revenue/1_000_000:.2f}M"
    else:
        online_display = f"${online_revenue:,.0f}"
    st.metric("Online Revenue", online_display)

st.markdown("---")

# Create tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Revenue Overview", 
    "🏪 Restaurant Analysis", 
    "📱 Channel Performance",
    "📊 Revenue Tiers",
    "📉 Trends & Insights",
    "🌐 Online Ordering Analysis",
    "📊 Month-over-Month Analysis"
])

with tab1:
    st.header("Revenue Overview")
    
    # Summary metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        # Count unique restaurants with revenue > 0
        if 'Amount_Collected' in df.columns and 'Restaurant_Name' in df.columns:
            active_df = df[df['Amount_Collected'] > 0]
            total_active = active_df['Restaurant_Name'].nunique()
        else:
            total_active = 0
        st.metric("Active Restaurants", f"{total_active:,}")
    with col2:
        if 'Amount_Collected' in df.columns:
            top_10_pct = df.nlargest(int(len(df)*0.1), 'Amount_Collected')['Amount_Collected'].sum() / df['Amount_Collected'].sum() * 100
            st.metric("Top 10% Revenue Share", f"{top_10_pct:.1f}%")
    with col3:
        if 'Source_File' in df.columns:
            st.metric("Data Sources", df['Source_File'].nunique())
    with col4:
        zero_revenue = len(df[df['Amount_Collected'] <= 1]) if 'Amount_Collected' in df.columns else 0
        st.metric("Zero Revenue", f"{zero_revenue:,}")
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue distribution by tier
        if 'Revenue_Tier' in df.columns:
            tier_summary = df.groupby('Revenue_Tier')['Amount_Collected'].agg(['count', 'sum']).reset_index()
            tier_summary.columns = ['Revenue Tier', 'Count', 'Total Revenue']
            tier_summary = tier_summary.sort_values('Total Revenue', ascending=False)
            
            fig_tier = px.pie(
                tier_summary, 
                values='Total Revenue', 
                names='Revenue Tier',
                title='Revenue Distribution by Tier',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig_tier.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
            )
            st.plotly_chart(fig_tier, use_container_width=True)
            
            # Tier breakdown table
            st.subheader("Tier Breakdown")
            tier_summary['Avg Revenue'] = tier_summary['Total Revenue'] / tier_summary['Count']
            tier_summary = tier_summary.sort_values('Total Revenue', ascending=False)
            st.dataframe(
                tier_summary.style.format({
                    'Total Revenue': '${:,.0f}',
                    'Avg Revenue': '${:,.0f}',
                    'Count': '{:,.0f}'
                }),
                use_container_width=True,
                hide_index=True
            )
    
    with col2:
        # Top 10 restaurants by revenue
        if 'Restaurant_Name' in df.columns and 'Amount_Collected' in df.columns:
            top_restaurants = df.groupby('Restaurant_Name')['Amount_Collected'].sum().sort_values(ascending=False).head(10)
            
            fig_top = px.bar(
                x=top_restaurants.values,
                y=top_restaurants.index,
                orientation='h',
                title='Top 10 Restaurants by Revenue',
                labels={'x': 'Revenue ($)', 'y': 'Restaurant'},
                color=top_restaurants.values,
                color_continuous_scale='Viridis',
                text=[f'${x:,.0f}' for x in top_restaurants.values]
            )
            fig_top.update_traces(textposition='auto', textfont_size=12)
            fig_top.update_layout(
                showlegend=False,
                margin=dict(r=100),  # Add right margin for text
                xaxis=dict(
                    tickformat='$,.0f',
                    title='Revenue ($)'
                )
            )
            st.plotly_chart(fig_top, use_container_width=True)
            
            # Bottom 10 restaurants (non-zero)
            bottom_restaurants = df[df['Amount_Collected'] > 0].groupby('Restaurant_Name')['Amount_Collected'].sum().sort_values().head(10)
            if len(bottom_restaurants) > 0:
                fig_bottom = px.bar(
                    x=bottom_restaurants.values,
                    y=bottom_restaurants.index,
                    orientation='h',
                    title='Bottom 10 Restaurants by Revenue (Non-Zero)',
                    labels={'x': 'Revenue ($)', 'y': 'Restaurant'},
                    color=bottom_restaurants.values,
                    color_continuous_scale='Reds',
                    text=[f'${x:,.0f}' for x in bottom_restaurants.values]
                )
                fig_bottom.update_traces(textposition='auto', textfont_size=12)
                fig_bottom.update_layout(
                    showlegend=False,
                    margin=dict(r=100),  # Add right margin for text
                    xaxis=dict(
                        tickformat='$,.0f',
                        title='Revenue ($)'
                    )
                )
                st.plotly_chart(fig_bottom, use_container_width=True)

with tab2:
    st.header("Restaurant Performance Analysis")
    
    # Restaurant filter
    if 'Restaurant_Name' in df.columns:
        selected_restaurants = st.multiselect(
            "Select Restaurants to Analyze",
            options=df['Restaurant_Name'].unique(),
            default=df['Restaurant_Name'].unique()[:5] if len(df['Restaurant_Name'].unique()) > 5 else df['Restaurant_Name'].unique()
        )
        
        filtered_df = df[df['Restaurant_Name'].isin(selected_restaurants)]
        
        if not filtered_df.empty:
            # Restaurant comparison
            restaurant_summary = filtered_df.groupby('Restaurant_Name').agg({
                'Amount_Collected': 'sum',
                'POS_Revenue_Amount': 'sum' if 'POS_Revenue_Amount' in filtered_df.columns else 'count',
                'KIOSK_Revenue_Amount': 'sum' if 'KIOSK_Revenue_Amount' in filtered_df.columns else 'count',
                'ONLINE_Revenue_Amount': 'sum' if 'ONLINE_Revenue_Amount' in filtered_df.columns else 'count'
            }).reset_index()
            
            # Create stacked bar chart
            fig_stack = go.Figure()
            
            if 'POS_Revenue_Amount' in restaurant_summary.columns:
                fig_stack.add_trace(go.Bar(name='POS', x=restaurant_summary['Restaurant_Name'], 
                                          y=restaurant_summary['POS_Revenue_Amount']))
            if 'KIOSK_Revenue_Amount' in restaurant_summary.columns:
                fig_stack.add_trace(go.Bar(name='KIOSK', x=restaurant_summary['Restaurant_Name'], 
                                          y=restaurant_summary['KIOSK_Revenue_Amount']))
            if 'ONLINE_Revenue_Amount' in restaurant_summary.columns:
                fig_stack.add_trace(go.Bar(name='ONLINE', x=restaurant_summary['Restaurant_Name'], 
                                          y=restaurant_summary['ONLINE_Revenue_Amount']))
            
            fig_stack.update_layout(
                barmode='stack',
                title='Revenue by Channel for Selected Restaurants',
                xaxis_title='Restaurant',
                yaxis_title='Revenue ($)',
                height=500
            )
            st.plotly_chart(fig_stack, use_container_width=True)
            
            # Detailed table
            st.subheader("Detailed Restaurant Metrics")
            st.dataframe(
                restaurant_summary.style.format({
                    'Amount_Collected': '${:,.2f}',
                    'POS_Revenue_Amount': '${:,.2f}',
                    'KIOSK_Revenue_Amount': '${:,.2f}',
                    'ONLINE_Revenue_Amount': '${:,.2f}'
                }),
                use_container_width=True
            )

with tab3:
    st.header("Channel Performance Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Channel revenue distribution
        channel_data = []
        if 'POS_Revenue_Amount' in df.columns:
            channel_data.append({'Channel': 'POS', 'Revenue': df['POS_Revenue_Amount'].sum()})
        if 'KIOSK_Revenue_Amount' in df.columns:
            channel_data.append({'Channel': 'KIOSK', 'Revenue': df['KIOSK_Revenue_Amount'].sum()})
        if 'ONLINE_Revenue_Amount' in df.columns:
            channel_data.append({'Channel': 'ONLINE', 'Revenue': df['ONLINE_Revenue_Amount'].sum()})
        
        if channel_data:
            channel_df = pd.DataFrame(channel_data)
            fig_channel = px.pie(
                channel_df,
                values='Revenue',
                names='Channel',
                title='Revenue Distribution by Channel',
                hole=0.3,
                color_discrete_map={'POS': '#1f77b4', 'KIOSK': '#ff7f0e', 'ONLINE': '#2ca02c'}
            )
            st.plotly_chart(fig_channel, use_container_width=True)
    
    with col2:
        # Channel performance metrics
        st.subheader("Channel Performance Metrics")
        
        for channel in ['POS', 'KIOSK', 'ONLINE']:
            col_name = f'{channel}_Revenue_Amount'
            if col_name in df.columns:
                channel_revenue = df[col_name].sum()
                channel_avg = df[col_name].mean()
                channel_max = df[col_name].max()
                non_zero_count = (df[col_name] > 0).sum()
                
                st.markdown(f"**{channel} Channel**")
                subcol1, subcol2 = st.columns(2)
                subcol3, subcol4 = st.columns(2)
                
                with subcol1:
                    if channel_revenue >= 1_000_000:
                        total_display = f"${channel_revenue/1_000_000:.1f}M"
                    else:
                        total_display = f"${channel_revenue:,.0f}"
                    st.metric("Total Revenue", total_display)
                with subcol2:
                    st.metric("Active Restaurants", f"{non_zero_count:,}")
                with subcol3:
                    if channel_avg >= 1000:
                        avg_display = f"${channel_avg/1000:.1f}K"
                    else:
                        avg_display = f"${channel_avg:,.0f}"
                    st.metric("Avg per Restaurant", avg_display)
                with subcol4:
                    if channel_max >= 1000:
                        max_display = f"${channel_max/1000:.1f}K"
                    else:
                        max_display = f"${channel_max:,.0f}"
                    st.metric("Max Revenue", max_display)
                st.markdown("---")

with tab4:
    st.header("Revenue Tier Analysis")
    
    if 'Revenue_Tier' in df.columns:
        # Tier distribution
        tier_counts = df['Revenue_Tier'].value_counts()
        tier_revenue = df.groupby('Revenue_Tier')['Amount_Collected'].sum()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_tier_count = px.bar(
                x=tier_counts.index,
                y=tier_counts.values,
                title='Number of Restaurants by Revenue Tier',
                labels={'x': 'Revenue Tier', 'y': 'Number of Restaurants'},
                color=tier_counts.values,
                color_continuous_scale='Teal'
            )
            st.plotly_chart(fig_tier_count, use_container_width=True)
        
        with col2:
            fig_tier_revenue = px.bar(
                x=tier_revenue.index,
                y=tier_revenue.values,
                title='Total Revenue by Tier',
                labels={'x': 'Revenue Tier', 'y': 'Total Revenue ($)'},
                color=tier_revenue.values,
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig_tier_revenue, use_container_width=True)

with tab5:
    st.header("Trends & Advanced Insights")
    
    # Statistical summary
    st.subheader("Statistical Summary")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if 'Amount_Collected' in numeric_cols:
        stats_df = df[['Amount_Collected']].describe()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean Revenue", f"${stats_df.loc['mean', 'Amount_Collected']:,.2f}")
        with col2:
            st.metric("Median Revenue", f"${stats_df.loc['50%', 'Amount_Collected']:,.2f}")
        with col3:
            st.metric("Std Deviation", f"${stats_df.loc['std', 'Amount_Collected']:,.2f}")
        with col4:
            q75 = stats_df.loc['75%', 'Amount_Collected']
            q25 = stats_df.loc['25%', 'Amount_Collected']
            iqr = q75 - q25
            st.metric("IQR", f"${iqr:,.2f}")
    
    # Revenue distribution histogram
    if 'Amount_Collected' in df.columns:
        st.subheader("Revenue Distribution")
        
        fig_dist = px.histogram(
            df,
            x='Amount_Collected',
            nbins=30,
            title='Revenue Distribution Across All Restaurants',
            labels={'Amount_Collected': 'Revenue ($)', 'count': 'Frequency'},
            color_discrete_sequence=['#1f77b4']
        )
        fig_dist.add_vline(x=df['Amount_Collected'].mean(), line_dash="dash", 
                         line_color="red", annotation_text="Mean")
        fig_dist.add_vline(x=df['Amount_Collected'].median(), line_dash="dash", 
                         line_color="green", annotation_text="Median")
        st.plotly_chart(fig_dist, use_container_width=True)

with tab6:
    st.header("🌐 Online Ordering Analysis")
    
    # Filter for restaurants with online revenue
    if 'ONLINE_Revenue_Amount' in df.columns:
        # Get restaurants with online revenue > 0
        online_df = df[df['ONLINE_Revenue_Amount'] > 0].copy()
        
        if not online_df.empty:
            # Key metrics for online ordering
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_online_restaurants = online_df['Restaurant_Name'].nunique()
                st.metric("Restaurants with Online Orders", f"{total_online_restaurants:,}")
            
            with col2:
                total_online_revenue = online_df['ONLINE_Revenue_Amount'].sum()
                st.metric("Total Online Revenue", f"${total_online_revenue:,.0f}")
            
            with col3:
                avg_online_revenue = online_df['ONLINE_Revenue_Amount'].mean()
                st.metric("Avg Online Revenue", f"${avg_online_revenue:,.0f}")
            
            with col4:
                online_penetration = (len(online_df) / len(df)) * 100
                st.metric("Online Adoption Rate", f"{online_penetration:.1f}%")
            
            st.markdown("---")
            
            # Two column layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Top 30 restaurants by online revenue
                st.subheader("Top 30 Restaurants by Online Revenue")
                
                top_30_online = online_df.groupby('Restaurant_Name').agg({
                    'ONLINE_Revenue_Amount': 'sum',
                    'Amount_Collected': 'sum'
                }).sort_values('ONLINE_Revenue_Amount', ascending=False).head(30)
                
                # Calculate online percentage
                top_30_online['Online_Percentage'] = (top_30_online['ONLINE_Revenue_Amount'] / top_30_online['Amount_Collected'] * 100)
                
                # Reverse the order so highest revenue appears at the top
                top_30_online_reversed = top_30_online.iloc[::-1]
                
                # Create horizontal bar chart
                fig_top30 = px.bar(
                    x=top_30_online_reversed['ONLINE_Revenue_Amount'].values,
                    y=top_30_online_reversed.index,
                    orientation='h',
                    title='Top 30 Restaurants - Online Revenue',
                    labels={'x': 'Online Revenue ($)', 'y': 'Restaurant'},
                    color=top_30_online_reversed['Online_Percentage'].values,
                    color_continuous_scale='Teal',
                    text=[f'${x:,.0f}' for x in top_30_online_reversed['ONLINE_Revenue_Amount'].values],
                    hover_data={'Online %': top_30_online_reversed['Online_Percentage'].values.round(1)}
                )
                fig_top30.update_traces(textposition='auto')
                fig_top30.update_layout(
                    height=800,
                    showlegend=False,
                    coloraxis_colorbar=dict(title="Online %"),
                    margin=dict(l=150, r=100, t=50, b=50)  # Add right margin for text
                )
                st.plotly_chart(fig_top30, use_container_width=True)
            
            with col2:
                # Online revenue by category/tier
                st.subheader("Online Revenue by Category")
                
                if 'Revenue_Tier' in online_df.columns:
                    # Group by revenue tier
                    online_by_tier = online_df.groupby('Revenue_Tier').agg({
                        'ONLINE_Revenue_Amount': 'sum',
                        'Restaurant_Name': 'count'
                    }).reset_index()
                    online_by_tier.columns = ['Revenue Tier', 'Online Revenue', 'Restaurant Count']
                    online_by_tier = online_by_tier.sort_values('Online Revenue', ascending=False)
                    
                    # Pie chart for online revenue by tier
                    fig_online_tier = px.pie(
                        online_by_tier,
                        values='Online Revenue',
                        names='Revenue Tier',
                        title='Online Revenue by Revenue Tier',
                        hole=0.4,
                        color_discrete_sequence=px.colors.sequential.Purples_r
                    )
                    fig_online_tier.update_traces(
                        textposition='inside',
                        textinfo='percent+label',
                        hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
                    )
                    st.plotly_chart(fig_online_tier, use_container_width=True)
                    
                    # Table showing tier breakdown
                    st.subheader("Category Breakdown")
                    online_by_tier['Avg per Restaurant'] = online_by_tier['Online Revenue'] / online_by_tier['Restaurant Count']
                    st.dataframe(
                        online_by_tier.style.format({
                            'Online Revenue': '${:,.0f}',
                            'Avg per Restaurant': '${:,.0f}',
                            'Restaurant Count': '{:,.0f}'
                        }),
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.warning("No restaurants with online revenue found in the data.")
    else:
        st.warning("Online revenue data not available in the uploaded files.")

with tab7:
    st.header("📊 Month-over-Month Analysis")
    
    # Check if we have multiple months of data
    if 'Month' not in df.columns or df['Month'].nunique() < 2:
        st.warning("Month-over-Month analysis requires at least 2 months of data. Please select multiple months in the period selector.")
    else:
        # Calculate MoM metrics
        mom_result = calculate_mom_metrics(df)
        
        if mom_result:
            pivot_df, mom_changes = mom_result
            categories = categorize_restaurant_performance(pivot_df, mom_changes)
            
            # Display period selector for MoM comparison
            st.subheader("Select Comparison Period")
            available_comparisons = list(mom_changes.keys())
            selected_comparison = st.selectbox(
                "Choose month-to-month comparison:",
                available_comparisons,
                index=len(available_comparisons)-1  # Default to most recent
            )
            
            # Get data for selected comparison
            comparison_data = mom_changes[selected_comparison]
            prev_month, curr_month = selected_comparison.split(' to ')
            
            # Summary metrics for selected comparison
            st.markdown("---")
            st.subheader(f"Performance Summary: {selected_comparison}")
            
            col1, col2, col3, col4, col5 = st.columns([1.2, 1, 1.2, 1.5, 1])
            
            with col1:
                total_prev = comparison_data['prev_month'].sum()
                total_curr = comparison_data['curr_month'].sum()
                total_change = total_curr - total_prev
                st.metric(
                    f"Total Revenue {curr_month}",
                    f"${total_curr:,.0f}",
                    f"${total_change:+,.0f}"
                )
            
            with col2:
                # Total restaurants in the dataset for current month
                total_restaurants = len(comparison_data['curr_month'])
                active_curr = (comparison_data['curr_month'] > 0).sum()
                st.metric(
                    f"Total Restaurants",
                    f"{total_restaurants}",
                    f"{active_curr} active"
                )
            
            with col3:
                # Count restaurants with revenue under $3K in current month only (excluding zero revenue)
                low_revenue_curr = ((comparison_data['curr_month'] > 0) & (comparison_data['curr_month'] < 3000)).sum()
                low_revenue_prev = ((comparison_data['prev_month'] > 0) & (comparison_data['prev_month'] < 3000)).sum()
                low_revenue_change = low_revenue_curr - low_revenue_prev
                st.metric(
                    f"Under $3K in {curr_month.split()[0]}",
                    f"{low_revenue_curr}",
                    f"{low_revenue_change:+d} vs {prev_month.split()[0]}"
                )
            
            with col4:
                # Only count restaurants that are active in at least one period
                active_mask = (comparison_data['curr_month'] > 0) | (comparison_data['prev_month'] > 0)
                growing = (active_mask & (comparison_data['percentage'] > 0)).sum()
                declining = (active_mask & (comparison_data['percentage'] < 0)).sum()
                stable = (active_mask & (comparison_data['percentage'] == 0)).sum()
                st.metric(
                    "Growing/Declining",
                    f"{growing} ↑ / {declining} ↓",
                    f"({stable} stable)"
                )
            
            with col5:
                # New entrants and churned restaurants
                new_entrants = ((comparison_data['prev_month'] == 0) & (comparison_data['curr_month'] > 0)).sum()
                churned = ((comparison_data['prev_month'] > 0) & (comparison_data['curr_month'] == 0)).sum()
                st.metric(
                    "New/Churned",
                    f"{new_entrants} new / {churned} lost",
                    f"in {curr_month.split()[0]}"
                )
            
            st.markdown("---")
            
            # Performance Categories
            st.subheader("Restaurant Performance Categories")
            
            cat_col1, cat_col2, cat_col3 = st.columns(3)
            
            with cat_col1:
                st.markdown("### 🌟 Rising Stars")
                st.markdown(f"*{len(categories['Rising Stars'])} restaurants with >20% growth*")
                if categories['Rising Stars']:
                    # Convert to dict for safe access
                    pct_dict = dict(zip(pivot_df.index, comparison_data['percentage']))
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    abs_dict = dict(zip(pivot_df.index, comparison_data['absolute']))
                    
                    # Sort Rising Stars by absolute revenue gain (Growth $)
                    sorted_rising_stars = sorted(categories['Rising Stars'], 
                                               key=lambda x: abs_dict.get(x, 0), 
                                               reverse=True)
                    
                    for i, restaurant in enumerate(sorted_rising_stars[:10], 1):
                        change = pct_dict.get(restaurant, 0)
                        amount = curr_dict.get(restaurant, 0)
                        gain = abs_dict.get(restaurant, 0)
                        st.markdown(f"{i}. **{restaurant}** (+{change:.1f}%, +${gain:,.0f}) - ${amount:,.0f}")
            
            with cat_col2:
                st.markdown("### ⚠️ Declining")
                st.markdown(f"*{len(categories['Declining'])} restaurants with >20% decline*")
                if categories['Declining']:
                    # Convert to dict for safe access
                    pct_dict = dict(zip(pivot_df.index, comparison_data['percentage']))
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    abs_dict = dict(zip(pivot_df.index, comparison_data['absolute']))
                    
                    # Sort Declining restaurants by absolute revenue loss (largest losses first)
                    sorted_declining = sorted(categories['Declining'], 
                                            key=lambda x: abs_dict.get(x, 0), 
                                            reverse=False)  # ascending for negative values
                    
                    for i, restaurant in enumerate(sorted_declining[:10], 1):
                        change = pct_dict.get(restaurant, 0)
                        amount = curr_dict.get(restaurant, 0)
                        loss = abs(abs_dict.get(restaurant, 0))
                        st.markdown(f"{i}. **{restaurant}** ({change:.1f}%, -${loss:,.0f}) - ${amount:,.0f}")
            
            with cat_col3:
                st.markdown("### 🆕 New & Churned")
                st.markdown(f"*{len(categories['New Entrants'])} new, {len(categories['Churned'])} churned*")
                if categories['New Entrants']:
                    st.markdown("**New Entrants:**")
                    curr_dict = comparison_data['curr_month'].to_dict() if hasattr(comparison_data['curr_month'], 'to_dict') else dict(comparison_data['curr_month'])
                    
                    # Sort New Entrants by highest current revenue
                    sorted_new = sorted(categories['New Entrants'], 
                                      key=lambda x: curr_dict.get(x, 0), 
                                      reverse=True)
                    
                    for restaurant in sorted_new[:5]:
                        amount = curr_dict.get(restaurant, 0)
                        st.markdown(f"• {restaurant} - ${amount:,.0f}")
                if categories['Churned']:
                    st.markdown("**Churned:**")
                    prev_dict = comparison_data['prev_month'].to_dict() if hasattr(comparison_data['prev_month'], 'to_dict') else dict(comparison_data['prev_month'])
                    
                    # Sort Churned restaurants by largest previous revenue (largest losses first)
                    sorted_churned = sorted(categories['Churned'], 
                                          key=lambda x: prev_dict.get(x, 0), 
                                          reverse=True)
                    
                    for restaurant in sorted_churned[:5]:
                        prev_amount = prev_dict.get(restaurant, 0)
                        st.markdown(f"• {restaurant} (was ${prev_amount:,.0f})")
            
            st.markdown("---")
            
            # Visualizations
            st.subheader("Month-over-Month Visualizations")
            
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Waterfall chart for top changes
                top_gainers = comparison_data['absolute'].nlargest(10)
                top_losers = comparison_data['absolute'].nsmallest(10)
                
                # Combine and sort
                waterfall_data = pd.concat([top_gainers, top_losers]).sort_values(ascending=False)
                
                fig_waterfall = go.Figure(go.Waterfall(
                    name="Revenue Change",
                    orientation="v",
                    x=waterfall_data.index[:15],  # Top 15 changes
                    y=waterfall_data.values[:15],
                    connector={"line": {"color": "rgb(63, 63, 63)"}},
                    increasing={"marker": {"color": "green"}},
                    decreasing={"marker": {"color": "red"}}
                ))
                fig_waterfall.update_layout(
                    title=f"Top Revenue Changes: {selected_comparison}",
                    height=400,
                    xaxis_tickangle=-45
                )
                st.plotly_chart(fig_waterfall, use_container_width=True)
            
            with viz_col2:
                # Distribution of percentage changes
                fig_dist = px.histogram(
                    x=comparison_data['percentage'],
                    nbins=30,
                    title="Distribution of % Changes",
                    labels={'x': 'Percentage Change (%)', 'count': 'Number of Restaurants'},
                    color_discrete_sequence=['#1f77b4']
                )
                fig_dist.add_vline(x=0, line_dash="dash", line_color="red", annotation_text="No Change")
                fig_dist.add_vline(x=np.median(comparison_data['percentage']), line_dash="dash", 
                                 line_color="green", annotation_text="Median")
                # Set x-axis range to maximum 1000%
                fig_dist.update_xaxes(range=[-100, 1000])
                fig_dist.update_layout(
                    xaxis=dict(range=[-100, 1000])
                )
                st.plotly_chart(fig_dist, use_container_width=True)
            
            # Monthly Trend Heatmap
            st.markdown("---")
            st.subheader("Monthly Performance Heatmap")
            
            # Create heatmap data
            heatmap_data = pivot_df.head(50)  # Top 50 restaurants
            
            # Calculate percentage changes for heatmap
            heatmap_pct = heatmap_data.pct_change(axis=1) * 100
            
            fig_heatmap = px.imshow(
                heatmap_pct,
                labels=dict(x="Month", y="Restaurant", color="% Change"),
                aspect="auto",
                color_continuous_scale="RdYlGn",
                color_continuous_midpoint=0,
                title="Month-over-Month % Change Heatmap (Top 50 Restaurants)"
            )
            fig_heatmap.update_layout(height=800)
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Detailed comparison table
            st.markdown("---")
            st.subheader("Detailed Restaurant Comparison")
            
            # Create detailed comparison dataframe
            prev_month_values = comparison_data['prev_month'].values if hasattr(comparison_data['prev_month'], 'values') else comparison_data['prev_month']
            curr_month_values = comparison_data['curr_month'].values if hasattr(comparison_data['curr_month'], 'values') else comparison_data['curr_month']
            absolute_values = comparison_data['absolute'] if isinstance(comparison_data['absolute'], np.ndarray) else comparison_data['absolute'].values
            percentage_values = comparison_data['percentage'] if isinstance(comparison_data['percentage'], np.ndarray) else comparison_data['percentage'].values
            
            comparison_df = pd.DataFrame({
                'Restaurant': pivot_df.index,
                f'{prev_month} Revenue': prev_month_values,
                f'{curr_month} Revenue': curr_month_values,
                'Absolute Change': absolute_values,
                '% Change': percentage_values
            })
            
            # Add performance category
            def get_category(restaurant):
                for cat, restaurants in categories.items():
                    if restaurant in restaurants:
                        return cat
                return 'Other'
            
            comparison_df['Category'] = comparison_df['Restaurant'].apply(get_category)
            
            # Sort by absolute change
            comparison_df = comparison_df.sort_values('Absolute Change', ascending=False)
            
            # Display with formatting
            st.dataframe(
                comparison_df.style.format({
                    f'{prev_month} Revenue': '${:,.0f}',
                    f'{curr_month} Revenue': '${:,.0f}',
                    'Absolute Change': '${:+,.0f}',
                    '% Change': '{:+.1f}%'
                }).background_gradient(subset=['% Change'], cmap='RdYlGn', vmin=-50, vmax=50),
                use_container_width=True,
                height=400
            )
        else:
            st.error("Unable to calculate month-over-month metrics. Please check your data.")

# Export functionality
st.markdown("---")
st.header("📥 Export Data")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Export Processed Data to Excel"):
        output_file = f"processed_restaurant_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(output_file, index=False)
        st.success(f"Data exported to {output_file}")

with col2:
    csv = df.to_csv(index=False)
    st.download_button(
        label="📄 Download as CSV",
        data=csv,
        file_name=f"restaurant_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )

with col3:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# Footer
st.markdown("---")
st.markdown(f"*🔒 Secure Dashboard v{__version__} - Data loaded from Google Sheets - Released {__release_date__}*")