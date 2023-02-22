from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxStorage:
    def __init__(self, token: str, org: str, bucket: str, url: str = "http://localhost:8086"):
        self.client = InfluxDBClient(url=url, token=token, org=org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.bucket = bucket
        self.org = org

    def __del__(self):
        self.write_api.close()
        self.client.close()

        # f.write( "#datatype measurement,long,double,double,long,long,double,double,dateTime,double,double\n" )
        # f.write( "#default ,,,,,,,,,,\n")
        # f.write("Actor,ApparentPower,Current,Factor,Power,ReactivePower,Today,Total,TotalStartTime,Voltage,Yesterday\n")

    def write(self, data):
        datapoint = (
            Point(data[0])
            .field("ApparentPower", int(data[1]))
            .field("Current", float(data[2]))
            .field("Factor", float(data[3]))
            .field("Power", int(data[4]))
            .field("ReactivePower", int(data[5]))
            .field("Today", float(data[6]))
            .field("Total", float(data[7]))
            # .field("Time", data[8])
            .field("Voltage", float(data[9]))
            .field("Yesterday", float(data[10]))
            .time(data[8])
        )
        # datapoint = {"measurement": data[0], "fields": {
        #    "ApparentPower": data[1], "Current": data[2],
        #    "Factor": data[3], "Power": data[4],
        #    "ReactivePower": data[5], "Today": data[6],
        #    "Total": data[7], "Time": data[8],
        #    "Voltage": data[9], "Yesterday": data[10] }, "time": data[8]}

        self.write_api.write(bucket=self.bucket, org=self.org, record=datapoint)
