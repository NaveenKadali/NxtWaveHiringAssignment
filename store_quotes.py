import json
import sqlite3
from unittest import result

connection = sqlite3.connect("quotes.db")
cursor = connection.cursor()
with open("./quotes.json","r") as json_file:
    quotes_data = json.load(json_file)

# executes the given query and returns the cursor object
def execute_query(query,*parameters):
    cursor_object = cursor.execute(query,parameters)
    return cursor_object.fetchall()

# inserts quote_id and tag_id into quote_tag junction table
def insert_into_quote_tag_table(quote, tags_list):
    insert_query = """INSERT INTO quote_tag(quote_id,tag_id) VALUES (?,?);"""
    quote_ids = dict(execute_query("""SELECT quote, id from quote;"""))
    tag_ids = dict(execute_query("""SELECT tag, id from tag;"""))
    quote_id = quote_ids.get(quote)
    for tag in tags_list:
        tag_id = tag_ids.get(tag)
        execute_query(insert_query, quote_id, tag_id)

# inserts tag_id and tag into tag table
def insert_into_tag_table(tags_list):
    insert_query = "INSERT INTO tag(tag) VALUES(?)"
    for tag in tags_list:
        execute_query(insert_query,tag)

# inserts quote, author_id into quote table
def insert_into_quote_table(quotes_list):
    author_ids = dict(execute_query("SELECT name, id FROM author;"))
    insert_query = """INSERT INTO quote(quote, author_id) VALUES(?,?)"""
    for quote_dictionary in quotes_list:
        quote, author_name = quote_dictionary["quote"], quote_dictionary["author"]
        author_id = author_ids[author_name]
        execute_query(insert_query,  quote, author_id)

# inserts author_data into author table
def insert_into_author_table(authors_list):
    insert_query = """INSERT INTO author(name,born,reference) VALUES (?, ?, ?)"""
    for author_dictionary in authors_list:
        author_name, author_born, reference_url = author_dictionary.values()
        execute_query(insert_query,author_name, author_born, reference_url)

# creates quote_tag juction table with quote_id and tag_id columns
def create_quote_tag_table():
    create_quote_tag_junction_table_query = """CREATE TABLE quote_tag (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        quote_id INTEGER NOT NULL, 
        tag_id INTEGER NOT NULL,
        FOREIGN KEY (quote_id) REFERENCES quote(id) ON DELETE CASCADE,
        FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
        ) """
    execute_query(create_quote_tag_junction_table_query)

# creates tag table with id, tag columns
def create_tag_table():
    create_tag_table_query = """CREATE TABLE tag (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        tag VARCHAR(255) NOT NULL UNIQUE
        )""" 
    execute_query(create_tag_table_query)

# creates quote table with id, quote, author_id columns
def create_quote_table():
    create_quote_table_query = """CREATE TABLE quote (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
        quote TEXT, 
        author_id INTEGER NOT NULL, 
        FOREIGN KEY(author_id) REFERENCES author(id) ON DELETE CASCADE
        )"""
    execute_query(create_quote_table_query)

# creates author table with id, name, born and reference columns
def create_author_table():
    create_author_table_query = """CREATE TABLE author (
         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
         name VARCHAR(255), 
         born VARCHAR(255), 
         reference VARCHAR(255)
         )"""
    execute_query(create_author_table_query)

# deletes existing tables from the database
def delete_existing_tables(*table_names):
    for table_name in table_names:
        execute_query("DROP TABLE IF EXISTS {}".format(table_name))

# retuns a list of all unique tags
def get_all_unique_tags(quotes_list):
    tags_list = []
    for quote_dictionary in quotes_list:
        tags_list.extend(quote_dictionary["tags"])
    tags_list = list(set(tags_list))
    return sorted(tags_list)

# organizing data into quotee.db starts from this function
def organize_quotes_data_into_db():
    authors_list = quotes_data["authors"]
    quotes_list = quotes_data["quotes"]
    tags_list = get_all_unique_tags(quotes_list)
    delete_existing_tables("author","quote","tag","quote_tag")
    create_author_table()
    create_quote_table()
    create_tag_table()
    create_quote_tag_table()
    insert_into_author_table(authors_list) 
    insert_into_quote_table(quotes_list)
    insert_into_tag_table(tags_list)
    for quote_dictionary in quotes_list:
        quote, tags_list = quote_dictionary["quote"], quote_dictionary["tags"]
        insert_into_quote_tag_table(quote,tags_list)

organize_quotes_data_into_db()
connection.commit()
connection.close
 
print("Organizing data into quotes.db completed successfully!")