import json
import sqlite3
from unittest import result

with open('./quotes.json','r') as json_file:
    quotes_data = json.load(json_file)

authors_list = quotes_data['authors']
quotes_list = quotes_data['quotes']

connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

author_table_query = """CREATE TABLE author (
         id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), 
         born VARCHAR(255), reference VARCHAR(255)
         )"""
quote_table_query = """CREATE TABLE quote (
        id INTEGER PRIMARY KEY AUTOINCREMENT, quote TEXT, 
        author_id INTEGER NOT NULL, FOREIGN KEY(author_id) REFERENCES author(id)
        )"""
tag_table_query = """CREATE TABLE tag (
        id INTEGER PRIMARY KEY AUTOINCREMENT, tag VARCHAR(255), 
        quote_id INTEGER NOT NULL, FOREIGN KEY(quote_id) REFERENCES quote(id)
        )""" 

#executes the given query and returns the cursor object
def execute_query(query,*args):
    cursor_object = cursor.execute(query,args)
    return cursor_object

#  returns quote_id of given quote
def get_quote_id(quote):
    get_quote_id_query = """SELECT id from quote WHERE quote = ?"""
    cursor_object = execute_query(get_quote_id_query,quote)
    author_id = cursor_object.fetchone()
    return author_id[0]

# returns author_id of given author
def get_author_id(author_name):
    get_author_id_query = "SELECT id from author WHERE name = '{}'".format(author_name)
    cursor_object = execute_query(get_author_id_query)
    author_id = cursor_object.fetchone()
    return author_id[0]

#iterates over all the quote dictionaries
def insert_into_tag_table(quote_dictionary):
    quote = quote_dictionary['quote']
    quote_id = get_quote_id(quote)
    tags_list = quote_dictionary['tags']
    for tag in tags_list:
        execute_query("INSERT INTO tag VALUES(?,?,?)",None,tag, quote_id)

# inserts quote, author_id into quote table
def insert_into_quote_table(quotes_list):
    insert_into_quote_query = """INSERT INTO quote VALUES(?,?,?)"""
    for quote_dictionary in quotes_list:
        quote, author_name, tags_list = quote_dictionary.values()
        author_id = get_author_id(author_name)
        execute_query(insert_into_quote_query,None, quote, author_id)

# inserts_author_data into author table
def insert_into_author_table(authors_list):
    insert_into_author_query = """INSERT INTO author VALUES (?,?, ?, ?)"""
    for author_dictionary in authors_list:
        author_name, author_born, reference_url = author_dictionary.values()
        execute_query(insert_into_author_query,None, author_name, author_born, reference_url)

# creates the tables author, quote, quote_tag in quotes.db
def create_tables(*create_table_queries):
    for create_table_query in create_table_queries:
        execute_query(create_table_query)

# deletes existing tables from the database
def delete_tables(*table_names):
    for table_name in table_names:
        execute_query("DROP TABLE IF EXISTS {}".format(table_name))


delete_tables("author","quote","tag")
create_tables(author_table_query, quote_table_query,tag_table_query)
insert_into_author_table(authors_list)
insert_into_quote_table(quotes_list)
for quote_dictionary in quotes_list:
    insert_into_tag_table(quote_dictionary)

connection.commit()
connection.close

print("Organizing data into quotes.db completed successfully!")
