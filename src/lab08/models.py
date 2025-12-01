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