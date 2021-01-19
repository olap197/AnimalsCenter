import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_connection(r"C:/Users/barte/Desktop/SQL/animals.db")

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def main():
    database = r"C:/Users/barte/Desktop/SQL/animals.db"

    sql_create_center_table = """ CREATE TABLE IF NOT EXISTS center (
                                        uniqueid integer PRIMARY KEY autoincrement,
                                        login text NOT NULL,
                                        password text NOT NULL,
                                        address text NOT NULL
                                    ); """

    sql_create_animals_table = """CREATE TABLE IF NOT EXISTS animals (
                                    uniqueid integer PRIMARY KEY autoincrement,
                                    centerid text NOT NULL,
                                    name text NOT NULL,
                                    description text,
                                    age integer NOT NULL,
                                    species text NOT NULL,
                                    price float,
                                    FOREIGN KEY (centerid) REFERENCES center (uniqueid)
                                    FOREIGN KEY (species) REFERENCES species (name)
                                );"""
    sql_create_species_table = """ CREATE TABLE IF NOT EXISTS species (
                                uniqueid integer PRIMARY KEY autoincrement,
                                name text NOT NULL,
                                description text,
                                price float NOT NULL
                            ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        
        create_table(conn, sql_create_center_table)
        create_table(conn, sql_create_animals_table)
        
        create_table(conn, sql_create_species_table)
    else:
        print("Error! cannot create the database connection.")