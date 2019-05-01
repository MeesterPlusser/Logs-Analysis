# Log Analysis Project
Building an informative summary from logs, using python and psql that prints out reports (in plain text) based on the data in the database, using the psycopg2 module to connect to the database
## Getting started
These instructions will help you to run the project on your local computer. See deployment for notes on how to deploy the project on a live system 
## Prerequisites
Install virtual machine(vagrant), download the newsdata.sql file and psycopg2
### Installation and Execution
This project makes use of the Linux-based virtual machine (VM). This will give you the PostgreSQL database and support software needed for this project, use tools called Vagrant and VirtualBox to install and manage the VM. VirtualBox is the software that actually runs the virtual machine download it https://www.virtualbox.org/wiki/Downloads
Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem download it https://www.vagrantup.com/downloads.html
After the successful installation of vagrant run 
```
Vagrant --version
Vagrant 1.9.8
```
after that download the VM configuration and navigate to your vagrant directory using `cd`. Inside the vagrant directory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. 
When `vagrant up` is finished running, run `vagrant ssh` to log in to your newly installed Linux VM!
```
The shared directory is located at /vagrant
To access your shared files: cd /vagrant
Last login: Thu Apr 25 08:44:27 2019 from 10.0.2.2
vagrant@vagrant:~$
``` 
navigate to your vagrant by `cd /vagrant` you'll get the command line like
```
vagrant@vagrant:~$ cd /vagrant
vagrant@vagrant:/vagrant$
```
after that install the required python libraries psycopyg2(used to connect to the database). To install pip package in ubuntu try the given commands
```
sudo easy_install pip
	or
sudo apt-get install python-pip
```
it’s better to use sudo while installing any packages in ubuntu instead of `pip install psycopg2` use `sudo pip install psycopg2`
#### Download and load the data
Put newsdata.sql file into the vagrant directory, which is shared with our virtual machine. To load the data, cd into the vagrant directory and use the command 
```
psql -d news -f newsdata.sql
```
from the above command -d is used to connect to the database as `-d news`, -f is used to run the SQL statements in the file `-f newsdata.sql`. After loading the data in to our database we can connect to our database as mentioned `psql -d news or psql news`.
to list out the tables use \dt
```
news-> \dt
          List of relations
 Schema |   Name   | Type  |  Owner
--------+----------+-------+---------
 public | articles | table | vagrant
 public | authors  | table | vagrant
 public | log      | table | vagrant
(3 rows)
```
to list out particular table rows and columns use \d table
```
news-> \d authors
                         Table "public.authors"
 Column |  Type   |                      Modifiers
--------+---------+------------------------------------------------------
 name   | text    | not null
 bio    | text    |
 id     | integer | not null default nextval('authors_id_seq'::regclass)
Indexes:
    "authors_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "articles" CONSTRAINT "articles_author_fkey" FOREIGN KEY (author) REFERENCES authors(id)
```
similarly check for `\d articles, \d log`, after successfully loading data try to extract data from the database try some basic queries. Use ctrl+D to come out of it
#### Procedure
open a new python file in the vagrant directory save it as analysis.py and import psycopg2 module `import psycopg2` and after that use the .connect() to connect to our database
```
DBNAME = "news"
db = psycopg2.connect(database=DBNAME)
```
And create 3 different procedures for our requirement, define a cur to use it as a connecting object, .execute() to execute our query and .fetchall() to fetch all the rows and after print our required data and close the connection using .close() 
```cur = db.cursor()
   cur.execute(query)
   data = cur.fetchall()
   for row in data:
   		print(row[0], row[1])	#row[0] the count depends upon our columns 
   db.close()
```
As the program execution starts from main use the below commands or we can simply call our required function `top_three_articles()`
```
if __name__=='__main__':
    top_three_articles()
    popular_authors()
    error_percentage()
```
From the first query
``` 
q_1 = """select a.title, count(b.id) as views \
		from articles a \
		inner join log b on b.path = '/article/' || a.slug \
		group by a.title \
		order by count(b.id) desc \
		limit 3"""
```
q_2 = """select c.name, count(b.id) as views \
		from articles a \
		inner join log b on b.path = '/article/' || a.slug \
		inner join authors c on c.id = a.author \
		group by c.name \
		order by views desc""" 
```
q_3 = """select c.date, c.numof_requests, c.numof_errors, (c.numof_errors/c.numof_requests)*100 as perc_errors
		from (
			select a.dtlog as date, sum(a.requests) as numof_requests, sum(a.errors) as numof_errors
			from (
				select date(l1.time) as dtlog, count(l1.*) as requests, 0 as errors
				from log l1
				group by date(l1.time)
				union
				select date(l2.time) as dtlog, 0 as requests, count(l2.*) as errors
				from log l2
				where status != '200 OK'
				group by date(l2.time)
			) as a
			group by a.dtlog 
		) as c 
		where (c.numof_errors/c.numof_requests)*100 > 1 
		order by perc_errors desc"""
```
#### Run the program
save your file open your vm and type python analysis.py it runs your python program  we’ll get the list of outputs, check the output.txt file for results.
