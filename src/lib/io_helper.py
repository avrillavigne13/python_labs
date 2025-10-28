from csv import writer
from pathlib import Path
from pathlib import Path
import json
import csv

def read_text(path: str, encoding: str = "utf-8") -> str:
    return Path(path).read_text(encoding=encoding)

def write_csv(rows: list, path: str, header: tuple = None) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, 'w', newline='', encoding='utf-8') as f:
        w = writer(f)
        if header:
            w.writerow(header)
        w.writerows(rows)

def get_file_extension(file_path: str) -> str:
    return Path(file_path).suffix.lower()