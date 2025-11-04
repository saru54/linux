#!/usr/bin/env python3
"""
main.py - Main entry point for Linux system monitoring tool
"""
import time
import sys
import os
import yaml
from datetime import datetime, timedelta
from collector import get_cpu_info, get_memory_info, get_disk_info, get_network_info, get_process_info
from display import DisplayManager
from storage import DataPersistence
from alert import AlertManager

def load_config(config_file='config.yaml'):
    """Load configuration from YAML file"""
    try:
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        # Return default config
        return {
            'monitor': {'interval': 5, 'retention_hours': 24},
            'alerts': {'cpu_threshold': 80, 'memory_threshold': 85, 'disk_threshold': 90, 'network_threshold': 100},
            'storage': {'storage_format': 'json', 'data_dir': './data', 'json_file': './data/monitor.json', 'csv_file': './data/monitor.csv'},
            'features': {'enable_alert': True, 'enable_visualization': False, 'enable_logging': False}
        }

def setup_logging(log_dir):
    """Setup logging to file and console"""
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, 'system_monitor.log')
    
    # Simple logging to file
    class Logger:
        def __init__(self, log_path):
            self.log_path = log_path
        
        def log(self, level, message):
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_message = f"{timestamp} - {level} - {message}"
            print(log_message)
            try:
                with open(self.log_path, 'a') as f:
                    f.write(log_message + '\n')
            except:
                pass
    
    return Logger(log_file)

def cleanup_old_data(csv_file, retention_hours):
    """Remove data older than retention period"""
    if not os.path.exists(csv_file):
        return
    
    try:
        import csv
        rows = []
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row.get('timestamp', ''))
                    if timestamp > cutoff_time:
                        rows.append(row)
                except:
                    rows.append(row)
        
        # Rewrite file with filtered data
        if rows and len(rows) > 0:
            keys = rows[0].keys()
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=keys)
                writer.writeheader()
                writer.writerows(rows)
    except Exception as e:
        pass

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
    
    # Load configuration from config.yaml
    config = load_config('config.yaml')
    
    # Extract configuration values
    interval = config.get('monitor', {}).get('interval', 5)
    retention_hours = config.get('monitor', {}).get('retention_hours', 24)
    data_dir = config.get('storage', {}).get('data_dir', './data')
    storage_format = config.get('storage', {}).get('storage_format', 'json').lower()
    csv_file = config.get('storage', {}).get('csv_file', './data/monitor.csv')
    json_file = config.get('storage', {}).get('json_file', './data/monitor.json')
    log_dir = config.get('storage', {}).get('log_dir', './logs')
    
    enable_alert = config.get('features', {}).get('enable_alert', True)
    enable_visualization = config.get('features', {}).get('enable_visualization', False)
    enable_logging = config.get('features', {}).get('enable_logging', False)
    
    # Setup logging if enabled
    logger = None
    if enable_logging:
        logger = setup_logging(log_dir)
        logger.log('INFO', 'Starting Linux System Monitoring Tool')
        logger.log('INFO', f'Configuration loaded: interval={interval}s, format={storage_format}, retention={retention_hours}h')
    
    # Display configuration
    print(f"\n[Configuration]")
    print(f"  Monitoring interval: {interval}s")
    print(f"  Data retention: {retention_hours}h")
    print(f"  Storage format: {storage_format.upper()}")
    print(f"  Data directory: {data_dir}")
    print(f"  Enable alerts: {enable_alert}")
    print(f"  Enable logging: {enable_logging}")
    print(f"  Enable visualization: {enable_visualization}")
    print()
    
    # Create data directory if not exists
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Initialize alert manager
    alert_config = config.get('alerts', {})
    alert_manager = AlertManager(
        cpu_threshold=alert_config.get('cpu_threshold', 80),
        memory_threshold=alert_config.get('memory_threshold', 85),
        disk_threshold=alert_config.get('disk_threshold', 90)
    )
    
    try:
        iteration = 0
        while True:
            iteration += 1
            print(f"\n[Iteration {iteration}] Collecting system data...")
            
            if enable_logging:
                logger.log('INFO', f'Iteration {iteration}: Collecting data')
            
            # Collect data
            system_data = collect_all_data()
            
            # Display data
            DisplayManager.display_all(system_data)
            
            # Check alerts
            if enable_alert:
                alerts = alert_manager.check_alerts(system_data)
                if alerts and enable_logging:
                    for alert in alerts:
                        logger.log('WARNING', alert)
            
            # Save data using configured format
            try:
                DataPersistence.save_by_format(system_data, config)
                if storage_format == 'csv':
                    print(f"✓ Data appended to CSV: {csv_file}")
                    if enable_logging:
                        logger.log('INFO', f'Data saved to CSV: {csv_file}')
                else:
                    print(f"✓ Data saved to JSON: {json_file}")
                    if enable_logging:
                        logger.log('INFO', f'Data saved to JSON: {json_file}')
            except Exception as e:
                print(f"✗ Error saving data: {e}")
                if enable_logging:
                    logger.log('ERROR', f'Error saving data: {e}')
            
            # Cleanup old data if using CSV
            if storage_format == 'csv' and iteration % 10 == 0:  # Check every 10 iterations
                cleanup_old_data(csv_file, retention_hours)
                if enable_logging:
                    logger.log('INFO', f'Cleaned up data older than {retention_hours}h')
            
            # TODO: Add visualization if enabled
            if enable_visualization:
                pass  # Visualization implementation
            
            print(f"Next update in {interval} seconds... (Press Ctrl+C to exit)")
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\n\nMonitor stopped by user")
        print(f"Alert history: {len(alert_manager.get_alert_history())} alerts recorded")
        if enable_logging:
            logger.log('INFO', f'Monitor stopped. Total alerts: {len(alert_manager.get_alert_history())}')
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if enable_logging:
            logger.log('ERROR', f'Fatal error: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()