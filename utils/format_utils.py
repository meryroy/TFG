def format_actividad(actividad):
    duracion_str = actividad.duracion.strftime("%H:%M:%S") if actividad.duracion else "N/A"
    texto = f"Actividad: {actividad.disciplina} - {actividad.distancia_km} km - Duración: {duracion_str}"
    if actividad.notas:
        texto += f" - Notas: {actividad.notas}"
    return texto

def format_plan(plan):
    return f"Plan: {plan.disciplina} - {plan.descripcion} - {plan.distancia_km} km"
