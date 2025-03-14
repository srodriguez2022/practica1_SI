import pandas as pd
import sqlite3
import os


#database = "../database/data.db"
database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'data.db')


def query_to_dataframe(query):
    con = sqlite3.connect(database_path)
    df = pd.read_sql_query(query, con)
    con.close()
    return df


def all_samples():
    return query_to_dataframe("SELECT * FROM TICKET")


def tickets_valorated_5():
    return query_to_dataframe(
        "SELECT T.ID_TICKET, C.ID_CLIENTE, C.NOMBRE, T.SATISFACCION FROM TICKET T JOIN CLIENTE C ON T.CLIENTE_ID = "
        "C.ID_CLIENTE WHERE T.SATISFACCION >= 5")


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


#querys para el analisis de fraude

def fraude_by_employee():
    query = """
    SELECT C.EMPLEADO_ID,
           COUNT(DISTINCT T.ID_TICKET) AS NUM_INCIDENTS,
           COUNT(*) AS NUM_CONTACTS
    FROM TICKET T
    JOIN CONTACTO C ON T.ID_TICKET = C.TICKET_ID
    WHERE T.INCIDENCIA_ID = 5
    GROUP BY C.EMPLEADO_ID
    """
    return query_to_dataframe(query)


def fraude_by_employee_level():
    query = """
    SELECT E.NIVEL,
           COUNT(DISTINCT T.ID_TICKET) AS NUM_INCIDENTS,
           COUNT(*) AS NUM_CONTACTS
    FROM TICKET T
    JOIN CONTACTO C ON T.ID_TICKET = C.TICKET_ID
    JOIN EMPLEADO E ON C.EMPLEADO_ID = E.ID_EMPLEADO
    WHERE T.INCIDENCIA_ID = 5
    GROUP BY E.NIVEL
    """
    return query_to_dataframe(query)


def fraude_by_client():
    query = """
    SELECT T.CLIENTE_ID,
           COUNT(DISTINCT T.ID_TICKET) AS NUM_INCIDENTS,
           COUNT(C.TICKET_ID) AS NUM_CONTACTS
    FROM TICKET T
    LEFT JOIN CONTACTO C ON T.ID_TICKET = C.TICKET_ID
    WHERE T.INCIDENCIA_ID = 5
    GROUP BY T.CLIENTE_ID
    """
    return query_to_dataframe(query)


def fraude_by_incident_type():
    query = """
    SELECT I.NOMBRE AS INCIDENT_TYPE,
           COUNT(DISTINCT T.ID_TICKET) AS NUM_INCIDENTS,
           COUNT(*) AS NUM_CONTACTS
    FROM TICKET T
    JOIN CONTACTO C ON T.ID_TICKET = C.TICKET_ID
    JOIN INCIDENTE I ON T.INCIDENCIA_ID = I.ID_INCIDENTE
    WHERE T.INCIDENCIA_ID = 5
    GROUP BY T.INCIDENCIA_ID
    """
    return query_to_dataframe(query)


def fraude_by_weekday():
    #strftime('%w', ...) para extraer el día (0 = domingo, 1 = lunes...)

    query = """
    SELECT strftime('%w', T.FECHA_APERTURA) AS weekday,
           COUNT(DISTINCT T.ID_TICKET) AS NUM_INCIDENTS,
           COUNT(*) AS NUM_CONTACTS
    FROM TICKET T
    JOIN CONTACTO C ON T.ID_TICKET = C.TICKET_ID
    WHERE T.INCIDENCIA_ID = 5
    GROUP BY weekday
    """
    df = query_to_dataframe(query)
    weekday_map = {'0': 'Domingo', '1': 'Lunes', '2': 'Martes', '3': 'Miércoles',
                   '4': 'Jueves', '5': 'Viernes', '6': 'Sábado'}
    df['weekday'] = df['weekday'].astype(str).map(weekday_map)
    return df


def compute_basic_stats(df, column):
    return {
        'median': df[column].median(),
        'mean': df[column].mean(),
        'variance': df[column].var(),
        'min': df[column].min(),
        'max': df[column].max()
    }

