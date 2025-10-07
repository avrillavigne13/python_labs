# Лабороторная работа 1

## Задание 1

```python
name = input("Имя ")

age = int(input("Возраст "))

print(f"Привет, {name}! Через год тебе будет {age+1}.")
```
![Картинка 1](/images/01_output.png)

## Задание 2

```python
a = float(input("a: ").replace(",", "."))
b = float(input("b: ").replace(",", "."))

sum = a + b
avg = (a + b) / 2

print(f"sum: {sum}; avg: {avg:.2f}")
```
![Картинка 2](/images/02_output.png)

## Задание 3

```python
price = float(input("price: ").replace(",", "."))
discount = float(input("discount: ").replace(",", "."))
vat = float(input("vat: ").replace(",", "."))

base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount

print(f"База после скидки: {base:.2f} ₽")
print(f"НДС:               {vat_amount:.2f} ₽")
print(f"Итого к оплате:    {total:.2f} ₽")
```
![Картинка 3](/images/03_output.png)

## Задание 4

```python
m = int(input("Минуты: "))
h = m//60
rm = m%60

print(f"{h}:{rm:02d}")
```
![Картинка 4](/images/04_output.png)

## Задание 5

```python
full_name = input("ФИО: ")
format_name = ' '.join(full_name.strip().split())
name_parts = format_name.split()

initials_list = [part[0].upper() for part in name_parts]

initials = ''.join(initials_list)

print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(format_name)}")
```
![Картинка 5](/images/05_output.png)

# Вывод

В ходе работы я освоил основы Python (пользовательский ввод, математические операции, обработка строк) и основы работы с GitHub. Навык позволяет создавать консольные приложения для решения практических задач.

# Лабороторная работа 2

## Задание 1

```python
def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError
    minimum = min(nums)
    maximum = max(nums)
    return(minimum, maximum)   


print(min_max([3, -1, 5, 5, 0]))
print(min_max([42]))
print(min_max([]))
print(min_max([1.5, 2, 2.0, -3.1]))
print(min_max([-5, -2, -9]))
```
![Картинка 1](/images/min_max_output.png)

## Задание 2

```python
def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return(sorted(set(nums)))
           
print(unique_sorted([3, 1, 2, 1, 3]))
print(unique_sorted([]))
print(unique_sorted([-1, -1, 0, 2, 2]))
print(unique_sorted([1.0, 1, 2.5, 2.5, 0]))
```
![Картинка 2](/images/unique_sorted_output.png)

## Задание 3

```python
def flatten(mat: list[list | tuple]) -> list:
    result = []
    for row in mat:
        if isinstance(row, (list,tuple)):
            result.extend(row)
        else:
            raise TypeError
    return(result)
    
print(flatten(([1, 2], [3, 4])))
print(flatten(([1, 2], (3, 4, 5))))
print(flatten(([1], [], [2, 3])))
print(flatten([[1, 2], "ab"]))
```
![Картинка 3](/images/flatten_output.png)

## Задание 4

```python
def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    
    rows = len(mat)
    cols = len(mat[0])
    
    for row in mat:
        if len(row) != cols:
            raise ValueError
    
    result = []
    
    for j in range(cols):
        new_row = []
        for i in range(rows):
            new_row.append(mat[i][j])
        result.append(new_row)
    
    return result

print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))
    
```
![Картинка 4](/images/transpose_output.png)

## Задание 5

```python
def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []    
    rows = len(mat)
    cols = len(mat[0])

    for row in mat:
        if len(row) != cols:
            raise ValueError        
    sums = []
    for row in mat:          
        total = sum(row)      
        sums.append(total)    
    return sums
print(row_sums([[1,2,3], [4,5,6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0,0], [0,0]]))
print(row_sums([[1,2], [3]]))
```
![Картинка 5](/images/row_sums_output.png)

## Задание 6

```python
def col_sums(mat: list[list[float | int]]):
    if not mat:
        return []
    
    rows = len(mat)
    cols = len(mat[0])

    for row in mat:
        if len(row) != cols:
            raise ValueError   
 
    sums = []

    for j in range(cols):
        column_sum = 0
        for i in range(rows):
            column_sum += mat[i][j]
        sums.append(column_sum)    
    return sums

print(col_sums([[1, 2, 3], [4, 5, 6]]))  
print(col_sums([[-1, 1], [10, -10]]))    
print(col_sums([[0, 0], [0, 0]]))        
print(col_sums([[1, 2], [3]]))    
```
![Картинка 6](/images/col_sums_output.png)

## Задание 7

```python
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
```
![Картинка 7](/images/tuples_output.png)

# Вывод
Освоил операции с данными, такие как работу с матрицами, поиск минимума и максимума, удаление дубликатов и работу со строками.
