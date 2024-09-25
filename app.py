#
# 
#  app.py for web scrapper
# 
#  Elias, Osman 9/25/2024
#
# 
# Web scrapper designed to fetch data in this format with all conditions met:
# 
# Author:
# Publication Date:
# Publication Source:
# Body:
#
#
# #



import requests
from bs4 import BeautifulSoup
import os 

def find_author(soup):
    #Various methods to find the author
    
    # 1. Look for meta tags 
    author_meta = soup.find('meta', {'name': 'author'})
    if author_meta and 'content' in author_meta.attrs:
        return author_meta['content']
    
    # 2. Try to find any <a> or <span> tags 
    author_tag = soup.find(['a', 'span'], class_=lambda value: value and 'author' in value.lower())
    if author_tag:
        return author_tag.get_text().strip()

    # 3. Look for <a> tags with rel="author"
    author_rel = soup.find('a', {'rel': 'author'})
    if author_rel:
        return author_rel.get_text().strip()

    # 4. Try to find structured data with info
    structured_data = soup.find('script', type='application/ld+json')
    if structured_data:
        import json
        try:
            data = json.loads(structured_data.string)
            if isinstance(data, dict):
                if 'author' in data:
                   
                    if isinstance(data['author'], dict) and 'name' in data['author']:
                        return data['author']['name']
                   
                    elif isinstance(data['author'], list) and 'name' in data['author'][0]:
                        return data['author'][0]['name']
        except json.JSONDecodeError:
            pass
    
    # 5. Search for any tags with the term "byline" or "author"
    author_byline = soup.find(class_=lambda value: value and 'byline' in value.lower())
    if author_byline:
        return author_byline.get_text().strip()

    # Fallback
    return "Author not found"




def find_publication_date(soup):
    #Various methods to find the publication date
    
    # 1. Check meta tags
    date_meta = soup.find('meta', {'name': 'article:published_time'}) or \
                soup.find('meta', {'property': 'og:published_time'}) or \
                soup.find('meta', {'name': 'date'}) or \
                soup.find('meta', {'property': 'article:published'})
    if date_meta and 'content' in date_meta.attrs:
        return date_meta['content']
    
    # 2. Look for <time> tags with the datetime attribute
    time_tag = soup.find('time')
    if time_tag and 'datetime' in time_tag.attrs:
        return time_tag['datetime']
    
    # 3. Try finding a <span> or <div> with 'date' in class or id
    date_tag = soup.find(['span', 'div'], class_=lambda value: value and 'date' in value.lower())
    if date_tag:
        return date_tag.get_text().strip()

    # 4. Look for JSON-LD structured data
    structured_data = soup.find('script', type='application/ld+json')
    if structured_data:
        import json
        try:
            data = json.loads(structured_data.string)
            if isinstance(data, dict) and 'datePublished' in data:
                return data['datePublished']
        except json.JSONDecodeError:
            pass

    # Fallback
    return "Date not found"



def scrape_article(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {url}")
        return None
    
    soup = BeautifulSoup(response.content, 'lxml')

    # Extracting publication source from title or meta tags
    site_name_meta = soup.find('meta', {'property': 'og:site_name'})
    if site_name_meta and 'content' in site_name_meta.attrs:
        publication_source = site_name_meta['content']
    else:
        publication_source = soup.title.get_text()
        if " - " in publication_source:
            publication_source = publication_source.split(" - ")[-1]
        elif " | " in publication_source:
            publication_source = publication_source.split(" | ")[-1]


    # Using functions to find author and publication
    author = find_author(soup)
    publication_date = find_publication_date(soup)

    # Extracting the body of the article
    body = ' '.join([p.get_text() for p in soup.find_all('p')])



    # Return a dictionary of the scraped data
    return {
        'Author': author,
        'Publication Date': publication_date,
        'Publication Source': publication_source,
        'Body': body
    }

# Scraping
url = "https://www.foodandwine.com/lactaid-dairy-free-milk-recall-8717123"  # Replace with the actual URL
article_data = scrape_article(url)




# Saving the data to a .txt file
if article_data:


    #Define folder name
    folder_name = 'textDump'

    txt_file = '0105_food.txt'  #Change name to whatever

    # Check if the folder exists; if not, create it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Define the file path 
    txt_file = os.path.join(folder_name, '0105_food.txt')

    with open(txt_file, mode='w', encoding='utf-8') as file:
        file.write(f"Author: {article_data['Author']}\n")
        file.write(f"Publication Date: {article_data['Publication Date']}\n")
        file.write(f"Publication Source: {article_data['Publication Source']}\n\n")
        file.write("Body:\n")
        file.write(f"{article_data['Body']}\n")

    print(f"Data saved to {txt_file}")
