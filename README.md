# prtg-pure-storage
PRTG script to check PURE storage SAN statistics using REST API


![All available sensors](https://github.com/tonkotsurobot/prtg-pure-storage/raw/master/all%20sensors.png)

To use: 
1. Copy necessary files (prtg.standardlookups.purestorage.hardwarestatus.ovl and prtg.standardlookups.purestorage.drivestatus.ovl) to the lookups directory of prtg (C:\Program Files (x86)\PRTG Network Monitor\lookups\custom) and (prtg-pure-storage.py to C:\Program Files (x86)\PRTG Network Monitor\Custom Sensors\python). Ensure you at least modify the API_TOKEN variable at the top. You can use the pureuser API key for this purpose
2. Restart PRTG core service to load these files as per https://www.paessler.com/manuals/prtg/prtg_probe_administrator
3. Create a "Python Script Advanced" sensor in PRTG
4. Select the right python script, and add the right additional parameter as the table below
![Adding a sensor](https://github.com/tonkotsurobot/prtg-pure-storage/raw/master/add-sensor.png)

5. Create a separate sensor for each switch/parameter


## LIST of SENSOR PARAMETERS
<table>
    <tr>
        <th>switch</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>-v</td>
        <td>List all PURE storage volumes and its front end disk usage (as seen by client) </td>
    </tr>
    <tr>
        <td>-u</td>
        <td>List all PURE storage volumes and its back end disk usage(after dedup/compress with parity overhead)</td>
    </tr>
    <tr>
        <td>-m</td>
        <td>List all manually created volume snapshots and its backend size </td>
    </tr>
    <tr>
        <td>-c</td>
        <td>List PURE storage controllers and their health</td>
    </tr>
    <tr>
        <td>-d</td>
        <td>List PURE storage drives and their health</td>
    </tr>
    <tr>
        <td>-h</td>
        <td>List PURE storage hardware (fans, PSU, chassis, etc) and their health</td>
    </tr>
    <tr>
        <td>-p</td>
        <td>List PURE storage array performance including queue depth (with threshold for warning), IOPS, and RW rate and latency </td>
    </tr>
     <tr>
        <td>-s</td>
        <td>List PURE storage array capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
     <tr>
        <td>-r</td>
        <td>List PURE storage volumes read and write stats in bytes/s</td>
    </tr>
    <tr>
        <td>-i</td>
        <td>List PURE storage volumes IOPS stats</td>
    </tr>
</table>



v20 addition.
Prtg has released its v20 of its prtg network monitor software.
Please use the corresponding script for this version.
Switches are also different and has checks to ensure that channel name is longer than prtg maximum (32 characters) and channel count is less than max (50). If you have more than 50 volumes, this will only display the first 50 returned by the pure storage SAN

## LIST of SENSOR PARAMETERS v20
<table>
    <tr>
        <th>switch</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>-v</td>
        <td>List all PURE storage volumes and its front end disk usage (as seen by client) </td>
    </tr>
    <tr>
        <td>-u</td>
        <td>List all PURE storage volumes and its back end disk usage(after dedup/compress with parity overhead)</td>
    </tr>
    <tr>
        <td>-m</td>
        <td>List all manually created volume snapshots and its backend size </td>
    </tr>
    <tr>
        <td>-c</td>
        <td>List PURE storage controllers and their health</td>
    </tr>
    <tr>
        <td>-d</td>
        <td>List PURE storage drives and their health</td>
    </tr>
    <tr>
        <td>-h</td>
        <td>List PURE storage hardware (fans, PSU, chassis, etc) and their health</td>
    </tr>
    <tr>
        <td>-p</td>
        <td>List PURE storage array performance including queue depth (with threshold for warning), IOPS, and RW rate and latency </td>
    </tr>
     <tr>
        <td>-s</td>
        <td>List PURE storage array capacity including snapshot size, data reduction and user definable WARNING and ERROR threshold for disk usage</td>
    </tr>
     <tr>
        <td>-br</td>
        <td>List PURE storage volumes read stats in bytes/s</td>
    </tr>
    <tr>
        <td>-bw</td>
        <td>List PURE storage volumes write stats in bytes/s</td>
    </tr>
    <tr>
        <td>-ir</td>
        <td>List PURE storage volumes read IOPS stats</td>
    </tr>
        <tr>
        <td>-iw</td>
        <td>List PURE storage volumes write IOPS stats</td>
    </tr>
    </tr>
        <tr>
        <td>-q</td>
        <td>List PURE storage volumes queue depth</td>
    </tr>

</table>



