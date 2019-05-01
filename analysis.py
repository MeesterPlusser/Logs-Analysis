# !/usr/bin/env python3

import psycopg2

DBNAME = "news"
db = psycopg2.connect(database=DBNAME)

def top_three_articles():
	print('What are the most popular three articles of all time?')
	q1 = """select a.title, count(b.id) as views \
		from articles a \
		inner join log b on b.path = '/article/' || a.slug \
		group by a.title \
		order by count(b.id) desc \
		limit 3"""
	cur.execute(q1)
	r1 = cur.fetchall()
	for row in r1:
		print ("%s -- %s views" % (row[0], row[1]))
	print
	
def popular_authors():
	print('Who are the most popular article authors of all time?')
	q2 = """select c.name, count(b.id) as views \
		from articles a \
		inner join log b on b.path = '/article/' || a.slug \
		inner join authors c on c.id = a.author \
		group by c.name \
		order by views desc""" 
		
	cur.execute(q2)
	r2 = cur.fetchall()
	for row in r2:
		print("%s -- %s views" % (row[0], row[1]))
	print

def error_percentage():
	print('On which days did more than 1% of requests lead to errors?')
	query_3 = """select c.date, c.numof_requests, c.numof_errors, (c.numof_errors/c.numof_requests)*100 as perc_errors
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
	cur.execute(query_3)
	r3 = cur.fetchall()
	for row in r3:
		print("%s -- %s requests -- %s errors -- (%.2f%%)" % (row[0], row[1], row[2], row[3]))
	print
	
if __name__ == '__main__':
	cur = db.cursor()

	top_three_articles()
	popular_authors()
	error_percentage()

	db.close()