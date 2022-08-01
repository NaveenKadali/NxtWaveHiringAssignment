import json
import sqlite3

connection = sqlite3.connect('./quote.db')
cursor = connection.cursor()
view_tables_query = """SELECT name FROM sqlite_master WHERE type = 'table';"""


def get_quotes_count():
    quotes_count_query = """SELECT count(*) FROM quote""" 
    cursor.execute(quotes_count_query) 
    quotes_count = cursor.fetchone()
    return quotes_count

quoted_count = get_quotes_count()
print(quoted_count[0])


def get_quotes_count_by_author(author):
    cursor.execute('''select count(*) as count from quote where author = ?''', (author,))
    return cursor.fetchone()

author_quotes_count = get_quotes_count_by_author('Albert Einstein')
print(author_quotes_count)



aggrigations_on_tags_query = """
select 
    min(tags_count.count), max(tags_count.count), avg(tags_count.count)
from 
    (
    select
        count(*) as count 
    from 
        quote_tag 
    group by 
        quote_id
    ) 
    as tags_count;"""

def get_min_max_avg_tags_count():
    aggrigations_on_tags_query = """
    select 
        min(tags_count.count), max(tags_count.count), avg(tags_count.count)
    from 
    (
        select
            count(*) as count 
        from 
            quote_tag 
        group by 
            quote_id
    ) 
    as tags_count;"""
    
    cursor.execute(aggrigations_on_tags_query);
    result = cursor.fetchone()
    return result

query_result = get_min_max_avg_tags_count()
  



