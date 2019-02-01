#!/usr/bin/python
import os,requests,json,operator,sys
# custom prtg module, run only on prtg server
from paepy.ChannelDefinition import CustomSensorResult

API_TOKEN = "MODIFY_ME_PLEASE" 
SIZE_WARNING_THRESHOLD = 80
SIZE_ERROR_THRESHOLD = 90

def _url(path):
    return 'https://todo.example.com' + path

def login(session):
    return session.post('https://mslnrcorpsan3/api/1.8/auth/session', json=apikey, verify=False)

def get_volumes(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/volume?space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Provisioned size")
    for item in results:
        output.add_channel(channel_name=item['name'], unit="Bytes", value=item['size'])
    print(output.get_json_result())

def get_volumes_usage(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/volume?space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Array real usage per volume")
    for item in results:
        output.add_channel(channel_name=item['name'], unit="Bytes", value=item['total'])
    print(output.get_json_result())

def get_volumes_io(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/volume?space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Volumes IO performance")
    for item in results:
        query = 'https://mslnrcorpsan3/api/1.8/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        output.add_channel(channel_name=item['name']+' IO Read B/s', unit="IOPS", value=new_results[0]['reads_per_sec'])
        output.add_channel(channel_name=item['name']+' IO Write B/s', unit="IOPS", value=new_results[0]['writes_per_sec'])
    print(output.get_json_result())
 
def get_volumes_rw(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/volume?space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Volumes RW performance")
    for item in results:
        query = 'https://mslnrcorpsan3/api/1.8/volume' + '/' + item['name'] + '?action=monitor'
        new_response = session.get(query, verify=False)
        new_results = json.loads(new_response.text)
        output.add_channel(channel_name=item['name']+' Read B/s', unit="BytesBandwidth", value=new_results[0]['input_per_sec'])
        output.add_channel(channel_name=item['name']+' Write B/s', unit="BytesBandwidth", value=new_results[0]['output_per_sec'])
    print(output.get_json_result())

def get_controllers(session):
    output = CustomSensorResult("Pure storage controllers")
    response = session.get('https://mslnrcorpsan3/api/1.8/array?controllers=true', verify=False)
    results = json.loads(response.text)
    for item in results:
        if item['status'] == 'ready':
            output.add_channel(channel_name=item['mode'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
        else:
            output.add_channel(channel_name=item['mode'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.get_json_result())     

def get_hardware(session):
    output = CustomSensorResult("Pure storage hardware")
    response = session.get('https://mslnrcorpsan3/api/1.8/hardware', verify=False)
    results = json.loads(response.text)
    for item in results:
        if item['status'] == 'ok' and ('FAN' in item['name'] or 'PWR' in item['name'] or 'FC' in item['name']):
            output.add_channel(channel_name=item['name'], value=0, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
        elif item['status'] != 'ok' and ('FAN' in item['name'] or 'PWR' in item['name'] or 'FC' in item['name']):
            output.add_channel(channel_name=item['name'], value=10, value_lookup="prtg.standardlookups.purestorage.hardwarestatus")
    print(output.get_json_result())     

def get_drives(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/drive', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("Disks status")
    for item in results:
        if item['status'] == 'healthy':
            output.add_channel(channel_name=item['name'], value=0, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'empty':
            output.add_channel(channel_name=item['name'], value=1, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'updating':
            output.add_channel(channel_name=item['name'], value=2, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'unused':
            output.add_channel(channel_name=item['name'], value=3, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'evacuating':
            output.add_channel(channel_name=item['name'], value=4, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'identifying':
            output.add_channel(channel_name=item['name'], value=5, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'unhealthy':
            output.add_channel(channel_name=item['name'], value=6, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'recovering':
            output.add_channel(channel_name=item['name'], value=7, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'unrecognized':
            output.add_channel(channel_name=item['name'], value=8, value_lookup="prtg.standardlookups.purestorage.drivestatus")
        elif item['status'] == 'failed':
            output.add_channel(channel_name=item['name'], value=9, value_lookup="prtg.standardlookups.purestorage.drivestatus")
    print(output.get_json_result())

def get_manual_snapshots(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/volume?snap=true&space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("List of manually created snapshots")
    for item in results:
        if ( "Daily" not in item['name'] ):
            output.add_channel(channel_name=item['name'], unit="Bytes", value=item['snapshots'], is_limit_mode=True, limit_max_warning=100000000000, limit_warning_msg="Snapshot size too large")
    print(output.get_json_result())

def get_performance(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/array?action=monitor', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("PURE array performance")
    for item in results:
        output.add_channel(channel_name="Write bytes per second", unit="Bytes", value=item['output_per_sec'])
        output.add_channel(channel_name="Read bytes per second", unit="Bytes", value=item['input_per_sec'])
        output.add_channel(channel_name="Queue depth", primary_channel=True, value=item['queue_depth'], is_limit_mode=True, limit_max_warning=60, limit_warning_msg="Large queue depth")
        output.add_channel(channel_name="Write IOPS per second", unit="IOPS", value=item['writes_per_sec'])
        output.add_channel(channel_name="Read IOPS per second", unit="IOPS", value=item['reads_per_sec'])
        output.add_channel(channel_name="Write latency", unit="usec", value=item['usec_per_write_op'])
        output.add_channel(channel_name="Read latency", unit="usec", value=item['usec_per_read_op'])
    print(output.get_json_result())

def get_capacity(session):
    response = session.get('https://mslnrcorpsan3/api/1.8/array?space=true', verify=False)
    results = json.loads(response.text)
    output = CustomSensorResult("PURE array capacity")
    for item in results:
        output.add_channel(channel_name="Capacity", unit="Bytes", value=item['capacity'])
        output.add_channel(channel_name="Snapshot", unit="Bytes", value=item['snapshots'])
        output.add_channel(channel_name="Used space", unit="Bytes", value=item['total'])
        output.add_channel(channel_name="Used %", primary_channel=True, unit="percent", value= (item['total'] * 100 / item['capacity']), is_limit_mode=True, limit_max_warning=SIZE_WARNING_THRESHOLD, limit_warning_msg="High array disk space usage", limit_max_error=SIZE_ERROR_THRESHOLD, limit_error_msg="Very high array disk space usage")
        output.add_channel(channel_name="Data reduction", is_float=True, value=item['data_reduction'])
    print(output.get_json_result())



#INITIALISATION AND LOGIN
apikey = {"api_token": API_TOKEN}
s = requests.session()
requests.packages.urllib3.disable_warnings()
response = login(s)
if response.status_code != 200:
    # This means something went wrong.
    raise ApiError('GET /tasks/ {}'.format(resp.status_code))

data = json.loads(sys.argv[1])

if (data['params']) == '-v':
    get_volumes(s)
elif (data['params']) == "-u":
    get_volumes_usage(s)
elif (data['params']) == "-m":
    get_manual_snapshots(s)
elif (data['params']) == "-c":
    get_controllers(s)
elif (data['params']) == "-d":
    get_drives(s)
elif (data['params']) == "-h":
    get_hardware(s)
elif (data['params']) == "-p":
    get_performance(s)
elif (data['params']) == "-s":
    get_capacity(s)
elif (data['params']) == "-r":
    get_volumes_rw(s)
elif (data['params']) == "-i":
    get_volumes_io(s)

