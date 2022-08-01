import json
import sqlite3
from textwrap import indent
file = open('./quotes.json','r')

quotes_data_dict = json.load(file) 

connection = sqlite3.connect('quote.db')
cursor = connection.cursor()

def drop_tables():
    cursor.execute('DROP TABLE IF EXISTS quote')
    cursor.execute('DROP TABLE IF EXISTS author')
    cursor.execute('DROP TABLE IF EXISTS quote_tag')

def create_tables():
    cursor.execute("CREATE TABLE quote (id INTEGER PRIMARY KEY AUTOINCREMENT, quote TEXT, author VARCHAR(255))")
    cursor.execute("CREATE TABLE author (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), born VARCHAR(250), reference VARCHAR(255)  )")
    cursor.execute("CREATE TABLE quote_tag ( id INTEGER PRIMARY KEY AUTOINCREMENT, tag VARCHAR(255), quote_id INTEGER, FOREIGN KEY(quote_id) REFERENCES quote(id))")

drop_tables()
create_tables()



def insert_to_quote_table(quote_id, quote, author):
    cursor.execute("""INSERT INTO quote VALUES(?,?,?)""",(quote_id,quote,author))

def insert_to_quote_tag(quote_id, tags_list):
    for tag in tags_list:
        cursor.execute('INSERT INTO quote_tag VALUES(?,?,?)',(None, tag,quote_id))


quote_id = 0
for quote_dict in quotes_data_dict['quotes']:
    quote = quote_dict['quote']
    author = quote_dict['author']
    tags_list = quote_dict['tags']
    insert_to_quote_table(quote_id, quote, author)
    insert_to_quote_tag(quote_id,tags_list)
    quote_id += 1



def insert_to_author(name, born, reference):
    cursor.execute("""INSERT INTO author VALUES (?,?, ?, ?)""",(None, name, born, reference))



for author_dict in quotes_data_dict['authors']:
    name = author_dict['name']
    born = author_dict['born']
    reference =  author_dict['reference']
    insert_to_author(name,born,reference)



cursor.execute('''select * from quote''')
def getAuthorDetails():
    print(f"AuthorId\tName\tBorn\treference" )
    for each in cursor.fetchall():
        print(each)

getAuthorDetails()

connection.commit()
connection.close