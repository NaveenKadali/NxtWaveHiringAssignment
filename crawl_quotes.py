import re
import lxml
import json
import requests
from bs4 import BeautifulSoup

#saves quotes_list and authors_list into a json file
def save_to_json_file(quotes_list, authors_list):
    quotes_dictionary = {"quotes":quotes_list, 'authors':authors_list}
    json_data = json.dumps(quotes_dictionary,ensure_ascii=False ,indent=4)
    file = open('./quotes.json','w',encoding = 'utf-8')
    file.write(json_data)
    file.close()

#returns quote dictionaries list and author dictionaries list
def get_quotes_list_and_authors_list(quotes_page_scraped_data):
    quotes_list, authors_list = [],[]
    for quote_dictionary, author_dictionary in quotes_page_scraped_data:
        quotes_list.append(quote_dictionary)
        if author_dictionary not in authors_list:
            authors_list.append(author_dictionary)
    return  (quotes_list,authors_list)


#returns next page url if next page available else retuns None
def get_next_page_url(quotes_page_parsed_response):
    pager_element = quotes_page_parsed_response.find('ul',class_="pager") 
    next_page_list_element = pager_element.find('li', class_='next')
    if next_page_list_element != None:
        next_page_href = next_page_list_element.select_one('a', href=True)['href']
        next_page_url = "http://quotes.toscrape.com"+next_page_href
        return next_page_url
    else:
        return None

#returns author dictionary if already exists in the scraped data
def get_author_data_from_existing_authors(author_reference_url):
    quotes_and_authors_list = get_quotes_list_and_authors_list(quotes_page_scraped_data)
    authors_list = quotes_and_authors_list[1]
    for author_dictionary in authors_list:
        if author_dictionary['reference'] == author_reference_url:
            return author_dictionary
    else:
        return None

#returns a dictionary of author_name, born and reference url from reference page
def get_author_dictionary_from_author_page(author_reference_url):
    author_page_response = get_response(author_reference_url)
    author_page_parsed_response = get_parsed_response(author_page_response)
    author_name = author_page_parsed_response.find('h3',class_='author-title').text.strip()
    born_date = author_page_parsed_response.find('span',class_='author-born-date').text.strip()
    born_place = author_page_parsed_response.find('span',class_='author-born-location').text.strip()
    author_name = replace_speacial_characters_with_space(author_name)
    born = born_date +" "+ born_place.strip() 
    reference = author_page_response.url
    author_dictionary = { 'name':author_name, 'born':born, 'reference':reference}
    return author_dictionary


#returns a dictionary of author_name, born and reference url
def get_author_dictionary(author_reference_url):
    author_dictionary = get_author_data_from_existing_authors(author_reference_url)
    if author_dictionary is not None:
        return author_dictionary
    else:
        author_dictionary = get_author_dictionary_from_author_page(author_reference_url)
        return author_dictionary

#returns the author reference url  that quote
def get_author_reference_url(quote_container):
    author_href = quote_container.select_one('a')['href']
    author_reference_url = "http://quotes.toscrape.com"+author_href    
    return author_reference_url

#replaces the special charachters with spaces and returns the plane text
def replace_speacial_characters_with_space(text):
    replaced_text = re.sub("[^\w\s]", " ", text)
    replaced_text = " ".join(replaced_text.split())
    return replaced_text

#removes unicode values and returns the text
def remove_unicodes(text):
    text = text.encode("ascii","ignore")
    text = text.decode()
    return text

#returns a list of tags of the quote
def get_tags(tags_container):
    tags_list = [] 
    for tag_element in tags_container:
        tag = tag_element.text.strip()
        tags_list.append(tag)
    return tags_list

#returns a dictionary of quote, author and tags_list 
def get_quote_dictionary(quote_container):
    quote = quote_container.select_one('div .text').text.strip()
    author = quote_container.select_one('.author').text.strip()
    tags_container = quote_container.select('div .tag')
    tags_list = get_tags(tags_container)
    quote = remove_unicodes(quote)
    author = replace_speacial_characters_with_space(author)
    quote_dictionary = {"quote": quote, "author": author, "tags": tags_list}
    return quote_dictionary

#returns a list of touples with quote_dictionary and author_dictionary
def get_quotes_and_authors_data(quotes_page_parsed_response):
    quotes_and_authors_data = []
    quote_containers = quotes_page_parsed_response.find_all('div',class_= 'quote')
    for quote_container in quote_containers:
        quote_dictionary = get_quote_dictionary(quote_container)
        author_reference_url = get_author_reference_url(quote_container)
        author_dictionary = get_author_dictionary(author_reference_url)
        quotes_and_authors_data.append((quote_dictionary, author_dictionary))
    return quotes_and_authors_data
    
#returns parsed response for the given resposne object
def get_parsed_response(response):
    parsed_response = BeautifulSoup(response.content, "lxml")
    return parsed_response

#returns response object for the requested url
def get_response(url): 
    response = requests.get(url)
    return response

#scrapping starts from this function
def start_scraping_quotes_page():
    global quotes_page_scraped_data
    quotes_page_scraped_data = []
    quotes_page_url = "http://quotes.toscrape.com/"
    while quotes_page_url is not None:
        quotes_page_response = get_response(quotes_page_url)
        quotes_page_parsed_response = get_parsed_response(quotes_page_response) 
        quotes_page_scraped_data.extend(get_quotes_and_authors_data(quotes_page_parsed_response))
        quotes_page_url = get_next_page_url(quotes_page_parsed_response)
    quotes_list, authors_list = get_quotes_list_and_authors_list(quotes_page_scraped_data)
    save_to_json_file(quotes_list, authors_list)

start_scraping_quotes_page()
print("Scraping completed successfully!")