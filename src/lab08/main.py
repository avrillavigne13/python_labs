import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from lab08.serialize import students_from_json, students_to_json
from lab08.models import Student

def main():
    students = students_from_json("data/lab08/students_input.json")
    for s in students:
        print(s)

    students_to_json(students, "data/lab08/students_output.json")

if __name__ == "__main__":
    main()