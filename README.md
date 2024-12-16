
# Trade Analysis Toolkit

This toolkit provides methods for analyzing trade data, including scaling, volatility calculation, and visualization.

## Features
1. **Data Aggregation and Scaling**: Aggregates and normalizes trade metrics.
2. **Volatility Calculation**: Computes log differences for metrics like `dollar`.
3. **Visualization**: Generates line and bar plots for trends and relationships.
4. **Excel Export**: Saves processed data to Excel with multiple sheets.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Prepare your trade data in Parquet format.
2. Update file paths in `trade_analysis_toolkit.py`.
3. Run the script:
   ```bash
   python trade_analysis_toolkit.py
   ```

## Requirements
- Python 3.7 or later
- Libraries: pandas, numpy, matplotlib, sklearn

## License
This project is licensed under the MIT License.
