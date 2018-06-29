import psycopg2
"""this file contains function for 3 main queries that aggregate data from
newspaper database containing 3 main tables
->log table which contain the server log for each client
->articles table which contain each article name,slug,authod,title and id
->authors table which contain data for each author, his bio and id.
"""
'''database name from newspaper.sql file which initialize our
data base with it's initial values'''
DBNAME = "news"

'''the first query adds the sentenct '/article/' to the slug in articles table
to join it with path column in log table with like clause because some clients
wrong type the article name or an error occurs in uri so we compare the right
slug from articles table with the inappropriate one in log table then counting
each slugs' access to determine the most import psycopg2
this file contains function for 3 main queries that aggregate data from
newspaper database containing 3 main tables
->log table which contain the server log for each client
->articles table which contain each article name,slug,authod,title and id
->authors table which contain data for each author, his bio and id.
'''
'''database name from newspaper.sql file which initialize our
data base with it's initial values'''
DBNAME = "news"

'''the first query adds the sentenct '/article/' to the slug in articles table
to join it with path column in log table with like clause because some clients
wrong type the article name or an error occurs in uri so we compare the right
slug from articles table with the inappropriate one in log table then counting
each slugs' access to determine the most popular articles according to
it's access
'''


def send_query1():
    # connect to a database with name DBNAME
    try:
        db = psycopg2.connect(database=DBNAME)
        # get the cursor that writes query to the database
        c = db.cursor()
        try:
                # this prints out each slug and it's views
            c.execute("select articles.slug, count(log.path) "
                      # joining the two tables
                      "from log,articles "
                      # adding '/article/ to slug for comparison with path'
                      "where '/article/'||articles.slug "
                      # execute function sends the query to the database
                      "like log.path group by articles.slug "
                      "order by count(log.path) desc")
        except psycopg2.Error as e:
            raise Exception

    except psycopg2.Error as e:
        print("database doesn't exist")
    except Exception as e:
        print("query error!")
        """tell the database in which order should it groub the tables after
  joining then order them in descending way
  collect the returned data with fetchall method in cursor pointer"""
        views = c.fetchall()
    '''close the data base but the returned data still in c
    structue or(object)'''
    db.close()
    return views  # return fetched value to function call


def send_query2():
    # also if any error occurs notify user about that
    try:
        # connect to a database with name DBNAME
        db = psycopg2.connect(database=DBNAME)
        # get the cursor that writes query to the database
        c = db.cursor()
        try:
            # show the name and the sum of each author article view
            c.execute("select authors.name, sum(numviews.count) "
                      # with the table extracted from
                      "from authors, (select articles.slug, count(log.path) "
                      # logs and articles table containing each article views
                      "from log,articles "  # joining log and articles tables
                      # add '/article/' to slug for comparison with path in log
                      "where '/article/'||articles.slug "
                      # compare the two values in order
                      "like log.path group by articles.slug "
                      "order by count(log.path) desc)as numviews,articles "
                      # to join the tables numviews which contains each
                      # article views and articles
                      # add some constrains to get the slug author and join
                      # it with the slug views
                      "where articles.slug=numviews.slug "
                      "and articles.author=authors.id "
                      # execute the query
                      "group by authors.name "
                      "order by sum(numviews.count) desc")
        except psycopg2.Error as e:
            raise Exception
    except psycopg2.Error as e:
        print("database doesn't exist")
    except Exception as e:
        print("query error!")

    '''this groub the two columns with authors name ordered by number
    of views for each author'''
    '''collect the returned data with fetchall method in cursor pointer'''
    view = c.fetchall()
    '''close the data base but the returned data still in c structue
    or(object)'''
    db.close()
    return view


