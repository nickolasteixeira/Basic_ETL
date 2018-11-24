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

## Reading Data
Write a SQL Query that pulls the  Engagements per Day broken   down by t  ype  . You should expose the counts per day as well. Present these results in a format that makes sense to view.

## Bonus Points
Present a rolling 2 week average for each day.

## Final Summary
Please provide steps - either in Python code, a Jupyter Notebook, or a step-by-step summary of your approach to the problem - and how you solved it. These steps should allow us to run through and implement your solution.
