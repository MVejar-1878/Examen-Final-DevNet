from flask import Flask
import sqlite3
import hashlib
import getpass

app = Flask(__name__)
DATABASE = "usuarios.db"

# Crear base de datos y tabla
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Generar hash SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Agregar usuario
def add_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        print("Usuario agregado correctamente")
    except sqlite3.IntegrityError:
        print("El usuario ya existe")
    conn.close()

# Validar usuario
def validate_user(username, password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM usuarios WHERE username = ?",
        (username,)
    )
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == hash_password(password):
        print("Autenticación exitosa")
    else:
        print("Usuario o contraseña incorrectos")

# Sitio web básico
@app.route("/")
def index():
    return "Servidor Web activo con autenticación y base de datos SQLite"

if __name__ == "__main__":
    init_db()

    print("1) Agregar usuario")
    print("2) Validar usuario")
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        user = input("Usuario: ")
        pwd = getpass.getpass("Contraseña: ")
        add_user(user, pwd)

    elif opcion == "2":
        user = input("Usuario: ")
        pwd = getpass.getpass("Contraseña: ")
        validate_user(user, pwd)

    print("Iniciando servidor web en puerto 5800...")
    app.run(host="0.0.0.0", port=5800)
