import datetime
import sqlite3

#Usuario
print("1. Estudiante")
print("2. Docente")

tipo_usuario = input("Seleccione una opción: ")
if tipo_usuario == "1":

    print("\nESTUDIANTE")
    print("1. Realizar evaluación")
    print("2. Ver mis resultados")

    opcion = input("Seleccione una opción: ")
    
elif tipo_usuario == "2":

    print("\nDOCENTE")
    print("1. Evaluaciones")
    print("2. Ver Cursos")
    print("3. Administración Académica")

    opcion = input("Seleccione una opción: ")
    
#opciones
print("1. Realizar evaluación")
print("2. Consultar historial")
print("3. Consultar curso")
print("4. Deficiencias por curso")
print("5. Asignaturas y temas")

#opcion 1
opcion = input("Seleccione una opción: ")

if opcion == "1":
    fecha = datetime.date.today()

    nombre = input("Ingrese Nombre: ")
    nombre_prueba = input("Prueba: ")
    curso = input("Curso: ")

    #BD
    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()

    #Tabla SQ
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

    preguntas = {
        "Algebra": [
            {
                "pregunta": "Resuelve para x:\nx+7=15",
                "respuesta": "8",
                "puntaje": 1
            }
            #Añadir
        ],

        "Fracciones": [
            {
                "pregunta": "Simplifica:\n8/12",
                "respuesta": "2/3",
                "puntaje": 1
            }
            #Añadir
        ],

        "Geometria": [
            {
                "pregunta": "Perímetro de un cuadrado de lado 5",
                "respuesta": "20",
                "puntaje": 1
            }
            #Añadir
        ]
    }

    resultados = {}

    def evaluar_nivel(porcentaje):

        if porcentaje < 50:
            return "Deficiente"

        elif porcentaje < 70:
            return "Estable"

        else:
            return "Adecuado"

    print("\nPrueba de Nivelación Matemática")
    print(f"Evaluación: {nombre_prueba}")
    print(f"Curso: {curso}")
    print(f"Fecha: {fecha}")
    print(f"Estudiante: {nombre}")

    # Realizar prueba
    for tema, lista_preguntas in preguntas.items():

        resultados[tema] = 0

        print("\n" + "=" * 30)
        print(f"Tema: {tema}")
        print("=" * 30)

        for pregunta in lista_preguntas:

            respuesta_usuario = input(pregunta["pregunta"] + "\n> ")

            if respuesta_usuario == pregunta["respuesta"]:
                resultados[tema] += pregunta["puntaje"]


    puntaje_total_obtenido = 0
    puntaje_total_maximo = 0

    #Resultados
    print("\n")
    print("=" * 30)
    print("RESULTADOS")
    print("=" * 30)

    for tema, puntaje_obtenido in resultados.items():

        puntaje_maximo = 0

        for pregunta in preguntas[tema]:
            puntaje_maximo += pregunta["puntaje"]

        porcentaje = (puntaje_obtenido / puntaje_maximo) * 100

        nivel = evaluar_nivel(porcentaje)

        puntaje_total_obtenido += puntaje_obtenido
        puntaje_total_maximo += puntaje_maximo

        print("\n" + "-" * 30)
        print(f"{tema}: {porcentaje:.0f}%")
        print(f"Nivel: {nivel}")
        print(f"Puntaje: {puntaje_obtenido}/{puntaje_maximo}")

        # Guardar BD
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

    #Resumen
    porcentaje_general = (
        puntaje_total_obtenido / puntaje_total_maximo
    ) * 100

    nivel_general = evaluar_nivel(porcentaje_general)

    print("\n" + "=" * 30)
    print("RESUMEN GENERAL")
    print("=" * 30)
    print(f"Promedio General: {porcentaje_general:.0f}%")
    print(f"Nivel General: {nivel_general}")
    print(f"Puntaje Total: {puntaje_total_obtenido}/{puntaje_total_maximo}")

    #Guardar BD
    conexion.commit()
    conexion.close()
elif opcion == "2":

    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()

    estudiante = input("Nombre del estudiante: ")

    cursor.execute(
        """
        SELECT fecha, prueba, curso, tema, porcentaje, nivel
        FROM resultados
        WHERE estudiante = ?
        ORDER BY fecha
        """,
        (estudiante,)
    )

    resultados = cursor.fetchall()

    if len(resultados) == 0:

        print("No se encontraron registros.")

    else:

        prueba_actual = ""

        for fila in resultados:

            fecha = fila[0]
            prueba = fila[1]
            curso = fila[2]
            tema = fila[3]
            porcentaje = fila[4]
            nivel = fila[5]

            encabezado = f"{fecha}-{prueba}-{curso}"

            if encabezado != prueba_actual:

                print("\n" + "=" * 40)
                print(f"Prueba: {prueba}")
                print(f"Fecha: {fecha}")
                print(f"Curso: {curso}")
                print("=" * 40)

                prueba_actual = encabezado

            print(f"{tema}: {porcentaje:.0f}% ({nivel})")

    conexion.close()

