# Disk Monitor Installation Manual

This manual guides you through the installation of the disk monitoring service on a Linux server.

## Prerequisites

- Python 3
- `psutil`, `request` and `python-dotenv` Python packages
    ```bash
    pip install psutil python-dotenv
    ```

- Root access

## Installation Steps

1. Copy the `monitor.py` script to the server.
2. Ensure that the `.env` file is configured correctly and located in the same directory as your script.
3. Run the installation script `install.sh` with root privileges:

```bash
sudo bash install.sh
```
4.  To  check if your script is running well execute the following command:

```bash
systemctl status monitor.timer
```