def send_query3():
    # also if any error occurs notify user about that
    try:
        # connect to a database with name DBNAME
        db = psycopg2.connect(database=DBNAME)
        c = db.cursor()  # get the cursor that writes query to the database
        try:
            '''convert the time to PST form in and round the error value for
            5 digits after the decimal point'''
            c.execute("select to_char(time,'Mon DD,YYYY'), "
                      "trunc(err::numeric,5) ||'%' as requesterrors "
                      "from ( "
                      # this subquery allow data base to
                      "select log.time::date,"
                      "sum(case when log.status!='200 OK' then 1 end)::float "
                      # count all errors and all accesses in log table for
                      # each day
                      "/sum(case when log.method='GET' then 1 end)::float*100 "
                      "::float as err "
                      # groub the data by time of each access
                      "from log group by log.time::date "
                      # order the data by time
                      "order by log.time::date)as result "
                      # select the value where the error > 1%
                      "where err > 1")
        except psycopg2.Error as e:
            raise Exception
    except psycopg2.Error as e:
        print("database doesn't exist")
    except Exception as e:
        print("query error!")
    '''collect the returned data with fetchall method in cursor pointer'''
    view = c.fetchall()
    '''close the data base but the returned data still in c structue
    or(object)'''
    db.close()
    return view


# popular articles according to it's access
def send_query1():
    # connect to a database with name DBNAME
    db = psycopg2.connect(database=DBNAME)
    # get the cursor that writes query to the database
    c = db.cursor()
    # this prints out each slug and it's views
    c.execute("select articles.slug, count(log.path) "
              # joining the two tables
              "from log,articles "
              # adding '/article/ to the slug in order of comparison with path'
              "where '/article/'||articles.slug "
              # execute function sends the query to the database
              "like log.path group by articles.slug "
              "order by count(log.path) desc")
    # tell the data base in which order should it groub the tables after
    # joining then order them in descending way
    # collect the returned data with fetchall method in cursor pointer
    views = c.fetchall()
    # close the data base but the returned data still in c structue or(object)
    db.close()
    return views  # return fetched value to function call


def send_query2():
    # connect to a database with name DBNAME
    db = psycopg2.connect(database=DBNAME)
    # get the cursor that writes query to the database
    c = db.cursor()
    # show the name and the sum of each author article view
    c.execute("select authors.name, sum(numviews.count) "
              # with the table extracted from
              "from authors, (select articles.slug, count(log.path) "
              # logs and articles table containing each article views
              "from log,articles "  # joining the log and articles tables
              # add '/article/' to slug to compare it with path in log table
              "where '/article/'||articles.slug "
              # compare the two values in order
              "like log.path group by articles.slug "
              "order by count(log.path) desc)as numviews,articles "
              # to join the tables numviews which contains each
              # article views and articles
              # add some constrains to get the slug author and join
              # it with the slug views
              "where articles.slug=numviews.slug "
              "and articles.author=authors.id "
              # execute the query
              "group by authors.name order by sum(numviews.count) desc")
    # this groub have two columns with authors name ordered by number of views
    # collect the returned data with fetchall method in cursor pointer
    view = c.fetchall()
    # close the data base but the returned data still in c structue or(object)
    db.close()
    return view


def send_query3():
    # connect to a database with name DBNAME
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()  # get the cursor that writes query to the database
    # convert time to PST form & round the err to 5-digits after decimal point
    c.execute("select to_char(time,'Mon DD,YYYY'), "
              "trunc(err::numeric,5) ||'%' as requesterrors "
              "from ( "
              # this subquery allow data base to
              "select log.time::date,"
              "sum(case when log.status!='200 OK' then 1 end)::float "
              # count all error and successful access of each day in log table
              "/ sum(case when log.method='GET' then 1 end)::float *100 "
              "::float as err "
              # groub the data by time of each access
              "from log group by log.time::date "
              # order the data by time
              "order by log.time::date)as result "
              # select the value where the error > 1%
              "where err > 1")
    # collect the returned data with fetchall method in cursor pointer
    view = c.fetchall()
    # close the database but returned data still in structue or object
    db.close()
    return view
