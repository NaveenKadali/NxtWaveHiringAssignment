import json
import sqlite3

connection = sqlite3.connect('./quotes.db')
cursor = connection.cursor()

def get_most_used_tag_by_author(author_name):
    most_used_tag_query = """SELECT tag.tag FROM tag 
        INNER JOIN  quote_tag ON tag.id = quote_tag.tag_id
        INNER JOIN quote ON quote_tag.quote_id = quote.id 
        INNER JOIN author ON quote.author_id = author.id 
        WHERE author.name = ? 
        GROUP BY tag.tag 
        ORDER BY count(tag.tag) 
        DESC LIMIT 1;"""
    query_result = execute_query(most_used_tag_query,author_name)
    return query_result[0][0]

# executes the given query and returns the query result
def execute_query(query,*args):
    cursor_object = cursor.execute(query,args)
    query_result = cursor_object.fetchall()
    return query_result

#retuns total no of quotes in the table
def get_quotes_count():
    quotes_count_query = """SELECT count(id) FROM quote""" 
    query_result = execute_query(quotes_count_query)
    return query_result[0][0]

#returns no_of_quotes authorised by a author
def get_quotes_count_by_author(author):
    quotes_count_by_author_query="""SELECT COUNT(quote.id) as count 
        FROM quote INNER JOIN author ON quote.author_id = author.id 
        WHERE author.name = ? """
    query_result = execute_query(quotes_count_by_author_query, author)
    return query_result[0][0]

#returns a tuple of min, max and avg tags count 
def get_min_max_avg_count_of_tags():
    min_max_avg_tags_query = """SELECT MIN(tags_count), MAX(tags_count), ROUND(AVG(tags_count)) 
        FROM (
            SELECT count(quote_id) as tags_count FROM quote_tag GROUP BY quote_id 
            );"""
    query_result = execute_query(min_max_avg_tags_query);
    return query_result[0]

#returns a list of top n authors
def get_top_n_authors(n): 
    top_n_authors_query = """SELECT name from author inner join quote on author.id = quote.author_id 
    group by author.id order by count(quote.id) desc limit ? """
    query_result = execute_query(top_n_authors_query,n,)
    return query_result

# function calls
N = 5
author = 'Albert Einstein'
quotes_count = get_quotes_count()
no_of_quotes_by_author = get_quotes_count_by_author(author)
min_max_avg_tags = get_min_max_avg_count_of_tags() 
top_n_authors_list = get_top_n_authors(5)
most_used_tag_by_author = get_most_used_tag_by_author(author)

# print 
print("Total no.of quotes : ",quotes_count)
print("no.of quotes authored by {}: {}".format(author,no_of_quotes_by_author))
print("Min, Max and Avg tags on quotations: ", end="")
print(min_max_avg_tags[0],"|",min_max_avg_tags[1],"|",min_max_avg_tags[2])
print("Top {} authors is: ".format(N),end = "")
for author in top_n_authors_list:
    print(author[0],end=", ")
print("\nMost used tag by author are:",most_used_tag_by_author)