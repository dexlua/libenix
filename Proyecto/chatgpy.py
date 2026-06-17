print("================================")
print("SISTEMA DE EVALUACIÓN")
print("================================")

print("1. Estudiante")
print("2. Docente")

tipo_usuario = input("Seleccione una opción: ")

# ---------------- ESTUDIANTE ----------------

if tipo_usuario == "1":

    print("\n================================")
    print("ESTUDIANTE")
    print("================================")

    print("1. Realizar evaluación")
    print("2. Ver mis resultados")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":

        print("Realizar evaluación")

    elif opcion == "2":

        print("Ver mis resultados")

    else:

        print("Opción inválida.")

# ---------------- DOCENTE ----------------

elif tipo_usuario == "2":

    print("\n================================")
    print("DOCENTE")
    print("================================")

    print("1. Evaluaciones")
    print("2. Ver Cursos")
    print("3. Administración Académica")

    opcion = input("Seleccione una opción: ")

    # ---------- EVALUACIONES ----------

    if opcion == "1":

        print("\n================================")
        print("EVALUACIONES")
        print("================================")

        print("1. Evaluaciones realizadas")
        print("2. Crear evaluación")

        subopcion = input("Seleccione una opción: ")

        if subopcion == "1":

            print("Evaluaciones realizadas")

        elif subopcion == "2":

            print("Crear evaluación")

        else:

            print("Opción inválida.")

    # ---------- VER CURSOS ----------

    elif opcion == "2":

        print("\n================================")
        print("VER CURSOS")
        print("================================")

        print("1. Estudiantes")
        print("2. Resultados Generales")
        print("3. Dificultades")

        subopcion = input("Seleccione una opción: ")

        if subopcion == "1":

            print("Estudiantes")

        elif subopcion == "2":

            print("Resultados Generales")

        elif subopcion == "3":

            print("Dificultades")

        else:

            print("Opción inválida.")

    # ---------- ADMINISTRACIÓN ACADÉMICA ----------

    elif opcion == "3":

        print("\n================================")
        print("ADMINISTRACIÓN ACADÉMICA")
        print("================================")

        print("1. Crear asignatura")
        print("2. Crear tema")
        print("3. Ver asignaturas y temas")

        subopcion = input("Seleccione una opción: ")

        if subopcion == "1":

            print("Crear asignatura")

        elif subopcion == "2":

            print("Crear tema")

        elif subopcion == "3":

            print("Ver asignaturas y temas")

        else:

            print("Opción inválida.")

    else:

        print("Opción inválida.")

else:

    print("Opción inválida.")