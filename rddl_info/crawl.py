from planetmint_driver import Planetmint
from ipld import unmarshal
import urllib3
import ast

import csv
import json

import sys



if len(sys.argv) != 3:
    print( "Define the start block number" )
    exit

number = sys.argv[1]
print( "Starting at : " + str( number ))

node_id = sys.argv[2]

plntmnt_uri = 'http://node' + node_id + '-rddl-testnet.twilightparadox.com:9984'
print( "Connecting to  : " + plntmnt_uri)

#plntmnt_uri = 'https://test.ipdb.io'
#plntmnt_uri = 'http://node1-rddl-testnet.twilightparadox.com:9984'
plntmnt = Planetmint(plntmnt_uri)

last_block_read = 0 # write/read to/from file/db

last_block_current =  plntmnt.blocks.retrieve(block_height="latest")
print(f"Last Block: {last_block_current['height']}")

def get_asset( tx ):
    if tx['version'] == '2.0':
        try:
            return [tx['asset']]
        except KeyError:
            return [tx['assets']]
    else:
        return tx['assets']

def get_default_download(cid: str):
    return "https://" + cid + ".ipfs.w3s.link"

def get_cid_data( cid: str):
    http = urllib3.PoolManager()
    consumption = http.request("GET", "https://cid-resolver.rddl.io/entry/cid?cid=" + cid)
    data = consumption.data.decode()
    cid_dict = ast.literal_eval(data)
    if cid_dict == {'detail': 'Item not found.'} :
        return None
    else:
        return cid_dict


filename = "extracted_data-" + number + ".csv"

f = open(filename, "w")
# Write CSV Header, If you donpackagingt need that, remove this line
#f.writerow( [[ "Actor", "ApparentPower", "Current", "Factor", "Power", "ReactivePower", "Today", "Total", "TotalStartTime", "Voltage", "Yesterday" ],])
f.write( "#datatype measurement,long,double,double,long,long,double,double,dateTime,double,double\n" )
f.write( "#default ,,,,,,,,,,\n")
f.write("Actor,ApparentPower,Current,Factor,Power,ReactivePower,Today,Total,TotalStartTime,Voltage,Yesterday\n")
f.close()

f = csv.writer(open(filename, "a"), delimiter=',')
range_from = int(number)
range_to = int(last_block_current["height"])

for blk_nr in range(range_from, range_to):
    print( f"Block : {blk_nr}")
    blk_content = plntmnt.blocks.retrieve(block_height=str(blk_nr))
    #print( f"BLK {blk_nr} : {blk_content}")
    print(f'BLK {blk_nr} : {len(blk_content["transaction_ids"])}')
    for tx in blk_content["transaction_ids"]:
        tx_old = tx
        tx = plntmnt.transactions.retrieve(tx)
        if( tx["operation"] == "CREATE" ):
            print( f"BLK {blk_nr} : {tx['inputs'][0]['owners_before']} : asset : {get_asset(tx)[0]['data']}")
            #print( tx )
            
            cid = get_asset(tx)[0]['data'].replace('"', '')
            print( f"CID : { cid } ")
            cided_data_url = get_cid_data( cid)
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
                        obj = unmarshal( consumption.data )
                        
                        print( obj )
                        try:                 
                            f.writerow([ tx["inputs"][0]["owners_before"][0],
                                    obj["StatusSNS"]["ENERGY"]["ApparentPower"],
                                    obj["StatusSNS"]["ENERGY"]["Current"],
                                    obj["StatusSNS"]["ENERGY"]["Factor"],
                                    obj["StatusSNS"]["ENERGY"]["Power"],
                                    obj["StatusSNS"]["ENERGY"]["ReactivePower"],
                                    obj["StatusSNS"]["ENERGY"]["Today"],
                                    obj["StatusSNS"]["ENERGY"]["Total"],
                                    obj["StatusSNS"]["Time"]+"Z",
                                    obj["StatusSNS"]["ENERGY"]["Voltage"],
                                    obj["StatusSNS"]["ENERGY"]["Yesterday"],
                                    ])
                        except KeyError as e:
                            print( "keyerror - not part of the CSV")
                except Exception as e:
                    print(f"invalid URL {e}")
    

