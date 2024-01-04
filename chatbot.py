# This file is the main driver file to run and process the user queries.
# This file also connects the chitchat componenet.
# Importing the necessary Libraries.
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import logging
import json
import datetime
import os
from datetime import datetime
import traceback
from solr_query import query_solr, summary_match
from preprocess import process_query
from topic_classifier import classify_query
from dotenv import load_dotenv
load_dotenv()

# Global variable to keep track of the model.
app = Flask(__name__)
CORS(app)
# rows value to set up the k value. 
rows_value = 5
# logging code to find errors or issues.
logging.basicConfig(level=logging.WARNING)
# conversation channel to switch between chitchat and queries.
convo_channel = 'chitchat'
# topic restriction for queries.
topic_present = None
# queries during chitchat.
SOLR_TRIGGER_KEYWORDS = ["what", "tell", "who"]
# global value for the topic accuracy.
global accuracy_topic

# API for huggingface. 
# API_CRED = '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'
API_CRED = os.environ.get('API_CRED')
print("API_CRED:", API_CRED)
#Dialo GPT is used as the chitchat model.
# CHITCHAT_API = 'https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium'
CHITCHAT_API_URL = os.environ.get('CHITCHAT_API_URL')
print("CHITCHAT_API_URL:", CHITCHAT_API_URL)


# Topic channels for restricting the queries to a single topic.
TOPIC_CHANNEL = {
    "\\Health": "Health",
    "\\Environment": "Environment",
    "\\Technology": "Technology",
    "\\Economy": "Economy",
    "\\Entertainment": "Entertainment",
    "\\Sports": "Sports",
    "\\Politics": "Politics",
    "\\Education": "Education",
    "\\Travel": "Travel",
    "\\Food": "Food"
}

# Joining the text for summaries obtained.
def text_join(txt, sum_length=500):
    if len(txt) <= sum_length:
        return txt
    else:
        return txt[:sum_length]

# logging the conversation for further visualization.
def log_conversation(u_msg, system_rep, topic_input=None):
    global accuracy_topic

    # Determining the accuracy of topics based on user texts.
    if u_msg.lower() == "correct":
        accurate_rep = "right"
    elif u_msg.lower() == "wrong":
        accurate_rep = "wrong"
    else:
        accurate_rep = None

    # Using the last user query to connect the topics with the accuracy, if the current one is None.
    if topic_input:
        accuracy_topic = topic_input
    elif accurate_rep:
        topic_input = accuracy_topic

    conversation_log = {
        'timestamp': datetime.now().isoformat(),
        'user_message': u_msg,
        'bot_response': system_rep,
        'user_topic': topic_input,
        'response_correctness': accurate_rep
    }

    log_file = 'data_coll_logs.json'

    if not os.path.exists(log_file):
        with open(log_file, 'w') as file:
            json.dump([conversation_log], file)
    else:
        with open(log_file, 'r+') as file:
            data = json.load(file)
            data.append(conversation_log)
            file.seek(0)
            json.dump(data, file)    
    
# App route to connect the system with the topic distribution component.
@app.route('/topic-distribution', methods=['GET'])
def topic_distribution():
    try:
        # Loading the conversation logs.
        with open('data_coll_logs.json', 'r') as file:
            data = json.load(file)
        
        # Calculating the frequency of each topic.
        topic_frequency = {}
        for entry in data:
            topic = entry.get('user_topic')
            if topic:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
        
        # Returning the topic frequency as JSON.
        return jsonify(topic_frequency), 200
    
    # Exception Handling for the topics.
    except FileNotFoundError as e:
        logging.error(f"File not found: {e}")
        return jsonify({'error': 'File not found'}), 500
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        return jsonify({'error': 'Invalid JSON format'}), 500
    except Exception as e:
        logging.error(f"An internal error occurred: {e}")
        stack_trace = traceback.format_exc()
        logging.error(f"{stack_trace}")
        return jsonify({'error': str(e)}), 500

