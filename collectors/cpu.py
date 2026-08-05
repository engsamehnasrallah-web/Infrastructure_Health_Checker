from utils.helpers import print_header
import psutil
import platform

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