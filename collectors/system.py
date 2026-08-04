from collectors.system import print_header
import datetime
import platform
import socket
import psutil
from datetime import datetime

def print_header(title):
    print("=" * 30)
    print(title)
    print("=" * 30 + "\n")

def system_monitor():
    """
    Collect and display basic infrastructure health metrics.
    """

    print_header("Infrastructure Health Checker")
    print("Version: v0.5.0\n")

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

def check_os_details():
    """
    Check and display Operating System details.
    """
    print_header("Operating System Details")

    try:
        os_name = platform.system()
        os_version = platform.version()
        os_release = platform.release()
        os_architecture = platform.architecture()[0]
        os_kernel = platform.uname().release
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        os_boot_time = boot_time.strftime('%Y-%m-%d %H:%M:%S')

        print(f"OS Name                       : {os_name}")
        print(f"OS Version                    : {os_version}")
        print(f"OS Release                    : {os_release}")
        print(f"OS Architecture               : {os_architecture}")
        print(f"OS Kernel                     : {os_kernel}")
        print(f"OS Boot Time                  : {os_boot_time}")
    except Exception as e:
        print(f"Error checking OS details          : {e}\n")