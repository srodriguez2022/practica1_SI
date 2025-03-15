from extraction import read_json


def transform_data():
    data = read_json()
    # Transformar datos de clientes (quitar espacios, ajustar valores, ...)
    for client in data["clientes"]:
        client["nombre"] = client["nombre"].strip()
        client["telefono"] = client.get("telefono", "None")
        client["provincia"] = client.get("provincia", "None")

    # Empleado
    for employee in data["empleados"]:
        employee["nombre"] = employee["nombre"].strip()
        employee["nivel"] = employee.get("nivel", 0)
        # employee["fecha_contrato"] = employee.get("fecha_contrato", "None")

    # Ticket
    for ticket in data["tickets_emitidos"]:

        # Cambios en la fecha de cierre
        fecha = None
        if ticket["contactos_con_empleados"]:
            fecha = max(iteration["fecha"] for iteration in ticket["contactos_con_empleados"])

        if fecha is not None:
            ticket["fecha_cierre"] = fecha
        else:
            ticket["fecha_cierre"] = ticket.get("fecha_cierre", "None")

        ticket["satisfaccion_cliente"] = ticket.get("satisfaccion_cliente", 1)
        ticket["es_mantenimiento"] = int(ticket["es_mantenimiento"])

    # Incidente
    for incident in data["tipos_incidentes"]:
        incident["nombre"] = incident["nombre"].strip()

    return data


if __name__ == "__main__":
    clean_data = transform_data()
    print(clean_data)
