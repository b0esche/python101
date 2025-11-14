import json
import os
from typing import Dict, List, Any, Union

class JSONProcessor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: Union[Dict[str, Any], List[Any], None] = None
    
    def load_json(self) -> Union[Dict[str, Any], List[Any], None]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.data = json.load(file)
            print(f"Successfully loaded JSON from {self.file_path}")
            return self.data
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
            return {}
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}
    
    def save_json(self, data: Union[Dict[str, Any], List[Any]], indent: int = 2) -> bool:
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
            print(f"Successfully saved JSON to {self.file_path}")
            return True
        except Exception as e:
            print(f"Error saving JSON: {e}")
            return False
    
    def get_value(self, key_path: str, default=None):
        if not self.data:
            self.load_json()
        
        if not isinstance(self.data, dict):
            return default
        
        keys = key_path.split('.')
        current = self.data
        
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default
    
    def set_value(self, key_path: str, value: Any):
        if not self.data:
            self.load_json()
        
        if not isinstance(self.data, dict):
            print("Cannot set value on non-dict data")
            return False
        
        keys = key_path.split('.')
        current = self.data
        
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        current[keys[-1]] = value
        return self.save_json(self.data)
    
    def filter_data(self, filter_func) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        if not self.data:
            self.load_json()
        
        if isinstance(self.data, list):
            return [item for item in self.data if filter_func(item)]
        elif isinstance(self.data, dict):
            return {k: v for k, v in self.data.items() if filter_func(k, v)}
        else:
            return []
    
    def merge_json(self, other_file_path: str) -> bool:
        try:
            with open(other_file_path, 'r', encoding='utf-8') as file:
                other_data = json.load(file)
            
            if not self.data:
                self.load_json()
            
            if isinstance(self.data, dict) and isinstance(other_data, dict):
                self.data.update(other_data)
            elif isinstance(self.data, list) and isinstance(other_data, list):
                self.data.extend(other_data)
            else:
                print("Cannot merge different data types")
                return False
            
            return self.save_json(self.data)
        except Exception as e:
            print(f"Error merging JSON: {e}")
            return False

def create_sample_data():
    sample_data = {
        "users": [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 2, "name": "Bob", "age": 25, "city": "Los Angeles"},
            {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"}
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "language": "en"
        }
    }
    
    with open('sample_data.json', 'w', encoding='utf-8') as file:
        json.dump(sample_data, file, indent=2)
    
    print("Sample data created in 'sample_data.json'")

def main():
    create_sample_data()
    
    processor = JSONProcessor('sample_data.json')
    
    print("\n--- Loading JSON ---")
    data = processor.load_json()
    print(f"Loaded data: {json.dumps(data, indent=2)}")
    
    print("\n--- Getting values ---")
    print(f"User 1 name: {processor.get_value('users.0.name')}")
    print(f"Settings theme: {processor.get_value('settings.theme')}")
    print(f"Non-existent key: {processor.get_value('non.existent.key', 'default')}")
    
    print("\n--- Setting values ---")
    processor.set_value('settings.new_setting', 'new_value')
    processor.set_value('users.0.email', 'alice@example.com')
    
    print("\n--- Filtering data ---")
    users_over_30 = processor.filter_data(lambda x: x.get('age', 0) > 30)
    print(f"Users over 30: {users_over_30}")
    
    print("\n--- Updated data ---")
    updated_data = processor.load_json()
    print(f"Updated data: {json.dumps(updated_data, indent=2)}")

if __name__ == "__main__":
    main()