# App route to connect the system with the total queries component.
@app.route('/total-queries', methods=['GET'])
def get_total_queries():
    try:
        # Collects the number of queries from data_coll_logs.json.
        with open('data_coll_logs.json') as f:
            logs = json.load(f)
        query_length = len(logs)
        return jsonify({'total': query_length})
    # Error Handling.
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# App route to connect the system with the response accuracy component.
@app.route('/response-accuracy', methods=['GET'])
def response_accuracy():
    try:
        with open('data_coll_logs.json', 'r') as file:
            data = json.load(file)
        
        detect_acc = {}
        for entry in data:
            topic = entry.get('user_topic', 'General')
            accuracy = entry.get('response_correctness', 'unknown')

            if accuracy is None:
                accuracy = 'unknown'

            if topic not in detect_acc:
                detect_acc[topic] = {'right': 0, 'wrong': 0, 'unknown': 0}
            detect_acc[topic][accuracy] += 1

        # Removing None keys if required.
        # Checking the accuracy based on the correctness of the topics and summary displayed.
        filtered_accuracy_distribution = {k: v for k, v in detect_acc.items() if k is not None}

        # Return the accuracy.
        return jsonify(filtered_accuracy_distribution), 200
    
    # Error Handling and Error Logging.
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        logging.info(f"Accuracy Distribution: {detect_acc}")
        logging.info(f"Processed accuracy distribution: {detect_acc}")
        return jsonify({'error': str(e)}), 500

