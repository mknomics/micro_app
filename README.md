# Elasticity Tool

An interactive tool for calculating price elasticity and cross-price elasticity for soda products using real market data.

## Launch Interactive App

### Full Version (Original)
**[Launch Elasticity Tool](https://mknomics.github.io/micro_app/lab/index.html?path=Elasticity_Tool.ipynb)** - Complete analysis tool with detailed explanations

### Simple Version (Single Cell)
**[Launch Simple Elasticity Tool](https://mknomics.github.io/micro_app/lab/index.html?path=Elasticity_Tool_Simple.ipynb)** - Streamlined version with core functionality

*Both versions run entirely in your browser using WebAssembly - no installation required!*

## Features

- **Own Price Elasticity**: Calculate how quantity demanded changes with price for a specific product
- **Cross-Price Elasticity**: Analyze how demand for one product responds to price changes of another
- **Market Analysis**: Compare cross-price elasticities across all competing brands
- **Interactive Visualizations**: Real-time plots showing price-quantity relationships

## How It Works

This app runs entirely in your browser using JupyterLite and WebAssembly. No installation required - just click the link above and start calculating elasticities!

## Data Source

The tool uses real soda sales data from Athens, analyzing five brands across three container types (plastic, can, glass).

## Technologies Used

- **JupyterLite**: Browser-based Jupyter environment using WebAssembly
- **ipywidgets**: Interactive widgets for parameter selection
- **pandas**: Data manipulation and analysis
- **scikit-learn**: Linear regression for elasticity calculations
- **matplotlib**: Data visualization

## How to Use

1. Click the launch link above to open the tool
2. Wait for the Python packages to install (first-time only)
3. Run all cells to initialize the interactive widgets
4. Select brand and container type from the dropdown menus
5. Adjust the price slider to your desired price point
6. Click the appropriate button to calculate elasticity
7. View the results and visualizations