import json
import sqlite3
file = open('./quotes.json','r')

quotes_data_dict = json.load(file) 

connection = sqlite3.connect('quote.db')
cursor = connection.cursor()

# this function will delete the existing tables in the database
def drop_tables():
    cursor.execute("""DROP TABLE IF EXISTS quote""")
    cursor.execute("""DROP TABLE IF EXISTS author""")
    cursor.execute("""DROP TABLE IF EXISTS quote_tag""")

# this function will create tables in the database
def create_tables():
    create_quote_table_query = """CREATE TABLE quote (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT, author VARCHAR(255))
        """
    create_author_table_query = """CREATE TABLE 
        author (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            born VARCHAR(250),
            reference VARCHAR(255)
            )"""
    create_quote_tag_table_query = """CREATE TABLE 
        quote_tag (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag VARCHAR(255),
            quote_id INTEGER, 
            FOREIGN KEY(quote_id) REFERENCES quote(id)
            )"""
    cursor.execute(create_quote_table_query)
    cursor.execute(create_author_table_query)
    cursor.execute(create_quote_tag_table_query)


def insert_to_quote_table(quote_id, quote, author):
    cursor.execute("""INSERT INTO quote VALUES(?,?,?)""",(quote_id,quote,author))

def insert_to_quote_tag(quote_id, tags_list):
    for tag in tags_list:
        cursor.execute('INSERT INTO quote_tag VALUES(?,?,?)',(None, tag,quote_id))

def insert_to_author(name, born, reference):
    cursor.execute("""INSERT INTO author VALUES (?,?, ?, ?)""",(None, name, born, reference))

drop_tables()
create_tables()

for author_dict in quotes_data_dict['authors']:
    name = author_dict['name']
    born = author_dict['born']
    reference =  author_dict['reference']
    insert_to_author(name,born,reference)

quote_id = 0
for quote_dict in quotes_data_dict['quotes']:
    quote = quote_dict['quote']
    author = quote_dict['author']
    tags_list = quote_dict['tags']
    insert_to_quote_table(quote_id, quote, author)
    insert_to_quote_tag(quote_id,tags_list)
    quote_id += 1


connection.commit()
connection.close