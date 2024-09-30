from flask import Flask, render_template, request
from main import fetch_current_affairs, generate_content_gemini, save_to_txt, save_to_pdf  # import your functions from main.py
import pathway as pw
import pathway.io.fs as io_fs # type: ignore
import pathway.io.gdrive as io_gdrive # type: ignore
from pathway.internals import udfs # type: ignore
from pathway.xpacks.llm import llms, prompts # type: ignore
from pathway.xpacks.llm.vector_store import VectorStoreServer # type: ignore

app = Flask(__name__)

# Define Pathway pipeline for vector storage or processing
def pathway_processing(news_data):
    # Create Pathway table from news data
    table = pw.Table.from_dict({
        "title": [article['title'] for article in news_data],
        "source": [article['source']['name'] for article in news_data],
        "url": [article['url'] for article in news_data]
    })
    
    # Processing the table using Pathway (example: filtering or vectorizing)
    filtered_table = table.filter(pw.this.source == "The Times of India")

    # Saving filtered data to local storage (or Google Drive, etc.)
    pw.io.jsonlines.write(filtered_table, "filtered_news.jsonl")
    
    # Run the Pathway pipeline
    pw.run()

    return filtered_table

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    topic = request.form['topic']
    category = request.form['category']

    # Fetch current news
    news = fetch_current_affairs(topic)

    # Use Pathway to process the news articles
    processed_news = pathway_processing(news)

    # Generate historical content using Gemini API
    content = generate_content_gemini(topic)
    
    # Save content if generated
    if content:
        save_to_txt(topic, content)
        save_to_pdf(topic, content)

    return render_template('result.html', topic=topic, news=processed_news, content=content)

if __name__ == "__main__":
    app.run(debug=True)
