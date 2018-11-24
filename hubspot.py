#!/usr/bin/python3
'''Module that pings Hubspot API and inserts engagement metrics into postgres database
    Usage:<executable> <database name> <table> <action ["create", "updated"]>. Ex: ./hubspot alooma engagements create
'''
from datetime import datetime
import os
import psycopg2
import requests
import sys

class Hubspot:
    '''Hubspot class that takes in Hubspot URL and has methods that retrieve/store data'''

    def __init__(self, client_id):
        '''Initailizes with client_id from your host env var CLIENT_ID'''
        self.client_id = client_id 

    def get_new_engagements(self, kwargs):
        '''Method that pings Hubspot Engagement API and writes to alooma database
        Args:
            url (str): the Hubspot URL to ping
            num (int): the offset number to recursively ping the Hubspot URL if there are more results       
        '''
        url, num, dbname, table, action = kwargs['url'], kwargs['offset'], kwargs['dbname'], kwargs['table'], kwargs['action']
        r = requests.get(url, params={'offset': num})
        print('Pinging {}&offset={}'.format(url, num))

        if r.status_code is 200:
            data = r.json()
            results = data.get('results')
            conn = None
            if results:
                try:    
                    conn = psycopg2.connect('dbname={} user={} password={}'.format(dbname, os.getenv('USER'), os.getenv('ALOOMA_PASSWORD')))
                    cur = conn.cursor()
                    added, updated = False, False
                    for item in results:
                        # create variales to insert into table
                        engagement_id = item.get('engagement').get('id')
                        created_at = item.get('engagement').get('createdAt')
                        updated_at = item.get('engagement').get('lastUpdated')
                        engagement_type = item.get('engagement').get('type')
                        # update or add new entries in table
                        cur.execute('select exists(select 1 from {} where engagement_id={})'.format(table, engagement_id))
                        if action == 'create':
                            # Checks first if the engagement_id is in the table, if not -> add the new entry into the table
                            if not cur.fetchone()[0]:
                                added = True
                                cur.execute('INSERT INTO {} (engagement_id, created_at, updated_at, engagement_type) VALUES(%s, %s, %s, %s)'.format(table), (engagement_id, datetime.fromtimestamp(created_at/1000), datetime.fromtimestamp(updated_at/1000), engagement_type))
                        elif action == 'update':
                            updated = True
                            cur.execute('UPDATE {} SET updated_at=to_timestamp({}) WHERE engagement_id={}'.format(table, updated_at/1000, engagement_id))
 
                    cur.close()
                    conn.commit() 
                    conn.close()
                    
                    if added:
                        print('New items added to the table') 
                    elif updated:
                        print('Items updated in table') 
                    else:
                        print('Items already in table')

                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)
                finally:
                    if conn is not None:
                        conn.close()

        # Recursively call API if there are more entries
        if data.get('hasMore') is True:
            kwargs['offset'] = data.get('offset')
            self.get_new_engagements(kwargs) 


    def create_database(self, dbname):
        '''method that creates a database
        Args:
            dbname (str): database name to create
        '''
        conn = None
        try: 
            conn = psycopg2.connect('dbname={} user={} host={} password={}'.format('postgres', os.getenv('USER'), 'localhost', os.getenv('ALOOMA_PASSWORD')))
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()

            cur.execute("""SELECT datname FROM pg_catalog.pg_database WHERE lower(datname) = lower(%s);""", (dbname,))
            if not cur.fetchone()[0]:
                cur.execute("""CREATE DATABASE %s;""" % dbname)
                print('Database {} created.'.format(dbname))
            else:
                print('Database {} already exists.'.format(dbname))

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()


    def create_tables(self, dbname, table):
        '''method that creates a new table
        Args:
            db (str): database name to use for the database
            table (str): table name to create
        '''
        conn = None
        try:
            conn = psycopg2.connect('dbname={} user={} password={}'.format(dbname, os.getenv('USER'), os.getenv('ALOOMA_PASSWORD')))
            cur = conn.cursor()
            cur.execute("""SELECT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME=%s)""", (table,))
            if not cur.fetchone()[0]:
                cur.execute("""CREATE TABLE IF NOT EXISTS %s(engagement_id integer PRIMARY KEY, created_at date NOT NULL, updated_at date NOT NULL, engagement_type text)""" % table)
                print("Table {} created.".format(table))
            else:
                print("Table {} already exists".format(table))        
     
            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

if __name__ == '__main__':
    url = 'https://api.hubapi.com/engagements/v1/engagements/paged?hapikey=demo'
    # Gets the CLIENT_ID associated with the hubspot API
    if len(sys.argv) is not 4:
        print('Usage:<executable> <database name> <table> <action ["create", "updated"]>. Ex: ./hubspot alooma engagements create')
        exit(0)

    client_id = os.getenv('CLIENT_ID')
    dbname = sys.argv[1]
    table = sys.argv[2]
    action = sys.argv[3]
 
    h = Hubspot(client_id) 
    kwargs = {'url': url, 'offset': 0, 'dbname': dbname, 'table': table, 'action': action}
    if action == 'create':
        h.create_database(dbname)
        h.create_tables(dbname, table)
        h.get_new_engagements(kwargs)
    elif action == 'update':
        h.get_new_engagements(kwargs)
