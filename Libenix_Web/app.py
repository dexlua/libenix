from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DB = "libenix.db"


# ==========================
# CONEXIÓN
# ==========================

def conectar():
    return sqlite3.connect(DB)


# ==========================
# CREAR TABLAS
# ==========================

def init_db():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS evaluaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        curso TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS preguntas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        evaluacion_id INTEGER,
        tema TEXT,
        pregunta TEXT,
        respuesta TEXT,
        puntaje INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS resultados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante TEXT,
    evaluacion_id INTEGER,
    tema TEXT,
    porcentaje REAL,
    nivel TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS respuestas_estudiante (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante TEXT,
    evaluacion_id INTEGER,
    pregunta_id INTEGER,
    respuesta TEXT
    )
    """)
    conn.commit()
    conn.close()


init_db()


# ==========================
# INICIO
# ==========================

@app.route("/")
def inicio():

    return render_template(
        "index.html"
    )


# ==========================
# DOCENTE
# ==========================

@app.route("/docente")
def docente():

    return render_template(
        "docente.html"
    )


# ==========================
# ESTUDIANTE
# ==========================

@app.route("/estudiante", methods=["GET", "POST"])
def estudiante():

    if request.method == "POST":

        curso = request.form["curso"]

        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
        SELECT id, nombre
        FROM evaluaciones
        WHERE curso = ?
        """, (curso,))

        evaluaciones = cur.fetchall()

        conn.close()

        return render_template(
            "lista_evaluaciones.html",
            curso=curso,
            evaluaciones=evaluaciones
        )

    return render_template(
        "estudiante.html"
    )

# ==========================
# CREAR EVALUACIÓN
# ==========================

@app.route(
    "/crear-evaluacion",
    methods=["GET", "POST"]
)
def crear_evaluacion():

    if request.method == "POST":

        nombre = request.form["nombre"]
        curso = request.form["curso"]

        cantidad = int(
            request.form["cantidad"]
        )

        return render_template(
            "preguntas.html",
            nombre=nombre,
            curso=curso,
            cantidad=cantidad
        )

    return render_template(
        "crear_evaluacion.html"
    )


# ==========================
# GUARDAR EVALUACIÓN
# ==========================

@app.route(
    "/guardar-evaluacion",
    methods=["POST"]
)
def guardar_evaluacion():

    conn = conectar()
    cur = conn.cursor()

    nombre = request.form["nombre"]
    curso = request.form["curso"]

    cantidad = int(
        request.form["cantidad"]
    )

    cur.execute("""
    INSERT INTO evaluaciones(
        nombre,
        curso
    )
    VALUES (?, ?)
    """, (
        nombre,
        curso
    ))

    evaluacion_id = cur.lastrowid

    for i in range(cantidad):

        tema = request.form[f"tema_{i}"]
        pregunta = request.form[f"pregunta_{i}"]
        respuesta = request.form[f"respuesta_{i}"]

        puntaje = int(
            request.form[f"puntaje_{i}"]
        )

        cur.execute("""
        INSERT INTO preguntas(
            evaluacion_id,
            tema,
            pregunta,
            respuesta,
            puntaje
        )
        VALUES (?, ?, ?, ?, ?)
        """, (
            evaluacion_id,
            tema,
            pregunta,
            respuesta,
            puntaje
        ))

    conn.commit()
    conn.close()

    return redirect(
        url_for(
            "ver_evaluaciones"
        )
    )


# ==========================
# VER EVALUACIONES
# ==========================

