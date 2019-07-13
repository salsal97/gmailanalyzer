import sqlite3
from datetime import datetime

def create_db(database_name):
    return sqlite3.connect(database_name)

def cursor_to_db(conn):
    return conn.cursor()

def create_table(cursor, table_name, fields):
    field_names = fields.copy()
    field_names[0] = field_names[0]+" PRIMARY KEY"
    query = "CREATE TABLE IF NOT EXISTS "+table_name+" ("+str(field_names)[1:-1]+")"
    cursor.execute(query)

def add_values(cursor, table_name, values):
    query = "INSERT INTO "+table_name+" VALUES ("+str(values)[1:-1]+")"
    cursor.execute(query)

def print_table(cursor, table_name, file_name=None, query=None):

    # Default -> Print all
    if (query is None):
        query = "SELECT * FROM "+table_name

    # Default -> Print to screen
    if (file_name is None):
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            print(str(row)[1:-1])
        print("Finished printing: "+table_name)
    else:
    # Printing to file
        time_now = time = str(datetime.now().strftime("%Y-%m-%d_%H%M"))
        file = open(file_name+"_"+time_now+".txt", "w")
        cursor.execute(query)
        data = cursor.fetchall()
        for row in data:
            file.write(str(row)[1:-1]+" \n")
        print(table_name+" printed to: "+file_name)

def close_conn(conn, cursor):
    cursor.close()
    conn.close()

if __name__=="__main__":
    database_name = "sample.db"
    table_name = "sample_table"
    fields = ["one","two","three"]
    values = [[1,2,3],[4,5,6],[7,8,9]]
    conn = create_db(database_name)
    cursor = cursor_to_db(conn)
    create_table(cursor, table_name, fields)
    add_values(cursor, table_name, values[0])
    print_table(cursor, table_name)
    add_values(cursor, table_name, values[1])
    print_table(cursor, table_name)
    # print_table(cursor, table_name, "sample_file")
    add_values(cursor, table_name, values[2])
    print_table(cursor, table_name)
    # print_table(cursor, table_name, "sample_file_2","SELECT * FROM "+table_name+" WHERE one = 1")
    cursor.execute("INSERT INTO "+table_name+"("+str(fields)[1:-1]+")VALUES(4, 32, 3)")
    print_table(cursor, table_name)
    card = cursor.execute("SELECT two FROM "+table_name+" WHERE one=1 OR one=4").fetchall()
    print(type(card))
    print(card)
    print(card[0][0])
    print(not card)
    card = cursor.execute("SELECT one FROM "+table_name+" WHERE one=34").fetchall()
    print(type(card))
    print(card)
    print(not card)
    close_conn(conn, cursor)
