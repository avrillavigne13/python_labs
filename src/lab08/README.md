# Лабораторная работа №8 — ООП в Python: @dataclass Student, методы и сериализация
## Задание A - Student (models.py)
### Исходный код:
```python
from dataclasses import dataclass, asdict
from datetime import datetime, date
import json
from typing import Dict, Any

@dataclass
class Student:
    fio: str
    birthdate: str
    group: str
    gpa: float
    
    def __post_init__(self):
        # Валидация даты рождения
        try:
            datetime.strptime(self.birthdate, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Неправильный формат даты: {self.birthdate}. Ожидается: YYYY-MM-DD")
        
        # Валидация среднего балла
        if not (0 <= self.gpa <= 5):
            raise ValueError(f"Средний балл должен быть от 0 до 5. Получено: {self.gpa}")
        
        # Валидация ФИО (минимум 3 слова)
        if len(self.fio.split()) < 3:
            raise ValueError(f"ФИО должно содержать 3 слова. Получено: {self.fio}")
    
    def age(self) -> int:
        # Кол-во полных лет
        birth_date = datetime.strptime(self.birthdate, "%Y-%m-%d").date()
        today = date.today()
        
        # Вычисляем разницу в годах
        age_years = today.year - birth_date.year
        
        # Проверяем, был ли уже день рождения в этом году
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age_years -= 1
        
        return age_years
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':

        return cls(
            fio=data['fio'],
            birthdate=data['birthdate'],
            group=data['group'],
            gpa=data['gpa']
        )
    
    def __str__(self) -> str:

        return f"Студент: {self.fio}\n" \
               f"Возраст: {self.age()} лет\n" \
               f"Группа: {self.group}\n" \
               f"Средний балл: {self.gpa}"
```

## Задание B - serialize.py
### Исходный код:
```python
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
```
## Тесты:
### Входной файл:
![1](/images/lab08/students_input.png)

**Вывод консоли:**
![2](/images/lab08/input_from_json.png)
![3](/images/lab08/output_from_json.png)

### Выходной файл:
![1](/images/lab08/students_output.png)


## Вывод
В ходе лабораторной работы выполнена разработка объектно-ориентированной модели данных: создан класс Student с использованием декоратора @dataclass, реализованы методы обработки данных и валидации, внедрены функции сериализации students_to_json() и students_from_json(). Проект имеет четкую модульную структуру с разделением на модели данных и логику сериализации, соответствующую стандартам объектно-ориентированного программирования в Python.
