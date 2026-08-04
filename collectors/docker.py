from collectors.system import print_header
from collectors.service import STATUS_MAP
import subprocess

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
