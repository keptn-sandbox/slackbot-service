import datetime
import dateutil.parser

def helper_datetime(mins):
	past = datetime.datetime.now() - datetime.timedelta(minutes=int(mins))
	return past.isoformat()

def convert_iso_to_datetime(s):
	d = dateutil.parser.parse(s)
	return d