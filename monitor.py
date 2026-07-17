import psutil
import platform
import socket

def system_monitor():
    """
    Collect and display basic infrastructure health metrics.
    """

    print("=" * 30)
    print("Infrastructure Health Checker")
    print("=" * 30)
    print("Version: v0.2.0\n")

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
    print(f"Disk Usage             : {disk_info.percent:.1f}%")