elif opcion == "3":

    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()

    curso = input("Ingrese el curso: ")

    cursor.execute(
        """
        SELECT estudiante, tema, porcentaje, nivel
        FROM resultados
        WHERE curso = ?
        ORDER BY estudiante
        """,
        (curso,)
    )

    resultados = cursor.fetchall()
     
    if len(resultados) == 0:

        print("No se encontraron registros para este curso.")
    
    else:

        estudiante_actual = ""

        for fila in resultados:

            estudiante = fila[0]
            tema = fila[1]
            porcentaje = fila[2]
            nivel = fila[3]

            if estudiante != estudiante_actual:

                print("\n" + "=" * 40)
                print("Estudiante:", estudiante)
                print("=" * 40)

                estudiante_actual = estudiante

            print(f"{tema}: {porcentaje:.0f}% ({nivel})")

    conexion.close()

elif opcion == "4":

    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()

    curso = input("Ingrese el curso: ")

    # Obtener temas con dificultades
    cursor.execute(
        """
        SELECT tema, COUNT(*)
        FROM resultados
        WHERE curso = ? AND nivel = 'Deficiente'
        GROUP BY tema
        """,
        (curso,)
    )

    resultados = cursor.fetchall()

    if len(resultados) == 0:

        print("\nNo se encontraron dificultades para este curso.")

    else:

        print("\n" + "=" * 40)
        print(f"DIFICULTADES DEL CURSO {curso}")
        print("=" * 40)

        temas = []

        for i, fila in enumerate(resultados, start=1):

            tema = fila[0]
            cantidad = fila[1]

            temas.append(tema)

            print(f"{i}. {tema} ({cantidad} estudiantes)")

        seleccion = int(input("\nSeleccione un tema: "))

        tema_seleccionado = temas[seleccion - 1]

        # Buscar estudiantes del tema seleccionado
        cursor.execute(
            """
            SELECT estudiante, porcentaje
            FROM resultados
            WHERE curso = ?
            AND tema = ?
            AND nivel = 'Deficiente'
            ORDER BY porcentaje ASC
            """,
            (curso, tema_seleccionado)
        )

        estudiantes = cursor.fetchall()

        print("\n" + "=" * 40)
        print(f"{tema_seleccionado.upper()}")
        print("=" * 40)

        for estudiante, porcentaje in estudiantes:

            print(f"{estudiante} - {porcentaje:.0f}%")

    conexion.close()

elif opcion == "5":

  
    conexion = sqlite3.connect("resultados.db")
    cursor = conexion.cursor()
    cursor.execute("""
CREATE TABLE IF NOT EXISTS asignaturas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT
)
""")
    cursor.execute("""
CREATE TABLE IF NOT EXISTS temas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asignatura TEXT,
    tema TEXT
)
""")

    print("\nADMINISTRACIÓN ACADÉMICA")
    print("1. Crear asignatura")
    print("2. Crear tema")

    subopcion = input("Seleccione una opción: ")
      
    if subopcion == "1":

        nombre_asignatura = input(
            "Nombre de la asignatura: "
        )

        cursor.execute(
            """
            INSERT INTO asignaturas(nombre)
            VALUES (?)
            """,
            (nombre_asignatura,)
        )

        conexion.commit()

        print("Asignatura creada correctamente.")
        
    elif subopcion == "2":

        cursor.execute(
            """
            SELECT nombre
            FROM asignaturas
            """
        )

        asignaturas = cursor.fetchall()

        if len(asignaturas) == 0:

            print(
                "Primero debe crear una asignatura."
            )

        else:

            print("\nAsignaturas disponibles:")

            for i, asignatura in enumerate(
                asignaturas,
                start=1
            ):

                print(
                    f"{i}. {asignatura[0]}"
                )

            seleccion = int(
                input(
                    "\nSeleccione una asignatura: "
                )
            )
            
            if seleccion < 1 or seleccion > len(asignaturas):
                print("Selección inválida.")
                conexion.close()
            
            else:

                asignatura_seleccionada = (
                asignaturas[seleccion - 1][0]
            )

            tema = input(
                "Nombre del tema: "
            )

            cursor.execute(
                """
                INSERT INTO temas(
                    asignatura,
                    tema
                )
                VALUES (?, ?)
                """,
                (
                    asignatura_seleccionada,
                    tema
                )
            )

            conexion.commit()

            print("Tema creado correctamente.")
    conexion.close()

else:

    print("Opción inválida.")