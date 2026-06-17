import sqlite3

conexion = sqlite3.connect("resultados.db")
cursor = conexion.cursor()

# TABLAS

cursor.execute("""
CREATE TABLE IF NOT EXISTS evaluaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    curso TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS preguntas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluacion_id INTEGER,
    tema TEXT,
    pregunta TEXT,
    respuesta TEXT,
    puntaje INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS resultados (
    fecha TEXT,
    prueba TEXT,
    curso TEXT,
    estudiante TEXT,
    tema TEXT,
    porcentaje REAL,
    nivel TEXT
)
""")

# MENÚ DOCENTE

print("DOCENTE")
print("1. Evaluaciones")
print("2. Ver Cursos")

opcion = input("Seleccione una opción: ")

# ==================================================
# EVALUACIONES
# ==================================================

if opcion == "1":

    print("\nEVALUACIONES")
    print("1. Evaluaciones realizadas")
    print("2. Crear evaluación")

    subopcion = input("Seleccione una opción: ")

    # ------------------------------------------
    # VER EVALUACIONES
    # ------------------------------------------

    if subopcion == "1":

        cursor.execute("""
        SELECT id, nombre, curso
        FROM evaluaciones
        ORDER BY id
        """)

        evaluaciones = cursor.fetchall()

        if len(evaluaciones) == 0:

            print("\nNo existen evaluaciones.")

        else:

            print("\nEVALUACIONES REGISTRADAS")

            for evaluacion in evaluaciones:

                print("\n" + "=" * 40)
                print(f"ID: {evaluacion[0]}")
                print(f"Nombre: {evaluacion[1]}")
                print(f"Curso: {evaluacion[2]}")
                print("=" * 40)

    # ------------------------------------------
    # CREAR EVALUACIÓN
    # ------------------------------------------

    elif subopcion == "2":

        nombre = input(
            "Nombre evaluación: "
        )

        curso = input(
            "Curso: "
        )

        cursor.execute("""
        INSERT INTO evaluaciones(
            nombre,
            curso
        )
        VALUES (?, ?)
        """,
        (
            nombre,
            curso
        ))

        conexion.commit()

        evaluacion_id = cursor.lastrowid

        cantidad = int(
            input(
                "Cantidad de preguntas: "
            )
        )

        for i in range(cantidad):

            print(f"\nPregunta {i+1}")

            tema = input(
                "Tema: "
            )

            pregunta = input(
                "Pregunta: "
            )

            respuesta = input(
                "Respuesta correcta: "
            )

            puntaje = int(
                input(
                    "Puntaje: "
                )
            )

            cursor.execute("""
            INSERT INTO preguntas(
                evaluacion_id,
                tema,
                pregunta,
                respuesta,
                puntaje
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                evaluacion_id,
                tema,
                pregunta,
                respuesta,
                puntaje
            ))

        conexion.commit()

        print(
            "\nEvaluación creada correctamente."
        )

# ==================================================
# VER CURSOS
# ==================================================

elif opcion == "2":

    cursos = [
        "1°A",
        "1°B",
        "2°A",
        "2°B"
    ]

    print("\nCURSOS")

    for i, curso in enumerate(cursos, start=1):

        print(f"{i}. {curso}")

    seleccion = int(
        input("\nSeleccione un curso: ")
    )

    if seleccion < 1 or seleccion > len(cursos):

        print("Selección inválida.")

    else:

        curso_seleccionado = (
            cursos[seleccion - 1]
        )

        print("\n" + "=" * 40)
        print(f"CURSO {curso_seleccionado}")
        print("=" * 40)

        cursor.execute("""
        SELECT DISTINCT estudiante
        FROM resultados
        WHERE curso = ?
        ORDER BY estudiante
        """,
        (curso_seleccionado,)
        )

        estudiantes = cursor.fetchall()

        if len(estudiantes) == 0:

            print(
                "\nAún no existen estudiantes "
                "con resultados en este curso."
            )

        else:

            print("\nESTUDIANTES")

            for estudiante in estudiantes:

                print(
                    f"- {estudiante[0]}"
                )

# ==================================================
# OPCIÓN INVÁLIDA
# ==================================================

else:

    print("Opción inválida.")

conexion.close()