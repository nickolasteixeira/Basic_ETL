# Basic ETL - Ping API -> Insert into Database

#### Environment
* OS - Linux Ubuntu 16.04
* Language - Python 3.5.2 with pip3 package manager installed (Backwards compatibility with Python 2.7.12 with pip package manager)
* Python Packages - psycopg2, psycopg2-binary, requests (in requirements.txt file)
* Database -  Postgres 9.5.14

Clone repo: </br>
`$ git clone https://github.com/nickolasteixeira/Basic_ETL.git` </br>
`$ cd Basic_ETL/` </br>

Export environment variables: </br>
`$ export challenge_PASSWORD='yourpasswordhere'` </br>

Run bash script to install all packages and set up database users/privileges: </br> 
`$ ./install_environment.sh` -> Look inside file to change db passwords (make sure the challenge_PASSWORD from env variable and password for DB are the same) </br>

Run application code to ping the Hubspot API engagement route, insert new rows into database/update rows into database: </br>
`Usage:<executable> <database name> <table> <action ["insert", "update"]>` </br>

* YOU HAVE TO RUN INSERT FIRST BEFORE UPDATING. If you do not insert new values into a db, you cannot update them.

To create a new database, table and ping the hubspot API for engagements to insert into your new table: (Be patient, this takes a while, grabbing 30K rows of data) </br>
`$ ./hubspot.py challenge engagements insert` </br>

To update your rows in your tables from the Hubspot API engagement route: </br>
`$ ./hubspot.py challenge engagements update` </br>

### Errors
If you encounter any errors, check the logs files in `./logs/hubspot.log`

To enter into your postgres database: </br>
`$ psql challenge` </br>

SQL Query that pulls the Engagements per Day broken down by type. </br>
`challenge=# select updated_at, engagement_type, count(engagement_type) from engagements group by updated_at, engagement_type order by updated_at desc, count desc;` </br>

My approach was two fold:</br>
1. Set up an environment and instructions that allowed for easy implementation.
2. Break down the problem into simple and small pieces to make the code reusable and extensible.  

The problem was to extract data from the HubSpot’s [engagement API route]( https://developers.hubspot.com/docs/methods/engagements/get-all-engagements)  and load it into a SQL database. The engagements API had a few different routes, but I chose to use the route that got all the engagements with their relevant information, parse through them and insert them into a database. I had to think about what parts of each engagement object I wanted to retrieve and store to be able to create a query that pulls all engagements per day broken down by type with an associated count. 

I decided to retrieve the id, createdAt, lastUpdated, and type attributes from each engagement object to store into one table in a Postgres relational database. I chose to store both the createdAt and lastUpdated attributes because the challenge wanted engagements per day and I would assume that the API would update engagements when a user interacts with them. I wrote the logic in the `./hubspot.py` to be able to both create and update engagements from HubSpot’s engagement API route. That way, if any you can run the `./hubspot.py` module to update each engagement so you can run accurate statistics if you are looking for updated daily engagements per day broken down by type.

I broke down the problem into pieces. I wrote the `./hubspot.py` module just to interact with the engagement route by creating a HubSpot Class that contains methods to create a database, create tables, and insert or update rows to a specified table based on data retrieved from this [route]( https://developers.hubspot.com/docs/methods/engagements/get-all-engagements). When you run the module, you have to specify what database you want to create, what table you want to create, and either insert or update rows in each database.

