import psutil
import platform
import socket
import subprocess

STATUS_MAP = {
                "active": "Running ✅",
                "inactive": "Stopped ❌",
                "failed": "Failed ❌",
                "unknown": "Not Installed ⚠️"
            }

def system_monitor():
    """
    Collect and display basic infrastructure health metrics.
    """

    print("=" * 30)
    print("Infrastructure Health Checker")
    print("=" * 30)
    print("Version: v0.3.0\n")

    hostname = platform.node()
    print(f"Hostname               : {hostname}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("8.8.8.8", 80))
    local_ip = sock.getsockname()[0]
    sock.close()
    print(f"Local IP Address       : {local_ip}")

    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        internet_connectivity = "Online"
    except OSError:
        internet_connectivity = "Offline"
    print(f"Internet Connectivity  : {internet_connectivity}")

    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"\nCPU Usage              : {cpu_usage:.1f}%")

    memory_info = psutil.virtual_memory()
    print(f"Memory Usage           : {memory_info.percent:.1f}%")

    disk_info = psutil.disk_usage('/')
    print(f"Disk Usage             : {disk_info.percent:.1f}%\n")

def check_services(services):
    """
    Check the status of specified services and display their status.
    """
    print("-" * 30)
    print("Services Status")
    print("-" * 30 + "\n")

    for service in services:
        try:
            result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True, check=False)
            status = result.stdout.strip()
            status = STATUS_MAP.get(status, status)
            print(f"{service:<22}: {status}")
        except Exception as e:
            print(f"Error checking {service}: {e}")