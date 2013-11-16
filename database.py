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
    with db.connection() as cnx:
        c = cnx.cursor()
        for command in load_sql('drop_all'):
            print(command)
            c.execute(command)
        print("Dropping")
        cnx.commit()
	d = cnx.cursor()
        for command in load_sql('create_all'):
            print(command)
            d.execute(command)
        print("Recreating")
        cnx.commit()
	e = cnx.cursor()
        for command in load_sql('pop_cap_shape'):
            print(command)
            e.execute(command)
        print("Populating CAP_SHAPE")
        cnx.commit()
        f = cnx.cursor()
        for command in load_sql('pop_gill_attatchment'):
            print(command)
            f.execute(command)
        print("Populating GILL_ATTATCHMENT")
        cnx.commit()
        g = cnx.cursor()
        for command in load_sql('pop_spore_surface'):
            print(command)
            g.execute(command)
        print("Populating SPORE_SURFACE")
        cnx.commit()
        h = cnx.cursor()
        for command in load_sql('pop_spore_color'):
            print(command)
            h.execute(command)
        print("Populating SPORE_COLOR")
        cnx.commit()
def load_sql(filename):
    with open("schema/%s.sql" % filename) as file:
        commands = file.read().split(';')
        commands = (command.strip() for command in commands if len(command) > 5)
        return commands
