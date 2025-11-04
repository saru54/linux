import json
import csv
import os
from datetime import datetime

class DataPersistence:
    @staticmethod
    def save_to_json(data, filename):
        """Save data to JSON file"""
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        return True

    @staticmethod
    def load_from_json(filename):
        """Load data from JSON file"""
        if os.path.exists(filename):
            with open(json_file, 'r') as json_file:
                return json.load(json_file)
        return None

    @staticmethod
    def save_to_csv(data, filename):
        """Append data to CSV file (not overwrite)"""
        # Flatten the nested dict structure for CSV
        flat_data = DataPersistence._flatten_data(data)
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.exists(filename)
        
        keys = flat_data.keys() if flat_data else []
        
        with open(filename, 'a', newline='') as csv_file:
            dict_writer = csv.DictWriter(csv_file, fieldnames=keys)
            
            # Write header only if file doesn't exist
            if not file_exists:
                dict_writer.writeheader()
            
            dict_writer.writerow(flat_data)
        
        return True

    @staticmethod
    def load_from_csv(filename):
        """Load data from CSV file"""
        if os.path.exists(filename):
            with open(filename, 'r') as csv_file:
                return list(csv.DictReader(csv_file))
        return None

    @staticmethod
    def _flatten_data(data):
        """Flatten nested dict structure for CSV storage"""
        flat = {
            'timestamp': datetime.now().isoformat(),
            'cpu_usage': data.get('cpu_info', {}).get('cpu_usage', 0),
            'cpu_count': data.get('cpu_info', {}).get('cpu_count', 0),
            'memory_total_gb': round(data.get('memory_info', {}).get('total_memory', 0) / (1024**3), 2),
            'memory_used_gb': round(data.get('memory_info', {}).get('used_memory', 0) / (1024**3), 2),
            'memory_percentage': data.get('memory_info', {}).get('memory_percentage', 0),
            'disk_total_gb': round(data.get('disk_info', {}).get('total_disk_space', 0) / (1024**3), 2),
            'disk_used_gb': round(data.get('disk_info', {}).get('used_disk_space', 0) / (1024**3), 2),
            'disk_percentage': data.get('disk_info', {}).get('disk_percentage', 0),
        }
        return flat
    
    @staticmethod
    def save_by_format(data, config):
        """Save data using format specified in config"""
        storage_format = config.get('storage', {}).get('storage_format', 'json').lower()
        data_dir = config.get('storage', {}).get('data_dir', './data')
        
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        if storage_format == 'csv':
            csv_file = config.get('storage', {}).get('csv_file', './data/monitor.csv')
            return DataPersistence.save_to_csv(data, csv_file)
        else:  # default to json
            json_file = config.get('storage', {}).get('json_file', './data/monitor.json')
            return DataPersistence.save_to_json(data, json_file)