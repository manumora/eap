# Ejercicio Práctico: Gestión de Red con Peewee ORM

Este ejercicio está diseñado para aprender a utilizar **Peewee**, un ORM (Object-Relational Mapping) ligero para Python, para gestionar una base de datos SQLite de infraestructura de red.

## Objetivo
El alumno deberá crear 4 scripts de Python que cubran el ciclo de vida de los datos (CRUD: Create, Read, Update, Delete) de una tabla de Puntos de Acceso (Access Points).

---

## Preparación
1. Asegúrate de tener instalado Peewee en tu entorno virtual (`venv`).
2. Mantén los archivos en la misma carpeta para que las importaciones funcionen correctamente.

---

## Instrucciones del Ejercicio

### 1. Definición del Modelo (`create.py`)
El primer paso es definir la estructura de nuestra base de datos.
- **Tarea**: Define una base de datos SQLite llamada `red_corporativa.db`.
- **Modelo**: Crea una clase `PuntoAcceso` con los siguientes campos:
    - `hostname`: Texto único de máximo 50 caracteres.
    - `ip`: Texto único (máximo 15 caracteres).
    - `planta`: Entero.
    - `activo`: Booleano (por defecto `True`).
- **Acción**: El script debe conectar a la base de datos y crear la tabla.

### 2. Inserción de Datos (`insert.py`)
Una vez creada la tabla, debemos poblarla con información.
- **Tarea**: Importa el modelo `PuntoAcceso`.
- **Acción**: Implementa tres formas de insertar datos (e inserta datos de prueba):
    1. Creando una instancia y llamando a `.save()`.
    2. Usando el método de clase `.create()`.
    3. Usando `.insert_many()` para una lista de diccionarios.

### 3. Actualización de Registros (`update.py`)
Aprenderemos a modificar datos existentes.
- **Tarea**: Busca un punto de acceso por su `hostname` (que tenga estado activo), y cambia su estado a inactivo (`activo = False`).
- **Acción Adicional**: Realiza una actualización masiva (ej. mover todos los APs de una planta a otra) usando el método `.update()`.

### 4. Eliminación de Registros (`delete.py`)
Por último, gestionaremos el borrado de datos.
- **Tarea**: Elimina un registro específico usando `.delete_instance()`.
- **Tarea**: Elimina registros que cumplan una condición (ej. todos los que estén inactivos) usando `.delete().where(...)`.

---

## Notas Importantes
- **Orden de ejecución**: Debes ejecutar `create.py` obligatoriamente antes que los demás para que la base de datos exista.
- **Commits en DB**: Recuerda que en Peewee, si modificas un objeto manualmente, debes llamar a `.save()` para que los cambios se guarden en el archivo `.db`.
- **DoesNotExist vs None**: Aprender la diferencia entre `.get()` (lanza excepción si falla) y `.get_or_none()` (manejable con un `if`).
- **Idempotencia**: El script `create.py` no debe intentar crear la tabla si esta ya existe. Un buen script debe poder ejecutarse varias veces sin fallar.