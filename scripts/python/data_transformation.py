# Import libraries. 
import pandas as pd
import numpy as np

# Core Function to Load CSV
def load_csv(file_path):
    data = pd.read_csv(file_path)
    print(f"Loaded data from {file_path}: {data.shape[0]} rows, {data.shape[1]} columns")
    return data


def merge_data(df1, df2, merge_key):
    merged_df = pd.merge(df1, df2, on=merge_key)
    print(f"Merged data on {merge_key}: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")
    return merged_df

def filter_data_by_date_and_location(df, date_column, location_column, date, location):
    return df[(df[date_column] == date) & (df[location_column] == location)]

# Visualization Preparation Functions
def prepare_data_for_map(df, lat_col, lon_col):
    # Ensure data is suitable for mapping
    if lat_col not in df.columns or lon_col not in df.columns:
        raise ValueError(f"DataFrame does not contain necessary columns: {lat_col}, {lon_col}")
    df[lat_col] = pd.to_numeric(df[lat_col], errors='coerce')
    df[lon_col] = pd.to_numeric(df[lon_col], errors='coerce')
    df = df.dropna(subset=[lat_col, lon_col])
    return df

def prepare_data_for_time_series(df, date_column):
    # Structure data for time series visualization
    if date_column not in df.columns:
        raise ValueError(f"DataFrame does not contain necessary column: {date_column}")
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
    df = df.dropna(subset=[date_column])
    df = df.sort_values(by=date_column)
    return df

# Main function to orchestrate data processing
def main():
    # Paths to the CSV files
    qpcr_path = '/home/cameron/Documents/gis-edna-app/data/csv/qPCR_results.csv'
    locations_path = '/home/cameron/Documents/gis-edna-app/data/csv/sampling_locations.csv'
    dates_path = '/home/cameron/Documents/gis-edna-app/data/csv/transformed_sampling_activity.csv'

    # Load data
    qpcr_data = load_csv(qpcr_path)
    locations_data = load_csv(locations_path)
    dates_data = load_csv(dates_path)

    # Merge qPCR data with location data
    merged_data = merge_data(qpcr_data, locations_data, 'sampling_station')

    # Merge the above merged data with dates data on 'sampling_activity'
    final_merged_data = merge_data(merged_data, dates_data, 'sampling_activity')
# Check if the final merged data is empty
    if final_merged_data.empty:
        print("Final merged data is empty. Check the merge keys and data compatibility.")
    else:
        # Save the processed data to a JSON file
        output_json_path = '/home/cameron/Documents/gis-edna-app/data/serve_to_frontend/processed_data.json'  
        final_merged_data.to_json(output_json_path, orient='records')
        print(f"Processed data saved to JSON: {output_json_path}")
    # Prepare data for visualization or further processing
    prepare_data_for_map(final_merged_data, 'station_lat', 'station_long')
    
    prepare_data_for_time_series(final_merged_data, 'activity_data')

    # Save the processed data to a JSON file
    output_json_path = '/home/cameron/Documents/gis-edna-app/data/serve_to_frontend/processed_data.json'  
    final_merged_data.to_json(output_json_path, orient='records')

if __name__ == "__main__":
    main()
