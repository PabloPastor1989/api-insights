import os
import pandas as pd
from flask import Flask, request, jsonify
import json

# Ruta del archivo CSV dentro de Render
file_path = os.path.join(os.path.dirname(__file__), "Dataset_Hoja_1.csv")

# Verificar si el archivo realmente existe en Render
if not os.path.exists(file_path):
    raise FileNotFoundError(f"El archivo {file_path} no se encontró en el servidor.")

# Cargar el archivo CSV en memoria y limpiar columnas vacías
df = pd.read_csv(file_path, encoding="utf-8-sig")  # Asegurar correcta codificación
df = df.dropna(axis=1, how='all')  # Eliminar columnas completamente vacías
df = df.loc[:, ~df.columns.str.contains('Unnamed', na=False)]  # Eliminar columnas "Unnamed"
df.columns = df.columns.str.strip()  # Eliminar espacios extra en nombres de columnas

# Inicializar la aplicación Flask
app = Flask(__name__)

# Función para buscar insights similares
def buscar_insight(insight):
    resultados = df[df.apply(lambda row: insight.lower() in str(row).lower(), axis=1)]
    return resultados.to_dict(orient='records') if not resultados.empty else []

# Ruta de la API para buscar insights
@app.route('/buscar_insight', methods=['GET'])
def buscar():
    insight = request.args.get('insight', '')
    resultados = buscar_insight(insight)
    return app.response_class(
        response=json.dumps(resultados, ensure_ascii=False).encode("utf-8"),
        mimetype="application/json; charset=utf-8"
    )

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)




