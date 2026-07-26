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
    print("Version: v0.4.0\n")

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

def check_docker_service():
    """
    Check the status of the Docker service and display its status.
    """

    print("=" * 30)
    print("Docker Service Status")
    print("=" * 30 + "\n")

    try:
        result = subprocess.run(["sudo", "docker", "--version"], capture_output=True, text=True, check=True)
        docker_version = result.stdout.strip()
        print(f"Docker is installed                 : {docker_version}")
    except FileNotFoundError:
        print("Docker is not installed.")
        return
    except Exception as e:
        print(f"Error checking Docker               : {e}")
    
    try:
        result = subprocess.run(["sudo", "systemctl", "is-active", "docker"], capture_output=True, text=True, check=False)
        status = result.stdout.strip()
        status = STATUS_MAP.get(status, status)
        print(f"Docker service status               : {status}")
    except Exception as e:
        print(f"Error checking Docker service       : {e}")

    running_containers = []
    try:
        result = subprocess.run(["sudo" ,"docker", "ps", "-q"], capture_output=True, text=True, check=True)
        running_containers = result.stdout.strip().splitlines()
        num_running_containers = len(running_containers)
        print(f"Number of running containers        : {num_running_containers}")
    except Exception as e:
        print(f"Error checking running Docker containers: {e}")

    try:
        result = subprocess.run(["sudo", "docker", "ps", "-a", "-q"], capture_output=True, text=True, check=True)
        all_containers = result.stdout.strip().splitlines()
        stopped_containers = [c for c in all_containers if c not in running_containers]
        num_stopped_containers = len(stopped_containers)
        print(f"Number of stopped containers        : {num_stopped_containers}")
    except Exception as e:
        print(f"Error checking stopped Docker containers: {e}")

# make output : port       service         status

SERVICE_MAP = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    631: "IPP",
    3306: "MySQL",
    5432: "PostgreSQL",
}

def check_listening_ports():
    """
    Check and display the TCP listening ports on the system.
    """
    print("=" * 30)
    print("TCP Listening Ports")
    print("=" * 30 + "\n")

    try:
        connections = psutil.net_connections(kind='tcp')
        listening_ports = sorted({
                conn.laddr.port
                for conn in connections
                    if conn.status == psutil.CONN_LISTEN
        })

        if listening_ports:
            print(f"{'Port':<8} {'Service':<18} {'Status'}")
            print("-" * 40)

            for port in listening_ports:
                service_name = SERVICE_MAP.get(port, "Unknown")
                print(f"{port:<8} {service_name:<18} {psutil.CONN_LISTEN}")
        else:
            print("No TCP listening ports found.")
    except Exception as e:
        print(f"Error checking TCP listening ports  : {e}\n")