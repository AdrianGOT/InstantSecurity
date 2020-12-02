### 1. Preparar
```sh
  # 1 Instalar el ambiente virtual en windows
  python -m venv venv
  
  # 2 Actiavar el ambiente virtual
  venv\scrip\activate

  # 3 Instalar todas las dependencias
    pip install -r requirements.txt

```

### 2. Ejecutar
```sh
    # En Windows
    # Asignar la aplicación que flask abrirá
    set FLASK_APP=app.py

    # Ejecutar flask con el puerto determinado
    flask run --port 5000