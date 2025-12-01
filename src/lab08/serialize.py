import json
from typing import List
from pathlib import Path
from lab08.models import Student

def students_to_json(students: List[Student], path: str) -> None:

    # Преобразуем каждого студента в словарь
    data = [student.to_dict() for student in students]
    
    # Создаем директорию, если её нет
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    # Записываем в файл
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"Данные сохранены в файл: {path}")

def students_from_json(path: str) -> List[Student]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Создаем объекты Student из словарей
        students = []
        for item in data:
            try:
                student = Student.from_dict(item)
                students.append(student)
            except (ValueError, KeyError) as e:
                print(f"Ошибка при создании студента из данных: {item}")
                print(f"Ошибка: {e}")
                continue
        
        print(f"Загружено {len(students)} студентов из файла: {path}")
        return students
        
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка при чтении JSON из файла: {path}")
        return []