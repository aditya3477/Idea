# Idea

# TechCrunch Startup Discovery Dashboard

TechCrunch Startup Discovery Dashboard is a web application that scrapes and analyzes startup-related articles from TechCrunch's RSS feed and website. The dashboard provides tools for searching, filtering, summarizing, and visualizing data, making it an essential tool for startup enthusiasts and researchers.

# Features

## Data Scraping

* RSS Feed Scraping: Collect articles from TechCrunch's startup RSS feed.

* Website Scraping: Retrieve additional articles directly from TechCrunch's startup section.

* Pagination Support: Scrape multiple pages for a more extensive dataset.

## Data Management

* Storage: Save scraped data locally as a CSV file.

* Deduplication: Ensure no duplicate articles are saved.

## Dashboard

* Search and Filter:

- Search articles by keywords.

- Filter articles by publication date.

* Summarization: Generate concise summaries for article titles.

* Sentiment Analysis: Analyze the sentiment of article titles.

* Knowledge Graph: Build and visualize relationships between keywords and articles.

* Visualization: Display publication trends with line charts.

* Download Data: Export the dataset as a CSV file.

# Installation

## Requirements

* Python 3.8 or later

* Pip (Python package manager)

## Dependencies

The required libraries are listed in requirements.txt. These include:

* beautifulsoup4

* pandas

* streamlit

* feedparser

* transformers

* torch

* schedule

* networkx

* matplotlib

## Steps

1. Clone the repository:

git clone https://github.com/your-username/techcrunch-dashboard.git
cd techcrunch-dashboard

2. Install dependencies:

``` console
pip install -r requirements.txt
```
Run the Streamlit app:

``` console
streamlit run app.py
```

3. Access the app in your browser at 

```console
http://localhost:8501.
```

# Deployment

## Using Streamlit Community Cloud

1.Push the project to a public GitHub repository.

2. Go to Streamlit Community Cloud.

3. Log in and create a new app.

4. Select the repository and branch containing app.py.

5. Deploy the app. The URL will be generated automatically.

## Docker Deployment

Create a Dockerfile:

``` FROM python:3.9
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run the Docker container:

``` docker build -t techcrunch-dashboard .
docker run -p 8501:8501 techcrunch-dashboard
```

Access the app at 
``` console
http://localhost:8501.
```

# Usage

1. Scrape Data: Use the "Scrape Latest Data" button to fetch articles.

2. Search and Filter:

* Enter keywords to search for specific startups.

* Use the date filter to narrow down articles by publication date.

3. Summarize and Analyze:

* View summarized titles of articles.

* Analyze the sentiment of article titles.

4. Visualize Trends: Use the line chart to observe publication trends.

5. Download Data: Export the dataset as a CSV file for offline analysis.

# Architecture

## 1. Data Ingestion:

* scrape_techcrunch_rss: Fetch articles from the RSS feed.

* scrape_techcrunch_pages: Scrape articles from TechCrunch's website.

## 2. Data Storage:

* Save articles locally in CSV format.

* Deduplicate data based on article links.

## 3. Dashboard:

* Streamlit app for interaction, visualization, and analysis.

## 4. Advanced Features:

* Summarization and sentiment analysis using Hugging Face Transformers.

* Knowledge graph construction using NetworkX.
