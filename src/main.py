# PROYECTO CONTROL CONSUMO DE AGUA

# IMPORTACIÓN DE LIBRERIAS
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime, timedelta

# CONEXION MONGODB + BASE DE DATOS + COLECCION
URL_MONGO = 'mongodb+srv://Invitado:Guest5050@cluster0-3lrrr.mongodb.net/test?retryWrites=true&w=majority'
cliente = MongoClient(URL_MONGO, ssl_cert_reqs=False)
db = cliente['primeraBD']
coleccion = db['consumoagua']

app = Flask(__name__)

# FUNCIONES
def convert_to_float(valor, valordefecto):
    try:
        return float(valor)
    except:
        return valordefecto

# RUTAS
@app.route('/', methods=["GET", "POST"])
def home():
    return render_template('index.html')


@app.route("/nuevo")
def nuevoConsumo():
    return render_template('nuevo.html', fecha_actual=datetime.utcnow())


@app.route("/entrar-nuevo", methods=['GET', 'POST'])
def entrarNuevoConsumo():
    if request.method == 'POST':
        try:
            fecha = request.form['fecha']
            # Conversión de texto a float, si no es posible conversión a 0
            manana = convert_to_float(request.form['manana'], 0)
            mediodia = convert_to_float(request.form['mediodia'], 0)
            tarde = convert_to_float(request.form['tarde'], 0)
            noche = convert_to_float(request.form['noche'], 0)
            # sumamos todo y dividimos entre 4 para que nos de litros (4 vasos = litro)
            total = (manana + mediodia + tarde + noche)/4 
            nuevoregistro = {"fecha": fecha, "manana": manana,
                            "mediodia": mediodia, "tarde": tarde, "noche": noche, "total_consumo_diario": total}
            coleccion.insert_one(nuevoregistro)
            return redirect(url_for('nuevoConsumo'))
        except ValueError:
            raise Exception("Valor no posible para conversión")
    return redirect(url_for('nuevoConsumo'))


@app.route("/mostrar-todos")
def mostrarTodos():
    registros = coleccion.find()
    tituloDelListado = "Listado de todos los consumos"
    return render_template('mostrar-todos.html', datos=registros, tituloDelListado=tituloDelListado)


@app.route("/editar/<id>")
def editarConsumo(id):
    buscarPorId = {"_id": ObjectId(id)}
    registro = coleccion.find_one(buscarPorId)
    return render_template('/editar.html', datos=registro)


@app.route("/editar-confirmado/<id>", methods=['GET', 'POST'])
def actualizarConsumo(id):
    if request.method == 'POST':
        fecha = request.form['fecha']
        manana = request.form['manana']
        mediodia = request.form['mediodia']
        tarde = request.form['tarde']
        noche = request.form['noche']
        registroActualizado = {"fecha": fecha, "manana": manana,
                               "mediodia": mediodia, "tarde": tarde, "noche": noche}
        buscarPorId = {"_id": ObjectId(id)}
        coleccion.update_one(buscarPorId, {"$set": registroActualizado})
        return redirect(url_for('mostrarTodos'))
    return redirect(url_for('editarConsumo'))

@app.route("/borrar/<id>")
def borrarConsumo(id):
    buscarPorId = {"_id": ObjectId(id)}
    registro = coleccion.find_one(buscarPorId)
    return render_template('/borrar.html', datos=registro)


@app.route("/confirmar-borrado/<string:id>")
def confirmadoBorrado(id):
    buscarPorId = {"_id": ObjectId(id)}
    coleccion.delete_one(buscarPorId)
    return redirect(url_for('mostrarTodos'))


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port, debug=True)
