import sqlite3
import datetime

conexion = sqlite3.connect("resultados.db")
cursor = conexion.cursor()

print("LIBENIX")
print(" ")
print("Modo de Ingreso")
print("1. Docente")
print("2. Estudiante")
print(" ")
tipo_usuario = input("Seleccione una opción: ")

if tipo_usuario == "1":
        
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

elif tipo_usuario == "2":
    import sqlite3
    import datetime

    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()


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


    def evaluar_nivel(porcentaje):

            if porcentaje < 50:
                return "Deficiente"

            elif porcentaje < 70:
                return "Estable"

            else:
                return "Adecuado"

    print("ESTUDIANTE")
    print("1. Realizar evaluación")
    print("2. Ver mis resultados")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":

            nombre = input("Nombre: ")
            curso = input("Curso: ")

            cursor.execute(
                """
                SELECT id, nombre
                FROM evaluaciones
                WHERE curso = ?
                """,
                (curso,)
            )

            evaluaciones = cursor.fetchall()

            if len(evaluaciones) == 0:

                print(
                    "\nNo existen evaluaciones para este curso."
                )

            else:

                print("\nEVALUACIONES DISPONIBLES")

                for evaluacion in evaluaciones:

                    print(
                        f"{evaluacion[0]}. "
                        f"{evaluacion[1]}"
                    )

                evaluacion_id = int(
                    input(
                        "\nSeleccione una evaluación: "
                    )
                )

                nombre_prueba = ""

                for evaluacion in evaluaciones:

                    if evaluacion[0] == evaluacion_id:

                        nombre_prueba = evaluacion[1]

                cursor.execute(
                    """
                    SELECT tema,
                        pregunta,
                        respuesta,
                        puntaje
                    FROM preguntas
                    WHERE evaluacion_id = ?
                    """,
                    (evaluacion_id,)
                )

                preguntas = cursor.fetchall()

                resultados = {}
                maximos = {}

                print("\nINICIO DE EVALUACIÓN")

                for pregunta in preguntas:

                    tema = pregunta[0]
                    texto = pregunta[1]
                    respuesta_correcta = pregunta[2]
                    puntaje = pregunta[3]

                    if tema not in resultados:

                        resultados[tema] = 0
                        maximos[tema] = 0

                    maximos[tema] += puntaje

                    respuesta_usuario = input(
                        f"\n{texto}\n> "
                    )

                    if (
                        respuesta_usuario.strip().lower()
                        ==
                        respuesta_correcta.strip().lower()
                    ):

                        resultados[tema] += puntaje

                fecha = datetime.date.today()

                print("\nRESULTADOS")

                for tema in resultados:

                    porcentaje = (
                        resultados[tema]
                        /
                        maximos[tema]
                    ) * 100

                    nivel = evaluar_nivel(
                        porcentaje
                    )

                    print(
                        f"{tema}: "
                        f"{porcentaje:.0f}% "
                        f"({nivel})"
                    )

                    cursor.execute(
                        """
                        INSERT INTO resultados
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            str(fecha),
                            nombre_prueba,
                            curso,
                            nombre,
                            tema,
                            porcentaje,
                            nivel
                        )
                    )

                conexion.commit()

                print(
                    "\nEvaluación finalizada."
                )

    elif opcion == "2":

                estudiante = input(
                    "Nombre del estudiante: "
                )

                cursor.execute(
                    """
                    SELECT fecha,
                        prueba,
                        curso,
                        tema,
                        porcentaje,
                        nivel
                    FROM resultados
                    WHERE estudiante = ?
                    ORDER BY fecha
                    """,
                    (estudiante,)
                )

                resultados = cursor.fetchall()

                if len(resultados) == 0:

                    print(
                        "No existen resultados."
                    )

                else:

                    prueba_actual = ""

                    for fila in resultados:

                        fecha = fila[0]
                        prueba = fila[1]
                        curso = fila[2]
                        tema = fila[3]
                        porcentaje = fila[4]
                        nivel = fila[5]

                        encabezado = (
                            f"{fecha}"
                            f"{prueba}"
                            f"{curso}"
                        )

                        if encabezado != prueba_actual:

                            print("\n" + "=" * 40)
                            print(f"Prueba: {prueba}")
                            print(f"Fecha: {fecha}")
                            print(f"Curso: {curso}")
                            print("=" * 40)

                            prueba_actual = encabezado

                        print(
                            f"{tema}: "
                            f"{porcentaje:.0f}% "
                            f"({nivel})"
                        )
    else:

        print("Opción inválida.")

    conexion.close()

else:

    print("Opción inválida.")

conexion.close()

