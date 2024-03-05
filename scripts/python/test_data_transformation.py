import pandas as pd
import pytest
from data_transformation import load_csv, merge_data

def test_load_csv():
    # Test loading a CSV file
    csv_path = '/home/cameron/Documents/gis-edna-app/data/csv/qPCR_results.csv'
    data = load_csv(csv_path)
    assert isinstance(data, pd.DataFrame)
    assert len(data) > 0

def test_merge_data():
    # Test merging two dataframes
    df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df2 = pd.DataFrame({'A': [1, 2, 3], 'C': [7, 8, 9]})
    merged_data = merge_data(df1, df2, 'A')
    assert isinstance(merged_data, pd.DataFrame)
    assert len(merged_data) > 0
    assert 'B' in merged_data.columns
    assert 'C' in merged_data.columns

def test_final_merged_data():
    # Test if the final merged data is empty
    df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    df2 = pd.DataFrame({'A': [1, 2, 3], 'C': [7, 8, 9]})
    final_merged_data = merge_data(df1, df2, 'A')
    assert isinstance(final_merged_data, pd.DataFrame)
    assert len(final_merged_data) > 0

    # Test if the final merged data is empty
    empty_df1 = pd.DataFrame({'A': [], 'B': []})
    empty_df2 = pd.DataFrame({'A': [], 'C': []})
    final_merged_data_empty = merge_data(empty_df1, empty_df2, 'A')
    assert isinstance(final_merged_data_empty, pd.DataFrame)
    assert len(final_merged_data_empty) == 0

if __name__ == '__main__':
    pytest.main()