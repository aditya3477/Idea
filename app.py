# Import libraries
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

# Risk & Viability Analysis Agent
def analyze_risk_and_viability(data):
    risk_scores = []
    for title in data['title']:
        risk_score = random.uniform(0, 1)  # Simulated risk score for demonstration
        risk_scores.append(risk_score)
    data['risk_score'] = risk_scores
    return data

# Recommendation & Reporting Agent
def generate_recommendations(data, threshold):
    filtered_data = data[data['risk_score'] >= threshold]
    recommendations = filtered_data[['title', 'risk_score', 'link']]
    return recommendations

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

    # Check session state and reload data if updated
    if "data_updated" not in st.session_state:
        st.session_state["data_updated"] = False

    # Load existing data
    data = load_data()

    if data.empty:
        st.warning("No data available. Please scrape data first.")
    else:
        st.write("### Latest Startups")
        st.dataframe(data)

        # Risk and viability analysis
        if st.checkbox("Run Risk & Viability Analysis"):
            data = analyze_risk_and_viability(data)
            st.write(data[['title', 'risk_score']])

        # Recommendations with user-defined threshold
        if st.checkbox("Generate Recommendations"):
            threshold = st.slider("Select Risk Score Threshold", 0.0, 1.0, 0.5, 0.05)
            recommendations = generate_recommendations(data, threshold)
            st.write("### Top Recommendations")
            st.dataframe(recommendations)

        # Download functionality
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name="techcrunch_startups.csv",
            mime="text/csv",
        )

# Run the app
if __name__ == "__main__":
    main()
