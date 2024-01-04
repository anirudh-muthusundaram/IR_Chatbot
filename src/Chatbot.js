// Importing the necessary libraries.
import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import TotalQueries from './TotalQueries';
import TopicDistributionPieChart from './TopicDistributionPieChart';
import ResponseAccuracyChart from './ResponseAccuracyChart'; 
import { BarElement } from 'chart.js';

// Declaring the necessary libraries for Chart.js
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';

// Declaring the necessary components for Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  ArcElement,
  BarElement, 
  Tooltip,
  Legend
);

// Declaring and Traversing all the Chatbot states.
const Chatbot = () => {
    const [input, setInput] = useState('');
    const [queries, setqueries] = useState([]);
    const [Chartdisplay, setChartdisplay] = useState(false); 
    const [ShowQueries, setShowQueries] = useState(false); 
    const [pagecovershow, setpagecovershow] = useState(true); 
    const [showAccuracyChart, setShowAccuracyChart] = useState(false);
    const chatBoxRef = useRef(null);
    const inactivityTimer = useRef(null);
    const apiUrl = process.env.REACT_APP_API_URL;


    useEffect(() => {
        // Messages scrolled to the bottom for every query and response.
        if (chatBoxRef.current) {
            chatBoxRef.current.scrollTop = chatBoxRef.current.scrollHeight;
        }
    }, [queries]);

    // Messages to indicate the end of the conversation.
    const isConversationEndingMessage = (message) => {
      const endingMessages = ["thank you", "thanks", "bye", "goodbye"];
      return endingMessages.includes(message.toLowerCase().trim());
    };
    
    //User messages are treated based on the inactivity.
    const sendQueries = (event) => {
      event.preventDefault();
      if (input) {
          setqueries([...queries, { text: input, sender: 'user' }]);
          UserQueriesProcessing(input);

          if (isConversationEndingMessage(input)) {
              clearTimeout(inactivityTimer.current);
          } else {
              turnOffTimer();
          }

          setInput('');
      }
  };

    const turnOffTimer = () => {
      // Clear existing timer.
      if (inactivityTimer.current) {
          clearTimeout(inactivityTimer.current);
      }

      // Set a new timer.
      inactivityTimer.current = setTimeout(() => {
          setqueries(queries => [...queries, { text: "How may I help you?", sender: 'bot' }]);
      }, 3000); // 3 Seconds Timer.
  };

  // Toggling the chart visibility.
  const ChartShowSwitch = () => { 
    setChartdisplay(!Chartdisplay);
};

// Function to hide the chart.
const turnOffChart = () => { 
    setChartdisplay(false);
};

// Fetch and log the total queries when showing the queries.
const toggleTotalQueriesVisibility = () => {
    setShowQueries(!ShowQueries);
    if (!ShowQueries) {
      GetQueries();
    }
  };

// Revealing the Chatbot.
const revealChatbot = () => {
    // Start the slide-up transition.
    const cover = document.getElementById('page-cover');
    if (cover) {
      cover.style.transform = 'translateY(-100%)';
    }
    // Wait for transition to complete before removing the cover from the DOM.
    setTimeout(() => {
      setpagecovershow(false);
    }, 500); 
  };

  // The user queries are sent to the backend api.
const GetQueries = async () => {
    try {
      const response = await fetch(`${apiUrl}/total-queries`);
      if (response.ok) {
        const totalQueries = await response.json();
        console.log('Total Queries:', totalQueries);
      } else {
        console.error('Failed to fetch total queries');
      }
    } catch (error) {
      console.error('Error fetching total queries:', error);
    }
  };

  // User Queries processing and all the chat componenets are connected to the Flask server.
  const UserQueriesProcessing = async (message) => {
    try {
        const isRespondingToFollowUp = queries.length > 0 && queries[queries.length - 1].text === "Do you want to ask anything else?";
        
        const response = await fetch(`${apiUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message, respondingToFollowUp: isRespondingToFollowUp })
        });

        if (response.ok) {
            const data = await response.json();
            let responseMessages = [];

            if (data.user_topic) {
                responseMessages.push({ text: `Topic: ${data.user_topic}`, sender: 'bot' });
            }
            
            responseMessages.push({ text: data.response, sender: 'bot' });

            if (data.follow_up && data.user_topic) {
                clearTimeout(inactivityTimer.current);
                setTimeout(() => {
                    setqueries(queries => [...queries, { text: data.follow_up, sender: 'bot' }]);
                }, 2000);
            } else if (!data.user_topic) {
                if (data.response.toLowerCase().includes("you're welcome")) {
                    // Clear the inactivity timer if the response is "You're welcome"
                    clearTimeout(inactivityTimer.current);
                } else if (!isConversationEndingMessage(data.response)) {
                    // Reset the inactivity timer for other chit-chat responses
                    turnOffTimer();
                }
            }

            setqueries(queries => [...queries, ...responseMessages]);
        } else {
            console.error('Failed to send message:', response.statusText);
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
};

  

   
      // All the necessary buttons and logic are initialized.
      return (
        <>
          {pagecovershow && (
            <div id="page-cover" onClick={revealChatbot}>
              <h1>Cyber Seeker Chatbot</h1>
              <h2>Please Click Anywhere on the screen</h2>
              <h3>To access the Chatbot</h3>
            </div>
          )}
          <div className={`chat-container ${pagecovershow ? 'hidden' : ''}`}>
            <div id="chat-box" ref={chatBoxRef}>
              {queries.map((message, index) => (
                <div key={index} className={`message ${message.sender === 'user' ? 'user' : 'bot'}`}>
                  {message.text}
                </div>
              ))}
            </div>
            <form onSubmit={sendQueries}>
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask something..."
              />
              <button type="submit">Send</button>
            </form>
            {ShowQueries && <TotalQueries />}
            <div className="chart-controls">
              <button className="toggle-chart-btn" onClick={ChartShowSwitch}>
                {Chartdisplay? "Back to Chat" : "Topics"}
              </button>
              {Chartdisplay&& <button className="hide-chart-btn" onClick={turnOffChart}>Back to Chat</button>}
              <button className="show-queries-btn" onClick={toggleTotalQueriesVisibility}>
                {ShowQueries ? "Hide User Queries" : "Show User Queries"}
              </button>
              <button className="toggle-accuracy-chart-btn" onClick={() => setShowAccuracyChart(!showAccuracyChart)}>
                {showAccuracyChart ? "Back to Chat" : "Response Accuracy"}
              </button>
            </div>
            {showAccuracyChart && <ResponseAccuracyChart />}
            {Chartdisplay&& <TopicDistributionPieChart />}
          </div>
        </>
      );
    };


export default Chatbot;