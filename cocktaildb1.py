# Obtener los datos de la API usando requests para hacer la petición HTTP
# Importar las librerias necesarias 
import requests
import sqlite3
import time

#Obtener los datos de la API 
#request hace solicitud HTTP, response lanza un error si alfo sale mal, data obtiene la lista de cocteles 
url = "https://www.thecocktaildb.com/api/json/v1/1/filter.php?i=Tequila"

#As e guarda el error especifico en la variable e, asi muestra el error 

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    cocteles = data["drinks"]
except requests.exceptions.RequestException as e:
    print(f"Error al obtener los datos: {e}")
    exit()

# Conexión a la base de datos SQLite
#Crea una base de datos locale llamada cocteles.db 
#Cursor se usa para ejecutar comandos SQL 
#Crea la tabla si no existe 

conexion = sqlite3.connect("cocteles.db")
cursor = conexion.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS cocteles (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        imagen TEXT
    )
""")
conexion.commit()

# Insertar los cócteles en la base de datos
#Los ? sprotegen de inyecciones SQL que es para que no entren codigos en vez de textos normales 
for coctel in cocteles:
    cursor.execute("""
        INSERT OR REPLACE INTO cocteles (id, nombre, imagen)
        VALUES (?, ?, ?)
    """, (coctel["idDrink"], coctel["strDrink"], coctel["strDrinkThumb"]))
conexion.commit()

# Mostrar cócteles guardados
#fetchall() devuelve todas las fichas 

print("\n--- Cócteles guardados ---")
cursor.execute("SELECT * FROM cocteles")
resultado = cursor.fetchall()
for id, nombre, imagen in resultado:
    print(f"ID: {id}, Nombre: {nombre}, Imagen: {imagen}")

# Modificar un dato con input
#Valida que sea un numero con isdigit() 
#UPDATE actualiza el registro

id_coctel = input("\nIntroduce el ID del cóctel que quieres renombrar: ")
if not id_coctel.isdigit():
    print("ID inválido.")
    exit()

nuevo_nombre = input("Nuevo nombre para el cóctel: ")
cursor.execute("""
    UPDATE cocteles
    SET nombre = ?
    WHERE id = ?
""", (nuevo_nombre, id_coctel))
conexion.commit()

#Confirma que el cambio se realizo 

print("\nNombre actualizado. Registro actualizado:")
cursor.execute("SELECT * FROM cocteles WHERE id = ?", (id_coctel,))
print(cursor.fetchone())

# Análisis de eficiencia
print("\n--- Análisis de eficiencia ---")

# Tiempo iterando sobre los datos desde la API
#Se mide el tiempo que toma recorrer los datos desde la respuesta de API (cocteles) 
#Luego de la base de datos local (cursor) d
inicio_api = time.time()
for coctel in cocteles:
    _ = coctel["idDrink"], coctel["strDrink"], coctel["strDrinkThumb"]
fin_api = time.time()
tiempo_api = fin_api - inicio_api
print(f"Tiempo iterando desde API: {tiempo_api:.6f} segundos")

# Tiempo iterando sobre los datos desde la base de datos
inicio_db = time.time()
cursor.execute("SELECT * FROM cocteles")
for fila in cursor.fetchall():
    _ = fila
fin_db = time.time()
tiempo_db = fin_db - inicio_db
print(f"Tiempo iterando desde base de datos: {tiempo_db:.6f} segundos")

# Cierre de la conexión
conexion.close()
