"""
Main script, runs all crawlers
"""
import thingspeak_crawler
from utilities import SQLConnectionHandler


def crawl():
	sql_connection = SQLConnectionHandler.get_connection()
	thingspeak_crawler.ThingspeakCrawler.crawl_and_save_to_sql(sql_connection, [1])


if __name__ == '__main__':
	crawl()
