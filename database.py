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
                c.execute(command)
            cnx.commit()

    def execute(self, sql, args):
        with self.connection() as cnx:
            try:
                c = cnx.cursor()
                if self._compat:
                    sql = self._compat(sql)
                c.execute(sql, args)
                return c.fetchall()
            except Error as e:
                cnx.rollback()
            cnx.commit()

    def connection(self):
        """ Abstract handle for getting a connection, irrelevent of backend
        Should use with keyword, and be a context manager """
        raise NotImplementedError("Cannot connect to abstract database; must subclass")

    # can also implement a "_compat" method to translate sql into local dialect


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
        return re.sub("AUTO_INCREMENT", "", sql, flags=re.IGNORECASE)


class MySQLDatabase(AbstractDatabase):
    def __init__(self, config):
        from mysql.connector import Connect
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
