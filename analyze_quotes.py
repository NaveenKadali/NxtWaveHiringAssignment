import json
import sqlite3

connection = sqlite3.connect('./quote.db')
cursor = connection.cursor()

# retuns count of quotes in the table
def get_quotes_count():
    quotes_count_query = """SELECT count(*) FROM quote""" 
    cursor.execute(quotes_count_query) 
    query_result = cursor.fetchone()
    return query_result[0]

# returns no_of_quotes authorised by a author
def get_quotes_count_by_author(author):
    quotes_count_by_author_query="""
        SELECT 
            COUNT(*) as count 
        FROM
            quote 
        WHERE author = ? """
    cursor.execute(quotes_count_by_author_query, (author,))
    query_result = cursor.fetchone()
    return query_result[0]

# returns a tuple of min, max and avg tags count 
def get_min_max_avg_tags_count():
    aggrigations_on_tags_query = """
        SELECT 
            MIN(tags_count), MAX(tags_count), AVG(tags_count) 
        FROM (
            SELECT 
                count(*) as tags_count 
            FROM 
                quote_tag 
            GROUP BY 
                quote_id); """
    cursor.execute(aggrigations_on_tags_query);
    query_result = cursor.fetchone()
    return query_result

# returns a list of top n authors
def get_top_n_authors(n):
    top_n_authors_query = """
        SELECT 
            author 
        FROM (
            SELECT 
                author, count(*) as no_of_quotes 
            FROM 
                quote 
            GROUP BY 
                author 
            ORDER BY 
                no_of_quotes desc
            ) 
        LIMIT ?;"""
    cursor.execute(top_n_authors_query,(n,))
    query_result = cursor.fetchall()
    return query_result

# function calls 
quotes_count = get_quotes_count()
no_of_quotes_by_author = get_quotes_count_by_author('Albert Einstein')
min_max_avg_tags = get_min_max_avg_tags_count() 
top_n_authors_list = get_top_n_authors(5)

print(quotes_count)
print(no_of_quotes_by_author)
print(min_max_avg_tags)
print(top_n_authors_list)