import streamlit as st
import pandas as pd

# Load data from the CSV file
@st.cache_data
def load_data(filename="techcrunch_startups.csv"):
    try:
        return pd.read_csv(filename)
    except FileNotFoundError:
        st.error(f"{filename} not found. Please upload or generate the data.")
        return pd.DataFrame()

# Main Streamlit app
def main():
    st.title("TechCrunch Startup Discovery Dashboard")

    # Load the data
    data = load_data()

    if data.empty:
        st.warning("No data available. Please scrape and upload the data first.")
    else:
        # Display the data
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

        # Option to download the data
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
