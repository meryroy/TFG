from db.database import SessionLocal
from db.modelos import Usuario, PlanEntrenamiento, Entrenamiento
from datetime import datetime, timedelta

def cargar_semanas(usuario_id):
    with SessionLocal() as db:
        semanas = (
            db.query(PlanEntrenamiento.semana)
            .filter_by(usuario_id=usuario_id)
            .distinct()
            .order_by(PlanEntrenamiento.semana)
            .all()
        )
    return [s[0] for s in semanas]

def obtener_datos_progreso_semanal(usuario_id, semanas_disponibles, semana_actual):
    dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
    esperada = [0] * 7
    realizada = [0] * 7

    with SessionLocal() as db:
        plan = db.query(PlanEntrenamiento).filter_by(
            usuario_id=usuario_id,
            semana=semana_actual
        ).all()

        for p in plan:
            if p.dia.lower() in dias:
                dia_index = dias.index(p.dia.lower())
                esperada[dia_index] += p.distancia_km or 0

        # Asumiendo una fecha fija para la última semana
        fecha_ultima_semana = datetime(2025, 6, 9).date()
        fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=max(semanas_disponibles) - 1)
        fecha_inicio_semana_actual = fecha_inicio_plan + timedelta(weeks=semana_actual - 1)
        fecha_fin_semana_actual = fecha_inicio_semana_actual + timedelta(days=6)

        entrenamientos = db.query(Entrenamiento).filter(
            Entrenamiento.usuario_id == usuario_id,
            Entrenamiento.fecha >= fecha_inicio_semana_actual,
            Entrenamiento.fecha <= fecha_fin_semana_actual
        ).all()

        dias_en = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        dias_es = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
        mapa_dias = dict(zip(dias_en, dias_es))

        for e in entrenamientos:
            if e.fecha:
                dia_nombre_en = e.fecha.strftime("%A").lower()
                dia_nombre_es = mapa_dias.get(dia_nombre_en, None)

                if dia_nombre_es in dias:
                    dia_index = dias.index(dia_nombre_es)
                    realizada[dia_index] += e.distancia_km or 0

    return {
        'dias': dias,
        'esperada': esperada,
        'realizada': realizada,
        'fecha_inicio_semana_actual': fecha_inicio_semana_actual,
        'fecha_fin_semana_actual': fecha_fin_semana_actual
    }


def obtener_usuario_y_semanas(nombre_usuario):
    with SessionLocal() as db:
        usuario = db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first()
        semanas_plan = []
        if usuario:
            semanas_plan = db.query(PlanEntrenamiento.semana).filter(
                PlanEntrenamiento.usuario_id == usuario.id
            ).distinct().order_by(PlanEntrenamiento.semana).all()
    return {
        "usuario": usuario,
        "semanas": sorted(set(s[0] for s in semanas_plan))
    }


def obtener_datos_progreso_general(usuario_id, disciplina, duracion):
    fecha_ultima_semana = datetime(2025, 6, 9).date()
    fecha_inicio_plan = fecha_ultima_semana - timedelta(weeks=duracion - 1)

    with SessionLocal() as db:
        planes = db.query(PlanEntrenamiento).filter(
            PlanEntrenamiento.usuario_id == usuario_id,
            PlanEntrenamiento.disciplina == disciplina
        ).all()

        plan_por_semana = {}
        for p in planes:
            plan_por_semana[p.semana] = plan_por_semana.get(p.semana, 0) + (p.distancia_km or 0)

        entrenamientos = db.query(Entrenamiento).filter(
            Entrenamiento.usuario_id == usuario_id,
            Entrenamiento.disciplina == disciplina
        ).all()

        real_por_semana = {}
        for e in entrenamientos:
            if e.fecha and e.fecha >= fecha_inicio_plan:
                delta = (e.fecha - fecha_inicio_plan).days
                semana = (delta // 7) + 1
                if 1 <= semana <= duracion:
                    real_por_semana[semana] = real_por_semana.get(semana, 0) + (e.distancia_km or 0)

    semanas = list(range(1, duracion + 1))
    plan_km = [plan_por_semana.get(s, 0) for s in semanas]
    real_km = [real_por_semana.get(s, 0) for s in semanas]

    return {
        "semanas": semanas,
        "plan_km": plan_km,
        "real_km": real_km
    }
