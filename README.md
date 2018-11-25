# Alooma CSE/DSE Challenge


## Extracting Data
Pull Data from Hubspot. Using their API and Python, build out logic to extract Engagement data from their endpoint. Organize this data and store it into a file structure that makes sense.
* Auth:  https://developers.hubspot.com/docs/overview  (see demo key)
* Engagements API: https://developers.hubspot.com/docs/methods/engagements/engagements-overview

Spin Up a relational db Instance, you can choose either:
* Postgres 9.4+
* MySQL 5.6+
* Oracle 11g+
* SQL server (but please provide the docker image tag for it)

Create a table and Load the Data In (this can be done during reads as well).

### Solution
#### Environment
* OS - Linux Ubuntu 16.04
* Language - Python 3.5.2 with pip3 package manager installed (Backwards compatibility with Python 2.7.12 with pip package manager)
* Python Packages - psycopg2, psycopg2-binary, requests (in requirements.txt file)
* Database -  Postgres 9.5.14

Clone repo: </br>
`$ git clone https://github.com/nickolasteixeira/Alooma_Challenge.git` </br>
`$ cd Alooma_Challenge/` </br>

Export environment variables: </br>
`$ export ALOOMA_PASSWORD='yourpasswordhere'` </br>

Run bash script to install all packages and set up database users/privileges: </br> 
`$ ./install_environment` -> Look inside file to change db passwords (make sure the ALOOMA_PASSWORD from env variable and password for DB are the same) </br>

Run application code to ping the Hubspot API engagement route, insert new rows into database/update rows into database: </br>
`Usage:<executable> <database name> <table> <action ["insert", "update"]>` </br>

* YOU HAVE TO RUN INSERT FIRST BEFORE UPDATING. If you do not insert new values into a db, you cannot update them.

To create a new database, table and ping the hubspot API for engagements to insert into your new table: (Be patient, this takes a while, grabbing 30K rows of data) </br>
`$ ./hubspot.py alooma engagements insert` </br>

To update your rows in your tables from the Hubspot API engagement route: </br>
`$ ./hubspot.py alooma engagements update` </br>

## Reading Data
Write a SQL Query that pulls the Engagements per Day broken down by type. You should expose the counts per day as well. Present these results in a format that makes sense to view. </br>

### Solution
To enter into your postgres database: </br>
`$ psql alooma` </br>

SQL Query that pulls the Engagements per Day broken down by type. </br>
`alooma=# select updated_at, engagement_type, count(engagement_type) from engagements group by updated_at, engagement_type order by updated_at desc, count desc;` </br>

## Bonus Points
Present a rolling 2 week average for each day.

### Solution
`alooma=# select updated_at, avg(count(engagement_type)) over (order by updated_at rows between 7 preceding and 7 following) from engagements group by 1 order by 1 desc;`

## Final Summary
Please provide steps - either in Python code, a Jupyter Notebook, or a step-by-step summary of your approach to the problem - and how you solved it. These steps should allow us to run through and implement your solution.

### Solution
My approach was two fold:</br>
1. Set up an environment and instructions that allowed for easy implementation.
2. Break down the problem into simple and small pieces to make the code reusable and extensible.  

The problem was to extract data from the HubSpot’s [engagement API route]( https://developers.hubspot.com/docs/methods/engagements/get-all-engagements)  and load it into a SQL database. The engagements API had a few different routes, but I chose to use the route that got all the engagements with their relevant information, parse through them and insert them into a database. I had to think about what parts of each engagement object I wanted to retrieve and store to be able to create a query that pulls all engagements per day broken down by type with an associated count. 

I decided to retrieve the id, createdAt, lastUpdated, and type attributes from each engagement object to store into one table in a Postgres relational database. I chose to store both the createdAt and lastUpdated attributes because the challenge wanted engagements per day and I would assume that the API would update engagements when a user interacts with them. I wrote the logic in the `./hubspot.py` to be able to both create and update engagements from HubSpot’s engagement API route. That way, if any you can run the `./hubspot.py` module to update each engagement so you can run accurate statistics if you are looking for updated daily engagements per day broken down by type.

I broke down the problem into pieces. I wrote the `./hubspot.py` module just to interact with the engagement route by creating a HubSpot Class that contains methods to create a database, create tables, and insert or update rows to a specified table based on data retrieved from this [route]( https://developers.hubspot.com/docs/methods/engagements/get-all-engagements). When you run the module, you have to specify what database you want to create, what table you want to create, and either insert or update rows in each database.

