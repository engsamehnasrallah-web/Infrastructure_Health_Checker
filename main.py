from config.config import load_config
from collectors.services import check_services
from collectors.docker import check_docker_service
from collectors.cpu import check_cpu_details
from collectors.system import(
    system_monitor,
    check_os_details,
)
from collectors.network import(
    check_listening_ports,
    check_network_interfaces,
)

config = load_config()
services = config["services"]

system_monitor()
check_services(services)
check_docker_service()
check_listening_ports()
check_cpu_details()
check_os_details()
check_network_interfaces()

input("\nPress Enter to exit...")