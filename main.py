from monitor import system_monitor, check_services, check_docker_service

system_monitor()

services = ["ssh", "apache2", "nginx", "mysql", "postgresql"]
check_services(services)
check_docker_service()

input("\nPress Enter to exit...")