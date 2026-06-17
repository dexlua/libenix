#==============
#Estudiante
#==============

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