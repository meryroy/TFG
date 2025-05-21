from datetime import timedelta

DIAS_SEMANA = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

def mapear_planes_a_fechas(planes, fecha_ultima_semana):
    """
    Mapea los planes de entrenamiento a fechas exactas según semana y día.
    Retorna un diccionario: {fecha: plan}, y la fecha de inicio del plan.
    """
    if not planes:
        return {}, None

    duracion_plan = max(plan.semana for plan in planes)
    fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=duracion_plan - 1)
    plan_por_fecha = {}

    for plan in planes:
        if plan.dia not in DIAS_SEMANA:
            continue
        dia_index = DIAS_SEMANA.index(plan.dia)
        fecha_mapeada = fecha_inicio_plan + timedelta(weeks=plan.semana - 1, days=dia_index)
        plan_por_fecha[fecha_mapeada] = plan  # fecha_mapeada es datetime.date

    return plan_por_fecha, fecha_inicio_plan
