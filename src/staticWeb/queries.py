import pandas as pd
import sqlite3

database = "../database/data.db"


def query_to_dataframe(query):
    con = sqlite3.connect(database)
    df = pd.read_sql_query(query, con)
    con.close()
    return df


def all_samples():
    return query_to_dataframe("SELECT * FROM TICKET")


def tickets_valorated_5():
    return query_to_dataframe(
        "SELECT T.ID_TICKET, C.ID_CLIENTE, C.NOMBRE, T.SATISFACCION FROM TICKET T JOIN CLIENTE C ON T.CLIENTE_ID = C.ID_CLIENTE WHERE T.SATISFACCION >= 5")


def incidents_per_client():
    return query_to_dataframe("SELECT CLIENTE_ID, COUNT(*) AS NUM_INCIDENTS FROM TICKET GROUP BY CLIENTE_ID")


def hours_per_incident():
    return query_to_dataframe("SELECT T.ID_TICKET, SUM(C.TIEMPO) AS TOTAL_HOURS FROM TICKET T JOIN CONTACTO C ON "
                              "T.ID_TICKET = C.TICKET_ID GROUP BY T.ID_TICKET ")


def hours_per_employee():
    return query_to_dataframe("SELECT EMPLEADO_ID, SUM(TIEMPO) AS TOTAL_HOURS FROM CONTACTO GROUP BY EMPLEADO_ID")


def time_per_incident():
    return query_to_dataframe(
        "SELECT ID_TICKET, JULIANDAY(FECHA_CIERRE) - JULIANDAY(FECHA_APERTURA) AS DAYS FROM TICKET")


def incidents_per_employee():
    return query_to_dataframe(
        "SELECT EMPLEADO_ID,COUNT (DISTINCT TICKET_ID) AS NUM_INCIDENTS  FROM CONTACTO GROUP BY EMPLEADO_ID")
