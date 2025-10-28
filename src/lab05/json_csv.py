import json
from pathlib import Path
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../lib'))
from io_helper import read_text, write_csv, get_file_extension

def json_to_csv(json_path: str, csv_path: str) -> None:
    if get_file_extension(json_path) != '.json':
        raise ValueError("Неверный тип файла. Ожидается .json")
    
    # Используем read_text для чтения JSON файла
    try:
        json_content = read_text(json_path)
        data = json.loads(json_content)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {json_path} не найден")
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON: {e}")
    
    if not data:
        raise ValueError("Пустой JSON или неподдерживаемая структура")
    
    if not isinstance(data, list):
        raise ValueError("JSON должен содержать список объектов")
    
    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Все элементы JSON должны быть словарями")
    
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    if data:
        first_item_keys = list(data[0].keys())
        remaining_keys = sorted(all_keys - set(first_item_keys))
        fieldnames = first_item_keys + remaining_keys
    else:
        fieldnames = sorted(all_keys)
    
    # Запись в CSV с использованием write_csv
    try:
        rows = []
        for row in data:
            complete_row = [row.get(key, '') for key in fieldnames]
            rows.append(complete_row)
        
        write_csv(rows, csv_path, header=fieldnames)
    except Exception as e:
        raise ValueError(f"Ошибка записи CSV: {e}")

def csv_to_json(csv_path: str, json_path: str) -> None:
    if get_file_extension(csv_path) != '.csv':
        raise ValueError("Неверный тип файла. Ожидается .csv")
    
    try:
        csv_content = read_text(csv_path)
        lines = csv_content.strip().split('\n')
        
        if not lines:
            raise ValueError("Пустой CSV файл")
            
        fieldnames = lines[0].split(',')
        data = []
        
        for line in lines[1:]:
            if line.strip():
                values = line.split(',')
                row = dict(zip(fieldnames, values))
                data.append(row)
                
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if not data:
        raise ValueError("Пустой CSV файл")

    try:
        Path(json_path).parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise ValueError(f"Ошибка записи JSON: {e}")
json_to_csv("src/data/lab05/samples/people.json", "src/data/lab05/out/people_from_json.csv")
csv_to_json("src/data/lab05/samples/people.csv", "src/data/lab05/out/people_from_csv.json")