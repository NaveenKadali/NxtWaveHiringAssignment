from ast import parse
from tracemalloc import start
import lxml
import json
import requests
from time import sleep
from bs4 import BeautifulSoup


def get_author_details(quote_container):
    about_author_href = quote_container.select_one('a')['href']
    author_url = quotes_page_url.strip('/')+about_author_href
    response = get_response(author_url)
    soup = parse_response_to_text_format(response)
    author_name = soup.find('h3',class_='author-title').text.strip()
    born_date = soup.find('span',class_='author-born-date').text.strip()
    born_place = soup.select_one('span',class_='author-born-location').text.strip()
    born = born_date +" "+ born_place
    reference = response.url
    return { 'name':author_name, 'born':born, 'reference':reference}

def get_tags(tags_container): # this function will return a list of tags
    tag_names = [] # Empty list for tag names
    for tag_element in tags_container:
        tag = tag_element.text.strip()
        tag_names.append(tag)
    return tag_names

def get_quote_data(quote_container):
    quote = quote_container.select_one('div .text').text.strip()
    author = quote_container.select_one('.author').text.strip()
    tags_container = quote_container.select('div .tag')
    tags_list = get_tags(tags_container) # function starts at line 22
    return {"quote": quote, "author": author, "tags": tags_list}


# Exicution Starts from here

quotes_page_url = "http://quotes.toscrape.com/" # Quotes to Screape url
quotes_list = list() # Empty list to store quote data
authors_list = list() # Empty list to store authors data


def parse_response_to_text_format(response):
    soup = BeautifulSoup(response.text, "lxml")
    return soup

def get_response(url): 
    response = requests.get(url)
    return response

def save_to_json_file():
    quotes_dictionary = {"quotes":quotes_list, 'authors':authors_list}
    json_data = json.dumps(quotes_dictionary, indent=4)
    file = open('./quotes.json','w')
    file.write(json_data)
    file.close()


def start_web_crawl(url):
    response = get_response(url)
    soup = parse_response_to_text_format(response)
    quote_containers = soup.find_all('div',class_= 'quote')
    for quote_container in quote_containers:
        quote_dictionary = get_quote_data(quote_container)
        author_dictionary = get_author_details(quote_container)
        quotes_list.append(quote_dictionary)
        if author_dictionary not in authors_list :
            authors_list.append(author_dictionary)
    next_page_element = soup.find('li', class_='next')
    if next_page_element != None:
        next_page_href = next_page_element.select_one('a', href=True)['href']
        next_page_url = quotes_page_url+next_page_href
        start_web_crawl(next_page_url)
    else:
        save_to_json_file()
        return False
        

start_web_crawl(quotes_page_url)
