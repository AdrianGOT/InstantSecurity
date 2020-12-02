from flask import Flask, request
from flask import jsonify
import sqlite3
import os 


direccion = os.getcwd() + '\database\Data.db'
conexion = sqlite3.connect(direccion)

try:
    conexion.execute("""
                    CREATE TABLE usuario (
                        
                    id INTEGER primary key autoincrement,
                    nombre varchar(25) NOT NULL,
                    apellido varchar(25) NOT NULL, 
                    CC INTEGER NOT NULL,
                    celular INTEGER NOT NULL,
                    email varchar(40) NOT NULL,
                    d TEXT NOT NULL
                    )
                    """)
    print("se creo ")
except sqlite3.OperationalError:
    print("The database is already created")


app = Flask(__name__)

@app.route('/clientes/', methods = ['GET'])
def all_client():
    data = []
    conexion  = sqlite3.connect(direccion)
    cursor = conexion.execute('select nombre, apellido, CC, celular, email from usuario')

    for fila in cursor:
        data.append(fila)

    conexion.close()

    return jsonify({'datas':data})
    

@app.route('/clientes/<Ident>', methods = ['GET'])
def one_client(Ident):    
    conexion  = sqlite3.connect(direccion)
    sql = 'SELECT * from usuario where CC=?'
    cursor = conexion.execute(sql,(Ident,))
    fila = cursor.fetchone()
        
    data = {    
        'nombre':fila[1],
        'apellido':fila[2],
        'celular':fila[4],
        'CC':fila[3],
        'email':fila[5],
        'direccion':fila[6]
    }
    conexion.close()
    
    return jsonify({'result':data})


@app.route('/clientes/', methods = ['POST'])
def new_client():
    
    CC =  request.json['CC']
    nombre =  request.json['nombre']
    apellido =  request.json['apellido']
    email =  request.json['email']
    celular =  request.json['celular']
    d = request.json['direccion']

    conexion = sqlite3.connect(direccion)
    sql = "INSERT INTO usuario(nombre, apellido, CC, celular, email, d) VALUES (?,?,?,?,?,?)"
    conexion.execute(sql, (nombre, apellido, CC, celular, email, d))
    conexion.commit()
    conexion.close()

    return "h"


@app.route('/clientes/<Ident>', methods = ['PUT'])
def update_client(Ident):
    print('\n ', Ident)
    conexion = sqlite3.connect(direccion)
    n = request.json['name']
    a = request.json['apellido']
    c = request.json['Celular']
    e = request.json['email']
    d = request.json['direccion']

    sql = 'update usuario set nombre=?, apellido=?, celular=?, email=?, d=? where CC = ?'
    conexion.execute(sql, (n, a, c, e, d, Ident))
    conexion.commit()    
    conexion.close()
    

@app.route('/clientes/<Ident>', methods = ['DELETE'])
def delete_client(Ident):
    print(Ident)
    conexion = sqlite3.connect(direccion)
    sql = "delete from usuario where CC=?"
    conexion.execute(sql,(Ident,))
    conexion.commit()
    conexion.close()


if __name__ == "__main__":
    app.run()