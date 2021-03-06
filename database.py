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

        print("Populating CAP_SHAPE")
        self.multirun('pop_cap_shape')
        
        print("Populating GILL_ATTATCHMENT")
        self.multirun('pop_gill_attatchment')

        print("Populating SPORE_COLOR")
        self.multirun('pop_spore_color')
        
        print("Populating SPORE_SURFACE")
        self.multirun('pop_spore_surface')

        print("Populating MUSHROOM")
        self.multirun('pop_mushroom')

        print("Populating RECIPE and MUSHROOM_RECIPE")
        self.multirun('pop_recipe_and_recipe_mushrooms')

        print("Populating APP_USER")
        self.multirun('pop_app_users')
        
        print("Populating MUSHROOM_FIND")
        self.multirun('pop_mushroom_find')
        
        print("Creating conveniece views")
        self.multirun('create_views')
        
    def get_query(self, filename):
        with open(path.join(self.sqlpath, filename + '.sql')) as file:
            return file.read()
        
    def multirun(self, filename):
        """ Runs the semi-colon deliminated set of sql commands from a file """
        commands = self.get_query(filename).split(';')
        # This heuristically strips out the useless parts, leaving pure sql commands
        commands = (command.strip() for command in commands if command != '')
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

#Decimal handling hackery for sqlite
import decimal
sqlite3.register_adapter(decimal.Decimal, lambda d: str(d))
sqlite3.register_converter("decimal", lambda s: decimal.Decimal(s))

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
        sql = re.sub("CREATE OR REPLACE VIEW", "CREATE VIEW IF NOT EXISTS", sql)
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
