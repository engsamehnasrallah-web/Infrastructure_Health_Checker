from utils.helpers import print_header
from config.constants import SERVICE_MAP
import psutil

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