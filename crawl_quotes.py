import encodings
from tokenize import Ignore
import lxml
import json
import requests
from time import sleep
from bs4 import BeautifulSoup

quotes_page_url = "http://quotes.toscrape.com/"     # Quotes to Screape url 

quotes_list = list()    # Empty list to store quote data
authors_list = list()   # Empty list to store authors data

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
        next_page_page_anchor_element = next_page_list_element.select_one('a', href=True)
        next_page_href = next_page_page_anchor_element['href']
        next_page_url = quotes_page_url.strip('/')+next_page_href
        return next_page_url
    else:
        return None

# returns a dictionary of author_name, born and reference url
def get_author_dictionary(author_reference_url):
    response = get_response(author_reference_url)
    soup = parse_response_to_text_format(response)
    author_name = soup.find('h3',class_='author-title').text.strip()
    born_date = soup.find('span',class_='author-born-date').text.strip()
    born_place = soup.find('span',class_='author-born-location').text.strip()
    born = born_date +" "+ born_place.strip()
    reference = response.url
    author_dictionary =  { 'name':author_name, 'born':born, 'reference':reference}
    return author_dictionary

# returns the author reference urlof that quote
def get_author_reference_url(quote_container):
    author_href = quote_container.select_one('a')['href']
    author_reference_url = quotes_page_url.strip('/')+author_href    
    return author_reference_url

# gets the author dictionary from get_auhtor_dictionary function and appends it to the authors list
def append_author_data_into_authors_list(quote_container):
    author_reference_url = get_author_reference_url(quote_container)
    author_dictionary = get_author_dictionary(author_reference_url)
    if author_dictionary not in authors_list :
        authors_list.append(author_dictionary)


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
    quote = quote.encode("ascii","ignore")
    quote = quote.decode()
    author = quote_container.select_one('.author').text.strip()
    tags_container = quote_container.select('div .tag')
    tags_list = get_tags(tags_container)
    quote_dictionary =  {"quote": quote, "author": author, "tags": tags_list}
    return quote_dictionary

# gets a dictionary from get_quote_dictionary function and appends it to the quotes list
def append_quote_data_into_quotes_list(quote_container):
    quote_dictionary = get_quote_dictionary(quote_container)
    quotes_list.append(quote_dictionary)

# finds all the quote_containers, iterates each container and calls the functions
def find_quote_containers_and_call_append_functions(soup):
    quote_containers = soup.find_all('div',class_= 'quote')
    for quote_container in quote_containers:
        append_quote_data_into_quotes_list(quote_container)
        append_author_data_into_authors_list(quote_container)


# returns a soup object by parseing the response object into text formart
def parse_response_to_text_format(response):
    soup = BeautifulSoup(response.content, "lxml")
    return soup

# returns response object for the requested url
def get_response(url): 
    response = requests.get(url)
    return response

# web crawling starts by calling this function
def start_web_crawl(url):
    response = get_response(url)
    soup = parse_response_to_text_format(response)
    find_quote_containers_and_call_append_functions(soup)
    print("Scraping {} completed".format(response.url))
    next_page_url = get_next_page_url(soup) 
    if next_page_url != None:
        start_web_crawl(next_page_url)
    else:
        save_to_json_file(quotes_list, authors_list)
        return True

start_web_crawl(quotes_page_url)
print("Scraping completed successfully!")