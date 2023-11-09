import os
import smtplib
import psutil
from dotenv import load_dotenv
from email.message import EmailMessage
import logging
import socket
import requests


# Load environment variables from .env file
load_dotenv()

# Environment variables
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_RECEIVER = os.getenv('EMAIL_RECEIVER').split(';')  # Assuming emails are separated by a semicolon
DISK_USAGE_THRESHOLD = int(os.getenv('DISK_USAGE_THRESHOLD', 85))
MONITORED_DEVICES = os.getenv('MONITORED_DEVICES').split(';')

# Logging
log_filename = './logs/disk_monitor.log'
logging.basicConfig(level=logging.INFO, filename=log_filename,
                    filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')


# Function to get the public IP address
def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except requests.RequestException:
        return "Unavailable"

# Updated send_email function
def send_email(used_percentage, partition, filesystem):
    hostname = socket.gethostname()
    public_ip = get_public_ip()

    msg = EmailMessage()
    msg['Subject'] = f'Disk Space Warning for {hostname}'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = EMAIL_RECEIVER

    # HTML message
    html_message = f"""
    <html>
    <head></head>
    <body>
        <h1>Disk Space Warning</h1>
        <p><strong>Hostname:</strong> {hostname}</p>
        <p><strong>Public IP:</strong> {public_ip}</p>
        <p>The device <strong>{partition}</strong> on filesystem <strong>{filesystem}</strong> has exceeded the threshold with a usage at <strong>{used_percentage}%</strong>.</p>
        <p>Please take action to prevent any potential issues.</p>
    </body>
    </html>
    """

    msg.add_alternative(html_message, subtype='html')

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")
        logging.error(f"Error sending email: {e}")

def check_disk_usage():
    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        used_percentage = usage.percent
        if partition.device in MONITORED_DEVICES:
            if used_percentage > DISK_USAGE_THRESHOLD:
                message = f"Device {partition.device} on {partition.mountpoint} exceeded threshold with {used_percentage}% used."
                print(message)
                logging.info(message)
                send_email(used_percentage, partition.device, partition.mountpoint)
            else:
                message = f"Device {partition.device} on {partition.mountpoint} is within threshold with {used_percentage}% used."
                print(message)
                logging.info(message)
        else:
            message = f"Device {partition.device} is not in the monitored devices list. but has {used_percentage}% used."
            print(message)
            logging.info(message)

if __name__ == "__main__":
    check_disk_usage()
