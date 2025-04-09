import pandas as pd
import sqlite3
import os

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
        "SELECT EMPLEADO_ID,COUNT (TICKET_ID) AS NUM_INCIDENTS  FROM CONTACTO GROUP BY EMPLEADO_ID")


# queries for fraud analysis

def fraude_by_employee():
    return query_to_dataframe("SELECT E.ID_EMPLEADO AS EMPLOYEE, COUNT(T.ID_TICKET) AS NUM_INCIDENTS, "
                              "COUNT(C.ID_CONTACTO) AS NUM_CONTACTS FROM CONTACTO C JOIN EMPLEADO E ON C.EMPLEADO_ID "
                              "= E.ID_EMPLEADO JOIN TICKET T ON C.TICKET_ID = T.ID_TICKET GROUP BY E.ID_EMPLEADO")


def fraude_by_employee_level():
    return query_to_dataframe("SELECT e.NIVEL, COUNT(DISTINCT t.ID_TICKET) AS NUM_INCIDENTS, COUNT(c.TICKET_ID) AS "
                              "NUM_CONTACTS FROM EMPLEADO e JOIN CONTACTO c  ON e.ID_EMPLEADO = c.EMPLEADO_ID JOIN "
                              "TICKET t ON t.ID_TICKET = c.TICKET_ID GROUP BY e.NIVEL")


def fraude_by_client():
    return query_to_dataframe("SELECT cl.ID_CLIENTE AS Cliente, cl.NOMBRE AS Nombre_Cliente, COUNT(DISTINCT "
                              "t.ID_TICKET) AS Num_Incidentes, COUNT(c.TICKET_ID) AS Num_Contacts FROM CLIENTE cl "
                              "LEFT JOIN TICKET t ON cl.ID_CLIENTE = t.CLIENTE_ID LEFT JOIN CONTACTO c ON t.ID_TICKET "
                              "= c.TICKET_ID GROUP BY cl.ID_CLIENTE")


def fraude_by_incident_type():
    return query_to_dataframe("SELECT T.INCIDENCIA_ID, I.NOMBRE AS Incident_type, COUNT(DISTINCT T.ID_TICKET) AS "
                              "Num_Incidents, COUNT(C.TICKET_ID) AS Num_Contact FROM TICKET T LEFT JOIN CONTACTO C ON "
                              "T.ID_TICKET = C.TICKET_ID LEFT JOIN INCIDENTE I ON T.INCIDENCIA_ID = I.ID_INCIDENTE "
                              "GROUP BY T.INCIDENCIA_ID, I.NOMBRE")


def fraude_by_weekday():
    # strftime('%w', ...) for extracting the day (0 = sunday, 1 = monday...)
    return query_to_dataframe("SELECT strftime('%w', T.FECHA_APERTURA) AS Dia_Semana, COUNT(DISTINCT T.ID_TICKET) AS "
                              "Num_Incidents, COUNT(C.TICKET_ID) AS Num_Contact FROM TICKET T LEFT JOIN CONTACTO C  "
                              "ON T.ID_TICKET = C.TICKET_ID GROUP BY strftime('%w', T.FECHA_APERTURA)")


def fraude_incidents():
    return query_to_dataframe("SELECT 'Fraude' AS Tipo, COUNT(*) AS Num_Incidents FROM TICKET WHERE INCIDENCIA_ID = 5")


def fraude_employee_contacts():
    return query_to_dataframe("SELECT 'Fraude' AS Tipo, COUNT(c.TICKET_ID) AS Num_Contacts FROM CONTACTO c JOIN TICKET "
                              "t ON c.TICKET_ID = t.ID_TICKET WHERE t.INCIDENCIA_ID = 5")


def fraude_per_employee():
    return query_to_dataframe("SELECT e.ID_EMPLEADO,COUNT(DISTINCT t.ID_TICKET) AS num_incidents FROM EMPLEADO e JOIN "
                              "CONTACTO c ON e.ID_EMPLEADO = c.EMPLEADO_ID JOIN TICKET t ON t.ID_TICKET = c.TICKET_ID "
                              "WHERE t.INCIDENCIA_ID = 5 GROUP BY e.ID_EMPLEADO")


def average_time_per_incident():
    return query_to_dataframe(
        "SELECT ES_MANTENIMIENTO, AVG(JULIANDAY(FECHA_CIERRE) - JULIANDAY(FECHA_APERTURA)) AS AVG_TIME FROM TICKET "
        "GROUP BY ES_MANTENIMIENTO")


def resolution_time_per_incident():
    return query_to_dataframe("SELECT I.NOMBRE AS INCIDENT_TYPE, (JULIANDAY(FECHA_CIERRE) - JULIANDAY("
                              "FECHA_APERTURA)) AS"
                              " RESOLUTION_TIME FROM TICKET T JOIN INCIDENTE I ON T.INCIDENCIA_ID = I.ID_INCIDENTE ")


def critical_clients():
    return query_to_dataframe("SELECT C.NOMBRE AS CLIENT, COUNT(*) AS INCIDENT_COUNT FROM TICKET T JOIN INCIDENTE I "
                              "ON T.INCIDENCIA_ID = I.ID_INCIDENTE JOIN CLIENTE C ON T.CLIENTE_ID = C.ID_CLIENTE "
                              "WHERE T.ES_MANTENIMIENTO = 1 AND I.ID_INCIDENTE <> 1 GROUP BY C.NOMBRE ORDER BY "
                              "INCIDENT_COUNT DESC LIMIT 5")


def acts_per_weekday():
    return query_to_dataframe("SELECT strftime('%w', C.FECHA) AS WEEKDAY, COUNT(*) AS NUM_ACTS FROM CONTACTO C GROUP "
                              "BY WEEKDAY ORDER BY WEEKDAY")


def acts_per_employee():
    return query_to_dataframe("SELECT EMPLEADO_ID, COUNT(*) AS NUM_ACTS FROM CONTACTO GROUP BY EMPLEADO_ID ORDER BY "
                              "NUM_ACTS DESC")


def top_clients_most_incidents(limit):
    return query_to_dataframe(f"""
        SELECT C.NOMBRE AS CLIENT, COUNT(*) AS INCIDENT_COUNT
        FROM TICKET T
        JOIN CLIENTE C ON T.CLIENTE_ID = C.ID_CLIENTE
        GROUP BY C.NOMBRE
        ORDER BY INCIDENT_COUNT DESC
        LIMIT {limit}
        """)


def top_incidents_type_by_resolution_time(limit):
    return query_to_dataframe(f"""
        SELECT I.NOMBRE AS INCIDENT_TYPE,
        AVG(JULIANDAY(T.FECHA_CIERRE) - JULIANDAY(T.FECHA_APERTURA)) AS AVG_RESOLUTION_TIME
        FROM TICKET T
        JOIN INCIDENTE I ON T.INCIDENCIA_ID = I.ID_INCIDENTE
        GROUP BY I.NOMBRE
        ORDER BY AVG_RESOLUTION_TIME DESC
        LIMIT {limit}
        """)


def top_employees_by_resolution_time(limit):
    return query_to_dataframe(f"""
        SELECT E.NOMBRE AS EMPLOYEE, SUM(C.TIEMPO) AS TOTAL_TIME
        FROM CONTACTO C
        JOIN EMPLEADO E ON C.EMPLEADO_ID = E.ID_EMPLEADO
        GROUP BY E.NOMBRE
        ORDER BY TOTAL_TIME DESC
        LIMIT {limit}
        """)