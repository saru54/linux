#!/usr/bin/env python3
"""
main.py - Main entry point for Linux system monitoring tool
"""
import time
import sys
import os
from collector import get_cpu_info, get_memory_info, get_disk_info, get_network_info, get_process_info
from display import DisplayManager
from storage import DataPersistence
from alert import AlertManager

def collect_all_data():
    """Collect all system monitoring data"""
    return {
        'cpu_info': get_cpu_info(),
        'memory_info': get_memory_info(),
        'disk_info': get_disk_info(),
        'network_info': get_network_info(),
        'processes_info': get_process_info()
    }

def main():
    """Main monitoring loop"""
    print("=" * 60)
    print("Linux System Monitoring Tool (Probe)")
    print("=" * 60)
    
    interval = 5
    data_dir = "./data"
    
    # Create data directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Initialize alert manager
    alert_manager = AlertManager(cpu_threshold=80, memory_threshold=85, disk_threshold=90)
    
    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Iteration {iteration}] Collecting system data...")
            
            # Collect data
            system_data = collect_all_data()
            
            # Display data
            DisplayManager.display_all(system_data)
            
            # Check alerts
            alert_manager.check_alerts(system_data)
            
            # Save data
            DataPersistence.save_to_json(system_data, os.path.join(data_dir, "monitor.json"))
            
            print(f"Data saved. Next update in {interval} seconds... (Press Ctrl+C to exit)")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\nMonitor stopped by user")
        print(f"Alert history: {len(alert_manager.get_alert_history())} alerts recorded")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()