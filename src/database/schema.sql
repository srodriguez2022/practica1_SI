-- PRACTICA SI

DROP TABLE CLIENTE CASCADE CONSTRAINTS;
CREATE TABLE CLIENTE (
    ID_CLIENTE       INT PRIMARY KEY,
    NOMBRE           VARCHAR(50),
    TELEFONO         VARCHAR(25),
    PROVINCIA       VARCHAR(25),
    CONSTRAINT PK_CLIENTE PRIMARY KEY (ID_CLIENTE)
);

DROP TABLE EMPLEADO CASCADE CONSTRAINTS;
CREATE TABLE EMPLEADO (
    ID_EMPLEADO     INT PRIMARY KEY,
    NOMBRE          VARCHAR(50),
    NIVEL           INT,
    FECHA_CONTRATO  DATE,
    CONSTRAINT PK_EMPLEADO PRIMARY KEY (ID_EMPLEADO)
);

DROP TABLE INCIDENTE CASCADE CONSTRAINTS;
CREATE TABLE INCIDENTE (
    ID_INCIDENTE      INT PRIMARY KEY,      -- tipo de incidente
    NOMBRE            VARCHAR(100),
    CONSTRAINT PK_INCIDENTE PRIMARY KEY (ID_INCIDENTE)
);

DROP TABLE TICKET CASCADE CONSTRAINTS;
CREATE TABLE TICKET(
    ID_TICKET          INT PRIMARY KEY,
    CLIENTE_ID         INT,
    FECHA_APERTURA     DATE,
    FECHA_CIERRE       DATE,
    ES_MANTENIMIENTO   BOOLEAN,
    SATISFACCION       INT,
    INCIDENCIA_ID      INT,
    CONSTRAINT PK_TICKET PRIMARY KEY (ID_TICKET),
    CONSTRAINT FK_TICKET_CLIENTE FOREIGN KEY (CLIENTE_ID) REFERENCES CLIENTE(ID_CLIENTE) ON DELETE CASCADE,
    CONSTRAINT FK_TICKET_INCIDENCIA FOREIGN KEY (INCIDENCIA_ID) REFERENCES INCIDENTE(ID_INCIDENTE) ON DELETE CASCADE
);


-- contactos con empleados
DROP TABLE CONTACTO CASCADE CONSTRAINTS;
CREATE TABLE CONTACTO (
    ID_CONTACTO         INT PRIMARY KEY,
    TICKET_ID           INT,
    EMPLEADO_ID         INT,
    FECHA               DATE,
    TIEMPO              FLOAT,
    CONSTRAINT PK_CONTACTO PRIMARY KEY (ID_CONTACTO),
    CONSTRAINT FK_CONTACTO_TICKET FOREIGN KEY (TICKET_ID) REFERENCES TICKET(ID_TICKET) ON DELETE CASCADE,
    CONSTRAINT FK_CONTACTO_EMPLEADO FOREIGN KEY (EMPLEADO_ID) REFERENCES EMPLEADO(ID_EMPLEADO) ON DELETE CASCADE
);
