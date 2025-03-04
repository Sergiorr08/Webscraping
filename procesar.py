import boto3
import datetime
import csv
from bs4 import BeautifulSoup

S3_BUCKET_INPUT = "landing-casas-xxx"
S3_BUCKET_OUTPUT = "casas-final-xxx"

def procesar_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    casas = []
    
    for casa in soup.find_all("div", class_="listing_item"):  # Ajustar selector según estructura
        barrio = casa.find("span", class_="location").text.strip()
        valor = casa.find("span", class_="price").text.strip()
        habitaciones = casa.find("span", class_="rooms").text.strip()
        banos = casa.find("span", class_="bathrooms").text.strip()
        metros = casa.find("span", class_="size").text.strip()
        fecha = datetime.datetime()
        casas.append([fecha, barrio, valor, habitaciones, banos, metros])
    
    return casas

def handler(event, context):
    s3 = boto3.client("s3")
    fecha = datetime.date.today().strftime("%Y-%m-%d")
    output_file = f"{fecha}.csv"

    # Obtener el archivo de S3
    for record in event["Records"]:
        key = record["s3"]["object"]["key"]
        response = s3.get_object(Bucket=S3_BUCKET_INPUT, Key=key)
        contenido = response["Body"].read().decode("utf-8")

        # Procesar HTML y generar CSV
        datos = procesar_html(contenido)
        output_path = f"s3://{S3_BUCKET_OUTPUT}/{output_file}"

        with open("/tmp/" + output_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["FechaDescarga", "Barrio", "Valor", "NumHabitaciones", "NumBanos", "mts2"])
            writer.writerows(datos)

        s3.upload_file("/tmp/" + output_file, S3_BUCKET_OUTPUT, output_file)

    return {"status": "OK"}
