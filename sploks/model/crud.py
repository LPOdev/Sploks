from os import sep
from const import *

cur = con.cursor()


def selectAll(table):
    """
    It selects all the rows from a table and returns them
    
    :param table: The name of the table you want to select all from
    :return: A list of tuples.
    """
    try:
        query = f"SELECT * FROM {table} Order by id"
        cur.execute(query)
        return cur.fetchall()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"


def selectWithParams(columns, table, params=""):
    """
    It takes in a list of columns, a table, and an optional string of parameters. It then executes a
    query with those parameters and returns the results
    
    :param columns: The columns you want to select
    :param table: The name of the table you want to select from
    :param params: The WHERE clause
    :return: A list of tuples.
    """
    try:
        query = f"SELECT {columns} FROM {table} {params} Order by {table}.id"
        cur.execute(query)
        return cur.fetchall()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"


def selectOneById(columns, table, id):
    """
    It takes in a list of columns, a table name, and an id and returns the row with that id
    
    :param columns: The columns you want to select
    :param table: The name of the table you want to query
    :param id: The id of the row you want to select
    :return: A dictionary of the row that was selected.
    """
    try:
        cur = con.cursor(dictionary=True)
        query = f"SELECT {columns} FROM {table} WHERE id={id} Order by {table}.id"
        cur.execute(query)
        return cur.fetchone()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"


def updateOne(table, values, params=""):
    """
    Update a table in the database
    
    :param table: The name of the table to update
    :param values: The values to be updated
    :param params: The WHERE clause
    """
    try:
        query = f"UPDATE {table} SET {values} {params}"
        cur.execute(query)
        con.commit()
    except mysql.connector.Error as sqlError:
        print(sqlError)
        return True
    except:
        return True
    
    return False


def createOne(table, columns, values):
    """
    Create a new row in a table
    
    :param table: The name of the table you want to insert into
    :param columns: The columns to insert into
    :param values: The values to insert into the table
    :return: The last row id of the table.
    """
    try:
        query = f"INSERT INTO {table} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print(query)
        cur.execute(query, values)
        con.commit()
        return cur.lastrowid
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        return "Unknown error"


def selectOneWithParams(columns, table, params):
    """
    It takes in a list of columns, a table, and a list of parameters. It then returns the first row of
    the table that matches the parameters
    
    :param columns: The columns you want to select
    :param table: The name of the table you want to query
    :param params: The WHERE clause of the query
    :return: A dictionary of the first row of the table.
    """
    try:
        cur = con.cursor(dictionary=True)
        query = f"SELECT {columns} FROM {table} {params} Order by {table}.id"
        cur.execute(query)
        return cur.fetchone()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"


def deleteFromTable(table, params):
    """
    This function deletes a row from a table
    
    :param table: The name of the table you want to delete from
    :param params: A string that contains the WHERE clause of the query
    """
    try:
        query = f"DELETE FROM {table} {params};"
        cur.execute(query)
        con.commit()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"


def selectDistinct(columns, table, params):
    """
    This function is used to select distinct values from a table
    
    :param columns: The columns you want to select
    :param table: The name of the table to query
    :param params: A string that contains the parameters for the SELECT statement
    :return: A list of tuples.
    """
    try:
        cur = con.cursor()
        query = f"SELECT DISTINCT {columns} FROM {table} {params}"
        cur.execute(query)
        return cur.fetchall()
    except mysql.connector.Error as sqlError:
        print(sqlError)
    except:
        "Unknown error"
