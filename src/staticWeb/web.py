from flask import Flask, render_template
import queries

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

    return render_template("index.html",
                           samples=samples_df.to_html(classes='table table-bordered'),
                           tickets=tickets_valorated_5_df.to_html(classes='table table-bordered'),
                           incidents_per_client=incidents_per_client_df.to_html(classes='table table-bordered'),
                           hours_incidents=hours_per_incident_df.to_html(classes='table table-bordered'),
                           hours_employee=hours_per_employee_df.to_html(classes='table table-bordered'),
                           time_incident=time_per_incident_df.to_html(classes='table table-bordered'),
                           incident_employee=incidents_per_employee_df.to_html(classes='table table-bordered'),
                           stats=stats)


@app.route('/fraude')
def fraude_analysis():
        # incidentes de fraude (INCIDENCIA_ID=5)
        # empleado, nivel, cliente, tipo y día de la semana.

        emp_df = queries.fraude_by_employee()
        nivel_df = queries.fraude_by_employee_level()
        cliente_df = queries.fraude_by_client()
        inci_df = queries.fraude_by_incident_type()
        weekday_df = queries.fraude_by_weekday()

        # estadisticas basicas
        stats_emp = {
            'incident': queries.compute_basic_stats(emp_df, 'NUM_INCIDENTS'),
            'contact': queries.compute_basic_stats(emp_df, 'NUM_CONTACTS')
        }

        return render_template(
            "fraude.html",
            emp_table=emp_df.to_html(classes='table table-bordered', index=False),
            nivel_table=nivel_df.to_html(classes='table table-bordered', index=False),
            cliente_table=cliente_df.to_html(classes='table table-bordered', index=False),
            inci_table=inci_df.to_html(classes='table table-bordered', index=False),
            weekday_table=weekday_df.to_html(classes='table table-bordered', index=False),
            stats_emp=stats_emp
        )

if __name__ == '__main__':
    app.run(debug=True)
