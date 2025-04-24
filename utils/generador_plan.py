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

        def ajustar_carga(disciplina, nivel):
            base = distancias[disciplina] * factor_genero
            if nivel == 'alto':
                return base * 1.5
            elif nivel == 'medio':
                return base * 1.3
            return base * 1.1

        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        for semana in range(1, duracion_plan + 1):
            indice_dia = 0
            for disciplina in ['natacion', 'ciclismo', 'correr']:
                nivel_actual = nivel
                carga = ajustar_carga(disciplina, nivel_actual)
                if semana == duracion_plan:
                    carga *= 0.7  # Tapering

                for _ in range(sesiones[disciplina]):
                    dia_nombre = dias_semana[indice_dia % len(dias_semana)]
                    fecha = datetime.now().date() + timedelta(weeks=semana - 1, days=indice_dia % 7)
                    descripcion = generar_descripcion(disciplina, semana, nivel)

                    plan = PlanEntrenamiento(
                        usuario_id=usuario.id,
                        semana=semana,
                        dia=dia_nombre,
                        disciplina=disciplina,
                        descripcion=descripcion,
                        duracion_min=round(carga * 10),
                        distancia_km=round(carga, 2),
                        fecha=fecha
                    )
                    db.add(plan)
                    indice_dia += 1

            # Añadir día de descanso (Domingo)
            descanso_fecha = datetime.now().date() + timedelta(weeks=semana - 1, days=6)
            plan_descanso = PlanEntrenamiento(
                usuario_id=usuario.id,
                semana=semana,
                dia="Domingo",
                disciplina="Descanso",
                descripcion="Descanso o movilidad suave",
                duracion_min=0,
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
