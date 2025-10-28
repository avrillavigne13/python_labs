# Лабораторная работа №5
## Задание A — JSON ↔ CSV

### Исходный код:
```python
import json
import csv
from pathlib import Path


def json_to_csv(json_path: str, csv_path: str) -> None:

    json_file = Path(json_path)
    csv_file = Path(csv_path)
    
    if not json_file.exists():
        raise FileNotFoundError(f"Файл {json_path} не найден")
    
    if json_file.suffix.lower() != '.json':
        raise ValueError("Неверный тип файла. Ожидается .json")
    
    try:
        with json_file.open('r', encoding='utf-8') as f:
            data = json.load(f)
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
    # Запись в CSV
    try:
        with csv_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                complete_row = {key: row.get(key, '') for key in fieldnames}
                writer.writerow(complete_row)
    except Exception as e:
        raise ValueError(f"Ошибка записи CSV: {e}")

def csv_to_json(csv_path: str, json_path: str) -> None:
  
    csv_file = Path(csv_path)
    json_file = Path(json_path)
    
    if not csv_file.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден")

    if csv_file.suffix.lower() != '.csv':
        raise ValueError("Неверный тип файла. Ожидается .csv")
    
    try:
        with csv_file.open('r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            if reader.fieldnames is None:
                raise ValueError("CSV файл не содержит заголовка")
            
            data = list(reader)
            
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")

    if not data:
        raise ValueError("Пустой CSV файл")

    try:
        with json_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        raise ValueError(f"Ошибка записи JSON: {e}")

json_to_csv("src/data/lab05/samples/people.json", "src/data/lab05/out/people_from_json.csv")
csv_to_json("src/data/lab05/samples/people.csv", "src/data/lab05/out/people_from_csv.json")
```
#### Преобразует JSON-файл в CSV.
```python
def json_to_csv(json_path: str, csv_path: str) -> None:
```
### Особенности:
 - Поддерживает список словарей [{...}, {...}], заполняет отсутствующие поля пустыми строками.
- Кодировка UTF-8. Порядок колонок — как в первом объекте или алфавитный

#### Преобразует CSV в JSON (список словарей).
```python
def csv_to_json(csv_path: str, json_path: str) -> None:
```
### Особенности:
- Заголовок обязателен, значения сохраняются как строки.
- json.dump(..., ensure_ascii=False, indent=2)

### Примеры использования:
```python
json_to_csv("src/data/lab05/samples/people.json", "src/data/lab05/out/people_from_json.csv")

csv_to_json("src/data/lab05/samples/people.csv", "src/data/lab05/out/people_from_csv.json")
```
## Задание B — CSV → XLSX
### Исходный код:
```python
import csv
from pathlib import Path
from openpyxl import Workbook
from openpyxl.utils import get_column_letter


def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:

    csv_file = Path(csv_path)
    xlsx_file = Path(xlsx_path)
    
    if not csv_file.exists():
        raise FileNotFoundError(f"Файл {csv_path} не найден")
    
    if csv_file.suffix.lower() != '.csv':
        raise ValueError("Неверный тип файла. Ожидается .csv")
    
    # Чтение CSV
    try:
        with csv_file.open('r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        raise ValueError(f"Ошибка чтения CSV: {e}")
    
    if not rows:
        raise ValueError("Пустой CSV файл")
    
    if not rows[0]:
        raise ValueError("CSV файл не содержит заголовка")
    
    # Создание XLSX
    try:
        wb = Workbook()
        ws = wb.active
        ws.title = "Sheet1"
        
        for row in rows:
            ws.append(row)
        
        
        for col_idx, column_cells in enumerate(ws.columns, 1):
            max_length = 8  
            column_letter = get_column_letter(col_idx)
            
            for cell in column_cells:
                try:
                    if cell.value:

                        cell_length = len(str(cell.value))
                        if cell_length > max_length:
                            max_length = cell_length
                except:
                    pass
            
            adjusted_width = max_length + 2
            ws.column_dimensions[column_letter].width = adjusted_width
        
        wb.save(xlsx_file)
        
    except Exception as e:
        raise ValueError(f"Ошибка создания XLSX: {e}")
    
csv_to_xlsx("src/data/lab05/samples/people.csv", "src/data/lab05/out/people.xlsx")
csv_to_xlsx("src/data/lab05/samples/cities.csv", "src/data/lab05/out/cities.xlsx")
```
#### Конвертирует CSV-файл в XLSX формат.
```python
def csv_to_xlsx(csv_path: str, xlsx_path: str) -> None:
```
### Особенности:
- Использует библиотеку openpyxl
- Первая строка CSV — заголовок.
- Лист называется "Sheet1"
- Колонки — автоширина по длине текста (не менее 8 символов).

### Примеры использования:
```python
csv_to_xlsx("src/data/lab05/samples/people.csv", "src/data/lab05/out/people.xlsx")
csv_to_xlsx("src/data/lab05/samples/cities.csv", "src/data/lab05/out/cities.xlsx")
```

## Установка зависимостей:
#### Через `requirements.txt`:
```bash
pip install -r requirements.txt
```
#### Напрямую
```bash
pip install openpyxl
```

## Примеры выполнений:

### Задание A

#### Входные данные:
![1](/images/lab05/people_json_input.png)
#### Вывод:
![2](/images/lab05/people_from_json_output.png)

#### Входные данные:
![3](/images/lab05/people_csv_input.png)
#### Вывод:
![4](/images/lab05/people_from_csv_output.png)

### Задание B

#### Входные данные:
![5](/images/lab05/people_csv_input.png)
#### Вывод:
![6](/images/lab05/people_xlsx.png)

#### Входные данные:
![7](/images/lab05/cities_csv_input.png)
#### Вывод:
![8](/images/lab05/cities_xlsx.png)

## Вывод:
Разработанный в ходе лабораторной работы программный комплекс позволяет автоматизировать анализ текста: подсчитывать частоту слов и формировать отчёты в CSV. Модульная архитектура обеспечивает гибкость и повторное использование кода. Все компоненты системы протестированы и функционируют в соответствии с заданием.