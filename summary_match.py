<<<<<<< HEAD
# Retrieves the summary based on the combined csv.
# Importing the necessary libraries.
import pandas as pd

# Loading the preprocessed data.
# Loading the combined data of the 10 data files.
Dataframe_process = pd.read_csv('preprocessed_text.csv')
original_df = pd.read_csv('combined.csv')

def summary_finder(summary_preprocess):
    # Checking if the preprocessed summary exists in the dataframe.
    if summary_preprocess in Dataframe_process['Summary'].values:
        # Find the index of the preprocessed summary.
        index = Dataframe_process[Dataframe_process['Summary'] == summary_preprocess].index[0]
        # Retrieving the summary from the combined data.
        summary_response = original_df['Summary'].iloc[index]
        return summary_response
    else:
        return "Preprocessed summary not found."
=======
# Retrieves the summary based on the combined csv.
# Importing the necessary libraries.
import pandas as pd

# Loading the preprocessed data.
# Loading the combined data of the 10 data files.
Dataframe_process = pd.read_csv('preprocessed_text.csv')
original_df = pd.read_csv('combined.csv')

def summary_finder(summary_preprocess):
    # Checking if the preprocessed summary exists in the dataframe.
    if summary_preprocess in Dataframe_process['Summary'].values:
        # Find the index of the preprocessed summary.
        index = Dataframe_process[Dataframe_process['Summary'] == summary_preprocess].index[0]
        # Retrieving the summary from the combined data.
        summary_response = original_df['Summary'].iloc[index]
        return summary_response
    else:
        return "Preprocessed summary not found."
>>>>>>> origin/main
