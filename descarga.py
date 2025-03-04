import requests
import boto3
import datetime

S3_BUCKET = "landing-casas-804"

def descargar_paginas():
    fecha = datetime.date.today().strftime("%Y-%m-%d")
    s3 = boto3.client("s3")

    for i in range(1, 11):
        url = f"https://casas.mitula.com.co/apartaestudio/bogota/page:{i}"
        response = requests.get(url)
        
        if response.status_code == 200:
            nombre_archivo = f"{fecha}_pagina_{i}.html"
            s3.put_object(Bucket=S3_BUCKET, Key=nombre_archivo, Body=response.text)
        else:
            print(f"Error al descargar {url}")

def main(event, context):
    descargar_paginas()
    return {"status": "OK"}
