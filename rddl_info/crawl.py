import typer
import urllib3
import json
from urllib.parse import urlparse

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
from rddl_info.config import RDDL_NODES


ENCODING = "utf-8"

app = typer.Typer()

current_node_id = 0
rddl_node_list = json.loads(RDDL_NODES)


def unmarshal_new(data: bytes):
    # unmarshal to dict
    return json.loads(data.decode(ENCODING))


def get_next_node_id() -> int:
    global current_node_id
    current_node_id = current_node_id + 1
    if current_node_id >= len(rddl_node_list):
        current_node_id = 0
    return current_node_id


def get_node_uri(node_id: int = current_node_id) -> str:
    uri = rddl_node_list[current_node_id]["uri"]
    print(f"SWITCHING to node: {uri}")
    return uri


def download_obj(url: str):
    try:
        http = urllib3.PoolManager()
        consumption = http.request("GET", url)
        if consumption.status == 200:
            obj = unmarshal_new(consumption.data)
            print(obj)
            return obj
    except UnicodeDecodeError:  # Exception 'utf-8' codec can't decode byte 0xa1 in position 0: invalid start byte
        obj = unmarshal(consumption.data)
        print(obj)
        return obj
    except Exception as e:
        print(f"Exception {e}")
    return None


def write_storage_entry(tx: dict, obj: dict, storage):
    try:
        o = str()
        for rddl_node in rddl_node_list:
            if rddl_node["pub"] == tx["inputs"][0]["owners_before"][0]:
                o = urlparse(rddl_node["uri"])
                break
        if not o:
            # we did not find a mapping, so do not store the data
            return
        data = [
            o.netloc,
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


def get_create_tx(plntmnt: Planetmint, tx_id: str, blk_nr: int) -> str:
    tx = plntmnt.transactions.retrieve(tx_id)
    if tx["operation"] == "CREATE":
        print(f"BLK {blk_nr} : {tx['inputs'][0]['owners_before']} : asset : {get_asset(tx)[0]['data']}")
        return tx
    else:
        return None


def get_cid_str(tx: dict) -> str:
    obj = get_asset(tx)[0]["data"]
    if not obj:
        return None
    cid = obj.replace('"', "")
    print(f"CID : { cid } ")
    return cid


def get_cid_url(cid: str) -> str:
    cided_data_url = get_cid_data(cid)
    url = None
    if cided_data_url == None:
        url = get_default_download(cid)
    else:
        url = cided_data_url["url"]
    return url


@app.command("synchronize")
def synchronize_storage(
    # from_block: int = typer.Argument(..., help="The block number the synchronization starts at."),
    # rddl_validator_id: int = typer.Argument(..., help="The id of the RDDL validator node to connect to."),
    influxdb: bool = typer.Option(False, "--influxdb/--no-influxdb"),
):
    plntmnt = Planetmint(get_node_uri())
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
        filename = "extracted_data-" + str(range_from) + ".csv"
        storage = CSVStorage(filename)

    for blk_nr in range(range_from, range_to):
        print(f"Block : {blk_nr}")
        try:
            blk_content = plntmnt.blocks.retrieve(block_height=str(blk_nr))
        except Exception as e:
            print(f"EXCEPTION in retrieving a Block: {e}")
            del plntmnt
            plntmnt = Planetmint(get_node_uri(node_id=get_next_node_id()))

        print(f'BLK {blk_nr} : {len(blk_content["transaction_ids"])}')
        for tx_id in blk_content["transaction_ids"]:
            tx = None
            while tx == None:
                try:
                    tx = get_create_tx(plntmnt, tx_id, blk_nr)
                    break
                except Exception as e:
                    print(f"EXCEPTION in retrieving a TX: {e}")
                    del plntmnt
                    plntmnt = Planetmint(get_node_uri(node_id=get_next_node_id()))
            if not tx:
                continue
            cid = get_cid_str(tx)
            if not cid:
                continue
            url = get_cid_url(cid)
            if not url:
                continue
            obj = download_obj(url)
            if not obj:
                continue
            try:
                write_storage_entry(tx, obj, storage)
            except Exception as e:
                print(f"storage exception: {e}")
        write_status(blk_nr)


if __name__ == "__main__":
    app()
