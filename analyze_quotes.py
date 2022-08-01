import json
import sqlite3


connection = sqlite3.connect('./quote.db')
cursor = connection.cursor()

def get_quotes_count():
    quotes_count_query = """SELECT count(*) FROM quote""" 
    cursor.execute(quotes_count_query) 
    quotes_count = cursor.fetchone()
    return quotes_count[0]


def get_quotes_count_by_author(author):
    cursor.execute('''select count(*) as count from quote where author = ?''', (author,))
    result = cursor.fetchone()
    return result[0]


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
  

def get_top_n_Authors(N):
    query = """
    select
        author.id, author.name, count(*) as no_of_quotes 
    from
        author inner join quote on author.name = quote.author 
    group by
         author.id 
    order by 
        no_of_quotes desc 
    limit ? ;"""
    cursor.execute(query,(N,))
    result = cursor.fetchall()
    return result








# function to call functions and t o print the response
def print_responses():

    #Below startements is print data returned by get_quotes_count function
    quotes_count = get_quotes_count()
    print("\nNumber of quotes on the website are: {}\n".format(quotes_count))
    
    # Below print statements is to print data returned get_quotes_count_by_author() function
    author = 'Albert Einstein'
    print("Number of quotations authored by {} are: {}\n".format(author, get_quotes_count_by_author(author)))

    # Below statements is to print the data returned by min_max_and_avg() function
    result = get_min_max_avg_tags_count()
    print("Minimum, Maximum and Average no.of tags: {}, {}, {}\n".format(result[0], result[1], result[2]))

    # Below statemnets are to print the data returned by get_top_n_Authors function.
    topAuthorsList = get_top_n_Authors(5)
    for each in topAuthorsList:
        id = each[0]            # this variable stores author_id 
        name = each[1]          # this variable stores author_name
        no_of_quotes = each[2]  # this variable stores author_no_of_quotes
        print("AuthorId: {} \tName: {} \tNo_of_quotes: {}".format(id,name,no_of_quotes))

print_responses() # function starts at line 67