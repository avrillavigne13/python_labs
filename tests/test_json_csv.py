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
        print("✅ Функция выполнилась БЕЗ ошибок")
        print(f"📁 Создан файл: {dst.exists()}")
        if dst.exists():
            print(f"📄 Содержимое: {dst.read_text()}")
    except Exception as e:
        print(f"❌ Ошибка: {type(e).__name__}: {e}")

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
