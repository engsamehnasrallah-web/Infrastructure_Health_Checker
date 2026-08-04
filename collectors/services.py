from collectors.system import print_header
import subprocess

STATUS_MAP = {
                "active": "Running ✅",
                "inactive": "Stopped ❌",
                "failed": "Failed ❌",
                "unknown": "Not Installed ⚠️"
            }

def check_services(services):
    """
    Check the status of specified services and display their status.
    """
    print_header("Services Status")

    for service in services:
        try:
            result = subprocess.run(["systemctl", "is-active", service], capture_output=True, text=True, check=False)
            status = result.stdout.strip()
            status = STATUS_MAP.get(status, status)
            print(f"{service:<22}: {status}")
        except Exception as e:
            print(f"Error checking {service}: {e}")
