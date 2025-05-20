from datetime import datetime, timedelta

from db.modelos import PlanEntrenamiento

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

def generar_plan(usuario, duracion_plan, db):
    try:
        categoria = usuario.categoria
        nivel = usuario.nivel
        frecuencia = usuario.frecuencia_semanal
        genero = usuario.genero

        distancias_base = {
            'super_sprint': {'natacion': 0.4, 'ciclismo': 10, 'correr': 2.5},
            'sprint': {'natacion': 0.75, 'ciclismo': 18.6, 'correr': 4.9},
            'estandar': {'natacion': 1.5, 'ciclismo': 40, 'correr': 10}
        }

        if categoria not in distancias_base:
            raise Exception("Categoría inválida.")

        distancias = distancias_base[categoria]
        factor_genero = 0.9 if genero == 'femenino' else 1.0

        if duracion_plan == 6:
            factor_incremento = 0.10
        elif duracion_plan == 8:
            factor_incremento = 0.08
        elif duracion_plan == 12:
            factor_incremento = 0.06
        elif duracion_plan == 24:
            factor_incremento = 0.04
        else:
            factor_incremento = 0.05

        def ajustar_carga(disciplina, nivel, semana):
            base = distancias[disciplina] * factor_genero

            if frecuencia in [3, 4]:
                if nivel == 'alto':
                    base *= 1.9
                elif nivel == 'medio':
                    base *= 1.7
                else:
                    base *= 1.4
            else:
                if nivel == 'alto':
                    base *= 1.5
                elif nivel == 'medio':
                    base *= 1.3
                else:
                    base *= 1.1

            carga = base * (1 + factor_incremento * (semana - 1))
            if semana == duracion_plan:
                carga *= 0.7  # aplicar tapering
            return carga

        plan_dias_por_frecuencia = {
            3: {
                "Lunes": "correr",
                "Martes": "Descanso",
                "Miércoles": "natacion",
                "Jueves": "Descanso",
                "Viernes": "Descanso",
                "Sábado": "ciclismo",
                "Domingo": "Descanso"
            },
            4: {
                "Lunes": "correr",
                "Martes": "Descanso",
                "Miércoles": "natacion",
                "Jueves": "correr",
                "Viernes": "Descanso",
                "Sábado": "ciclismo",
                "Domingo": "Descanso"
            },
            5: {
                "Lunes": "correr",
                "Martes": "ciclismo",
                "Miércoles": "Descanso",
                "Jueves": "correr",
                "Viernes": "natacion",
                "Sábado": "ciclismo",
                "Domingo": "Descanso"
            },
            6: {
                "Lunes": "correr",
                "Martes": "ciclismo",
                "Miércoles": "natacion",
                "Jueves": "Descanso",
                "Viernes": "correr",
                "Sábado": "ciclismo",
                "Domingo": "natacion"
            },
            7: {
                "Lunes": "correr",
                "Martes": "ciclismo",
                "Miércoles": "natacion",
                "Jueves": "correr",
                "Viernes": "correr",
                "Sábado": "ciclismo",
                "Domingo": "natacion"
            }
        }

        if frecuencia not in plan_dias_por_frecuencia:
            raise Exception(f"Frecuencia semanal inválida: {frecuencia}")

        plan_dias = plan_dias_por_frecuencia[frecuencia]
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

        fecha_inicio_plan = usuario.fecha_inicio_plan

        for semana in range(1, duracion_plan + 1):
            for dia in dias_semana:
                disciplina = plan_dias[dia]

                if disciplina == "Descanso":
                    descripcion = "Descanso o movilidad suave"
                    distancia_km = 0
                else:
                    carga = ajustar_carga(disciplina, nivel, semana)
                    descripcion = generar_descripcion(disciplina, semana, nivel)
                    distancia_km = round(carga, 2)

                fecha_entrenamiento = fecha_inicio_plan + timedelta(weeks=semana - 1)

                plan = PlanEntrenamiento(
                    usuario_id=usuario.id,
                    fecha=fecha_entrenamiento,
                    semana=semana,
                    dia=dia,
                    disciplina=disciplina,
                    distancia_km=distancia_km,
                    descripcion=descripcion
                )

                db.add(plan)

        db.commit()

    except Exception as e:
        print(f"Error al generar plan: {e}")
