# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis project focused on restaurant sales data and residual calculations for Innowi and TekCard systems. The project uses Jupyter notebooks for analysis and visualization of sales performance across multiple restaurant locations.

## Key Files

- **innowi_all_restaurants_June-July-2025.ipynb**: Main analysis notebook for all restaurant sales data, including revenue categorization (Zero, 1K, 10K, 20K, 50K, and 100K accounts) and week-over-week sales analysis
- **tekcard-residual-calculator.ipynb**: Notebook for calculating residual values
- **Excel files**: Various exported data summaries including executive sales analytical summaries, network dues, and residual summaries

## Development Environment

### Python Libraries Used
- pandas - Data manipulation and analysis
- numpy - Numerical computations  
- matplotlib - Data visualization
- seaborn - Statistical data visualization
- plotly - Interactive visualizations

### Running Notebooks

To work with the Jupyter notebooks:
```bash
jupyter notebook [notebook_name].ipynb
```

Or use JupyterLab:
```bash
jupyter lab
```

## Data Analysis Focus Areas

1. **Revenue Categorization**: Analysis segments accounts into revenue tiers (Zero, 1K, 10K, 20K, 50K, 100K)
2. **POS Accounts Revenue**: Specific analysis for point-of-sale system accounts
3. **Week-over-Week Comparisons**: Tracking sales performance trends across weekly periods
4. **Network Dues Calculations**: Processing and analyzing network-related fees
5. **Residual Calculations**: Computing residual values for TekCard system

## Working with Data Files

The Excel files contain processed output from the notebooks:
- Executive Sales Analytical Summaries provide high-level insights
- Network dues files track payment obligations
- Residual summaries show calculated residual values

When modifying analysis, ensure consistency between notebook calculations and exported Excel summaries.