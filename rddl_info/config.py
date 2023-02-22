from decouple import config

INFLUXDB_HOST_URL = config("INFLUXDB_HOST_URL", default="http://influxdb:8086")
INFLUXDB_TOKEN = config("INFLUXDB_TOKEN", default="")
INFLUXDB_ORG = config("INFLUXDB_ORG", default="RDDL Network")
INFLUXDB_BUCKET = config("INFLUXDB_BUCKET", default="")
