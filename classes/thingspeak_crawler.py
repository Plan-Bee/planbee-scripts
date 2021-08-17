import json
from datetime import datetime

import pymysql
import requests


class ThingspeakCrawler:
	# TODO Class Description

	FIELD_NAMES = {
		1: 'broodroom_temperature',
		2: 'outdoor_temperature',
		3: 'outdoor_humidity',
		4: 'outdoor_airpressure',
		5: 'broodroom_humidity',
		6: 'beehiveweight'
	}

	@staticmethod
	def download_field_content(field_number: int) -> dict:
		content_url = f'https://thingspeak.com/channels/1112556/field/{field_number}.json'
		download_url = requests.get(content_url, allow_redirects=True)

		downloaded_json = download_url.content.decode('utf-8')
		converted_dict = json.loads(downloaded_json)

		return converted_dict

	@staticmethod
	def download_all_field_content() -> dict:
		"""
		Crawls the json containing all fields for every measure point
		:return: The returned json, converted to a dict
		"""
		content_url = f'https://thingspeak.com/channels/1112556/feed.json'
		download_url = requests.get(content_url, allow_redirects=True)

		downloaded_json = download_url.content.decode('utf-8')
		converted_dict = json.loads(downloaded_json)

		return converted_dict

	@staticmethod
	def crawl_and_save_to_sql(connection: pymysql.Connection, hives: [int]):
		"""
		Crawls all data from ThingSpeak and saves them to SQL using the given connector
		:param connection: The pymysql connection object
		:param hives: A list of hive Ids to crawl
		:return:
		"""
		cursor = connection.cursor()
		cursor.execute('SELECT hive_id, MAX(thingspeak_id) FROM honeypi_data WHERE hive_id IN %s GROUP BY hive_id',
					   (hives,))
		rows = cursor.fetchall()
		latest_existing_data = {}
		for row in rows:
			latest_existing_data[row[0]] = row[1]

		rows_to_insert: [()] = []

		for hive in hives:
			crawled_data = ThingspeakCrawler.download_all_field_content()['feeds']

			for data in crawled_data:
				# If the entry id is greater than what is already known, insert the new data
				if int(data['entry_id']) > latest_existing_data[hive] or latest_existing_data[hive] is None:
					entry_timestamp = datetime.strptime(data['created_at'], '%Y-%m-%dT%H:%M:%SZ')

					rows_to_insert.append((
						data['entry_id'],
						entry_timestamp,
						hive,
						data['field1'],
						data['field2'],
						data['field3'],
						data['field4'],
						data['field5'],
						data['field6']
					))

		if len(rows_to_insert) < 1:
			return

		cursor.executemany(
			'INSERT INTO honeypi_data (thingspeak_id, timestamp, hive_id, broodroom_temperature, outdoor_temperature, outdoor_humidity, outdoor_airpressure, broodroom_humidity, hive_weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
			rows_to_insert)
		connection.commit()
		cursor.close()
		connection.close()
