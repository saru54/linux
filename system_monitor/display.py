from tabulate import tabulate
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

class DisplayManager:
    """管理系统监控数据的展示"""
    
    @staticmethod
    def display_cpu_info(cpu_data):
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}CPU 信息")
        print(f"{Fore.CYAN}{'='*60}")
        
        table_data = [
            ["CPU核心数", cpu_data.get('cpu_count', 'N/A')],
            ["CPU使用率(%)", f"{cpu_data.get('cpu_usage', 0):.2f}%"],
            ["用户时间(s)", f"{cpu_data.get('cpu_times', {}).get('user', 0):.2f}"],
            ["系统时间(s)", f"{cpu_data.get('cpu_times', {}).get('system', 0):.2f}"],
            ["空闲时间(s)", f"{cpu_data.get('cpu_times', {}).get('idle', 0):.2f}"],
        ]
        print(tabulate(table_data, headers=["指标", "数值"], tablefmt="grid"))
    
    @staticmethod
    def display_memory_info(memory_data):
        print(f"\n{Fore.GREEN}{'='*60}")
        print(f"{Fore.GREEN}内存信息")
        print(f"{Fore.GREEN}{'='*60}")
        
        total = memory_data.get('total_memory', 0) / (1024**3)
        used = memory_data.get('used_memory', 0) / (1024**3)
        available = memory_data.get('available_memory', 0) / (1024**3)
        percent = memory_data.get('memory_percentage', 0)
        
        table_data = [
            ["总内存(GB)", f"{total:.2f}"],
            ["已用(GB)", f"{used:.2f}"],
            ["可用(GB)", f"{available:.2f}"],
            ["使用率(%)", f"{percent:.2f}%"],
        ]
        print(tabulate(table_data, headers=["指标", "数值"], tablefmt="grid"))
    
    @staticmethod
    def display_disk_info(disk_data):
        print(f"\n{Fore.YELLOW}{'='*60}")
        print(f"{Fore.YELLOW}磁盘信息")
        print(f"{Fore.YELLOW}{'='*60}")
        
        total = disk_data.get('total_disk_space', 0) / (1024**3)
        used = disk_data.get('used_disk_space', 0) / (1024**3)
        free = disk_data.get('free_disk_space', 0) / (1024**3)
        percent = disk_data.get('disk_percentage', 0)
        
        table_data = [
            ["总容量(GB)", f"{total:.2f}"],
            ["已用(GB)", f"{used:.2f}"],
            ["可用(GB)", f"{free:.2f}"],
            ["使用率(%)", f"{percent:.2f}%"],
        ]
        print(tabulate(table_data, headers=["指标", "数值"], tablefmt="grid"))
    
    @staticmethod
    def display_network_info(network_data):
        print(f"\n{Fore.MAGENTA}{'='*60}")
        print(f"{Fore.MAGENTA}网络接口信息")
        print(f"{Fore.MAGENTA}{'='*60}")
        
        table_data = []
        for iface, addrs in network_data.items():
            for addr in addrs:
                table_data.append([iface, addr])
        
        if table_data:
            print(tabulate(table_data, headers=["接口名", "IP地址"], tablefmt="grid"))
    
    @staticmethod
    def display_all(system_data):
        print(f"\n{Fore.WHITE}{'='*60}")
        print(f"{Fore.WHITE}系统监控面板 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{Fore.WHITE}{'='*60}")
        DisplayManager.display_cpu_info(system_data.get('cpu_info', {}))
        DisplayManager.display_memory_info(system_data.get('memory_info', {}))
        DisplayManager.display_disk_info(system_data.get('disk_info', {}))
        DisplayManager.display_network_info(system_data.get('network_info', {}))
        print(f"\n{Fore.WHITE}{'='*60}\n")
