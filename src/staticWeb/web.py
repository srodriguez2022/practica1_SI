import base64
import io
from flask import Flask, render_template
from matplotlib import pyplot as plt
from staticWeb import queries

app = Flask(__name__)


@app.route('/')
def index():
    samples_df = queries.all_samples()
    tickets_valorated_5_df = queries.tickets_valorated_5()
    incidents_per_client_df = queries.incidents_per_client()
    hours_per_incident_df = queries.hours_per_incident()
    hours_per_employee_df = queries.hours_per_employee()
    time_per_incident_df = queries.time_per_incident()
    incidents_per_employee_df = queries.incidents_per_employee()
    average_time_incident_df = queries.average_time_per_incident()
    resolution_time_per_incident_df = queries.resolution_time_per_incident()
    critical_clients_df = queries.critical_clients()

    stats = {
        "Numero_de_muestras_totales": len(samples_df),
        "Media_Incidentes_valorados": tickets_valorated_5_df['SATISFACCION'].mean(),
        "Desviacion_Incidentes_valorados": tickets_valorated_5_df['SATISFACCION'].std(),
        "Media_incidentes_por_clientes": incidents_per_client_df['NUM_INCIDENTS'].mean(),
        "Desviacion_incidentes_por_clientes": incidents_per_client_df['NUM_INCIDENTS'].std(),
        "Media_horas_por_incidentes": hours_per_incident_df['TOTAL_HOURS'].mean(),
        "Desviacion_horas_por_incidentes": hours_per_incident_df['TOTAL_HOURS'].std(),
        "Minimo_horas_por_empleado": hours_per_employee_df['TOTAL_HOURS'].min(),
        "Maximo_horas_pr_empleado": hours_per_employee_df['TOTAL_HOURS'].max(),
        "Minimo_tiempo_por_incidente": time_per_incident_df['DAYS'].min(),
        "Maximo_tiempo_incidente": time_per_incident_df['DAYS'].max(),
        "Minimo_incidentes_por_empleado": incidents_per_employee_df['NUM_INCIDENTS'].min(),
        "Maximo_incidentes_por_empleado": incidents_per_employee_df['NUM_INCIDENTS'].max(),
    }

    # Graph 1
    fig, ax = plt.subplots()
    ax.bar(average_time_incident_df['ES_MANTENIMIENTO'].astype(str), average_time_incident_df['AVG_TIME'])
    ax.set_title("Tiempo medio por incidente")
    ax.set_xlabel("Es mantenimiento")
    ax.set_ylabel("Tiempo medio")

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    graph_1 = base64.b64encode(img.getvalue()).decode()

    # Graph 2
    fig2, ax2 = plt.subplots(figsize=(15, 4))
    resolution_time_per_incident_df.boxplot(column='RESOLUTION_TIME', by='INCIDENT_TYPE', ax=ax2)
    p5 = resolution_time_per_incident_df['RESOLUTION_TIME'].quantile(0.05)
    p90 = resolution_time_per_incident_df['RESOLUTION_TIME'].quantile(0.90)

    ax2.axhline(p5, color='r', linestyle='--', label='Percentil 5')
    ax2.axhline(p90, color='g', linestyle='--', label='Percentil 90')

    ax2.set_title("Boxplot de Tiempo de resolución por tipo de incidente")
    ax2.set_xlabel("Tipo de incidente")
    ax2.set_ylabel("Tiempo de resolución")
    ax2.legend()
    plt.suptitle("")

    img2 = io.BytesIO()
    fig2.savefig(img2, format='png')
    img2.seek(0)
    graph_2 = base64.b64encode(img2.getvalue()).decode()

    # Graph 3
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    ax3.bar(critical_clients_df['CLIENT'], critical_clients_df['INCIDENT_COUNT'], color='red')

    ax3.set_title("5 Clientes más críticos")
    ax3.set_xlabel("Cliente")
    ax3.set_ylabel("Número de incidentes")

    img3 = io.BytesIO()
    fig3.savefig(img3, format='png')
    img3.seek(0)
    graph_3 = base64.b64encode(img3.getvalue()).decode()

    # Graph 4

    acts_per_employee_df = queries.acts_per_employee()

    fig4, ax4 = plt.subplots(figsize=(12, 4))
    ax4.bar(acts_per_employee_df['EMPLEADO_ID'], acts_per_employee_df['NUM_ACTS'], color='blue')

    ax4.set_title("Número total de actuaciones por empleado")
    ax4.set_xlabel("ID del empleado")
    ax4.set_ylabel("Número de actuaciones")

    img4 = io.BytesIO()
    fig4.savefig(img4, format='png')
    img4.seek(0)
    graph_4 = base64.b64encode(img4.getvalue()).decode()

    # Graph 5

    acts_per_weekday_df = queries.acts_per_weekday()

    weekday_map = {0: 'Domingo', 1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado'}
    acts_per_weekday_df['WEEKDAY'] = acts_per_weekday_df['WEEKDAY'].astype(int).map(weekday_map)

    fig5, ax5 = plt.subplots(figsize=(12, 4))
    ax5.bar(acts_per_weekday_df['WEEKDAY'], acts_per_weekday_df['NUM_ACTS'], color='green')

    ax5.set_title("Número total de actuaciones por día de la semana")
    ax5.set_xlabel("Día de la semana")
    ax5.set_ylabel("Número de actuaciones")

    img5 = io.BytesIO()
    fig5.savefig(img5, format='png')
    img5.seek(0)
    graph_5 = base64.b64encode(img5.getvalue()).decode()

    return render_template("index.html",
                           samples=samples_df.to_html(classes='table table-bordered'),
                           tickets=tickets_valorated_5_df.to_html(classes='table table-bordered'),
                           incidents_per_client=incidents_per_client_df.to_html(classes='table table-bordered'),
                           hours_incidents=hours_per_incident_df.to_html(classes='table table-bordered'),
                           hours_employee=hours_per_employee_df.to_html(classes='table table-bordered'),
                           time_incident=time_per_incident_df.to_html(classes='table table-bordered'),
                           incident_employee=incidents_per_employee_df.to_html(classes='table table-bordered'),
                           stats=stats,
                           table_graph1=average_time_incident_df.to_html(classes='table table-bordered'),
                           graph_1=graph_1,
                           table_graph2=resolution_time_per_incident_df.to_html(classes='table table-bordered'),
                           graph_2=graph_2,
                           table_graph3=critical_clients_df.to_html(classes='table table-bordered'),
                           graph_3=graph_3,
                           table_graph4=acts_per_employee_df.to_html(classes='table table-bordered'),
                           graph_4=graph_4,
                           table_graph5=acts_per_weekday_df.to_html(classes='table table-bordered'),
                           graph_5=graph_5)


@app.route('/fraude')
def fraude_analysis():
    # incidentes de fraude (INCIDENCIA_ID=5)
    # empleado, nivel, cliente, tipo y día de la semana.
    emp_df = queries.fraude_by_employee()
    nivel_df = queries.fraude_by_employee_level()
    cliente_df = queries.fraude_by_client()
    inci_df = queries.fraude_by_incident_type()
    weekday_df = queries.fraude_by_weekday()
    fraude_df = queries.fraude_incidents()
    contacts_df = queries.fraude_employe_contacts()
    stats = queries.basic_stats_incidents()

    return render_template(
        "fraude.html",
        emp_table=emp_df.to_html(classes='table table-bordered', index=False),
        nivel_table=nivel_df.to_html(classes='table table-bordered', index=False),
        cliente_table=cliente_df.to_html(classes='table table-bordered', index=False),
        inci_table=inci_df.to_html(classes='table table-bordered', index=False),
        weekday_table=weekday_df.to_html(classes='table table-bordered', index=False),
        fraude_table=fraude_df.to_html(classes='table table-bordered', index=False),
        contacts_table=contacts_df.to_html(classes='table table-bordered', index=False),
        stats_table=stats.to_html(classes='table table-bordered', index=False)
    )

