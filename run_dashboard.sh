#!/bin/bash

# Restaurant Sales Dashboard Launcher

echo "🚀 Starting Restaurant Sales Analytics Dashboard..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing required packages..."
    pip install -r requirements.txt
fi

# Launch the dashboard
echo "📊 Launching dashboard on http://localhost:8501"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run restaurant_sales_dashboard.py