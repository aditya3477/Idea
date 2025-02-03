# Import libraries
import os
import requests
import pandas as pd
from transformers import pipeline
import streamlit as st
import time
import schedule
import networkx as nx
import matplotlib.pyplot as plt
import random
import feedparser
from bs4 import BeautifulSoup

# Function to scrape TechCrunch RSS feed with pagination
def scrape_techcrunch_rss(pages=5):
    base_url = "https://techcrunch.com/tag/startups/feed/"
    articles = []

    for page in range(1, pages + 1):
        feed_url = f"{base_url}?paged={page}"
        feed = feedparser.parse(feed_url)

        # Stop if no entries are found
        if not feed.entries:
            print(f"No entries found on page {page}. Stopping.")
            break

        for entry in feed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.published
            })

    return pd.DataFrame(articles)

# Function to scrape TechCrunch website pages
def scrape_techcrunch_pages(max_pages=5):
    base_url = "https://techcrunch.com/startups/"
    articles = []

    for page in range(1, max_pages + 1):
        url = f"{base_url}page/{page}/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        for item in soup.find_all("div", class_="post-block"):
            title = item.find("h2", class_="post-block__title").get_text(strip=True) if item.find("h2", class_="post-block__title") else "N/A"
            link = item.find("a", href=True)["href"] if item.find("a", href=True) else "N/A"
            date = item.find("time")["datetime"] if item.find("time") else "N/A"
            articles.append({"title": title, "link": link, "date": date})

    return pd.DataFrame(articles)

# Function to save data locally with deduplication
def save_data_locally(data, filename="techcrunch_startups.csv"):
    if os.path.exists(filename):
        existing_data = pd.read_csv(filename)
        combined_data = pd.concat([existing_data, data]).drop_duplicates(subset="link").reset_index(drop=True)
        combined_data.to_csv(filename, index=False)
    else:
        data.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Function to load data
def load_data(filename="techcrunch_startups.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        return pd.DataFrame()

# Summarization agent
def summarize_text(text):
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    try:
        input_length = len(text.split())
        max_length = max(10, min(50, input_length * 2 // 3))
        return summarizer(
            text,
            max_length=max_length,
            min_length=max(5, input_length // 3),
            do_sample=False
        )[0]["summary_text"]
    except Exception:
        return "Summary not available."

# Sentiment analysis agent
def analyze_sentiment(text):
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
    try:
        result = sentiment_analyzer(text)[0]
        return f"{result['label']} (Confidence: {result['score']:.2f})"
    except Exception:
        return "Sentiment analysis failed."

# Knowledge graph agent
def build_knowledge_graph(data):
    graph = nx.Graph()
    for _, row in data.iterrows():
        graph.add_node(row['title'], type='article', link=row['link'])
        for keyword in row['title'].split():
            graph.add_node(keyword, type='keyword')
            graph.add_edge(row['title'], keyword)
    return graph

def visualize_knowledge_graph(graph):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=50, font_size=8)
    st.pyplot(plt)

# Streamlit app
def main():
    st.title("TechCrunch Startup Discovery Dashboard")

    # Button to scrape data
    if st.button("Scrape Latest Data"):
        scraped_data = scrape_techcrunch_rss(pages=5)
        if not scraped_data.empty:
            save_data_locally(scraped_data)
            st.success("Data scraped and updated successfully!")
            st.session_state["data_updated"] = True
        else:
            st.warning("No new data found.")

    # Load existing data
    data = load_data()

    if data.empty:
        st.warning("No data available. Please scrape data first.")
    else:
        st.write("### Latest Startups")
        st.dataframe(data)

        # Summarization
        if st.checkbox("Show Summaries"):
            data['summary'] = data['title'].apply(summarize_text)
            st.write(data[['title', 'summary']])

        # Sentiment analysis
        if st.checkbox("Show Sentiment Analysis"):
            data['sentiment'] = data['title'].apply(analyze_sentiment)
            st.write(data[['title', 'sentiment']])

        # Knowledge graph
        if st.checkbox("Visualize Knowledge Graph"):
            graph = build_knowledge_graph(data)
            visualize_knowledge_graph(graph)

# Run the app
if __name__ == "__main__":
    main()
