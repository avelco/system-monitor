#!/bin/bash

# Define paths
SERVICE_FILE=/etc/systemd/system/monitor.service
TIMER_FILE=/etc/systemd/system/monitor.timer
SCRIPT_PATH=/usr/local/bin/monitor.py

# Check if running as root
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Copy the Python script to /usr/local/bin or another appropriate directory
cp monitor.py $SCRIPT_PATH
chmod +x $SCRIPT_PATH

# Create the systemd service file
cat > $SERVICE_FILE << EOF
[Unit]
Description=Disk Space Monitor Service
Wants=monitor.timer

[Service]
Type=simple
ExecStart=/usr/bin/python3 $SCRIPT_PATH
EOF

# Create the systemd timer file
cat > $TIMER_FILE << EOF
[Unit]
Description=Runs Disk Monitor every hour

[Timer]
OnCalendar=hourly
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Reload systemd to recognize new service and timer
systemctl daemon-reload

# Enable and start the timer
systemctl enable monitor.timer
systemctl start monitor.timer

# Output the status
systemctl status monitor.timer