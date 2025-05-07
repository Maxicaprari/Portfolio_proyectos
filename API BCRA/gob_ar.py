import requests
import pandas as pd

#FUCNION PARA VER SI RESPONDE 


#url = "https://apis.datos.gob.ar/series/api/series/?ids=143.3_PBI_2016_A_19&format=json"
#response = requests.get(url)
#print(response.json())

#FUNCION PARA OBTENER LA API Y PASARLA A DF
def get_pbi_trimestral():
    url = "https://apis.datos.gob.ar/series/api/series/?ids=220.1_PCONSTRCAS_1970_0_33&format=json"    #CAMBIAR ID POR EL QUE QUIERAS
    response = requests.get(url)
    json_data = response.json()
    if "data" in json_data:
        data = json_data["data"]
        df_pbi = pd.DataFrame(data, columns=["fecha", "valor"])
        df_pbi["valor"] = pd.to_numeric(df_pbi["valor"], errors="coerce")
        return df_pbi
    else:
        print("No se encontró la clave 'data'. Respuesta de la API:")
        print(json_data)
        return pd.DataFrame()  # Devuelve un DataFrame vacío

df_pbi = get_pbi_trimestral()
print(df_pbi.head())
