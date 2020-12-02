from flask import Flask, render_template, redirect
from flask import  jsonify, request, url_for
from flask import session
import requests
import random
import json 

 
app = Flask(__name__)

url_cliente = 'http://127.0.0.1:5001/clientes/'
url_producto = 'http://127.0.0.1:5002/producto/'
url_factura = 'http://127.0.0.1:5003/factura/'

app.secret_key="lalocura123456789"

#  Función que buscar un solo producto
def buscar_un_producto(name):
    response = requests.get(url_producto + name)
    return json.loads(response.text)


#  Función que buscar un solo cliente
def buscar_un_cliente(id):
    response = requests.get(url_cliente + str(id))
    return  json.loads(response.text)


#  Función que busca todos los productos
def buscar_productos():
    response = requests.get(url_producto)
    return json.loads(response.text)


#  Función que busca todas las facturas
def buscar_facturas():
    response = requests.get(url_factura)
    return json.loads(response.text)


# Función que agrega datos del cliente a la session
def registroSesion(todo):
    session['nombre'] = todo['nombre']
    session['cc'] = todo['CC']
    print(session['cc'])
 

@app.route('/')
def index():
    return redirect(url_for('all_products'))


#       Guardar cliente
@app.route('/guardar', methods = ['POST'])
def save_client():
    data = {
        'nombre' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'CC': request.form['CC'],
        'celular':request.form['celular'],
        'email' : request.form['email'],
        'direccion':request.form['direccion']
    }

    registroSesion(data)
    
    requests.post(url_cliente, json = data)
    return redirect(url_for('index'))


# Actualizar la información del cliente
@app.route('/actualizar', methods = ['POST'])
def update():
    data = {
        'name' : request.form['nombre'],
        'apellido' : request.form['apellido'],
        'Celular':request.form['celular'],
        'email' : request.form['email']
    }
    requests.put(url_cliente + request.form['CC'], json = data)
    return redirect(url_for('index'))


#   Obtiene todos los prodcutos
@app.route('/obtener_productos/', methods=['GET', 'POST'])
def all_products():
    
    todo = buscar_productos()
    
    comprobante = False
    n = 'Desconocido'
    cc = 'Desconocido'
    if "nombre" in session:
        comprobante = True 
        n = session['nombre']
        cc = session['cc']
        return render_template('index.html', productos = todo['result'], title='InstantSecurity', c = comprobante, n = n)     

    return render_template('index.html', productos = todo['result'], title='InstantSecurity', c = comprobante, n = n)


#      Registro e Inicio de sesión
@app.route('/Inicio_de_sesión', methods=['GET','POST'])
def inicioSesion():
    if request.method == 'POST':
        todo = buscar_un_cliente(request.form['CC'])
        registroSesion(todo['result'])

        return redirect(url_for('all_products'))

    return render_template('inicioSesion.html', title='Iniciar sesión')


@app.route('/Registrarse', methods=['GET','POST'])
def registro():
    return render_template('registrarse.html', title='Registro')


#    Creación de la factura 
@app.route('/factura/<productName>', methods=['GET','POST'])
def facturacion(productName):
    if "nombre" in session:
        comprobante = True 
        producto = buscar_un_producto(productName)    
        cliente = buscar_un_cliente(str(session['cc']))

        factura = {
            'Nombre': cliente['result']['nombre'],
            'Identificacion': cliente['result']['CC'],
            'Direccion del cliente': cliente['result']['direccion'],
            'Nombre del producto o servicio': producto['result']['name'],
            'Precio': producto['result']['price'],
            'Número de telefono': cliente['result']['celular']
        }

        if request.method == 'POST':
            n = random.randint(0,100000000)
            data_check={
                'numero_factura':n,
                'direccion': factura['Direccion del cliente'],
                'precio': factura['Precio'],
                'nombre_producto':factura['Nombre del producto o servicio'],
                'nombre_cliente':factura['Nombre'],
                'CC_cliente':factura['Identificacion']
            }
            requests.post(url_factura, json=data_check)

            return render_template('resultado.html', num = n)

        return render_template('factura.html', Factura = factura, 
                                n=session['nombre'], title = 'Factura')


#  Perfil del usuario
@app.route('/obtener_productos/perfil', methods=['GET','POST'])
def perfil():
    if "cc" in session: 
        info = buscar_un_cliente(str(session['cc']))
        f = buscar_facturas()

        return render_template('perfil.html', title=session['nombre'], n=session['nombre'], info = info['result'], facturas = f['result'])
    
    else:
        return redirect(url_for('index'))
    
    
#  Elimiar factura 
@app.route('/Elimar_factura/<numero>', methods = ['GET','POST'])
def eliminar_factura(numero):
    requests.delete(url_factura + numero)
    
    return redirect(url_for('perfil'))


#  Editar Cuenta
@app.route('/Editar_cuenta/<cc>', methods=['GET', 'POST'])
def editar_cuenta(cc):

    if request.method == 'POST':

        new_data={
            'name':request.form['nombre'],
            'apellido':request.form['apellido'],
            'Celular':request.form['celular'], 
            'email':request.form['email'],
            'direccion':request.form['direccion']
        }

        requests.put(url_cliente + str(cc), json=new_data)

        return redirect(url_for('perfil'))

    todo = buscar_un_cliente(session['cc'])
    return render_template('editarPerfil.html', title="Editar Perfil", info=todo['result'])


#  Eliminar Cuenta
@app.route('/eliminar_cuenta/<int:cc>', methods=['GET', 'POST'])
def eliminar_cuenta(cc):
    if 'nombre' in session:
        requests.delete(url_cliente + str(cc))

        return redirect(url_for('logout'))
    
    return redirect(url_for('index')) 



#      Cerrar sesión 
@app.route('/Cerrar Session')
def logout():
    session.pop('nombre',None)
    session.pop('cc',None)

    return redirect(url_for('all_products'))