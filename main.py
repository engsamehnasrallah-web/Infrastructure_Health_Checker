from monitor import( 
    system_monitor, 
    check_services, 
    check_docker_service,
    check_listening_ports,
    check_cpu_details,
    check_os_details,
    check_network_interfaces
    )

system_monitor()

services = ["ssh", "apache2", "nginx", "mysql", "postgresql"]
check_services(services)
check_docker_service()
check_listening_ports()
check_cpu_details()
check_os_details()
check_network_interfaces()

input("\nPress Enter to exit...")