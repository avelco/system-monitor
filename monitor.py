import os
import smtplib
import psutil
from dotenv import load_dotenv
from email.message import EmailMessage
import logging


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


def send_email(used_percentage):
    msg = EmailMessage()
    msg['Subject'] = 'Disk Space Warning'
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content(f'Warning: Your disk space usage has reached {used_percentage}%. Please take action.')

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_disk_usage():
   for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        used_percentage = usage.percent
        if partition.device in MONITORED_DEVICES:
            if used_percentage > DISK_USAGE_THRESHOLD:
                message = f"Device {partition.device} exceeded threshold with {used_percentage}% used."
                print(message)
                logging.info(message)
                send_email(used_percentage, partition.device)
            else:
                message = f"Device {partition.device} is within threshold with {used_percentage}% used."
                print(message)
                logging.info(message)
        else:
            message = f"Device {partition.device} is not in the monitored devices list. but has {used_percentage}% used."
            print(message)
            logging.info(message)

if __name__ == "__main__":
    check_disk_usage()
