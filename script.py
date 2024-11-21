import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import matplotlib.pyplot as plt


# Function to save data to a CSV file
def save_to_csv(data, filename="quotes.csv"):
    """
    Save quote data to a CSV file.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["quote", "author", "tags"])
        writer.writeheader() # Write the header row
        writer.writerows(data) # Write the book data
    print(f"Data saved to {filename}")


# Function to fetch the webpage content
def fetch_page(url):
    """
    Fetch the HTML content of a webpage.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error if the request fails
        return response.text  # Return the page's HTML content
    except requests.RequestException as e:
        print(f"Error fetching the URL: {url}\n{e}")
        return None
    

# Function to parse the HTML content
def parse_page(html):
    """
    Parse the HTML content with BeautifulSoup.
    """
    return BeautifulSoup(html, 'html.parser')  # Return the parsed HTML


# Function to extract quote data
def extract_quotes(soup):
    """
    Extract quote details from the parsed HTML content.
    """
    quotes = []  # Initialize a list to store quote data
    quote_elements = soup.select('.quote')  # Select all HTML elements with the class "quote"
    
    for quote in quote_elements:  # Loop through each quote container
        text = quote.select_one('.text').text  # Get the quote text
        author = quote.select_one('.author').text  # Get the author
        tags = [tag.text for tag in quote.select('.tag')]  # Get all tags associated with the quote
        quotes.append({  # Append a dictionary with the extracted data to the list
            'quote': text,
            'author': author,
            'tags': ", ".join(tags)  # Join tags into a comma-separated string
        })
    
    return quotes


# Function to scrape quotes
def scrape_quotes(base_url):
    """
    Scrape quotes from all pages of the website.
    """
    quotes = []  # Initialize a list to store all quotes
    current_page = 1  # Start with the first page

    while True:  # Loop until there are no more pages
        print(f"Scraping page {current_page}...")

        page_url = f"{base_url}page/{current_page}/"  # Construct the URL for the current page
        
        html = fetch_page(page_url)  # Fetch the HTML content of the page
        if not html:
            break  # Stop if the page couldn't be fetched

        soup = parse_page(html)  # Parse the HTML content
        page_quotes = extract_quotes(soup)  # Extract quotes from the parsed HTML
        if not page_quotes:
            break  # Stop if no quotes are found (end of pages)

        quotes.extend(page_quotes)  # Add the quotes from the current page to the main list
        current_page += 1  # Increment to the next page

    return quotes


# Function to clean data
def clean_data(data):
    """
    Clean data by removing non-ASCII characters.
    """
    for quote in data:  # Loop through each quote
        # Remove non-ASCII characters from quote text, author, and tags
        quote['quote'] = quote['quote'].encode('ascii', 'ignore').decode('ascii')
        quote['author'] = quote['author'].encode('ascii', 'ignore').decode('ascii')
        quote['tags'] = quote['tags'].encode('ascii', 'ignore').decode('ascii')

    return data


# Function to create visualizations
def create_visualizations(data):
    """
    Create visualizations from the scraped data.
    """
    # Convert data to a pandas DataFrame
    df = pd.DataFrame(data)
    
    # Data for Visualization 1: Most common tags
    tags_series = df['tags'].str.split(', ').explode()  # Split tags and count occurrences
    tag_counts = tags_series.value_counts().head(10)  # Get the top 10 tags
    
    # Data for Visualization 2: Most popular authors
    author_counts = df['author'].value_counts().head(10)  # Count authors and get top 10
    
    # Create a figure with subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))  # 1 row, 2 columns of subplots

    # Plot 1: Most common tags
    tag_counts.plot(
        kind='bar',
        color='purple',
        edgecolor='black',
        ax=axes[0]  # Specify the first subplot
    )
    axes[0].set_title("Top 10 Most Common Tags")
    axes[0].set_xlabel("Tags")
    axes[0].set_ylabel("Number of Quotes")
    axes[0].tick_params(axis='x', rotation=45)

    # Plot 2: Most popular authors
    author_counts.plot(
        kind='bar',
        color='skyblue',
        edgecolor='black',
        ax=axes[1]  # Specify the second subplot
    )
    axes[1].set_title("Top 10 Most Popular Authors")
    axes[1].set_xlabel("Authors")
    axes[1].set_ylabel("Number of Quotes")
    axes[1].tick_params(axis='x', rotation=45)

    # Adjust layout for clarity
    plt.tight_layout()
    plt.show()


# Main function
def main():
    """
    Main function to run the web scraper.
    """
    base_url = "https://quotes.toscrape.com/"
    all_quotes = scrape_quotes(base_url)

    # Display the extracted data
    for quote in all_quotes:
        print(quote)

    # Clean non-ASCII characters
    all_quotes = clean_data(all_quotes)

    # Save data to a CSV file
    save_to_csv(all_quotes)

    # Create visualizations
    create_visualizations(all_quotes)


# Run the script
if __name__ == "__main__":
    main()