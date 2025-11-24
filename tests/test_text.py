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
        ),  # обычный текст
        ("один, два, три!", ["один", "два", "три"]),  # спецсимволы и знаки препинания
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
        ({"a": 3, "b": 2, "c": 1}, [("a", 3), ("b", 2), ("c", 1)]),  # обычный случай
        (
            {
                "яблоко": 2,
                "апельсин": 2,
                "банан": 2,
            },  # одинаковые частоты → сортировка по алфавиту
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
