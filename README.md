# Gestor de Entrenamiento - Triatlón Madrid

Aplicación de escritorio desarrollada en Python con PySide6 para planificar, registrar y visualizar el progreso de entrenamientos orientados a triatlón.

---

## 📊 Características principales

* Registro de usuarios con plan personalizado de entrenamiento
* Generación automática de planes según:

  * Nivel (bajo, medio, alto)
  * Frecuencia semanal (3 a 7 días)
  * Categoría (Super Sprint, Sprint, Estándar)
  * Género
* Registro manual de actividades deportivas
* Visualización en calendario de:

  * Plan previsto por fecha
  * Actividades realizadas
* Análisis de progreso:

  * Progreso semanal (planificado vs. realizado)
  * Progreso general por disciplina
* Exportación de gráficas como imagen

---

## 🚀 Tecnologías utilizadas

* **Python 3.10+**
* **PySide6**: Interfaz gráfica de usuario
* **SQLAlchemy**: ORM para gestión de base de datos SQLite
* **Matplotlib**: Generación de gráficos
* **Bcrypt**: Encriptación segura de contraseñas

---

## 📁 Estructura del proyecto

```
TFG/
├── db/                     # Configuración y modelos de base de datos
│   ├── database.py
│   └── modelos.py
├── ui/                     # Interfaces gráficas (ventanas/dialogs)
│   ├── inicio.py
│   ├── formulario.py
│   ├── area_usuario.py
│   └── ...
├── controllers/            # Lógica de aplicación y negocio
│   ├── registro_controller.py
│   ├── plan_controller.py
│   └── ...
├── utils/                  # Funciones auxiliares (formatos, fechas, estilos)
│   └── ...
├── css/                    # Estilos visuales (QSS)
│   └── style.css
├── data/                   # Base de datos SQLite generada
│   └── entrenamiento.db
└── main.py                 # Punto de entrada de la aplicación
```

---

## 📅 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/tfg-triatlon.git
cd tfg-triatlon
```

### 2. Crear entorno virtual y activarlo (opcional pero recomendado)

```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación

```bash
python main.py
```

---

## 📃 Dependencias principales (`requirements.txt`)

```txt
PySide6
SQLAlchemy
bcrypt
matplotlib
```

---


## 📄 Licencia

Este proyecto se entrega como parte del Trabajo de Fin de Grado y no está destinado a uso comercial. Uso académico bajo licencia MIT.

---

## 🚀 Autor

**María Roy Bueno**
Tecnico Superior en Desarrollo de Aplicaciones Multiplataforma
Centro de Formación Profesional Alfonso X El Sabio
Curso 2024/2025
