from flask import Flask, request 
from flask import jsonify
import sqlite3
import os 

direccion = os.getcwd() + '\database\Data.db'
conexion = sqlite3.connect(direccion)
try:
    conexion.execute("""
                    CREATE TABLE factura (
                    id INTEGER primary key autoincrement,
                    numero_factura INTEGER NOT NULL,
                    direccion TEXT NOT NULL,
                    precio INTEGER NOT NULL,
                    nombre_producto varchar(30) NOT NULL,
                    nombre_cliente varchar(20) NOT NULL,
                    CC_cliente INTEGER NOT NULL
                    )
                    """)
except sqlite3.OperationalError:
    print("The database is already created")


app = Flask(__name__)


@app.route('/factura/', methods=['GET'])
def all_products():

    data = []

    conexion = sqlite3.connect(direccion)
    sql = 'SELECT * FROM factura'
    cursor = conexion.execute(sql)
    
    for fila in cursor: 
        nuevo_producto = {
            'numero_factura' : fila[1],
            'direccion' : fila[2],
            'price' : fila[3],
            'nombre_producto' : fila[4],
            'nombre_cliente':fila[5],
            'CC_cliente':fila[6]
        }
        data.append(nuevo_producto)
    conexion.close()

    return jsonify({'result':data})


@app.route('/factura/<idfactura>',methods=['GET'])
def one_product(idfactura):

    conexion = sqlite3.connect(direccion)
    sql = "select * from producto where numero_factura=?"
    cursor = conexion.execute(sql,(idfactura,))
    fila = cursor.fetchone()

    new_data = {
            'numero_factura' : fila[0],
            'direccion' : fila[1],
            'price' : fila[2],
            'nombre_producto' : fila[3],
            'cantidad' : fila[4],
            'nombre_cliente':fila[5],
            'CC_cliente':fila[6]
        }

    conexion.close()

    return jsonify({'result':new_data})


@app.route('/factura/', methods=['POST'])
def new_factura():

    numeroF = request.json['numero_factura']
    direc = request.json['direccion']
    p = request.json['precio']
    nombreP = request.json['nombre_producto']
    nombreC = request.json['nombre_cliente']
    cc = request.json['CC_cliente']

    conexion = sqlite3.connect(direccion)
    sql = 'INSERT INTO factura(numero_factura , direccion, precio, nombre_producto,  nombre_cliente, CC_cliente) VALUES (?,?,?,?,?,?)'
    conexion.execute(sql, (numeroF,direc,p,nombreP, nombreC, cc))
    conexion.commit()
    conexion.close()

    return "h"


@app.route('/factura/<idfactura>', methods=['DELETE'])
def delete_product(idfactura):

    conexion = sqlite3.connect(direccion)
    sql = 'delete from factura where numero_factura =?'
    conexion.execute(sql, (idfactura,))
    conexion.commit()
    conexion.close()
    
