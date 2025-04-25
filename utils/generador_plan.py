from db.database import SessionLocal
from db.modelos import PlanEntrenamiento, Usuario
from datetime import datetime, timedelta

def generar_descripcion(disciplina, semana, nivel):
    if disciplina == 'correr':
        if semana % 4 == 0:
            return "Rodaje largo progresivo"
        elif semana % 3 == 0:
            return "Intervalos cortos (4x400m)"
        else:
            return "Rodaje suave"
    elif disciplina == 'ciclismo':
        if semana % 4 == 0:
            return "Salida larga en terreno variado"
        else:
            return "Rodaje de resistencia"
    elif disciplina == 'natacion':
        if semana % 3 == 0:
            return "Técnica y resistencia con repeticiones"
        else:
            return "Nado continuo moderado"
    return "Sesión estándar"

def generar_plan(usuario_id: int, duracion_plan: int):
    db = SessionLocal()

    try:
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if not usuario:
            raise Exception(f"No se encontró al usuario con ID {usuario_id}")

        categoria = usuario.categoria
        nivel = usuario.nivel
        frecuencia = usuario.frecuencia_semanal
        genero = usuario.genero

        distancias_base = {
            'super_sprint': {'natacion': 0.4, 'ciclismo': 10, 'correr': 2.5},
            'sprint': {'natacion': 0.75, 'ciclismo': 18.6, 'correr': 4.9},
            'estandar': {'natacion': 1.5, 'ciclismo': 40, 'correr': 10}
        }

        sesiones_por_dia = {
            3: {'natacion': 1, 'ciclismo': 1, 'correr': 1},
            4: {'natacion': 2, 'ciclismo': 1, 'correr': 2},
            5: {'natacion': 2, 'ciclismo': 2, 'correr': 2},
            6: {'natacion': 2, 'ciclismo': 2, 'correr': 3},
            7: {'natacion': 3, 'ciclismo': 3, 'correr': 3}
        }

        if categoria not in distancias_base or frecuencia not in sesiones_por_dia:
            raise Exception("Categoría o frecuencia inválida.")

        distancias = distancias_base[categoria]
        sesiones = sesiones_por_dia[frecuencia]
        factor_genero = 0.9 if genero == 'femenino' else 1.0

        # Definir el incremento progresivo según la duración del plan
        if duracion_plan == 6:
            factor_incremento = 0.10  # 10% de incremento semanal
        elif duracion_plan == 8:
            factor_incremento = 0.08  # 8% de incremento semanal
        elif duracion_plan == 12:
            factor_incremento = 0.06  # 6% de incremento semanal
        elif duracion_plan == 24:
            factor_incremento = 0.04  # 4% de incremento semanal
        else:
            factor_incremento = 0.05

        def ajustar_carga(disciplina, nivel, frecuencia, semana):
            # Cálculo de la carga base
            base = distancias[disciplina] * factor_genero
            if nivel == 'alto':
                base *= 1.5
            elif nivel == 'medio':
                base *= 1.3
            else:
                base *= 1.1

            # Factor de ajuste por frecuencia (ajustar la carga de acuerdo con la frecuencia de entrenamientos)
            if frecuencia == 3:
                base *= 1.0
            elif frecuencia == 4:
                base *= 0.9
            elif frecuencia == 5:
                base *= 0.75
            elif frecuencia == 6:
                base *= 0.6
            else:
                base *= 0.5

            # Cálculo de la carga progresiva semanal
            carga_progresiva = base * (1 + factor_incremento * (semana - 1))  # Aumento progresivo semanal
            return carga_progresiva

        # Definir los días de descanso según la frecuencia
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        dias_descanso_por_frecuencia = {
            3: ["Martes", "Miércoles", "Viernes", "Sábado"],
            4: ["Lunes", "Miércoles", "Viernes"],
            5: ["Martes", "Jueves"],
            6: ["Viernes"],
            7: []
        }
        dias_descanso = dias_descanso_por_frecuencia.get(frecuencia, [])

        # Calcular cuántas sesiones por disciplina por semana
        for semana in range(1, duracion_plan + 1):
            indice_dia = 0


            # Generar lista de días hábiles para entrenar en esta semana
            dias_entrenamiento = [d for d in dias_semana if d not in dias_descanso]

            for disciplina in ['natacion', 'ciclismo', 'correr']:
                carga = ajustar_carga(disciplina, nivel, frecuencia, semana)
                if semana == duracion_plan:
                    carga *= 0.7  # Tapering

                for _ in range(sesiones[disciplina]):
                    dia_nombre = dias_entrenamiento[indice_dia % len(dias_entrenamiento)]
                    fecha = datetime.now().date() + timedelta(weeks=semana - 1, days=dias_semana.index(dia_nombre))
                    descripcion = generar_descripcion(disciplina, semana, nivel)

                    plan = PlanEntrenamiento(
                        usuario_id=usuario.id,
                        semana=semana,
                        dia=dia_nombre,
                        disciplina=disciplina,
                        descripcion=descripcion,
                        distancia_km=round(carga, 2),
                        fecha=fecha
                    )
                    db.add(plan)
                    indice_dia += 1

            # Añadir explícitamente los días de descanso si hay
            for dia_descanso in dias_descanso:
                descanso_fecha = datetime.now().date() + timedelta(weeks=semana - 1, days=dias_semana.index(dia_descanso))
                plan_descanso = PlanEntrenamiento(
                    usuario_id=usuario.id,
                    semana=semana,
                    dia=dia_descanso,
                    disciplina="Descanso",
                    descripcion="Descanso o movilidad suave",
                    distancia_km=0,
                    fecha=descanso_fecha
                )
                db.add(plan_descanso)

        db.commit()

    except Exception as e:
        print(f"Error al generar el plan: {e}")
        db.rollback()

    finally:
        db.close()

    print("Plan de entrenamiento generado con éxito.")
