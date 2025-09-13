# Elasticity Tool

An interactive tool for calculating price elasticity and cross-price elasticity for soda products using real market data.

## Launch Interactive App

### Option 1: JupyterLite (Runs in Browser - No Server!)
**[Launch with JupyterLite](https://mknomics.github.io/micro_app/)** - Runs entirely in your browser using WebAssembly

### Option 2: MyBinder (Full Python Environment)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mknomics/micro_app/HEAD?urlpath=voila%2Frender%2FElasticity_Tool.ipynb)

## Features

- **Own Price Elasticity**: Calculate how quantity demanded changes with price for a specific product
- **Cross-Price Elasticity**: Analyze how demand for one product responds to price changes of another
- **Market Analysis**: Compare cross-price elasticities across all competing brands
- **Interactive Visualizations**: Real-time plots showing price-quantity relationships

## Local Setup

If you want to run this locally:

```bash
# Clone the repository
git clone https://github.com/mknomics/micro_app.git
cd micro_app

# Install dependencies
pip install -r requirements.txt

# Run with Voilà
voila Elasticity_Tool.ipynb
```

## Data Source

The tool uses real soda sales data from Athens, analyzing five brands across three container types (plastic, can, glass).

## Technologies Used

- **Voilà**: Turns Jupyter notebooks into standalone web applications
- **ipywidgets**: Interactive widgets for parameter selection
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Linear regression for elasticity calculations
- **matplotlib**: Data visualization

## How to Use

1. Click the Binder badge above to launch the app
2. Select brand and container type from the dropdown menus
3. Adjust the price slider to your desired price point
4. Click the appropriate button to calculate elasticity
5. View the results and visualizations