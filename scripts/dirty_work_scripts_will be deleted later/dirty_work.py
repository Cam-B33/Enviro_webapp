import pandas as pd

def load_csv(file_path):
    return pd.read_csv(file_path)

def transform_sampling_activity_column(df, column_name):
    def reformat_value(val):
        # Remove the character and hyphen at positions 4 and 5, then append the character to the end
        return val[:4] + val[6:] + val[5]

    df[column_name] = df[column_name].apply(reformat_value)
    return df

def main():
    file_path = '/home/cameron/Documents/gis-edna-app/data/csv/sampling_activity.csv'  # Update with the actual file path
    df = load_csv(file_path)

    transformed_df = transform_sampling_activity_column(df, 'sampling_activity')
    transformed_df.to_csv('/home/cameron/Documents/gis-edna-app/data/csv/transformed_sampling_activity.csv', index=False)  # Update with desired output path

if __name__ == "__main__":
    main()

 
