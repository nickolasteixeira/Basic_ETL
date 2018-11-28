#!/usr/bin/python
# #!/usr/bin/python3
'''Module that pings Hubspot API and inserts engagement metrics into
    postgres database
    Usage:<executable> <database name> <table> <action ["insert", "update"]>.
    Ex: ./hubspot challenge engagements insert
'''
import argparse
from datetime import datetime
from inputs import kwargs
import logging
import os
import psycopg2
import requests
import sys


class Hubspot:
    '''Hubspot class that takes in Hubspot URL and has
    methods that retrieve/store data'''

    # set up a logfile for the class
    logging.basicConfig(filename='./logs/hubspot.log',
                        format='%(levelname)s:%(asctime)s:%(message)s',
                        level=logging.DEBUG)

    def __init__(self, kwargs):
        '''Initailizes object attributes. url, params
        Args:
            kwargs:
        '''
        self.url = kwargs['base'] + kwargs['endpoints']
        self.params = kwargs['params']

    def get_new_engagements(self, kwargs):
        '''Method that pings Hubspot Engagement API and writes to challenge database
        Args:
            kwargs (dict): dict of items for actions associated with the method
            ex: base, enpoints, params, dbname, table, action
        '''
        url, num, dbname, table, action = self.url, \
            kwargs['offset'], kwargs['dbname'], \
            kwargs['table'], kwargs['action']
        self.params['offset'] = num

        r = requests.get(url, params=self.params)
        if r.status_code is 200:
            print('Pinging {}'.format(r.url))
            data = r.json()
            results = data.get('results')
            conn = None
            try:
                conn = psycopg2.connect(
                    """dbname={} user={} password={}""".format(
                        dbname, os.getenv('USER'),
                        os.getenv('challenge_PASSWORD')))
                cur = conn.cursor()
                added, updated = False, False
                for item in results:
                    # create variales to insert into table
                    engagement_id = item.get('engagement').get('id')
                    created_at = item.get('engagement').get('createdAt')
                    updated_at = item.get('engagement').get('lastUpdated')
                    engagement_type = item.get('engagement').get('type')
                    # update or add new entries in table
                    cur.execute(
                        """select exists
                            (select 1 from {}
                            where engagement_id={})""".format(
                            table, engagement_id))
                    if action == 'insert':
                        # Checks first if the engagement_id is in the
                        # table, if not -> add the new entry into the table
                        if not cur.fetchone()[0]:
                            added = True
                            cur.execute(
                                """INSERT INTO {}
                                (engagement_id, created_at,
                                updated_at, engagement_type)
                                VALUES(%s, %s, %s, %s)""".format(
                                    table),
                                (engagement_id,
                                 datetime.fromtimestamp(created_at / 1000),
                                 datetime.fromtimestamp(updated_at / 1000),
                                 engagement_type))
                    elif action == 'update':
                        updated = True
                        cur.execute(
                            """UPDATE {}
                            SET updated_at=to_timestamp({})
                            WHERE engagement_id={}""".format(
                                table, updated_at / 1000,
                                engagement_id))

                cur.close()
                conn.commit()
                conn.close()

                if added:
                    self.log_info('New items added to the table')
                elif updated:
                    self.log_info('Items updated in table')
                else:
                    self.log_info('Items already in table')
            except (Exception, psycopg2.DatabaseError) as error:
                self.log_debug(error)
            finally:
                if conn is not None:
                    conn.close()

        if data.get('hasMore'):
            kwargs['offset'] = data.get('offset')
            self.get_new_engagements(kwargs)

    def create_database(self, dbname):
        '''Method that creates a database
        Args:
            dbname (str): database name to create
        '''
        conn = None
        try:
            conn = psycopg2.connect(
                'dbname={} user={} host={} password={}'.format(
                    'postgres',
                    os.getenv('USER'),
                    'localhost',
                    os.getenv('challenge_PASSWORD')))
            conn.set_isolation_level(
                psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            cur = conn.cursor()
            cur.execute(
                """SELECT datname
                FROM pg_catalog.pg_database
                WHERE lower(datname) = lower(%s);""",
                (dbname,))
            if cur.fetchone() is None:
                cur.execute("""CREATE DATABASE %s;""" % dbname)
                message = '{:%Y-%m-%d %H:%M:%S} '\
                    '--> Database {} created.'\
                    .format(datetime.now(), dbname)
                print(message)
                self.log_info(message)
            else:
                message = '{:%Y-%m-%d %H:%M:%S} '\
                    '--> Database {} exists.'\
                    .format(datetime.now(), dbname)
                print(message)
                self.log_info(message)

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_debug(error)
        finally:
            if conn is not None:
                conn.close()

    def create_tables(self, dbname, table):
        '''Method that creates a new table
        Args:
            db (str): database name to use for the database
            table (str): table name to create
        '''
        conn = None
        try:
            conn = psycopg2.connect('dbname={} user={} password={}'.format(
                dbname, os.getenv('USER'), os.getenv('challenge_PASSWORD')))
            cur = conn.cursor()
            cur.execute(
                """SELECT EXISTS
                (SELECT 1
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_NAME=%s)""",
                (table,
                 ))
            if not cur.fetchone()[0]:
                cur.execute(
                    """CREATE TABLE IF NOT EXISTS %s
                    (engagement_id integer PRIMARY KEY,
                    created_at date NOT NULL,
                    updated_at date NOT NULL,
                    engagement_type text)""" %
                    table)
                message = '{:%Y-%m-%d %H:%M:%S} '\
                    '--> Table {} created.'\
                    .format(datetime.now(), table)
                print(message)
                self.log_info(message)
            else:
                message = '{:%Y-%m-%d %H:%M:%S} '\
                    '--> Table {} exists.'\
                    .format(datetime.now(), table)
                print(message)
                self.log_info(message)

            cur.close()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            self.log_debug(error)
        finally:
            if conn is not None:
                conn.close()

    def log_debug(self, error):
        '''Method that logs begugging data into a file
            Args:
                error (str): error that gets log into a file
        '''
        logging.debug(error)

    def log_info(self, info):
        '''Method that logs infor data into a file
            Args:
                info (str): info that gets logged into a file
        '''
        logging.info(info)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "database",
        help="input the name of the database you want to create",
        type=str)
    parser.add_argument(
        "table",
        help="input the name of the table you want to create",
        type=str)
    parser.add_argument(
        "command",
        help="type the command you want to execute. Ex: 'insert' \
        'to insert rows into a database. 'update' to update rows in a databse",
        type=str)
    args = parser.parse_args()

    # Get arguments from command line
    kwargs['dbname'] = args.database
    kwargs['table'] = args.table
    kwargs['action'] = args.command

    h = Hubspot(kwargs)
    if kwargs['action'] == 'insert':
        # create database
        h.create_database(kwargs['dbname'])
        # create tables
        h.create_tables(kwargs['dbname'], kwargs['table'])
        # ping Hubspot API and insert rows into table
        h.get_new_engagements(kwargs)
    elif kwargs['action'] == 'update':
        print('Updating...')
        h.get_new_engagements(kwargs)
    print('Checks logs in ./logs/hubspot.log for more log detail.')
