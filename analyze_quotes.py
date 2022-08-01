import json
import sqlite3

connection = sqlite3.connect('./quote.db')
cursor = connection.cursor()

# function to retun count of quotes in the table
def get_quotes_count():
    quotes_count_query = """SELECT count(*) FROM quote""" 
    cursor.execute(quotes_count_query) 
    quotes_count = cursor.fetchone()
    return quotes_count[0]

# function to return no_of_quotes authorised by author
def get_quotes_count_by_author(author):
    quotes_count_by_author_query="""
        select 
            count(*) as count 
        from 
            quote 
        where author = ? """
    cursor.execute(quotes_count_by_author_query, (author,))
    result = cursor.fetchone()
    return result[0]

# function to return min, max and avg tags count 
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

# function to return t 
def get_top_n_Authors(N):
    query = """
    select
        author.name, count(*) as no_of_quotes 
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


# function to call all the functions and to print the result
def print_responses():

    
    quotes_count = get_quotes_count()
    print("\nNumber of quotes on the website are: {}\n".format(quotes_count))
    
    # Below print statements is to print data returned get_quotes_count_by_author() function
    author = 'Albert Einstein'
    no_of_quotes_by_author = get_quotes_count_by_author(author)
    print("Number of quotations authored by {} are: {}\n".format(author,no_of_quotes_by_author))

    # Below statements is to print the data returned by min_max_and_avg() function
    result = get_min_max_avg_tags_count()
    print("Minimum, Maximum and Average no.of tags: {}, {}, {}\n".format(result[0], result[1], result[2]))

    # Below statemnets are to print the data returned by get_top_n_Authors function.
    topAuthorsList = get_top_n_Authors(5)
    for each in topAuthorsList:
        name = each[0]          # this variable stores author_name
        no_of_quotes = each[1]  # this variable stores author_no_of_quotes
        print("Name: {} \tNo_of_quotes: {}".format(name,no_of_quotes))

print_responses() 