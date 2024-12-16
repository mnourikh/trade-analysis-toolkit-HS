
# Trade Analysis Toolkit
# This script provides tools for processing, visualizing, and exporting trade data.

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from matplotlib.dates import ConciseDateFormatter, AutoDateLocator

# Data Aggregation and Scaling
def aggregate_and_scale(df, code_column='Code', scaler=None):
    # Aggregates and scales trade data by year, month, and code levels
    df = df.groupby(['year', 'month', code_column]).agg({
        'weight': 'sum',
        'rial': 'sum',
        'dollar': 'sum'
    }).reset_index()

    if scaler is None:
        scaler = MinMaxScaler()

    df[['weight_scaled', 'rial_scaled', 'dollar_scaled']] = scaler.fit_transform(
        df[['weight', 'rial', 'dollar']]
    )
    return df

# Volatility Calculation
def calculate_volatility(df, column='dollar', name='Volatility', code_column='Code'):
    # Calculates volatility as the log difference of the specified column
    df[column] = df[column].replace(0, np.nan)
    df[name] = df.groupby(code_column)[column].apply(lambda x: np.log(x).diff())
    df[name].replace([np.inf, -np.inf], np.nan, inplace=True)
    return df

# Plotting
def plot_data(ax, df, x_col, y_col, label, plot_type='line', **kwargs):
    # Plots data as a line or bar chart
    if plot_type == 'line':
        ax.plot(df[x_col], df[y_col], label=label, **kwargs)
    elif plot_type == 'bar':
        ax.bar(df[x_col], df[y_col], label=label, **kwargs)

# Export Results to Excel
def export_to_excel(dfs, output_path):
    # Saves multiple DataFrames to an Excel file with separate sheets
    with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
        for sheet_name, df in dfs.items():
            if not df.empty:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    # Example Usage
    # Load datasets
    export_data = pd.read_parquet("export_data.parquet")
    import_data = pd.read_parquet("import_data.parquet")

    # Scale and aggregate data
    export_scaled = aggregate_and_scale(export_data, code_column='Code')
    import_scaled = aggregate_and_scale(import_data, code_column='Code')

    # Calculate volatility
    export_volatility = calculate_volatility(export_scaled, column='dollar', name='Volatility')
    import_volatility = calculate_volatility(import_scaled, column='dollar', name='Volatility')

    # Plot example
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_data(ax, export_scaled, 'month', 'dollar_scaled', label='Export (scaled)', plot_type='line', color='blue')
    plt.legend()
    plt.show()

    # Save results to Excel
    output_file = "trade_analysis_results.xlsx"
    results = {
        "Export Data": export_scaled,
        "Export Volatility": export_volatility,
        "Import Data": import_scaled,
        "Import Volatility": import_volatility,
    }
    export_to_excel(results, output_file)
