import subprocess
import paho.mqtt.client as mqtt
import re
import time

# MQTT Configuration
# Change the user and password to either one youve created or our own login for HA

MQTT_BROKER = "your.broker.ip"
MQTT_PORT = 1883
MQTT_USERNAME = "user"
MQTT_PASSWORD = "password"
MQTT_TOPIC_PREFIX = "homeassistant/sensor/ups"

# Function to execute pwrstat and get output
def get_ups_status():
    try:
        result = subprocess.run(["sudo", "pwrstat", "-status"], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error running pwrstat: {e}")
        return None

# Function to parse pwrstat output
def parse_ups_status(output):
    ups_data = {}

    patterns = {
        "state": r"State\.+\s(.+)",
        "power_supply": r"Power Supply by\.+\s(.+)",
        "utility_voltage": r"Utility Voltage\.+\s(\d+) V",
        "output_voltage": r"Output Voltage\.+\s(\d+) V",
        "battery_capacity": r"Battery Capacity\.+\s(\d+) %",
        "remaining_runtime": r"Remaining Runtime\.+\s(\d+) min",
        "load_watt": r"Load\.+\s(\d+) Watt",
        "line_interaction": r"Line Interaction\.+\s(.+)",
        "last_power_event": r"Last Power Event\.+\s(.+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, output)
        if match:
            ups_data[key] = match.group(1)

    return ups_data

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        print("Connected to MQTT broker successfully")
    else:
        print(f"Connection failed, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully")

# Function to publish data to MQTT
def publish_to_mqtt(ups_data):
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_publish = on_publish

    print(f"Connecting to MQTT Broker at {MQTT_BROKER}:{MQTT_PORT}...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    client.loop_start()
    time.sleep(1)  # Allow connection to complete

    for key, value in ups_data.items():
        topic = f"{MQTT_TOPIC_PREFIX}/{key}"
        print(f"Publishing {topic} => {value}")
        client.publish(topic, value, qos=0, retain=False)

    time.sleep(1)
    client.loop_stop()
    client.disconnect()

# Main loop: Run every 10 seconds
def main():
    while True:
        print("Fetching UPS status...")
        output = get_ups_status()
        if output:
            print("Parsing UPS data...")
            ups_data = parse_ups_status(output)
            print("Publishing UPS data to MQTT...")
            publish_to_mqtt(ups_data)
        else:
            print("No UPS data retrieved.")

        print("Sleeping for 10 seconds...\n")
        time.sleep(10)

if __name__ == "__main__":
    main()
