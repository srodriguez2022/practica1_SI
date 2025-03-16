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
SELECT
    e.ID_EMPLEADO AS EMPLEADO,
    COALESCE(inc.num_incidents, 0) AS Num_Incidents,
    COALESCE(ct.num_contacts, 0) AS Num_Contacts
FROM EMPLEADO e
LEFT JOIN (
    SELECT
         c.EMPLEADO_ID,
         COUNT(DISTINCT t.ID_TICKET) AS Num_Incidents
    FROM CONTACTO c
    JOIN TICKET t ON t.ID_TICKET = c.TICKET_ID
    GROUP BY c.EMPLEADO_ID
) inc ON e.ID_EMPLEADO = inc.EMPLEADO_ID
LEFT JOIN (
    SELECT
         EMPLEADO_ID,
         COUNT(*) AS Num_Contacts
    FROM CONTACTO
    GROUP BY EMPLEADO_ID
) ct ON e.ID_EMPLEADO = ct.EMPLEADO_ID;

    """
    return query_to_dataframe(query)


def fraude_by_employee_level():
    query = """
 SELECT
    e.NIVEL,
    COUNT(DISTINCT t.ID_TICKET) AS Num_Incidentes,
    COUNT(c.TICKET_ID)         AS Num_Contacts
FROM EMPLEADO e
JOIN CONTACTO c  ON e.ID_EMPLEADO = c.EMPLEADO_ID
JOIN TICKET t    ON t.ID_TICKET   = c.TICKET_ID
GROUP BY e.NIVEL;


    """
    return query_to_dataframe(query)


def fraude_by_client():
    query = """SELECT 
    cl.ID_CLIENTE AS Cliente,
    cl.NOMBRE AS Nombre_Cliente,
    COUNT(DISTINCT t.ID_TICKET) AS Num_Incidentes,
    COUNT(c.TICKET_ID) AS Num_Contacts
FROM CLIENTE cl
LEFT JOIN TICKET t ON cl.ID_CLIENTE = t.CLIENTE_ID
LEFT JOIN CONTACTO c ON t.ID_TICKET = c.TICKET_ID
GROUP BY cl.ID_CLIENTE;

    """
    return query_to_dataframe(query)


def fraude_by_incident_type():
    query = """SELECT 
    T.INCIDENCIA_ID,
    I.NOMBRE AS Incident_type,
    COUNT(DISTINCT T.ID_TICKET) AS Num_Incidents,
    COUNT(C.TICKET_ID) AS Num_Contacts
FROM TICKET T
LEFT JOIN CONTACTO C 
    ON T.ID_TICKET = C.TICKET_ID
LEFT JOIN INCIDENTE I 
    ON T.INCIDENCIA_ID = I.ID_INCIDENTE
GROUP BY T.INCIDENCIA_ID, I.NOMBRE;
    """
    return query_to_dataframe(query)# esta ya es correcta


def fraude_by_weekday():
    #strftime('%w', ...) para extraer el día (0 = domingo, 1 = lunes...)

    query = """
   SELECT
    strftime('%w', T.FECHA_APERTURA) AS Dia_Semana,
    COUNT(DISTINCT T.ID_TICKET) AS Num_Incidents,
    COUNT(C.TICKET_ID) AS Num_Contacts
FROM TICKET T
LEFT JOIN CONTACTO C 
    ON T.ID_TICKET = C.TICKET_ID
GROUP BY strftime('%w', T.FECHA_APERTURA);

    """
    df = query_to_dataframe(query)

    weekday_map = {'0': 'Domingo', '1': 'Lunes', '2': 'Martes', '3': 'Miércoles',
                   '4': 'Jueves', '5': 'Viernes', '6': 'Sábado'}

    df['Dia_Semana'] = df['Dia_Semana'].astype(str).map(weekday_map)

    return df

def fraude_incidents():
    query = '''
    SELECT 'Fraude' AS Tipo,
       COUNT(*) AS Num_Incidents
    FROM TICKET
    WHERE INCIDENCIA_ID = 5;
'''
    return query_to_dataframe(query)# esta ya es correcta

def fraude_employe_contacts():
    query = """
 SELECT 
  'Fraude' AS Tipo,
  COUNT(c.TICKET_ID) AS Num_Contacts
FROM CONTACTO c
JOIN TICKET t ON c.TICKET_ID = t.ID_TICKET
WHERE t.INCIDENCIA_ID = 5;


"""
    return query_to_dataframe(query)


def basic_stats_incidents():
    query = """WITH emp_incidents AS (
  SELECT 
    e.ID_EMPLEADO,
    COUNT(DISTINCT t.ID_TICKET) AS num_incidents
  FROM EMPLEADO e
  JOIN CONTACTO c ON e.ID_EMPLEADO = c.EMPLEADO_ID
  JOIN TICKET t ON t.ID_TICKET = c.TICKET_ID
  WHERE t.INCIDENCIA_ID = 5
  GROUP BY e.ID_EMPLEADO
),
ordered_incidents AS (
  SELECT 
    num_incidents,
    ROW_NUMBER() OVER (ORDER BY num_incidents) AS rn,
    COUNT(*) OVER () AS total
  FROM emp_incidents
),
med_incidents AS (
  SELECT AVG(num_incidents) AS mediana_incidents
  FROM ordered_incidents
  WHERE rn IN ((total+1)/2, (total+2)/2)
)
SELECT 
  AVG(num_incidents) AS media_incidents,
  (AVG(num_incidents * num_incidents) - AVG(num_incidents)*AVG(num_incidents)) AS varianza_incidents,
  MIN(num_incidents) AS min_incidents,
  MAX(num_incidents) AS max_incidents,
  (SELECT mediana_incidents FROM med_incidents) AS mediana_incidents
FROM emp_incidents;

"""
    return query_to_dataframe(query)


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

