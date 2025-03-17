# Homeassistant-CyberPower-UPS-Monitor
Python Script to execute and parse data from the CyberPower UPS Debian Software

https://www.cyberpower.com/global/en/product/sku/powerpanel_for_linux

Download the .deb package either 32 or 64 depending on your os.

Install the package...

sudo apt install ./CyberPower_PPL_Linux+64bit+(deb)_v1.4.1 - where ever you have this file.

it will install and place a couple of .sh scripts in the root of your /etc directory.
download and put this script "pwrstatd-ha.py" in the /etc directory.

########################################################################################
Create a Systemd Service to Run the Script at Boot
A systemd service will:

Start the script automatically at boot.
Restart it if it crashes.
Run it continuously in the background.
1️⃣ Create the Systemd Service File

sudo nano /etc/systemd/system/ups-mqtt.service
Paste this:

[Unit]
Description=UPS MQTT Publisher Service
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/script.py
WorkingDirectory=/path/to/your/script
StandardOutput=journal
StandardError=journal
Restart=always
User=root

[Install]
WantedBy=multi-user.target
Replace /path/to/your/script.py with the actual path of your script.

save this file and exit.

2️⃣ Enable and Start the Service

- After saving the file, reload systemd to recognize the new service:
sudo systemctl daemon-reload

- Start the service manually:
sudo systemctl start ups-mqtt

- Enable it to start at boot:
sudo systemctl enable ups-mqtt

- Check the service status:
sudo systemctl status ups-mqtt


Step 3: Verify Everything Works

- Check if the service is running:
sudo systemctl status ups-mqtt

- You should see output like:

● ups-mqtt.service - UPS MQTT Publisher Service
   Loaded: loaded (/etc/systemd/system/ups-mqtt.service; enabled; vendor preset: enabled)
   Active: active (running) since Mon 2025-03-17 10:00:00 UTC; 5s ago

Check logs if there are any errors:
sudo journalctl -u ups-mqtt -f

🎯 Final Setup Summary
✅ Script now runs in a loop every 10 seconds
✅ Runs as a systemd service at boot
✅ Restarts automatically if it crashes
✅ Fully integrates with Home Assistant via MQTT

Now your UPS monitoring will always run in the background! 

Now add the entities fromthe  configuration.yaml to your own config, save and restart HA


This will add all the entities from the script and mqtt payloads,
You can add these entities wherever you like. Enjoy !!
