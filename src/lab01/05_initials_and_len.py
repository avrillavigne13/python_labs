
full_name = input("ФИО: ")
format_name = ' '.join(full_name.strip().split())
name_parts = format_name.split()

initials_list = [part[0].upper() for part in name_parts]

initials = ''.join(initials_list)

print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(format_name)}")
