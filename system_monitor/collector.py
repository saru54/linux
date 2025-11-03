import psutil
import platform

def get_cpu_info():
    """Collects and returns CPU information."""
    return {
        'cpu_count': psutil.cpu_count(),
        'cpu_usage': psutil.cpu_percent(interval=1),
        'cpu_times': psutil.cpu_times()._asdict()
    }

def get_memory_info():
    """Collects and returns memory information."""
    memory = psutil.virtual_memory()
    return {
        'total_memory': memory.total,
        'available_memory': memory.available,
        'used_memory': memory.used,
        'memory_percentage': memory.percent
    }

def get_disk_info():
    """Collects and returns disk information."""
    disk = psutil.disk_usage('/')
    return {
        'total_disk_space': disk.total,
        'used_disk_space': disk.used,
        'free_disk_space': disk.free,
        'disk_percentage': disk.percent
    }

def get_network_info():
    """Collects and returns network information."""
    network = psutil.net_if_addrs()
    return {iface: [addr.address for addr in addresses] for iface, addresses in network.items()}

def get_process_info():
    """Collects and returns process information."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        processes.append(proc.info)
    return processes

if __name__ == "__main__":
    print("CPU Info:", get_cpu_info())
    print("Memory Info:", get_memory_info())
    print("Disk Info:", get_disk_info())
    print("Network Info:", get_network_info())
    print("Processes Info:", get_process_info())
