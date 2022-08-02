import json
import sqlite3

with open('./quotes.json','r') as json_file:
    quotes_data = json.load(json_file) 

# creates a quote tabele to maintain quote and author name
def create_quote_table():
    cursor.execute("""DROP TABLE IF EXISTS quote""") # deletes table if exists
    create_quote_table_query = """
        CREATE TABLE 
            quote (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                quote TEXT, author VARCHAR(255)
            )"""
    cursor.execute(create_quote_table_query)

# creates an author table in the database to maintain author name, born detials and reference url
def create_author_table():
    cursor.execute("""DROP TABLE IF EXISTS author""") # deletes table if exists
    create_author_table_query = """
        CREATE TABLE 
            author (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255),
                born VARCHAR(250),
                reference VARCHAR(255)
            )"""
    cursor.execute(create_author_table_query)

# creates a quote_tag table to maintain quote_id and corresponding tags
def create_quote_tag_table():
    cursor.execute("""DROP TABLE IF EXISTS quote_tag""") #deletes table if exists
    create_quote_tag_table_query = """
        CREATE TABLE 
            quote_tag (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag VARCHAR(255),
                quote_id INTEGER NOT NULL, 
                FOREIGN KEY(quote_id) REFERENCES quote(id)
            )"""
    cursor.execute(create_quote_tag_table_query) 

# inserts quote and author name into the quote table
def insert_into_quote_table():
    for quote_dict in quotes_data['quotes']:
        quote = quote_dict['quote']
        author = quote_dict['author']
        insert_into_quote_query = """INSERT INTO quote VALUES(?,?,?)"""
        cursor.execute(insert_into_quote_query,(None,quote,author)) 

# inserts author name, born details and reference url into author table
def insert_into_author_table():
    for author_dict in quotes_data['authors']:
        name = author_dict['name']
        born = author_dict['born']
        reference =  author_dict['reference']
        insert_into_author_query = """INSERT INTO author VALUES (?,?, ?, ?)"""
        cursor.execute(insert_into_author_query,(None, name, born, reference))

# inserts quote_id and corresponding tags into the quote_tag table
def insert_into_quote_tag_table():
    quote_id = 0
    for quote_dictionary in quotes_data['quotes']:
        tags_list = quote_dictionary['tags']
        for tag in tags_list:
            insert_into_tag_query = """INSERT INTO quote_tag VALUES(?,?,?)"""
            cursor.execute(insert_into_tag_query,(None, tag,quote_id))
        quote_id += 1


connection = sqlite3.connect('quotes.db')
cursor = connection.cursor()

create_quote_table()            # function declaration starts at line 5
create_author_table()           # function declaration starts at line 15
create_quote_tag_table()        # function declaration starts at line 28
insert_into_quote_table()       # function declaration starts at line 41
insert_into_author_table()      # function declaration starts at line 49
insert_into_quote_tag_table()   # function declaration starts at line 59

connection.commit()
connection.close

print("Organizing data into quuotes.db completed successfully!")