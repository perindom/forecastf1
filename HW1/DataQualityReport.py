import pandas as pd
import numpy as np

# Assume you already have your DataFrame loaded as df.
# For example:
df = pd.read_csv('diabetic_data.csv')

def generate_data_quality_report(df):
    nrows = df.shape[0]
    report_data = []

    for col in df.columns:
        col_data = df[col]
        col_report = {}

        # Column name (will be used as index later)
        col_report['column'] = col

        # Data type and cardinality
        col_report['dtype'] = col_data.dtype
        col_report['cardinality'] = col_data.nunique(dropna=True)

        # For numeric columns, compute mean, median, stddev, min, max, and count at median
        if pd.api.types.is_numeric_dtype(col_data):
            col_report['mean'] = col_data.mean()
            col_report['median'] = col_data.median()
            median_val = col_report['median']
            col_report['n_at_median'] = (col_data == median_val).sum()
            col_report['stddev'] = col_data.std()
            col_report['min'] = col_data.min()
            col_report['max'] = col_data.max()
        else:
            col_report['mean'] = np.nan
            col_report['median'] = np.nan
            col_report['n_at_median'] = np.nan
            col_report['stddev'] = np.nan
            # For non-numeric columns, try to use the natural ordering (if possible)
            try:
                col_report['min'] = col_data.min()
                col_report['max'] = col_data.max()
            except Exception:
                col_report['min'] = np.nan
                col_report['max'] = np.nan

        # Mode and count at mode (works for both numeric and non-numeric)
        mode_series = col_data.mode(dropna=True)
        if not mode_series.empty:
            mode_val = mode_series.iloc[0]
            col_report['mode'] = mode_val
            col_report['n_at_mode'] = (col_data == mode_val).sum()
        else:
            col_report['mode'] = np.nan
            col_report['n_at_mode'] = np.nan

        # Total number of rows in the DataFrame
        col_report['nrows'] = nrows

        # Count of zeros: for numeric columns, count 0; for non-numeric, count "0" strings.
        if pd.api.types.is_numeric_dtype(col_data):
            col_report['nzero'] = (col_data == 0).sum()
        else:
            col_report['nzero'] = (col_data == '0').sum()

        # Count of question marks: typically relevant for string/object columns.
        if pd.api.types.is_string_dtype(col_data) or pd.api.types.is_object_dtype(col_data):
            col_report['nquestionmark'] = (col_data == '?').sum()
        else:
            col_report['nquestionmark'] = 0

        # Count of missing values (NaNs)
        col_report['nmissing'] = col_data.isna().sum()

        report_data.append(col_report)

    report_df = pd.DataFrame(report_data).set_index('column')
    return report_df

# Generate the report and print it
quality_report = generate_data_quality_report(df)
quality_report.to_csv("quality_report.csv", index=True)
