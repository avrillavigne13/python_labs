import re

def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if text is None:
        raise ValueError
    if not isinstance(text, str):
        raise TypeError
    if len(text) == 0:
        return ""

    if casefold == True:
        text = text.casefold()

    if yo2e == True:
        text = text.replace('ё', 'е')
        text = text.replace('Ё', 'Е')
        text = text.replace('\t', ' ')
        text = text.replace('\r', ' ')
        text = text.replace('\n', ' ')
    text = ' '.join(text.split())
    text = text.strip()
    return text

def tokenize(text: str) -> list[str]:
    trash = r'\w+(?:-\w+)*'
    token = re.findall(trash, text)
    return token

def count_freq(tokens: list[str]) -> dict[str, int]:
    if not tokens:
        return {}
    freq_dict = {}
    for token in tokens:
        freq_dict[token] = freq_dict.get(token, 0) + 1
    return freq_dict

def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    if not freq:
        return []
    items = list(freq.items())
    items.sort(key=lambda x: x[0])          
    items.sort(key=lambda x: x[1], reverse=True)
    return items[:n]



print(normalize("ПрИвЕт\nМИр\t"))
print(normalize("ёжик, Ёлка")) 
print(normalize("Hello\r\nWorld"))
print(normalize("  двойные   пробелы  "))

print(tokenize("привет мир" ))
print(tokenize("hello,world!!!"))
print(tokenize("по-настоящему круто"))
print(tokenize("2025 год" ))
print(tokenize("emoji 😀 не слово" ))

print(count_freq(["a","b","a","c","b","a"]))
print(count_freq(["bb", "aa", "bb", "aa", "cc"]))

freq0 = {"a": 3, "b": 2, "c": 1}
print(top_n(freq0, 2))
freq1 = {"bb": 2, "aa": 2, "cc": 1}
print(top_n(freq1, 2))


    
    
    

    
    

    