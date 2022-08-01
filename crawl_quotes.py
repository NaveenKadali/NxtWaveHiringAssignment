#from email.quoprimime import quote
#from re import A, L
#from typing import Container
import lxml
import json
#from pytest import console_main
import requests
from time import sleep
from bs4 import BeautifulSoup


def getTagNames(tag_elements):
    tagNames = []
    for element in tag_elements:
        tagName = element.text.strip()
        tagNames.append(tagName)
    return tagNames


def getAuthorDetailsDictionary(author_href):
    reference = url.strip('/')+author_href
    response = requests.get(reference)
    soup = BeautifulSoup(response.text, "lxml")
    Author_name = soup.select_one('.author-title').text.strip()
    born_date = soup.select_one('.author-born-date').text.strip()
    born_place = soup.select_one('.author-born-location').text.strip()
    born = born_date +" "+ born_place
    reference = response.url
    return { 'name':Author_name, 'born':born, 'reference':reference}


def getQuoteDictionary(quoteContainer):
    quote = quote_container.select_one('div .text').text.strip()
    author = quote_container.select_one('.author').text.strip()
    tag_elements = (quote_container.select('div .tag'))
    tags = getTagNames(tag_elements) # function to get tag names / declared above this function
    return {"quote": quote, "author": author, "tags": tags}



# Exicution Starts from here

url = "http://quotes.toscrape.com/" # Quotes to Screape url
quotes_list = list() # Empty list to store quote data
authors_list = list() # Empty list to store authors data


def getQuotes():
    global quote_containers
    global quote_container
    quote_containers = soup.select('div .quote')
    for quote_container in quote_containers:
        quote_dictionary = getQuoteDictionary(quote_container)
        author_href = quote_container.select_one('a')['href']
        authorDetailsDictionary = getAuthorDetailsDictionary(author_href)
        quotes_list.append(quote_dictionary)
        if authorDetailsDictionary not in authors_list :
            authors_list.append(authorDetailsDictionary)


# function to request webcontent for given url
def getResponse(url): 
    global response
    response = requests.get(url)
    global soup
    soup = BeautifulSoup(response.text, "html.parser")

getResponse(url)

getQuotes()

def check_for_next_page():
    next_page_element = soup.find('li', class_='next')
    if next_page_element != None:
        anchor_element = next_page_element.select_one('a', href=True)
        href = anchor_element['href'].strip('/')
        return href
    else:
        return False


def saveToFile():
    pass

'''
while True:
    href = check_for_next_page()
    if href == False:
        break
    else:
        getResponse(url+href)
        getQuotes()
'''


quotes_dictionary = {"quotes":quotes_list, 'authors':authors_list}
json_data = json.dumps(quotes_dictionary, indent=4)
file = open('./quotes.json','w')
file.write(json_data)
file.close()