@app.route("/evaluaciones")
def ver_evaluaciones():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    SELECT id, nombre, curso
    FROM evaluaciones
    ORDER BY curso, nombre
    """)

    registros = cur.fetchall()

    conn.close()

    cursos = {}

    for fila in registros:

        curso = fila[2]

        if curso not in cursos:
            cursos[curso] = []

        cursos[curso].append(fila)

    return render_template(
        "evaluaciones.html",
        cursos=cursos
    )

@app.route("/rendir/<int:id>", methods=["GET", "POST"])
def rendir(id):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    SELECT nombre, curso
    FROM evaluaciones
    WHERE id = ?
    """, (id,))

    evaluacion = cur.fetchone()

    cur.execute("""
    SELECT id,
           tema,
           pregunta,
           respuesta,
           puntaje
    FROM preguntas
    WHERE evaluacion_id = ?
    """, (id,))

    preguntas = cur.fetchall()

    if request.method == "POST":

        resultados_tema = {}
        total_tema = {}

        estudiante = request.form["estudiante"]

        correctas = 0
        total = len(preguntas)

        for pregunta in preguntas:

            pregunta_id = pregunta[0]
            tema = pregunta[1]
            respuesta_correcta = pregunta[3]

            respuesta_usuario = request.form.get(f"pregunta_{pregunta_id}")

            # guardar respuesta estudiante
            cur.execute("""
            INSERT INTO respuestas_estudiante(
                estudiante,
                evaluacion_id,
                pregunta_id,
                respuesta
            )
            VALUES (?, ?, ?, ?)
            """, (
                estudiante,
                id,
                pregunta_id,
                respuesta_usuario
            ))

            if tema not in resultados_tema:
                resultados_tema[tema] = 0
                total_tema[tema] = 0

            total_tema[tema] += 1

            if respuesta_usuario:

                if respuesta_usuario.strip().lower() == respuesta_correcta.strip().lower():
                    correctas += 1
                    resultados_tema[tema] += 1

        porcentaje = 0

        if total > 0:
            porcentaje = (correctas / total) * 100

        # -------------------------
        # NIVEL (NUEVO)
        # -------------------------
        nivel = "Reprobado"

        if porcentaje > 75:
            nivel = "Aprobado"
        elif porcentaje > 50:
            nivel = "Estable"

        # guardar resultado general
        cur.execute("""
        INSERT INTO resultados(
            estudiante,
            evaluacion_id,
            porcentaje,
            nivel
        )
        VALUES (?, ?, ?, ?)
        """, (
            estudiante,
            id,
            porcentaje,
            nivel
        ))

        conn.commit()

        falencias = []

        for tema in resultados_tema:

            porcentaje_tema = (
                resultados_tema[tema] /
                total_tema[tema]
            ) * 100

            if porcentaje_tema < 70:
                falencias.append(
                    f"{tema} ({round(porcentaje_tema,2)}%)"
                )

        conn.close()

        return render_template(
            "resultado_prueba.html",
            correctas=correctas,
            total=total,
            porcentaje=round(porcentaje, 2),
            nivel=nivel,
            falencias=falencias
        )

    return render_template(
        "rendir.html",
        evaluacion=evaluacion,
        preguntas=preguntas
    )

@app.route("/resultados/<int:evaluacion_id>")
def ver_resultados(evaluacion_id):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    SELECT estudiante, porcentaje
    FROM resultados
    WHERE evaluacion_id = ?
    ORDER BY porcentaje DESC
    """, (evaluacion_id,))

    resultados = cur.fetchall()

    conn.close()

    return render_template(
        "ver_resultados.html",
        resultados=resultados,
        evaluacion_id=evaluacion_id
    )

@app.route("/detalle/<int:evaluacion_id>/<estudiante>")
def detalle_estudiante(evaluacion_id, estudiante):

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
    SELECT p.tema,
           p.pregunta,
           p.respuesta,
           r.respuesta
    FROM preguntas p
    LEFT JOIN respuestas_estudiante r
    ON p.id = r.pregunta_id
    AND r.estudiante = ?
    WHERE p.evaluacion_id = ?
    """, (estudiante, evaluacion_id))

    preguntas = cur.fetchall()

    conn.close()

    return render_template(
        "detalle_estudiante.html",
        preguntas=preguntas,
        estudiante=estudiante,
        evaluacion_id=evaluacion_id
    )
# ==========================
# EJECUTAR
# ==========================

if __name__ == "__main__":

    app.run(
        debug=True
    )