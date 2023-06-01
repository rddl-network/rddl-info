from decouple import config

INFLUXDB_HOST_URL = config("INFLUXDB_HOST_URL", default="http://influxdb:8086")
INFLUXDB_TOKEN = config("INFLUXDB_TOKEN", default="")
INFLUXDB_ORG = config("INFLUXDB_ORG", default="RDDL Network")
INFLUXDB_BUCKET = config("INFLUXDB_BUCKET", default="")
RDDL_NODES = config(
    "RDDL_NODES",
    default='[\
    {"uri":"http://node1-rddl-testnet.twilightparadox.com:9984","pub":"4dtjJJAHngcLSd1BFpfJVcvubSye8zA8H5cAdDtAdLMJ"},\
    {"uri":"http://node2-rddl-testnet.twilightparadox.com:9984","pub":"McGeAMUVpaURm2nfHym5pEXMFCHoHoJtwTportcJNd8"},\
    {"uri":"http://node3-rddl-testnet.twilightparadox.com:9984","pub":"6wELv3KjtPPEznXYSfjBeZYjBsdx91prUDKJBxwgRhb2"},\
    {"uri":"http://node4-rddl-testnet.twilightparadox.com:9984","pub":"9tZ3twvWYeELvbdSYR9FdQJM3tYu9iRQ4u6nnqqfQ62v"},\
    {"uri":"http://node5-rddl-testnet.chickenkiller.com:9984","pub":"2eBpuzzscZVGgmxfCH9DakpH4zAZSXYZLnrs6tSgBwsK"},\
    {"uri":"http://node8-rddl-testnet.twilightparadox.com:9984","pub":"CmX7akU8G5tiQfxgxYykGeiYAHTLa4bs3A5pKf1xVKHz"},\
    {"uri":"http://node9-rddl-testnet.twilightparadox.com:9984","pub":"8Tr71EWFVAB6TnQUxhzUPwh3EyZLN1YyNxd4y2fnpTDC"},\
    {"uri":"http://node12-rddl-testnet.twilightparadox.com:9984","pub":"Fjj1yu1uXhsmq89qJU5tYqXfMPaZsA3K95xHCkvrcEUM"},\
    {"uri":"http://node14-rddl-testnet.twilightparadox.com:9994","pub":"4zwmCxhVEsmNko8KofkzxTrfjnRPoDXowGWJRPm5refo"},\
    {"uri":"http://node15-rddl-testnet.twilightparadox.com:10004","pub":"G8HWRJBq2jAdKrf5vrqTB6uSnYnQa61QenXfVbaWtATh"}\
    ]',
)
