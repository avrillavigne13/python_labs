# Лабораторная работа №7
## Установка зависимостей
```bash
pip install -e ".[dev]"
```
## Задание A - Тесты для text.py
### Исходный код:
```python
import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.lib.text import normalize, tokenize, count_freq, top_n  # type: ignore


@pytest.mark.parametrize(
    "source, expected",
    [
        ("ПрИвЕт\nМИр\t", "привет мир"),  # обычный текст + спецсимволы
        ("ёжик, Ёлка", "ежик, елка"),  # буквы с разным регистром
        ("Hello\r\nWorld", "hello world"),  # английский текст
        ("  двойные   пробелы  ", "двойные пробелы"),  # лишние пробелы
        ("", ""),  # пустая строка
        ("\t\n   ", ""),  # только пробельные символы
    ],
)
def test_normalize(source, expected):
    assert normalize(source) == expected


@pytest.mark.parametrize(
    "source, expected",
    [
        (
            "привет мир, привет-привет!",
            ["привет", "мир", "привет-привет"],
        ),  
        ("один, два, три!", ["один", "два", "три"]),  
        ("", []),  # пустая строка
        ("   много   пробелов   ", ["много", "пробелов"]),  # повторяющиеся пробелы
        ("слово слово слово", ["слово", "слово", "слово"]),  # повторяющиеся слова
    ],
)
def test_tokenize(source, expected):
    assert tokenize(source) == expected


@pytest.mark.parametrize(
    "tokens, expected",
    [
        (["a", "b", "a", "c", "b", "a"], {"a": 3, "b": 2, "c": 1}),
        ([], {}),
    ],
)
def test_count_freq(tokens, expected):
    assert count_freq(tokens) == expected


@pytest.mark.parametrize(
    "freq_dict, expected",
    [
        ({"a": 3, "b": 2, "c": 1}, [("a", 3), ("b", 2), ("c", 1)]),  
        (
            {
                "яблоко": 2,
                "апельсин": 2,
                "банан": 2,
            },  
            [("апельсин", 2), ("банан", 2), ("яблоко", 2)],
        ),
        ({}, []),  # пустой словарь
        (
            {
                "a": 5,
                "b": 4,
                "c": 3,
                "d": 2,
                "e": 1,
                "f": 1,
            },  # больше 5 элементов при n=5
            [("a", 5), ("b", 4), ("c", 3), ("d", 2), ("e", 1)],
        ),
    ],
)
def test_top_n(freq_dict, expected):
    assert top_n(freq_dict) == expected

```

### Тесты для ```text.py```

```bash
py -m pytest tests/test_text.py -v
```

**Тестируемые функции:**
* normalize() - нормализация текста
* tokenize() - токенизация текста
* count_freq() - подсчет частот слов
* top_n() - топ-N частых слов

**Вывод консоли:**

![1](/images/lab07/test_text.png)

## Задание B - Тесты для json_csv.py
### Исходный код:
```python
import json
import csv
import pytest
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.lib.json_csv import json_to_csv, csv_to_json  # type:ignore


def test_json_to_csv_roundtrip(
    tmp_path: Path,
) -> None:  # Успешная конвертация JSON to CSV
    src = tmp_path / "people.json"
    dst = tmp_path / "people.csv"

    data = [
        {"name": "Alice", "age": 22},
        {"name": "Bob", "age": 25},
    ]

    src.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    json_to_csv(str(src), str(dst))

    with dst.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 2
    assert rows[0]["name"] == "Alice"
    assert rows[1]["age"] == "25"


def test_csv_to_json_roundtrip(tmp_path: Path):  # Успешная конвертация CSV to JSON
    src = tmp_path / "people.csv"
    dst = tmp_path / "people.json"

    with src.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerow({"name": "Alice", "age": "22"})
        writer.writerow({"name": "Bob", "age": "25"})

    csv_to_json(str(src), str(dst))

    data = json.loads(dst.read_text(encoding="utf-8"))

    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == "25"


def test_json_to_csv_invalid_json(
    tmp_path: Path,
):  # Входной файл "сломан"/не является корректным файлом JSON
    src = tmp_path / "broken.json"
    dst = tmp_path / "output.csv"
    src.write_text("not a json", encoding="utf-8")

    with pytest.raises(ValueError):
        json_to_csv(str(src), str(dst))


def test_csv_to_json_invalid_csv(
    tmp_path: Path,
):  # Входной файл "сломан"/не является корректным файлом CSV
    src = tmp_path / "broken.csv"
    dst = tmp_path / "output.json"
    src.write_text("Это не таблица", encoding="utf-8")

    try:
        csv_to_json(str(src), str(dst))
        print("Функция выполнилась БЕЗ ошибок")
        print(f"Создан файл: {dst.exists()}")
        if dst.exists():
            print(f"Содержимое: {dst.read_text()}")
    except Exception as e:
        print(f"Ошибка: {type(e).__name__}: {e}")

    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))


def test_missing_file():  # Входного файла не существует
    with pytest.raises(FileNotFoundError):
        json_to_csv("no_such_file.json", "output.csv")


def test_invalid_suffix_to_json(tmp_path: Path):  # Входной файл не CSV
    src = tmp_path / "input.txt"
    dst = tmp_path / "output.json"
    src.write_text("This is 100% json, trust me", encoding="utf-8")
    with pytest.raises(ValueError):
        csv_to_json(str(src), str(dst))
```
### Тесты для ```json_csv.py```

```bash
py -m pytest tests/test_json_csv.py -v
```

**Тестируемые функции:**
* json_to_csv() - конвертация JSON в CSV
* csv_to_json() - конвертация CSV в JSON


**Вывод консоли:**

![1](/images/lab07/test_json_csv.png)

## Задание C - Проверка стиля кода
### Команды:
```bash
py -m black .
py -m black --check .
```
**Вывод консоли:**

![1](/images/lab07/black.png)

## Вывод
В ходе лабораторной работы выполнена настройка инфраструктуры тестирования: написаны модульные тесты для функций обработки текста и конвертации данных, внедрен инструмент автоматического форматирования black. Проект имеет четкую модульную структуру, соответствующую стандартам