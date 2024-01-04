# This file sends the query to solr, which hosts the Inverted Index.
# Importing the necessary libraries.
import os
import pysolr
import csv
import requests
import pandas as pd
import pickle
import json
import summary_ret 


# Function to get the summary from inverted index hosted on SOLR.
def query_solr(topic_present, user_summary_query, solr_base_url, solr_core="IRF23P1", rows=5):

    # Query Construction to retrieve data.
    query_url = f"{solr_base_url}/{solr_core}/select"
    
    # The structure of SOLR queries is declared.
    params = {
        'q': f"summary:\"{user_summary_query}\"",
        'fq': f"topic:\"{topic_present}\"",
        'rows': rows,
        'wt': 'json',
        'indent': 'true',
        'q.op': 'AND'
    }
    
    # Getting the SOLR response to obtain the summary.
    response = requests.get(query_url, params=params)
    
    # Error Handling and Success queries for the data obtained from SOLR.
    if response.status_code == 200:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            # JSON file is incorrect or has an issue.
            print("Invalid JSON response:", e)
            return None
    else:
        # If data that needs to be obtained takes too long or couldn't find the summary.
        print("Failed to fetch data:", response.status_code, response.text)
        return None

    
# Matching the summary to obtain a proper and coherent summary for the user. 
def summary_match(solr_reply, rows_value):
    solr_docs = solr_reply['response']['docs']
    rows_value
    # Getting top k summaries similar to the user queried summaries.
    top_k = 1  
    top_k_docs = [doc['summary'] for doc in solr_docs[:top_k]]
    total_summaries = []
    for summary in top_k_docs:
        first_summary = summary_ret.get_original_summary(summary)
        total_summaries.append(first_summary)
    
    return total_summaries