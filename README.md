# :exclamation:logs-analysis-tool:anger:

#**Database content**
this is a tool to aggregate important data from live database using psycopg2 with PostgreSQL database

# **required tools to run this program**:umbrella:
* Vagrant [Vagrant 1.9.2 .msi](https://releases.hashicorp.com/vagrant/1.9.2/)
* VirtualBox [Virualbox 5.1.38-win.exe](https://download.virtualbox.org/virtualbox/5.1.38/)
* postgres python library on linux shell with pip command

# SETUP & RUN :frog:
  * **1-** you need to setup virtualbox then vagrent and run the terminal (of GIT is prefered [GIT BASH](https://git-scm.com/downloads))
  * **2-** to establish ubuntu os on vagrant machine by following [this link](https://app.vagrantup.com/ubuntu/boxes/trusty64)
  * **3-** then we need to run ubuntu first we turn vagrant on with this command in Git command Shell```vagrant up``` and run the vm with this command ```vagrant ssh``` 
  * **4-** now we typing on ubuntu shell throw git shell also if you want to switch back to git command shell you need to press ctl+z
  * **5-** setup postgres library with python using this command on vagrant shell ```sudo pip install psycopg2``` ***note** after login to ubuntu vagrant 
  * **6-** now we need to load the newspaper.sql file to news database with this command ```psql -d news -f newsdata.sql ```
  * **7-** then login to th news data base and run the folloing queries to test it then run python code  to get the data printed out in an appropriate way

## :star2:tables contained:star2:

### log table:running:

this table record the server logs with each client access also this table contains
  * **path**    contain path of article that the client access [foreign key]
  * **ip**      contain ip address that connects to the server
  * **method**  contain the method connection whether it is GET,POST,....
  * **status**  contain the state of connection between server and client whether it is 200 OK or 404 NOTFOUN ,.....
  * **time**    contain the time of each access 
  * **ID**      contain the id number of each connection [primary key]

### articles table:couple:

this table contain the data of each article that is written by each user, this data is contained in the following columns
  * **author**  contain the id number of each author in the authors table [foreign key]
  * **title**   contain the title of each article
  * **slug**    contain a short slug of each article that describes it's content [primary key]
  * **lead**    describes the heading of the entry of each article
  * **body**    the body of each article
  * **time**    the time when this article is written
  * **ID**      specific for each article

### authors table:walking:

this table contain the data about each author who had written or upload the article, this table has columns
  * **name**    contain the name of each author 
  * **ID**      contain the id of each author [primary key]
  * **BIO**     contain the bio of each author
  
  
# **this database is meant to analyse the log table and specify :**
## the most popular articles:metal:
this query add **'/article/'** to slug in the articles table and then join this table with log table groubed by slug and ordered by logs count then count the reputation of each path that is like the corresponding slug in articles table then print the numbers in descend ing order

```
select articles.slug, count(log.path) from log,articles where '/article/'||articles.slug like log.path group by articles.slug order by count(log.path) desc;
```
## the most popular authors:point_up_2:
this query can be extracted from the first query with create view clause or as a single line stand alone query such a query is implemented by joining the ordered number of views of each article to each author from it's id in articles table specicially author column
```
select authors.name, sum(numviews.count) from authors, (select articles.slug, count(log.path) from log,articles where '/article/'||articles.slug like log.path group by articles.slug order by count(log.path) desc)as numviews,articles where articles.slug=numviews.slug and articles.author=authors.id group by authors.name order by sum(numviews.count) desc;
```
## the error percentage in one day that exceeds 1%:fu:
the last query is using subquery methodology to use it's result to extract it's result which contain the value of errors during a day which later in this query will be constrained to a value that exceeds 1% error during a day
```
select to_char(time,'Mon DD,YYYY'),trunc(err::numeric,5) ||'%' as requesterrors from (select log.time::date,sum(case when log.status!='200 OK' then 1 end)::float / sum(case when log.method='GET' then 1 end)::float *100 ::float as err from log group by log.time::date order by log.time::date)as result where err > 1;
```
