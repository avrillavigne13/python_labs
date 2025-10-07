def format_record(rec: tuple[str, str, float]):
    fio, group, gpa = rec
    if not isinstance(fio, str) or not fio.strip():
        raise ValueError("ФИО не должно быть пустой строкой.")
    if not isinstance(group, str) or not group.strip():
        raise ValueError("Группа не должна быть пустой строкой.")
    if not isinstance(gpa, (int, float)):
        raise ValueError("GPA должно быть числом.")
    parts = fio.strip().split()
    surname = parts[0]
    surname=(surname.title())
    initials = ""
    for part in parts[1:]:
        initials += part[0].upper() + "."
    if not initials:
        initials = ""
    form_gpa=f"{gpa:.2f}"
    return f"{surname} {initials}, гр. {group}, GPA {form_gpa}"
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))
print(format_record((34141, "BIVT-25", 4.6)))
