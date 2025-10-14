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