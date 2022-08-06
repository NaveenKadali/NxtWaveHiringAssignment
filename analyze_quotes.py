import json
import sqlite3

connection = sqlite3.connect('./quotes.db')
cursor = connection.cursor()

#executes the given query and returns the query result
def execute_query(query,*args):
    cursor_object = cursor.execute(query,args)
    return cursor_object.fetchall()

#retuns total no of quotes in the table
def get_quotes_count():
    quotes_count_query = """SELECT count(id) FROM quote""" 
    query_result = execute_query(quotes_count_query)
    return query_result[0]

#returns no_of_quotes authorised by a author
def get_quotes_count_by_author(author):
    quotes_count_by_author_query="""SELECT COUNT(quote.id) as count 
        FROM quote INNER JOIN author ON quote.author_id = author.id 
        WHERE author.name = ? """
    query_result = execute_query(quotes_count_by_author_query, author)
    return query_result[0]

#returns a tuple of min, max and avg tags count 
def get_min_max_avg_count_of_tags():
    min_max_avg_tags_query = """SELECT 
    MIN(tags_count), MAX(tags_count), ROUND(AVG(tags_count))
    FROM ( SELECT COUNT(id) as tags_count FROM tag GROUP BY quote_id);"""
    query_result = execute_query(min_max_avg_tags_query);
    return query_result[0]

#returns a list of top n authors
def get_top_n_authors(n):
    top_n_authors_query = """SELECT name from author inner join quote on author.id = quote.author_id 
    group by author.id order by count(quote.id) desc limit ? """
    query_result = execute_query(top_n_authors_query,n,)
    return query_result

# function calls 
quotes_count = get_quotes_count()
no_of_quotes_by_author = get_quotes_count_by_author('Albert Einstein')
min_max_avg_tags = get_min_max_avg_count_of_tags() 
top_n_authors_list = get_top_n_authors(5)

print(quotes_count)
print(no_of_quotes_by_author)
print(min_max_avg_tags)
print(top_n_authors_list) 