import psutil

def system_monitor():
    """
    Collect and display basic infrastructure health metrics.
    """

    print("=" * 30)
    print("Infrastructure Health Checker")
    print("=" * 30)

    cpu_usage = psutil.cpu_percent(interval=1)
    print(f"CPU Usage              : {cpu_usage}%")

    memory_info = psutil.virtual_memory()
    print(f"Memory Usage           : {memory_info.percent}%")

    disk_info = psutil.disk_usage('/')
    print(f"Disk Usage             : {disk_info.percent}%")