# Retrieves the summary based on the combined csv.
# Importing the necessary libraries.
import pandas as pd

# Loading the preprocessed data.
# Loading the combined data of the 10 data files.
preprocessed_df = pd.read_csv('preprocessed_text.csv')
original_df = pd.read_csv('combined.csv')

def get_original_summary(input_preprocessed_summary):
    # Check if the preprocessed summary exists in the dataframe
    if input_preprocessed_summary in preprocessed_df['Summary'].values:
        # Find the index of the preprocessed summary
        index = preprocessed_df[preprocessed_df['Summary'] == input_preprocessed_summary].index[0]

        # Retrieve the corresponding original summary using the same index
        original_summary = original_df['Summary'].iloc[index]
        return original_summary
    else:
        return "Preprocessed summary not found."


