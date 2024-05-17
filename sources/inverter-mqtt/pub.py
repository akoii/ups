import json
import paho.mqtt.client as mqtt
import subprocess
import time


with open('/etc/inverter/mqtt.json') as f:
    config = json.load(f)

MQTT_SERVER = config['server']
#MQTT_PORT = int(MQTT_PORTX)

#MQTT_PORTX = config['port']
MQTT_TOPIC = "test"
MQTT_DEVICENAME = config['devicename']
MQTT_USERNAME = config['username']
MQTT_PASSWORD = config['password']
MQTT_CLIENTID = "UPS-PUB"

KEYS = [
    "Inverter_mode",
    "AC_grid_voltage",
    "AC_grid_frequency",
    "AC_out_voltage",
    "AC_out_frequency",
    "PV_in_voltage",
    "PV_in_current",
    "PV_in_watts",
    "PV_in_watthour",
    "SCC_voltage",
    "Load_pct",
    "Load_watt",
    "Load_watthour",
    "Load_va",
    "Bus_voltage",
    "Heatsink_temperature",
    "Battery_capacity",
    "Battery_voltage",
    "Battery_charge_current",
    "Battery_discharge_current",
    "Load_status_on",
    "SCC_charge_on",
    "AC_charge_on",
    "Battery_recharge_voltage",
    "Battery_under_voltage",
    "Battery_bulk_voltage",
    "Battery_float_voltage",
    "Max_grid_charge_current",
    "Max_charge_current",
    "Out_source_priority",
    "Charger_source_priority",
    "Battery_redischarge_voltage",
    "Warnings",
    "Machine_Type",
    "Topology",
    "Out_Mode",
    "AC_or_PV_feed",
    "Charge_Status",
    "Equalization_time",
    "Equalization_period",
    "Equalization_max_current",
    "Reserved1",
    "Equalization_voltage",
    "Reserved2",
    "Equalization_over_time",
    "Equalization_active_status",
    "Equalization_elapse_time",
    "Solar_feed_grid",
    "Country",
    "Solar_feed_grid_power",
    "Charge_to_float_Status",
    "Switch_on",
    "Dustproof",
    "Qflag"
]

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
    
client = mqtt.Client(MQTT_CLIENTID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.connect(MQTT_SERVER, 1883, 600)
client.loop_start()

def pushMQTTData(client, name, payload):
    
    state_topic = "UPS/sensor/{}/{}/state".format(MQTT_DEVICENAME, name)

    
    client.publish(state_topic, payload)
    print(name, payload)
while True:  
    result = subprocess.run(["/opt/inverter-cli/bin/inverter_poller", "-1"], capture_output=True, text=True)
    inverter_data = json.loads(result.stdout)

    Inverter_mode = inverter_data.get('Inverter_mode')
    
    for key in KEYS:
        value = inverter_data.get(key)
        if value is not None:
            pushMQTTData(client, key, str(value))
time.sleep(1)

client.loop_stop()
