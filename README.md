Python3 Web Scraper

Overview
This web scraper is designed to extract article data from web pages, including:

Author
Publication Date
Publication Source
Article Body

It uses multiple strategies to handle the various HTML structures across different websites. The scraper supports searching for author and publication date information from meta tags, structured data (like JSON-LD), <time> elements, and other common HTML patterns.

Features
Robust author extraction: Attempts to find the author using multiple patterns.

Publication date extraction: Extracts the publication date from meta tags, <time> elements, and structured data.

Flexible handling of publication source: Uses both Open Graph meta tags and the title of the page to identify the source.

Handles various HTML structures: Designed to work across many different news sites, blogs, and content platforms.
Saves data to .txt: The extracted article data is saved in a readable .txt format. (This can be changed)

Requirements
Before running the scraper, ensure you have the following Python packages installed:

pip install requests beautifulsoup4 lxml


Setup
Clone the repository to your local machine:

git clone https://github.com/your-username/web-scraper.git


Navigate to the project directory:

cd PythonWebScraper

Install the required Python packages:

pip install -r requirements.txt


Replace the url in the Python script with the actual URL of the article you want to scrape.



How to Run
To run the web scraper, execute the Python script within the project directory:

python app.py


The scraper will extract the following data from the provided URL:

Author
Publication Date
Publication Source
Article Body

The data will be saved to a .txt file in the following format:

Author: [Author Name]
Publication Date: [Publication Date]
Publication Source: [Source Name]

Body:
[Article Body Text]

Example Output

For example, if you scrape an article from example.com:


Author: John Doe
Publication Date: 2020-09-25
Publication Source: News

Body:
This is the body of the article.

The scraper uses Python's BeautifulSoup to parse HTML.


Contributing
Feel free to submit pull requests if you want to contribute to improving the scraper. Here are a few ways you can help:

Add support for additional HTML structures.
Improve error handling.
Extend functionality.