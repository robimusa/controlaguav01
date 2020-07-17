# PROYECTO CONTROL CONSUMO DE AGUA

# IMPORTACIÓN DE LIBRERIAS
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

# CONEXION MONGODB + BASE DE DATOS + COLECCION
URL_MONGO = 'mongodb+srv://Invitado:Guest5050@cluster0-3lrrr.mongodb.net/test?retryWrites=true&w=majority'
cliente = MongoClient(URL_MONGO, ssl_cert_reqs=False)
db = cliente['primeraBD']
coleccion = db['consumoagua']

app = Flask(__name__)

# RUTAS
@app.route('/', methods=["GET","POST"])
def home():
    return render_template ('index.html')



if __name__ == '__main__':
    port = int(os.environ.get("PORT",4000))
    app.run(host='0.0.0.0',port=port,debug=True)