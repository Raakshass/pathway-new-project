UPSC Interpreter with Pathway and Generative AI
This project is a Flask-based web application that provides users with the latest news articles, generates topic-specific content using Google Gemini API (a Generative AI model), and processes the content using Pathway for advanced data transformations. The application is designed for UPSC aspirants who require historical and current affairs content in a structured format.

Key Features
Real-time Current Affairs: Fetches live news data using the NewsAPI, allowing users to stay updated with current events.
Generative AI Content: Uses the Google Gemini API (LLM) to generate comprehensive content on various UPSC topics.
Advanced Data Processing with Pathway: Pathway’s powerful data processing and vector storage capabilities are used to transform, filter, and manage content dynamically.
PDF and Text Export: Saves generated content in both text and PDF formats for easy offline access.
Modular Design: The project is split between main.py (which handles data fetching, content generation, and file saving) and app.py (the Flask app, which serves the web interface).
Architecture
This project uses the following key components:

Pathway:

Pathway is utilized in main.py and app.py to handle the transformation and filtering of data tables created from the news articles fetched from NewsAPI.
It enables fast and scalable data operations, such as filtering, vector storage, and output generation (e.g., JSON lines).
Generative AI (Google Gemini API):

Google Gemini, a Large Language Model (LLM), is employed to generate topic-based content for UPSC topics like Indian History, World Geography, Environmental Science, and more.
This content is dynamically created using an API call to the Gemini service and can be saved in multiple formats (PDF and text).
Flask Web App:

The user interface is built using Flask, allowing users to enter a topic and category to fetch the news and generate historical content.
The app processes the input, calls the LLM, and displays results to the user.
Usage Instructions
Requirements
Docker: Docker is used to run the application in an isolated environment.
AWS/Gemini API Keys: You'll need your API keys for NewsAPI and Gemini (Google Generative AI).
Setup Instructions
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/pathway-new-project.git
cd pathway-new-project
Set up environment variables:

Add your API keys in the .env file:

makefile
Copy code
NEWS_API_KEY=your_news_api_key
GEMINI_API_KEY=your_gemini_api_key
Build and run with Docker:

bash
Copy code
docker-compose up --build
Access the Application:

Open your browser and navigate to:

arduino
Copy code
http://localhost:8000
Code Overview
main.py
This file contains the main logic of the project, including:

Current Affairs Fetching:

fetch_current_affairs() fetches live news articles using the NewsAPI.
Generative AI Content Generation:

generate_content_gemini() calls the Google Gemini API to generate topic-specific content based on UPSC-related queries.
Pathway Data Processing:

pathway_processing() processes the news articles using Pathway’s table operations.
A table is created from the news data, and Pathway is used to filter, store, and vectorize the data.
File Saving:

Functions like save_to_txt() and save_to_pdf() are used to save generated content in multiple formats.
app.py
This file manages the Flask web application.

Routes:

/: Displays the homepage with a form for inputting the topic.
/generate: Processes the form submission, fetches the news articles, and generates historical content using Pathway and Generative AI.
Pathway Integration:

Pathway is used in pathway_processing() to filter news data and handle data operations, which are then rendered on the results page.
Templates
index.html: A simple input form where users can specify their desired topic.
result.html: Displays the news articles and generated content after processing the input.
How to Extend
Additional Pathway Features: You can expand on Pathway's functionality to include more advanced transformations, joins, and vector operations in the main.py file.
New LLM Models: If required, you can integrate different Generative AI models for generating various types of content, or process additional input/output formats.
Customization: Modify the Flask routes and add more interactive elements to the front-end.
Example Use Cases
UPSC Aspirants: Fetch the latest news and generate concise historical content for exam preparation.
Educational Tools: Provide students with dynamically generated content based on the latest available data.
Content Filtering and Storage: Use Pathway for filtering news articles and vector storage for future retrieval or machine learning applications.
License
This project is open-source and distributed under the MIT License.
