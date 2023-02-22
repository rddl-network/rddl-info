import ast
import urllib3


def get_asset(tx):
    if tx["version"] == "2.0":
        try:
            return [tx["asset"]]
        except KeyError:
            return [tx["assets"]]
    else:
        return tx["assets"]


def get_default_download(cid: str):
    return "https://" + cid + ".ipfs.w3s.link"


def get_cid_data(cid: str):
    http = urllib3.PoolManager()
    consumption = http.request("GET", "https://cid-resolver.rddl.io/entry/cid?cid=" + cid)
    data = consumption.data.decode()
    cid_dict = ast.literal_eval(data)
    if cid_dict == {"detail": "Item not found."}:
        return None
    else:
        return cid_dict
