# ЛР9 — «База данных» на CSV: класс Group, CRUD-операции и CLI
## Задание A - Реализовать класс Group
### Код(Реализация класса Group):
```python
import csv
from pathlib import Path
from src.lab08.models import Student


class Group:
    HEADER = ["fio", "birthdate", "group", "gpa"]

    def __init__(self, storage_path):
        self.path = Path(storage_path)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self):
        if not self.path.exists():
            with self.path.open("w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.HEADER)

    def _read_all(self):
        students = []
        with self.path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                students.append(
                    Student(
                        fio=row["fio"],
                        birthdate=row["birthdate"],
                        group=row["group"],
                        gpa=float(row["gpa"]),
                    )
                )
        return students

    def list(self):
        return self._read_all()

    def add(self, student):
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(
                [student.fio, student.birthdate, student.group, student.gpa]
            )

    def find(self, substr):
        substr = substr.lower()
        return [s for s in self._read_all() if substr in s.fio.lower()]

    def remove(self, fio):
        students = self._read_all()
        students = [s for s in students if s.fio != fio]

        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for s in students:
                writer.writerow([s.fio, s.birthdate, s.group, s.gpa])

    def update(self, fio: str, **fields):
        students = self._read_all()

        for student in students:
            if student.fio == fio:
                for key, value in fields.items():
                    setattr(student, key, value)
                break

        with self.path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(self.HEADER)
            for st in students:
                writer.writerow([st.fio, st.birthdate, st.group, st.gpa])

```
### Код для проверки(main.py):
```python
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.lab09.group import Group
from src.lab08.models import Student

def print_students(title, students):
    print("\n" + title)
    for s in students:
        print(f"{s.fio} | {s.birthdate} | {s.group} | {s.gpa}")
        

g = Group("data/lab09/students.csv")

print_students("Изначальный CSV:", g.list())

new_st = Student("Легенда Артем Академович", "2007-08-10", "БИВТ-25-8", 4.7)
g.add(new_st)
print_students("После добавления:", g.list())

found = g.find("те")  # ищем по подстроке
print_students("Поиск 'те':", found)

g.update("Петров Петр Туборошович", gpa=4.1, group="БИВТ-21-5")
print_students("После обновления данных Петрова:", g.list())

g.remove("Сидорова Анна ЫАЫАЫшевна")
print_students("После удаления Сидоровой:", g.list())
```

### Входной файл CSV:
![1](/images/lab09/csv.png)

### Тесты(вывод в консоли):
![2](/images/lab09/tests.png)

### Файл CSV после тестов:
![3](/images/lab09/csv_out.png)

# Вывод:
В этой лабораторной работе я реализовал класс Group для выполнения всех CRUD-операций над данными студентов, хранящимися в CSV-файле. Я создал методы для добавления новых записей, поиска по ФИО, обновления полей и удаления студентов. Класс работает с объектами Student, которые я разработал ранее, и самостоятельно обеспечивает целостность хранилища, создавая файл с нужной структурой при первом запуске. В результате я получил готовый и надёжный модуль для управления данными, который я смогу использовать как основу для командной строки в следующей работе. Эта задача позволила мне закрепить на практике принципы объектно-ориентированного программирования и работу с файловой системой в Python.