import logging
import os

import pymysql


def get_connection() -> pymysql.Connection:
	"""
	Get a connection to SQL.
	This function is used on the vServer and for local testing
	@return: pymysql connection object
	"""
	try:
		if os.environ['IS_VSERVER'] == 'true':
			conn = pymysql.connect(
				user=os.environ['vServer_SQL_User'],
				password=os.environ['vServer_SQL_Password'],
				host='localhost',
				port=3306,
				database='Plan-Bee'
			)
		else:
			conn = pymysql.connect(
				user=os.environ['PADDY_SQL_USER'],
				password=os.environ['PADDY_SQL_PASSWORD'],
				host=os.environ['SQL_SERVER'],
				port=3306,
				database='Plan-Bee'
			)

		return conn
	except pymysql.Error as e:
		logging.error('SQL Connection error: %s', e)
		return None
