from collectors.system import print_header
import psutil

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