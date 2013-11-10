# Singleton for dealing with the backend
from contextlib import contextmanager

class AbstractDatabase(object):
    def __init__(self):
        pass
        # Will contain table creation and fixing logic

    def connection(self):
        """ Abstract handle for getting a connection, irrelevent of backend
        Should use with keyword, and be a context manager """
        raise NotImplementedError("Cannot connect to abstract database; must subclass")


import sqlite3
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

def reinit_database(db): 
    with open("schema/schema.sql") as schema:
        sql = schema.read()
    with db.connection() as cnx:
        c = cnx.cursor()
        c.execute(sql, multi = True)

       
