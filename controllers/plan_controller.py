from datetime import datetime, timedelta
from db.modelos import PlanEntrenamiento

class PlanController:
    @staticmethod
    def generar_plan(usuario, duracion_plan, db):
        from datetime import timedelta
        from db.modelos import PlanEntrenamiento

        categoria = usuario.categoria
        nivel = usuario.nivel
        frecuencia = usuario.frecuencia_semanal
        genero = usuario.genero

        distancias_base = {
            'super_sprint': {'natacion': 0.4, 'ciclismo': 10, 'correr': 2.5},
            'sprint': {'natacion': 0.75, 'ciclismo': 18.6, 'correr': 4.9},
            'estándar': {'natacion': 1.5, 'ciclismo': 40, 'correr': 10}
        }

        if categoria not in distancias_base:
            raise Exception("Categoría inválida.")

        distancias = distancias_base[categoria]
        factor_genero = 0.9 if genero == 'femenino' else 1.0

        factor_incremento = {
            6: 0.10,
            8: 0.08,
            12: 0.06,
            24: 0.04
        }.get(duracion_plan, 0.05)

        def calcular_objetivo(disciplina):
            base = distancias[disciplina] * factor_genero
            if frecuencia in [3, 4]:
                return base * {'alto': 1.7, 'medio': 1.5, 'bajo': 1.3}[nivel]
            else:
                return base * {'alto': 1.5, 'medio': 1.3, 'bajo': 1.1}[nivel]

        def ajustar_carga(disciplina, semana):
            carga_final = calcular_objetivo(disciplina)
            # Progresión lineal inversa: calculamos el punto inicial para que el incremento acumulado nos lleve al objetivo
            progreso = (1 + factor_incremento) ** (semana - 1)
            progreso_total = (1 + factor_incremento) ** (duracion_plan - 1)
            carga = carga_final * (progreso / progreso_total)
            return carga * 0.7 if semana == duracion_plan else carga

        plan_dias = {
            3: {"Lunes": "correr", "Miércoles": "natacion", "Sábado": "ciclismo"},
            4: {"Lunes": "correr", "Miércoles": "natacion", "Jueves": "correr", "Sábado": "ciclismo"},
            5: {"Lunes": "correr", "Martes": "ciclismo", "Jueves": "correr", "Viernes": "natacion", "Sábado": "ciclismo"},
            6: {"Lunes": "correr", "Martes": "ciclismo", "Miércoles": "natacion", "Viernes": "correr", "Sábado": "ciclismo", "Domingo": "natacion"},
            7: {"Lunes": "correr", "Martes": "ciclismo", "Miércoles": "natacion", "Jueves": "correr", "Viernes": "correr", "Sábado": "ciclismo", "Domingo": "natacion"}
        }.get(frecuencia)

        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        fecha_inicio_plan = usuario.fecha_inicio_plan

        for semana in range(1, duracion_plan + 1):
            for dia in dias_semana:
                disciplina = plan_dias.get(dia, "Descanso")
                descripcion = "Descanso o movilidad suave" if disciplina == "Descanso" else PlanController.generar_descripcion(disciplina, semana, nivel)
                distancia_km = 0 if disciplina == "Descanso" else round(ajustar_carga(disciplina, semana), 2)

                plan = PlanEntrenamiento(
                    usuario_id=usuario.id,
                    fecha=fecha_inicio_plan + timedelta(weeks=semana - 1),
                    semana=semana,
                    dia=dia,
                    disciplina=disciplina,
                    distancia_km=distancia_km,
                    descripcion=descripcion
                )
                db.add(plan)

        db.commit()

    @staticmethod
    def generar_descripcion(disciplina, semana, nivel):
        if disciplina == 'correr':
            return "Rodaje largo progresivo" if semana % 4 == 0 else ("Intervalos cortos (4x400m)" if semana % 3 == 0 else "Rodaje suave")
        if disciplina == 'ciclismo':
            return "Salida larga en terreno variado" if semana % 4 == 0 else "Rodaje de resistencia"
        if disciplina == 'natacion':
            return "Técnica y resistencia con repeticiones" if semana % 3 == 0 else "Nado continuo moderado"
        return "Sesión estándar"
