-- PRACTICA SI

DROP TABLE IF EXISTS CLIENTE;
CREATE TABLE CLIENTE (
    ID_CLIENTE       INT PRIMARY KEY,
    NOMBRE           VARCHAR(50),
    TELEFONO         VARCHAR(25),
    PROVINCIA       VARCHAR(25)
);

DROP TABLE IF EXISTS EMPLEADO;
CREATE TABLE EMPLEADO (
    ID_EMPLEADO     INT PRIMARY KEY,
    NOMBRE          VARCHAR(50),
    NIVEL           INT,
    FECHA_CONTRATO  DATE
);

DROP TABLE IF EXISTS INCIDENTE;
CREATE TABLE INCIDENTE (
    ID_INCIDENTE      INT PRIMARY KEY,      -- tipo de incidente
    NOMBRE            VARCHAR(100)
);

DROP TABLE IF EXISTS TICKET;
CREATE TABLE TICKET(
    ID_TICKET          INT PRIMARY KEY,
    CLIENTE_ID         INT,
    FECHA_APERTURA     DATE,
    FECHA_CIERRE       DATE,
    ES_MANTENIMIENTO   CHECK (ES_MANTENIMIENTO IN (0,1)),
    SATISFACCION       INT CHECK (SATISFACCION BETWEEN 1 AND 10),
    INCIDENCIA_ID      INT,
    FOREIGN KEY (CLIENTE_ID) REFERENCES CLIENTE(ID_CLIENTE) ON DELETE CASCADE,
    FOREIGN KEY (INCIDENCIA_ID) REFERENCES INCIDENTE(ID_INCIDENTE) ON DELETE CASCADE
);


-- contactos con empleados
DROP TABLE IF EXISTS CONTACTO;
CREATE TABLE CONTACTO (
    ID_CONTACTO         INT PRIMARY KEY,
    TICKET_ID           INT,
    EMPLEADO_ID         INT,
    FECHA               DATE,
    TIEMPO              FLOAT,
    FOREIGN KEY (TICKET_ID) REFERENCES TICKET(ID_TICKET) ON DELETE CASCADE,
    FOREIGN KEY (EMPLEADO_ID) REFERENCES EMPLEADO(ID_EMPLEADO) ON DELETE CASCADE
);
