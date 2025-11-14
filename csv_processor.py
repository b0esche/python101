import csv
import json
from typing import List, Dict, Any, Optional, Union
import os
from datetime import datetime
import statistics

class CSVProcessor:
    def __init__(self, file_path: str, delimiter: str = ',', encoding: str = 'utf-8'):
        self.file_path = file_path
        self.delimiter = delimiter
        self.encoding = encoding
        self.data = []
        self.headers = []
    
    def read_csv(self, has_header: bool = True) -> List[Dict[str, Any]]:
        try:
            with open(self.file_path, 'r', encoding=self.encoding, newline='') as file:
                reader = csv.reader(file, delimiter=self.delimiter)
                
                if has_header:
                    self.headers = next(reader)
                    for row in reader:
                        if len(row) == len(self.headers):
                            self.data.append(dict(zip(self.headers, row)))
                        else:
                            print(f"Skipping row with mismatched columns: {row}")
                else:
                    for i, row in enumerate(reader):
                        self.data.append({f'column_{j}': value for j, value in enumerate(row)})
            
            print(f"Loaded {len(self.data)} rows from {self.file_path}")
            return self.data
            
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found")
            return []
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return []
    
    def write_csv(self, data: List[Dict[str, Any]], output_path: Optional[str] = None):
        if not data:
            print("No data to write")
            return
        
        if output_path is None:
            output_path = self.file_path
        
        if not data:
            return
        
        fieldnames = data[0].keys()
        
        try:
            with open(output_path, 'w', encoding=self.encoding, newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=self.delimiter)
                writer.writeheader()
                writer.writerows(data)
            
            print(f"Written {len(data)} rows to {output_path}")
            
        except Exception as e:
            print(f"Error writing CSV: {e}")
    
    def filter_rows(self, condition) -> List[Dict[str, Any]]:
        return [row for row in self.data if condition(row)]
    
    def sort_by_column(self, column: str, reverse: bool = False) -> List[Dict[str, Any]]:
        try:
            return sorted(self.data, key=lambda x: x.get(column, ''), reverse=reverse)
        except Exception as e:
            print(f"Error sorting: {e}")
            return self.data
    
    def get_unique_values(self, column: str) -> List[Any]:
        return list(set(row.get(column) for row in self.data if row.get(column) is not None))
    
    def group_by_column(self, column: str) -> Dict[Any, List[Dict[str, Any]]]:
        groups = {}
        for row in self.data:
            key = row.get(column)
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
        return groups
    
    def get_column_stats(self, column: str) -> Dict[str, Any]:
        values = []
        for row in self.data:
            value = row.get(column)
            if value is not None:
                try:
                    values.append(float(value))
                except ValueError:
                    pass
        
        if not values:
            return {"error": "No numeric values found"}
        
        return {
            "count": len(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "mode": statistics.mode(values) if len(set(values)) < len(values) else None,
            "min": min(values),
            "max": max(values),
            "sum": sum(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0
        }
    
    def add_column(self, column_name: str, default_value: Any = None):
        for row in self.data:
            row[column_name] = default_value
    
    def update_column(self, column: str, update_func):
        for row in self.data:
            if column in row:
                row[column] = update_func(row[column])
    
    def delete_column(self, column: str):
        for row in self.data:
            if column in row:
                del row[column]
    
    def merge_csv(self, other_csv: 'CSVProcessor', on_column: str, how: str = 'inner') -> List[Dict[str, Any]]:
        other_data = other_csv.data
        
        if how == 'inner':
            merged = []
            for row1 in self.data:
                for row2 in other_data:
                    if row1.get(on_column) == row2.get(on_column):
                        merged_row = {**row1, **row2}
                        merged.append(merged_row)
            return merged
        
        elif how == 'left':
            merged = []
            for row1 in self.data:
                matching_row = None
                for row2 in other_data:
                    if row1.get(on_column) == row2.get(on_column):
                        matching_row = row2
                        break
                
                if matching_row:
                    merged_row = {**row1, **matching_row}
                else:
                    merged_row = row1.copy()
                merged.append(merged_row)
            return merged
        
        return self.data
    
    def to_json(self, output_path: str):
        try:
            with open(output_path, 'w', encoding=self.encoding) as file:
                json.dump(self.data, file, indent=2, ensure_ascii=False)
            print(f"Data exported to JSON: {output_path}")
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
    
    def from_json(self, json_path: str):
        try:
            with open(json_path, 'r', encoding=self.encoding) as file:
                self.data = json.load(file)
            
            if self.data:
                self.headers = list(self.data[0].keys())
            
            print(f"Loaded {len(self.data)} rows from JSON: {json_path}")
        except Exception as e:
            print(f"Error loading from JSON: {e}")

def create_sample_csv():
    sample_data = [
        {"name": "Alice", "age": "30", "city": "New York", "salary": "75000"},
        {"name": "Bob", "age": "25", "city": "Los Angeles", "salary": "65000"},
        {"name": "Charlie", "age": "35", "city": "Chicago", "salary": "80000"},
        {"name": "Diana", "age": "28", "city": "New York", "salary": "70000"},
        {"name": "Eve", "age": "32", "city": "Los Angeles", "salary": "72000"},
        {"name": "Frank", "age": "29", "city": "Chicago", "salary": "68000"}
    ]
    
    processor = CSVProcessor('sample_data.csv')
    processor.write_csv(sample_data)
    print("Sample CSV created: sample_data.csv")

def main():
    print("CSV Processing Examples")
    print("=" * 50)
    
    create_sample_csv()
    
    print("\n1. Reading CSV data:")
    processor = CSVProcessor('sample_data.csv')
    data = processor.read_csv()
    
    print(f"Headers: {processor.headers}")
    print(f"First 3 rows: {data[:3]}")
    
    print("\n2. Filtering data:")
    high_earners = processor.filter_rows(lambda x: float(x.get('salary', 0)) > 70000)
    print(f"High earners (>70000): {len(high_earners)}")
    for person in high_earners:
        print(f"  {person['name']}: ${person['salary']}")
    
    print("\n3. Sorting data:")
    sorted_by_age = processor.sort_by_column('age')
    print("Sorted by age:")
    for person in sorted_by_age:
        print(f"  {person['name']}: {person['age']}")
    
    print("\n4. Grouping data:")
    grouped_by_city = processor.group_by_column('city')
    for city, people in grouped_by_city.items():
        print(f"  {city}: {len(people)} people")
    
    print("\n5. Column statistics:")
    salary_stats = processor.get_column_stats('salary')
    print("Salary statistics:")
    for key, value in salary_stats.items():
        print(f"  {key}: {value}")
    
    print("\n6. Adding and updating columns:")
    processor.add_column('bonus', '0')
    processor.update_column('bonus', lambda x: str(float(x) * 0.1))
    processor.update_column('total_compensation', lambda row: str(float(row['salary']) + float(row['bonus'])))
    
    print("Updated data with bonus:")
    for person in processor.data[:3]:
        print(f"  {person['name']}: Salary=${person['salary']}, Bonus=${person['bonus']}, Total=${person['total_compensation']}")
    
    print("\n7. Exporting to different formats:")
    processor.write_csv(processor.data, 'updated_data.csv')
    processor.to_json('data.json')
    
    print("\n8. Merging CSV files:")
    create_sample_csv()
    
    department_data = [
        {"name": "Alice", "department": "Engineering"},
        {"name": "Bob", "department": "Marketing"},
        {"name": "Charlie", "department": "Engineering"},
        {"name": "Diana", "department": "Sales"},
        {"name": "Eve", "department": "Marketing"},
        {"name": "Frank", "department": "Engineering"}
    ]
    
    dept_processor = CSVProcessor('departments.csv')
    dept_processor.write_csv(department_data)
    dept_processor.read_csv()
    
    merged_data = processor.merge_csv(dept_processor, 'name', how='left')
    print("Merged data:")
    for person in merged_data[:3]:
        print(f"  {person['name']}: {person['city']}, {person.get('department', 'N/A')}")
    
    processor.write_csv(merged_data, 'merged_data.csv')
    
    print("\nCSV processing completed!")

if __name__ == "__main__":
    main()