"""
Evaluación 3 - Programación Web
Aplicación Flask con un menú principal y dos ejercicios:
  - Ejercicio 1: promedio de 3 notas y estado (aprobado/reprobado) según asistencia.
  - Ejercicio 2: nombre con mayor cantidad de caracteres entre 3 nombres.
"""

from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

# Registros almacenados en memoria (se pierden al reiniciar la aplicación)
historial_notas = []
historial_nombres = []

# Constantes de evaluación
NOTA_MINIMA = 10
NOTA_MAXIMA = 70
NOTA_APROBACION = 40
ASISTENCIA_MINIMA = 75


# ---------------------------------------------------------------------------
# Funciones de lógica
# ---------------------------------------------------------------------------
def calcular_promedio(notas):
    """Devuelve el promedio de una lista de notas, redondeado a 1 decimal."""
    return round(sum(notas) / len(notas), 1)


def obtener_estado(promedio, asistencia):
    """Aprueba solo si el promedio es >= 40 y la asistencia es >= 75 %."""
    if promedio >= NOTA_APROBACION and asistencia >= ASISTENCIA_MINIMA:
        return "APROBADO"
    return "REPROBADO"


def nombre_mas_largo(nombres):
    """Devuelve el nombre con más caracteres y su cantidad de caracteres."""
    mayor = nombres[0]
    for nombre in nombres[1:]:
        if len(nombre) > len(mayor):
            mayor = nombre
    return mayor, len(mayor)


# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Menú principal con los dos botones."""
    return render_template("index.html")


@app.route("/inicio")
def inicio():
    """Redirección: /inicio lleva al menú principal."""
    return redirect(url_for("index"))


@app.route("/ejercicio1", methods=["GET", "POST"])
def ejercicio1():
    promedio = None
    estado = None
    error = None
    datos = {"nota1": "", "nota2": "", "nota3": "", "asistencia": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        try:
            notas = [float(datos["nota1"]), float(datos["nota2"]), float(datos["nota3"])]
            asistencia = float(datos["asistencia"])

            if any(n < NOTA_MINIMA or n > NOTA_MAXIMA for n in notas):
                error = f"Las notas deben estar entre {NOTA_MINIMA} y {NOTA_MAXIMA}."
            elif asistencia < 0 or asistencia > 100:
                error = "La asistencia debe estar entre 0 y 100."
            else:
                promedio = calcular_promedio(notas)
                estado = obtener_estado(promedio, asistencia)
                historial_notas.append(
                    {"notas": notas, "asistencia": asistencia,
                     "promedio": promedio, "estado": estado}
                )
        except ValueError:
            error = "Debes ingresar solo valores numéricos en todos los campos."

    return render_template("ejercicio1.html", promedio=promedio, estado=estado,
                           error=error, datos=datos, historial=historial_notas)


@app.route("/ejercicio2", methods=["GET", "POST"])
def ejercicio2():
    resultado = None
    cantidad = None
    error = None
    datos = {"nombre1": "", "nombre2": "", "nombre3": ""}

    if request.method == "POST":
        datos = {campo: request.form.get(campo, "").strip() for campo in datos}
        nombres = list(datos.values())

        if any(n == "" for n in nombres):
            error = "Debes completar los 3 nombres."
        elif len({n.lower() for n in nombres}) < 3:
            error = "Los 3 nombres deben ser diferentes."
        else:
            resultado, cantidad = nombre_mas_largo(nombres)
            historial_nombres.append(
                {"nombres": nombres, "mayor": resultado, "cantidad": cantidad}
            )

    return render_template("ejercicio2.html", resultado=resultado, cantidad=cantidad,
                           error=error, datos=datos, historial=historial_nombres)


@app.route("/ejercicio/<int:numero>")
def ejercicio(numero):
    """Ruta con parámetro por URL: /ejercicio/1 o /ejercicio/2.
    Si el número no existe, se aborta la conexión con error 404."""
    if numero == 1:
        return redirect(url_for("ejercicio1"))
    if numero == 2:
        return redirect(url_for("ejercicio2"))
    abort(404)


@app.route("/historial/limpiar", methods=["POST"])
def limpiar_historial():
    """Elimina los registros almacenados en memoria."""
    historial_notas.clear()
    historial_nombres.clear()
    return redirect(request.referrer or url_for("index"))


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
