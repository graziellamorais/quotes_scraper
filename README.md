# Quotes Scraper and Visualization
This repository contains a Python web scraper for extracting quotes and related information from the website Quotes to Scrape. It also includes visualizations for the most common tags and the most popular authors based on the scraped data.

## Features
- Scrapes quotes, authors, and tags from multiple pages of the website.
- Cleans and processes the data to remove unwanted characters.
- Saves the scraped data into a CSV file for further analysis.
- Creates visualizations for:
  - Most common tags (Top 10).
  - Most popular authors (Top 10).

## Technologies Used

- **Python**: Primary language used.
- **Libraries**:
  - `requests`: For fetching webpage content.
  - `BeautifulSoup` (`bs4`): For HTML parsing and data extraction.
  - `csv`: For saving scraped data.
  - `pandas`: For data manipulation and analysis.
  - `matplotlib`: For creating visualizations.
