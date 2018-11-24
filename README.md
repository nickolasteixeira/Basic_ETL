# Alooma CSE/DSE Challenge


## Extracting Data
Pull Data from Hubspot. Using their API and Python, build out logic to extract Engagement data from their endpoint. Organize this data and store it into a file structure that makes sense.
* Auth:  https://developers.hubspot.com/docs/overview  (see demo key)
* Engagments API: https://developers.hubspot.com/docs/methods/engagements/engagements-overview

Spin Up a relational db Instance, you can choose either:
* Postgres 9.4+
* MySQL 5.6+
* Oracle 11g+
* SQL server (but please provide the docker image tag for it)

Create a table and Load the Data In (this can be done during reads as well).

### Solution
#### Environment
* OS - Linux Ubuntu 16.04
* Language - Python 3.5.2 with pip package manager installed
* Python Packages - psycopg2, requests (in requirements.txt file)
* Database -  Postgres 9.5.14

Run bash script to install all packages and set up database users/privileges: </br> 
`$ ./install_environment` -> Look inside file to change db passwords, client_ids for API and environment variables

Run application code to ping the Hubspot API engagement route, insert new rows into database/update rows into database: </br>
`Usage:<executable> <database name> <table> <action ["create", "updated"]>. Ex: ./hubspot alooma engagements create`

To create a new database, table and ping the hubspot API for engagements to insert into your new table: </br>
`$ ./hubspot alooma engagements create`

To update your rows in your tables from the Hubspot API engagement route: </br>
`$ ./hubspot alooma engagements update`

## Reading Data
Write a SQL Query that pulls the  Engagements per Day broken down by type. You should expose the counts per day as well. Present these results in a format that makes sense to view. </br>

To enter into your postgres database: </br>
`$ psql alooma`
`select updated_at, engagement_type, count(engagement_type) from engagements group by updated_at, engagement_type order by updated_at desc, count desc;`

## Bonus Points
Present a rolling 2 week average for each day.

## Final Summary
Please provide steps - either in Python code, a Jupyter Notebook, or a step-by-step summary of your approach to the problem - and how you solved it. These steps should allow us to run through and implement your solution.
