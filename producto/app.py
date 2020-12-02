from flask import Flask, request 
from flask import jsonify
import sqlite3
import os 

direccion = os.getcwd() + '\database\Data.db'
conexion = sqlite3.connect(direccion)
try:
    conexion.execute("""
                    CREATE TABLE producto (
                    id INTEGER primary key autoincrement,
                    nombre_producto varchar(30) NOT NULL,
                    descripcion TEXT NOT NULL, 
                    precio INTEGER NOT NULL,
                    nombre_imagen TEXT NOT NULL,
                    cantidad INTEGER
                    )
                    """)
except sqlite3.OperationalError:
    print("The database is already created")


app = Flask(__name__)


@app.route('/producto/', methods=['GET'])
def all_products():
    
    data = []

    conexion = sqlite3.connect(direccion)
    sql = 'SELECT * FROM producto'
    cursor = conexion.execute(sql)

    for fila in cursor: 
        nuevo_producto = {
            'name' : fila[1],
            'description' : fila[2],
            'price' : fila[3],
            'pictureName' : fila[4], 
            'amount':fila[5]
        }
        data.append(nuevo_producto)
    conexion.close()
        
    return jsonify({'result':data})


@app.route('/producto/<name>',methods=['GET'])
def one_product(name):

    conexion = sqlite3.connect(direccion)
    sql = "select * from producto where nombre_producto=?"
    cursor = conexion.execute(sql,(name,))
    fila = cursor.fetchone()

    new_data = {
            'name' : fila[1],
            'description' : fila[2],
            'price' : fila[3],
            'picture' : fila[4],
            'amount' : fila[5]
        }

    conexion.close()

    return jsonify({'result':new_data})


@app.route('/producto/', methods=['POST'])
def new_product():
    
    nombre = request.json['name']
    descripcion = request.json['description']
    precio = request.json['price']
    nombreImagen = request.json['picture']
    cantidad = request.json['amount']
    
    conexion = sqlite3.connect(direccion)
    sql = 'INSERT INTO producto(nombre_producto, descripcion, precio, nombre_imagen, cantidad) VALUES (?,?,?,?,?)'
    conexion.execute(sql, (nombre, descripcion, precio, nombreImagen, cantidad))
    conexion.commit()
    conexion.close()

    return "h"


@app.route('/producto/<name>', methods=['PUT'])
def update(name):
    
    descripcion = request.json['descriction']
    precio = request.json['price']
    nombreImagen = request.json['photoName']

    conexion = sqlite3.connect(direccion)
    sql = 'update producto set descripcion=?, precio=?,  nombre_imagen=?  where nombre_producto=?'
    conexion.execute(sql,(descripcion, precio, nombreImagen, name))
    conexion.commit()
    conexion.close()


@app.route('/producto/<name>', methods=['DELETE'])
def delete_product(name):

    conexion = sqlite3.connect(direccion)
    sql = 'delete from producto where nombre_producto =?'
    conexion.execute(sql, (name,))
    conexion.commit()
    conexion.close()
    
