from decouple import config

INFLUXDB_HOST_URL = config("INFLUXDB_HOST_URL", default="http://influxdb:8086")
INFLUXDB_TOKEN = config("INFLUXDB_TOKEN", default="")
INFLUXDB_ORG = config("INFLUXDB_ORG", default="RDDL Network")
INFLUXDB_BUCKET = config("INFLUXDB_BUCKET", default="")
RDDL_NODES = config("RDDL_NODES", default= '["http://node1-rddl-testnet.twilightparadox.com:9984",\
    "http://node2-rddl-testnet.twilightparadox.com:9984",\
    "http://node3-rddl-testnet.twilightparadox.com:9984",\
    "http://node4-rddl-testnet.twilightparadox.com:9984",\
    "http://node6-rddl-testnet.twilightparadox.com:9984",\
    "http://node7-rddl-testnet.twilightparadox.com:9984",\
    "http://node8-rddl-testnet.twilightparadox.com:9984",\
    "http://node9-rddl-testnet.twilightparadox.com:9984" ]')
