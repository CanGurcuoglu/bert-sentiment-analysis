import pandas as pd

# Load the dataset
file_path = 'vodafone_data_updated.csv'  # Update this path if needed
test_df = pd.read_csv(file_path)

# 1. Check for NaN values in the 'text' column
nan_count = test_df['text'].isna().sum()
print(f"Number of NaN values in 'text' column: {nan_count}")

# 2. Get the indexes of rows with NaN values in the 'text' column
if nan_count > 0:
    nan_indexes = test_df[test_df['text'].isna()].index
    print(f"Indexes of rows with NaN values in 'text' column: {nan_indexes.tolist()}")

    # 3. Drop rows with NaN values in the 'text' column
    test_df = test_df.drop(nan_indexes)
    print(f"\n{nan_count} rows with NaN values in 'text' column have been deleted.")

    # 4. Save the cleaned DataFrame to a new file
    output_file_path = 'vodafone_data_cleaned.csv'  # Update this path if needed
    test_df.to_csv(output_file_path, index=False)
    print(f"\nCleaned dataset saved to: {output_file_path}")
else:
    print("No NaN values found in the 'text' column. No rows were deleted.")