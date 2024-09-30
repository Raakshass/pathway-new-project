import requests
import os
from dotenv import load_dotenv
import pathway as pw
from fpdf import FPDF
import pandas as pd


# Load environment variables from .env file
load_dotenv()

# Get API keys from environment variables
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# URLs for the APIs
NEWS_API_URL = "https://newsapi.org/v2/everything"
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"

def fetch_current_affairs(query):
    """
    Fetches live news related to the query from NewsAPI.
    """
    params = {
        'q': query,
        'apiKey': NEWS_API_KEY,
        'sortBy': 'publishedAt',
        'language': 'en'
    }
    response = requests.get(NEWS_API_URL, params=params)
    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

def generate_content_gemini(topic):
    """
    Use Google Gemini API to generate content based on the UPSC topic.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Explain {topic} for UPSC preparation"
                    }
                ]
            }
        ]
    }

    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    if response.status_code == 200:
        content = response.json()
        if "candidates" in content and content["candidates"]:
            return content["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Error: 'content' not found in the response.")
            return None
    else:
        print(f"Error fetching historical content: {response.status_code}, {response.text}")
        return None

def save_to_txt(topic, content):
    """
    Save the generated content to a text file.
    """
    with open(f"historical_docs/{topic}.txt", "w") as file:
        file.write(content)

def save_to_pdf(topic, content):
    """
    Save the generated content to a PDF.
    """
    # Replace problematic characters and ensure all content is latin-1 encodable
    clean_content = content.encode('latin-1', 'replace').decode('latin-1')  # Replace unencodable characters with '?'

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, clean_content)
    pdf.output(f"historical_docs/{topic}.pdf")

class NewsSchema(pw.Schema):
    title: str
    source: str

def process_and_filter_with_pathway():
    """
    Sample Pathway usage for filtering and processing data for UPSC interpreter.
    """
    # Assuming some input is fetched from current affairs
    news_articles = fetch_current_affairs("Indian Economy")

    # Create a Pathway table from the news articles
    input_table = pw.debug.table_from_pandas(
        pd.DataFrame({
            "title": [article['title'] for article in news_articles],
            "source": [article['source']['name'] for article in news_articles]
        })
    )

    # Filter and process with Pathway
    filtered_table = input_table.filter(input_table.source == "The Times of India")

    # Output result to JSON Lines
    pw.io.jsonlines.write(filtered_table, "filtered_news.jsonl")
    pw.run()  # Run the Pathway computation
  

if __name__ == "__main__":
    # Create the folder if it doesn't exist
    if not os.path.exists('historical_docs'):
        os.makedirs('historical_docs')

    # Define the UPSC topics and a query for current affairs
    topics = ["Indian Economy", "Indian History", "World Geography", "Environmental Science"]
    query = "Indian economy"

    # Fetch current affairs for the query
    print(f"Fetching current news for: {query}")
    current_affairs = fetch_current_affairs(query)

    for i, article in enumerate(current_affairs[:5]):
        print(f"{i+1}. {article['title']} - {article['source']['name']}")
        print(f"Published at: {article['publishedAt']}")
        print(f"URL: {article['url']}\n")

    # Generate content for UPSC topics and save them as .txt and .pdf
    for topic in topics:
        print(f"Generating historical content for: {topic}")
        content = generate_content_gemini(topic)

        if content:
            # Save the content to both .txt and .pdf formats
            save_to_txt(topic, content)
            save_to_pdf(topic, content)
            print(f"Content for {topic} saved as text and PDF.")
        else:
            print(f"Failed to generate content for: {topic}")

    # Process and filter data using Pathway
    print("Processing and filtering news with Pathway.")
    process_and_filter_with_pathway()
