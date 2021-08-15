import requests

class ThingspeakCrawler:
    # TODO Class Description

    FIELD_NAMES = {
        1 : 'broodroom_temperature',
        2 : 'outdoor_temperature',
        3 : 'outdoor_humidity',
        4 : 'outdoor_airpressure',
        5 : 'broodroom_humidity',
        6 : 'beehiveweight'
    }

    @staticmethod
    def download_field_content(field_number : int) -> str:
        content_url = f'https://thingspeak.com/channels/1112556/field/{field_number}.json'
        download_url = requests.get(content_url, allow_redirects=True)

        return download_url.content.decode('utf-8') # returns JSON
