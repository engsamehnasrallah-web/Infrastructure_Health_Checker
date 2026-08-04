from datetime import datetime
import psutil
import platform
import socket
import subprocess

def print_header(title):
    print("=" * 30)
    print(title)
    print("=" * 30 + "\n")

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

    print_header("Docker Service Status")

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
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    465: "SMTPS",
    587: "SMTP Submission",
    993: "IMAPS",
    995: "POP3S",
    21: "FTP",
    20: "FTP Data",
    23: "Telnet",
    3389: "RDP",
    8080: "HTTP-Alt",
    27017: "MongoDB",
    6379: "Redis"
}

def check_listening_ports():
    """
    Check and display the TCP listening ports on the system.
    """
    print_header("TCP Listening Ports")

    try:
        connections = psutil.net_connections(kind='tcp')
        listening_connections = []
        seen_ports = set()

        for conn in connections:
            if conn.status != psutil.CONN_LISTEN:
                continue

            port = getattr(getattr(conn, "laddr", None), "port", None)
            if port is None or port in seen_ports:
                continue

            seen_ports.add(port)
            listening_connections.append((port, conn))

        if listening_connections:
            print(f"{'Port':<8} {'Service':<18} {'Process':<20} {'Status'}")
            print("-" * 70)

            for port, conn in sorted(listening_connections, key=lambda item: item[0]):
                service_name = SERVICE_MAP.get(port, "Unknown")
                process_name = "N/A"

                try:
                    process_name = psutil.Process(conn.pid).name()
                except psutil.NoSuchProcess:
                    process_name = "N/A (process exited)"
                except psutil.AccessDenied:
                    process_name = "Access denied"
                except Exception as e:
                    process_name = f"Error: {e}"

                print(f"{port:<8} {service_name:<18} {process_name:<20} LISTENING")
        else:
            print("No TCP listening ports found.")
    except Exception as e:
        print(f"Error checking TCP listening ports  : {e}\n")

def check_cpu_details():
    """
    Check and display CPU details.
    """
    print_header("CPU Details")

    try:
        cpu_model = platform.processor()
        cpu_logical = psutil.cpu_count(logical=True)
        cpu_physical = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        cpu_cores_usage = psutil.cpu_percent(interval=1, percpu=True)

        print(f"CPU Model                     : {cpu_model}")
        print(f"Number of Logical Cores       : {cpu_logical}")
        print(f"Number of Physical Cores      : {cpu_physical}")
        print("\nPer-Core Usage:")
        for index, usage in enumerate(cpu_cores_usage):
            print(f"Core {index:<2}               : {usage:.1f}%")
        if cpu_freq:
            print(f"CPU Frequency                 : {cpu_freq.current:.2f} MHz")
        else:
            print("CPU Frequency                  : N/A")
    except Exception as e:
        print(f"Error checking CPU details        : {e}\n")

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

def check_network_interfaces():
    """
    Check and display network interface details.
    """
    print_header("Network Interface Details")

    try:
        interfaces = psutil.net_if_addrs()
        for interface_name, interface_addresses in interfaces.items():
            print(f"Interface: {interface_name}")
            for address in interface_addresses:
                if str(address.family) == 'AddressFamily.AF_INET':
                    print(f"{'IP Address':<30} {address.address}")
                    print(f"{'Netmask':<30} {address.netmask}")
                    print(f"{'Broadcast IP':<30} {address.broadcast}")
                elif str(address.family) == 'AddressFamily.AF_PACKET':
                    print(f"{'MAC Address':<30} {address.address}")
                    print(f"{'Netmask':<30} {address.netmask}")
                    print(f"{'Broadcast MAC':<30} {address.broadcast}")
            print()
    except Exception as e:
        print(f"Error checking network interfaces     : {e}\n")