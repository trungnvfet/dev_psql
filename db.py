from oslo_config import cfg
import psycopg2.extras
import psycopg2


CONF = cfg.CONF
opts = [
    cfg.StrOpt('db_connection',
               default="host='127.0.0.1' dbname='postgres' user='postgres' password='abc123'",
               help='postgres account')
]

params = CONF.db_connection


def register_opts(conf):
    conf.register_opts(opts)


def postgre_connection(params):
    return psycopg2.connect(params)


def create_tables():
    """ Create tables in the PostgreSQL database"""
    commands = [(
        """
        CREATE TABLE test (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        )
        """)]
    conn = None
    try:
        conn = postgre_connection(params)
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update_tables(name, id):
    """ Update tables in the PostgreSQL database"""
    sql = """ UPDATE test
                    SET name = %s
                    WHERE id = %s"""
    conn = None
    updated_rows = 0
    try:
        conn = postgre_connection(params)
        cur = conn.cursor()
        cur.execute(sql, (name, id))
        updated_rows = cur.rowcount
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return updated_rows


def insert_tables(name):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(name)
                 VALUES(%s);"""
    sql2 = "INSERT INTO vendors(name) VALUES(%s)"
    conn = None
    try:
        conn = postgre_connection(params)
        cur = conn.cursor()
        if name is list:
            cur.execute(sql2, (name,))
        cur.execute(sql, (name,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
