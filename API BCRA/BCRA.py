import requests
import pandas as pd

# Paso 1: Obtener todos los idVariable y buscar el de reservas (por ejemplo) 

url_variables = "https://api.bcra.gob.ar/estadisticas/v3.0/Monetarias"
response = requests.get(url_variables, verify=False)
variables = pd.DataFrame(response.json()["results"])

# Filtrar por la palabra 'reserva' (puedes ajustar el filtro según el nombre exacto)
print(variables[variables["descripcion"].str.contains("Base monetaria", case=False)])

id_reservas = 15  # Cambia este valor por el correcto si es diferente
url_reservas = f"https://api.bcra.gob.ar/estadisticas/v3.0/Monetarias/{id_reservas}"

response = requests.get(url_reservas, verify=False)
data = response.json()["results"]

# Convertir a DataFrame
df = pd.DataFrame(data)
df["fecha"] = pd.to_datetime(df["fecha"])
df = df.sort_values("fecha")


#EN CASO DE GRAFICAR DIRECTO, AGREGAR:

import matplotlib.pyplot as plt

plt.figure(figsize=(12,6))
plt.plot(df["fecha"], df["valor"], marker="o")
plt.title("Evolución de Base monetaria en pesos")
plt.xlabel("Fecha")
plt.ylabel("Reservas (millones de USD)")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
