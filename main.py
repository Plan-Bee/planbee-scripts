import requests
from datetime import datetime, date

def get_download_name(field_number : int) -> str:
    current_date = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # TODO Replace Directory with Database
    download_name = f'./bigdata/{current_date}-{current_time}-field-{field_number}.json'
    return download_name

def download_files(field_number : int) -> None:
    download_name = get_download_name(field_number)
    url = f'https://thingspeak.com/channels/1112556/field/{field_number}.json'
    download_url = requests.get(url, allow_redirects=True)
    print(download_name)
    downloaded_file = open(download_name, 'x')
    downloaded_file.write(download_url.content.decode('utf-8'))
    downloaded_file.close()
    print("Downloaded!")

field_names = {
    1 : 'broodroomtemperature',
    2 : 'temperature',
    3 : 'humidity',
    4 : 'airpressure',
    5 : 'broodroomhumidity',
    6 : 'beehiveweight'
}
for x in range(1,7):
    download_files(x)