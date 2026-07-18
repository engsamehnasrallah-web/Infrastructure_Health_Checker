from monitor import system_monitor, check_services

system_monitor()

services = ["ssh", "apache2", "nginx", "mysql", "postgresql"]
check_services(services)

input("\nPress Enter to exit...")