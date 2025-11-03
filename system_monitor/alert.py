"""
alert.py - Alert and notification system
"""
from datetime import datetime

class AlertManager:
    def __init__(self, cpu_threshold=80, memory_threshold=85, disk_threshold=90):
        self.cpu_threshold = cpu_threshold
        self.memory_threshold = memory_threshold
        self.disk_threshold = disk_threshold
        self.alert_history = []
    
    def check_alerts(self, system_data):
        """Check system metrics against thresholds"""
        alerts = []
        
        cpu_usage = system_data.get('cpu_info', {}).get('cpu_usage', 0)
        if cpu_usage > self.cpu_threshold:
            msg = f"WARNING: CPU usage {cpu_usage:.2f}% exceeds threshold {self.cpu_threshold}%"
            alerts.append(msg)
            print(f"[ALERT] {msg}")
        
        memory_usage = system_data.get('memory_info', {}).get('memory_percentage', 0)
        if memory_usage > self.memory_threshold:
            msg = f"WARNING: Memory usage {memory_usage:.2f}% exceeds threshold {self.memory_threshold}%"
            alerts.append(msg)
            print(f"[ALERT] {msg}")
        
        disk_usage = system_data.get('disk_info', {}).get('disk_percentage', 0)
        if disk_usage > self.disk_threshold:
            msg = f"WARNING: Disk usage {disk_usage:.2f}% exceeds threshold {self.disk_threshold}%"
            alerts.append(msg)
            print(f"[ALERT] {msg}")
        
        self.alert_history.extend(alerts)
        return alerts
    
    def get_alert_history(self):
        """Get all alert history"""
        return self.alert_history
    
    def clear_alerts(self):
        """Clear alert history"""
        self.alert_history = []