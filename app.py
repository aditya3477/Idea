# Import libraries
import os
import requests
import pandas as pd
import feedparser
from transformers import pipeline
import streamlit as st

# Function to scrape TechCrunch RSS feed
def scrape_techcrunch_rss():
    feed_url = "https://techcrunch.com/tag/startups/feed/"
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published
        })

    return pd.DataFrame(articles)

# Function to save data locally
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

# Summarization function
def summarize_text(text):
    summarizer = pipeline("summarization")
    return summarizer(text, max_length=50, min_length=10, do_sample=False)[0]["summary_text"]

# Streamlit app
def main():
    st.title("TechCrunch Startup Discovery Dashboard")

    # Button to scrape data
    if st.button("Scrape Latest Data"):
        scraped_data = scrape_techcrunch_rss()
        if not scraped_data.empty:
            save_data_locally(scraped_data)
            st.success("Data scraped and updated successfully!")
            st.experimental_rerun()
        else:
            st.warning("No new data found.")

    # Load existing data
    data = load_data()

    if data.empty:
        st.warning("No data available. Please scrape data first.")
    else:
        st.write("### Latest Startups")
        st.dataframe(data)

        # Search functionality
        search_query = st.text_input("Search for a startup:")
        if search_query:
            filtered_data = data[data["title"].str.contains(search_query, case=False, na=False)]
            if not filtered_data.empty:
                st.write("### Search Results")
                st.dataframe(filtered_data)
            else:
                st.info("No results found for your search query.")

        # Filter by date
        if "published" in data.columns:
            date_filter = st.date_input("Filter by Date")
            if date_filter:
                filtered_data = data[data['published'] >= date_filter.strftime('%Y-%m-%d')]
                st.write("### Filtered Results")
                st.dataframe(filtered_data)

        # Download functionality
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="techcrunch_startups.csv",
            mime="text/csv",
        )

        # Visualization of publication trends
        if "published" in data.columns:
            data['published_date'] = pd.to_datetime(data['published'], errors='coerce')
            trends = data['published_date'].value_counts().sort_index()
            st.line_chart(trends)

# Run the app
if __name__ == "__main__":
    main()