# App route to connect the system with the response accuracy component.
@app.route('/chat', methods=['POST'])
def chat():
    global convo_channel
    global rows_value
    global topic_present
    u_msg = request.json.get('message', '')
    responding_to_follow_up = request.json.get('respondingToFollowUp', False)

    # conversation mode should switch back to chitchat.
    if u_msg.lower() in ["hi", "thank you"]:
        topic_present = None
        convo_channel = 'chitchat'

    # conversation mode restricted to that particular topic.
    if u_msg in TOPIC_CHANNEL:
        topic_present = TOPIC_CHANNEL[u_msg]
        convo_channel = 'solr'

    # conversation mode switched to wikipedia retrieval.
    if any(keyword in u_msg.lower() for keyword in SOLR_TRIGGER_KEYWORDS):
        topic_present = None
        convo_channel = 'solr'

    # reranking the top k values for correct and wrong results.
    if "wrong" in u_msg.lower():
        rows_value = 8
        convo_channel = 'solr'
        response_message = "We are sorry, we will correct it next time"
        log_conversation(u_msg, response_message)
        return jsonify({'response': response_message}), 200
          
    elif "correct" in u_msg.lower():
        rows_value = 3
        convo_channel = 'solr'
        response_message = "Thank you for your response"
        log_conversation(u_msg, response_message)
        return jsonify({'response': response_message}), 200

    # Error Handling implementation.
    if not u_msg:
        logging.debug("No message provided in the request.")
        error_message = 'No message provided'
        log_conversation(u_msg, error_message)
        return jsonify({'error': 'No message provided'}), 400
    
    # Follow up questions for wikipedia response.
    # Exception Handling.
    if responding_to_follow_up:
        if u_msg.lower() in ['yes', 'yupp', 'yeah']:
            return jsonify({'response': "Sure, Please do ask", 'reset': False}), 200
        elif u_msg.lower() in ['no', 'nope', 'nothing else', "that's it"]:
            convo_channel = 'chitchat'
            topic_present = None
            return jsonify({'response': "Okay, Thank you!", 'reset': True}), 200

    headers = {"Authorization": f"Bearer {API_CRED}"}
    data = {"inputs": u_msg}
    try:
        if topic_present and convo_channel == 'solr':
            # Inverted Index url on SOLR.
            solr_base_url = os.environ.get('SOLR_BASE_URL', "http://localhost:8983/solr")
            if topic_present:
                # Preprocess the user message to create a summary query.
                user_summary_query = process_query(u_msg)

                # Call the Solr query function with the current topic.
                solr_reply = query_solr(topic_present, user_summary_query, solr_base_url, rows=rows_value)

                if solr_reply:
                    # Extract summaries from the Solr response.
                    summaries = summary_match(solr_reply, rows_value)
                    if summaries:
                        response_message = ' '.join(summaries)
                    else:
                        response_message = "I found the topic but couldn't find a specific summary. Could you please provide more details?"
                else:
                    response_message = "I couldn't find any information on that topic. Could you please try a different query?"

                log_conversation(u_msg, response_message, topic_present)
                return jsonify({'response': response_message, 'user_topic': topic_present, 'follow_up': 'Do you want to ask anything else?'}), 200
            else:
                 # Handle case where there's no current topic set
                 # Exception Handling
                response_message = "Please specify a topic to continue."
                log_conversation(u_msg, response_message)
                return jsonify({'response': response_message}), 200

        elif convo_channel != 'solr' and "wikipedia" in u_msg.lower():
            # Switch to Solr query mode if the user asks for wikipedia.
            convo_channel = 'solr'
            response_message = "Please ask anything for Wiki"
            log_conversation(u_msg, response_message)
            return jsonify({'response': response_message}), 200

        elif convo_channel == 'solr':
            # Solr querying.
            solr_base_url = os.environ.get('SOLR_BASE_URL', "http://localhost:8983/solr")
            # processing the query.
            user_summary_query = process_query(u_msg)
            # classifying the topc, if it isn't provided by the user.
            topic_input = classify_query(user_summary_query)
            # Send query to SOLR to retrieve data.
            solr_reply = query_solr(topic_input, user_summary_query, solr_base_url, rows=rows_value)

            logging.debug(f"Solr response: {solr_reply}")
            if solr_reply:
                summaries = summary_match(solr_reply, rows_value)
                # Check if summaries list is not empty.
                if summaries:  
                    # Join summaries
                    response_join = summaries
                    logging.debug(f"Truncated response to be returned: {response_join}")
                    log_conversation(u_msg, response_join, topic_input)
                    return jsonify({'response': response_join, 'user_topic': topic_input, 'follow_up': 'Do you want to ask anything else?'}), 200
                else:
                    # Return a specific message when the summary is empty.
                    empty_summary_message = "I was able to get the topic, could you please be more specific"
                    log_conversation(u_msg, empty_summary_message, topic_input)
                    return jsonify({'response': empty_summary_message, 'user_topic': topic_input, 'follow_up': 'Do you want to ask anything else?'}), 200
            else:
                # Exception Handling.
                logging.debug("No data returned from Solr. Sending empty response.")
                error_message = 'Sorry, I currently have no records of that'
                log_conversation(u_msg, error_message)
                return jsonify({'error': error_message}), 404

        else:
            # Chit Chat model
            response = requests.post(CHITCHAT_API_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            model_response = response.json()

            # Extracting the chatbot response 
            chitchat_rep = model_response.get('generated_text', '')
            response_join = text_join(chitchat_rep)

            logging.debug(f"Received response: {response_join}")
            log_conversation(u_msg, response_join)

            # Check if the chatbot response is empty and handle accordingly
            # Exception Handling
            if not response_join.strip():
                follow_up_message = 'Could you please try that again?'
                return jsonify({'response': follow_up_message}), 200
            else:
                return jsonify({'response': response_join}), 200
    
    # Exception Handling and Error responses.
    except requests.exceptions.HTTPError as err:
        error_details = f'Failed to get response from the model API: {err}'
        logging.error(error_details)
        logging.error(f"Response Content: {err.response.content}")
        log_conversation(u_msg, error_details)
        return jsonify({'error': error_details}), response.status_code

    except requests.exceptions.Timeout as err:
        error_details = f'Request to model API timed out: {err}'
        logging.error(error_details)
        log_conversation(u_msg, error_details)
        return jsonify({'error': error_details}), 408

    except Exception as err:
        error_details = f'An internal error occurred: {err}'
        stack_trace = traceback.format_exc()
        logging.error(f"{error_details}\n{stack_trace}")
        return jsonify({'error': error_details}), 500


if __name__ == '__main__':
    app.run(debug=False)
