# Singleton for dealing with the backend
from contextlib import contextmanager
from os import path
from collections import namedtuple

class AbstractDatabase(object):
    # TODO: Add overrides for this in the settings
    def __init__(self, sqlpath='schema'):
        self.sqlpath = sqlpath

    def reinitialize(self):
        print("Dropping old tables")
        self.multirun('drop_all')

        print("Creating new tables")
        self.multirun('create_all')

    def multirun(self, filename):
        """ Runs the semi-colon deliminated set of sql commands from a file """
        with open(path.join(self.sqlpath, filename + '.sql')) as file:
            commands = file.read().split(';')
            # This heuristically strips out the useless parts, leaving pure sql commands
            commands = (command.strip() for command in commands if len(command) > 5)
        with self.connection() as cnx:
            c = cnx.cursor()
            for command in commands:
                if self._compat:
                    command = self._compat(command)
                print(command)
                c.execute(command)
            cnx.commit()

    def execute(self, sql, *args):
        """ Hacky yet somewhat universal direct sql execution function """
        with self.connection() as cnx:
            try:
                c = cnx.cursor()
                if self._compat:
                    sql = self._compat(sql)
                c.execute(sql, args)
                try:
                    results = c.fetchall()
                    cnx.commit()
                    return results
                except InterfaceError:
                    cnx.commit()
            except Exception as e:
                cnx.rollback()
                raise

    def connection(self):
        """ Abstract handle for getting a connection, irrelevent of backend
        Should use with keyword, and be a context manager """
        raise NotImplementedError("Cannot connect to abstract database; must subclass")

    def _compat(self, sql):
        """ Override to provide MySQL compatibility """
        return sql

import sqlite3
import re
class SQLiteDatabase(AbstractDatabase):
    def __init__(self, config):
        self.filename = config['filename']
        super(SQLiteDatabase, self).__init__()

    @contextmanager
    def connection(self):
        cnx = sqlite3.connect(self.filename)
        yield cnx
        cnx.close()
        return

    def _compat(self, sql):
        sql = re.sub("AUTO_INCREMENT", "", sql, flags=re.IGNORECASE)
        sql = re.sub("%s", "?", sql)
        return sql

from mysql.connector import Connect
from mysql.connector.errors import InterfaceError
class MySQLDatabase(AbstractDatabase):
    def __init__(self, config):
        self.Connect = Connect
        self.params = config['params']
        super(MySQLDatabase, self).__init__()

    @contextmanager
    def connection(self):
        cnx = self.Connect(**self.params)
        yield cnx
        cnx.close()


def get_database(config):
    dbconfig = config['database']
    if dbconfig['type'] == 'sqlite':
        return SQLiteDatabase(dbconfig)
    elif dbconfig['type'] == 'mysql':
        return MySQLDatabase(dbconfig)
    else:
        raise NotImplementedError("Invalid DB type")


       


