import requests
import pandas as pd

def get_indec_serie(serie_id):
    url = f"https://apis.datos.gob.ar/series/api/series/?ids={serie_id}&format=json"
    response = requests.get(url)
    data = response.json()["data"]
    df = pd.DataFrame(data, columns=["fecha", "valor"])
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    return df

# Ejemplo: IPC Nacional (inflación) - cambiar el ID por el que necesites

df_indec = get_indec_serie("148.3_INIVELNAL_DICI_M_26")
print(df_indec.head())
