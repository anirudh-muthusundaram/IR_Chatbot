Hello Everyone, I will describe about each and every files in this directory

A: Scraping Wiki pages
For scraping the Wiki pages, I have used the API endpoint and Wrapper as given in the handout. The ipynb file titled "scrapper.ipynb" contains the code for scraping the wikipedia data based on the topics and subtopics. I have taken 5600 documents for each topic which brings the total data documents collected to 56000 documents. The ipynb file saves all the collected data as CSV files within the "Data" Folder of the main directory. 

B: The Chit Chat model 
The Chitchat model used is DialoGPT and it is hosted on chatbot.py file.

C: Topic Analysis
The Topic Analysis is restricted to a single topic if the user intends to provide the topic, or if the user doesn't specify the topic, the query classifier will classify the user query and return the topic related to the query. The topics can be restricted to a specific topic by querying i.e: \Health, \Environment etc.

D: Wiki Q/A Bot
When the User restricts the query or has a wikipedia keyword or even in the chitchat model, they can query it with keywords like What is, who is or tell me about to access the wikipedia server and retrieve the data.

E: Exception Handling
The Chat responds to every user query and doesn't stop replying until the user says Thank you or thanks or related keywords. Other parts of the wikipedia conversation channel is handled the same way. This is not the only Exception Handling done and there are many more from Error Handling and Error Responses.

F: Visualization
Visualization is done with ReactJs, there are visualization techniques implemented like Topic Distribution, Total User Queries and Accuracy chart based on the user responses. All these would help in understanding the data obtained as well as in enhancing it further in the future.

G. Chat UI
The Chat UI is created with ReactJs, This will help in creating robust system to traverse the front end. All the necessary clauses given in the handout is here, including the topics. Note that the Topic restriction to the chat is implemented as given in C: Topic Analysis. Also, it will be able to return the summary even if the user doesn't restrict the chat or also if they are in the Chitchat conversation.

Now the files present in the directory

flask-app:
The flask-app contains all the code to run the backend server. you can type python chatbot.py or  python3 chatbot.py or your corresponding python variable to run it.

front-end:
This is a ReactJs app and it contains all the front end components, so please use npm install first then type npm start to run it.

web-scraper:
This has all the necessary files for scraping 56000 wikipedia data and saving it as ten different csv, preprocessing those csv and uploading it to Apache SOLR for the inverted index.

To Run the program, 
1: please install the requirements.txt file from flask-app.
2: python chatbot.py or python3 chatbot.py, to run the backend flask application in flask-app.
3: type flask run to run the code
4: npm install on front-end
5: npm start on front-end
