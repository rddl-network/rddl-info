import csv


class CSVStorage:
    def __init__(self, filename):
        self.csv_handle = None
        self.filename = filename
        self._set_file_header()

    def _set_file_header(self):
        f = open(self.filename, "w")
        f.write("#datatype measurement,long,double,double,long,long,double,double,dateTime,double,double\n")
        f.write("#default ,,,,,,,,,,\n")
        f.write(
            "Actor,ApparentPower,Current,Factor,Power,ReactivePower,Today,Total,TotalStartTime,Voltage,Yesterday\n"
        )
        f.close()

    def _open_csv_writer(self):
        if not self.csv_handle:
            self.csv_handle = csv.writer(open(self.filename, "a"), delimiter=",")

    def write(self, data: list):
        self._open_csv_writer()
        self.csv_handle.writerow(data)
