import typer
import urllib3

from ipld import unmarshal
from planetmint_driver import Planetmint

from rddl_info.rddl.utils import get_asset, get_default_download, get_cid_data
from rddl_info.storage.csv_storage import CSVStorage
from rddl_info.storage.influx_storage import InfluxStorage
from storage.status import write_status, read_status

from rddl_info.config import INFLUXDB_TOKEN
from rddl_info.config import INFLUXDB_ORG
from rddl_info.config import INFLUXDB_BUCKET
from rddl_info.config import INFLUXDB_HOST_URL


app = typer.Typer()


@app.command("synchronize")
def synchronize_storage(
    # from_block: int = typer.Argument(..., help="The block number the synchronization starts at."),
    rddl_validator_id: int = typer.Argument(..., help="The id of the RDDL validator node to connect to."),
    influxdb: bool = typer.Option(False, "--influxdb/--no-influxdb"),
):
    plntmnt_uri = "http://node" + str(rddl_validator_id) + "-rddl-testnet.twilightparadox.com:9984"
    plntmnt = Planetmint(plntmnt_uri)
    last_block_current = plntmnt.blocks.retrieve(block_height="latest")

    range_from = read_status() + 1
    range_to = int(last_block_current["height"]) + 1
    print(f"Starting at block: {read_status()}")
    print(f"Ending at block: {last_block_current['height']}")
    print(f" INFLUXDB {INFLUXDB_TOKEN} {INFLUXDB_ORG} {INFLUXDB_BUCKET} {INFLUXDB_HOST_URL}")
    storage = None
    if influxdb:
        storage = InfluxStorage(token=INFLUXDB_TOKEN, org=INFLUXDB_ORG, bucket=INFLUXDB_BUCKET, url=INFLUXDB_HOST_URL)
    else:
        filename = "extracted_data-" + range_from + ".csv"
        storage = CSVStorage(filename)

    for blk_nr in range(range_from, range_to):
        print(f"Block : {blk_nr}")
        blk_content = plntmnt.blocks.retrieve(block_height=str(blk_nr))
        # print( f"BLK {blk_nr} : {blk_content}")
        print(f'BLK {blk_nr} : {len(blk_content["transaction_ids"])}')
        for tx in blk_content["transaction_ids"]:
            tx_old = tx
            tx = plntmnt.transactions.retrieve(tx)
            if tx["operation"] == "CREATE":
                print(f"BLK {blk_nr} : {tx['inputs'][0]['owners_before']} : asset : {get_asset(tx)[0]['data']}")
                # print( tx )
                obj = get_asset(tx)[0]["data"]
                if not obj:
                    continue
                cid = obj.replace('"', "")
                print(f"CID : { cid } ")
                cided_data_url = get_cid_data(cid)
                url = None
                if cided_data_url == None:
                    url = get_default_download(cid)
                else:
                    url = cided_data_url["url"]
                if url:
                    try:
                        http = urllib3.PoolManager()
                        consumption = http.request("GET", url)
                        if consumption.status == 200:
                            obj = unmarshal(consumption.data)

                            print(obj)
                            try:
                                data = [
                                    tx["inputs"][0]["owners_before"][0],
                                    obj["StatusSNS"]["ENERGY"]["ApparentPower"],
                                    obj["StatusSNS"]["ENERGY"]["Current"],
                                    obj["StatusSNS"]["ENERGY"]["Factor"],
                                    obj["StatusSNS"]["ENERGY"]["Power"],
                                    obj["StatusSNS"]["ENERGY"]["ReactivePower"],
                                    obj["StatusSNS"]["ENERGY"]["Today"],
                                    obj["StatusSNS"]["ENERGY"]["Total"],
                                    obj["StatusSNS"]["Time"].replace("T", "t") + "+01:00",
                                    obj["StatusSNS"]["ENERGY"]["Voltage"],
                                    obj["StatusSNS"]["ENERGY"]["Yesterday"],
                                ]
                                storage.write(data)
                            except KeyError as e:
                                print("keyerror - not part of the CSV")
                            except Exception as e:
                                print(f"exception writing to the DB: {e}")
                    except Exception as e:
                        print(f"Exception {e}")
        write_status(blk_nr)


if __name__ == "__main__":
    app()
