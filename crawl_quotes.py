import re
import lxml
import json
import requests
from bs4 import BeautifulSoup

# saves the quetes data (quotes_list and authors_list) into a json file
def save_to_json_file(quotes_list, authors_list):
    quotes_dictionary = {"quotes":quotes_list, 'authors':authors_list}
    json_data = json.dumps(quotes_dictionary,ensure_ascii=False ,indent=4)
    file = open('./quotes.json','w',encoding = 'utf-8')
    file.write(json_data)
    file.close()

# returns next page url if next page available else retuns None
def get_next_page_url(soup):
    pager_element = soup.find('ul',class_="pager")
    next_page_list_element = pager_element.find('li', class_='next')
    if next_page_list_element != None:
        next_page_href = next_page_list_element.select_one('a', href=True)['href']
        next_page_url = "http://quotes.toscrape.com"+next_page_href
        return next_page_url
    else:
        return None

# returns a dictionary of author_name, born and reference url
def get_author_dictionary(quote_container):
    author_reference_url = get_author_reference_url(quote_container)
    response = get_response(author_reference_url)
    soup = parse_response_to_text_format(response)
    author_name = soup.find('h3',class_='author-title').text.strip()
    born_date = soup.find('span',class_='author-born-date').text.strip()
    born_place = soup.find('span',class_='author-born-location').text.strip()
    author_name = replace_speacial_chars_with_spaces(author_name)
    born = born_date +" "+ born_place.strip()
    reference = response.url
    author_dictionary =  { 'name':author_name, 'born':born, 'reference':reference}
    return author_dictionary

# returns the author reference urlof that quote
def get_author_reference_url(quote_container):
    author_href = quote_container.select_one('a')['href']
    author_reference_url = "http://quotes.toscrape.com"+author_href    
    return author_reference_url

# removes special charachters and returns the plane text
def replace_speacial_chars_with_spaces(text):
    replaced_text = re.sub("[^\w\s]", " ", text)
    replaced_text = " ".join(replaced_text.split())
    return replaced_text

# removes unicode values and returns the text
def remove_unicodes(text):
    text = text.encode("ascii","ignore")
    text = text.decode()
    return text

# returns a list of tags of the quote
def get_tags(tags_container):
    tags_list = [] 
    for tag_element in tags_container:
        tag = tag_element.text.strip()
        tags_list.append(tag)
    return tags_list

# returns a dictionary of quote, author and tags_list 
def get_quote_dictionary(quote_container):
    quote = quote_container.select_one('div .text').text.strip()
    author = quote_container.select_one('.author').text.strip()
    tags_container = quote_container.select('div .tag')
    tags_list = get_tags(tags_container)
    quote = remove_unicodes(quote)
    author = replace_speacial_chars_with_spaces(author)
    quote_dictionary =  {"quote": quote, "author": author, "tags": tags_list}
    return quote_dictionary

# web crawling starts by calling this function 
def get_quotes_and_authors_data_on_the_page(soup):
    quotes_and_authors_data = []
    quote_containers = soup.find_all('div',class_= 'quote')
    for quote_container in quote_containers:
        quote_dictionary = get_quote_dictionary(quote_container)
        author_dictionary = get_author_dictionary(quote_container)
        quotes_and_authors_data.append((quote_dictionary, author_dictionary))
    return quotes_and_authors_data
    
# returns a soup object by parseing the response object into text formart
def parse_response_to_text_format(response):
    soup = BeautifulSoup(response.content, "lxml")
    return soup

# returns response object for the requested url
def get_response(url): 
    response = requests.get(url)
    return response

#scrapping starts from this function
def start_web_scraping():
    quotes_list = []
    authors_list = []
    quotes_and_authors_data = []
    url = "http://quotes.toscrape.com/"
    while url != None:
        response = get_response(url)
        soup = parse_response_to_text_format(response) 
        quotes_and_authors_data.extend(get_quotes_and_authors_data_on_the_page(soup))
        url = get_next_page_url(soup)
    for quote_dictionary, author_dictionary in quotes_and_authors_data:
        quotes_list.append(quote_dictionary)
        if author_dictionary not in authors_list:
            authors_list.append(author_dictionary)
    save_to_json_file(quotes_list, authors_list)

start_web_scraping()
print("Scraping completed successfully!")