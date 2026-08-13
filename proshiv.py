import os
import shutil

def extract_lines(source_file, target_file, num_lines):
    # Читаем исходный файл
    with open(source_file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    # Разделяем на нужные строки и остаток
    extracted = lines[:num_lines]
    remaining = lines[num_lines:]
    # Записываем первые строки в новый файл
    with open(target_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(extracted)
    # Перезаписываем исходный файл без этих строк
    with open(source_file, 'w', encoding='utf-8', errors='ignore') as f:
        f.writelines(remaining)

def replace_word_file(file_path, old, new):
    """Надёжная замена по всему файлу"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    # Простая и надёжная замена
    new_content = content.replace(old, new)
    with open(file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.write(new_content)

d = int(input("Сколько скриптов: "))
logiin = str(input("логин: ")).strip()
q = sum(1 for line in open('brute.txt', encoding='utf-8', errors='replace'))
v = (q//d)
print(f"Всего: {q}")
print(f"1 словарь: {v}")
idd = 1
shutil.copy2("brute.txt", "brute_backup.txt")
while True:
    with open(f'temp/brute_{idd}.txt', 'w', encoding='utf-8') as f:
        pass
    extract_lines('brute.txt', f'temp/brute_{idd}.txt', v)
    if sum(1 for line in open('brute.txt', encoding='utf-8')) == 0:
        os.remove("brute.txt")
        os.rename("brute_backup.txt", "brute.txt ")
        break
    idd += 1
idd = 1
while True:
    if idd > d:
        break
    else:
        shutil.copy2("obraz.py", f"temp/brute_{idd}.py")
        replace_word_file(f"temp/brute_{idd}.py", "login = 'LOGIN_REG'", f"login = '{logiin}'")
        replace_word_file(f"temp/brute_{idd}.py", "with open('FILE_BRUTE_REG', 'r', encoding='utf-8', errors='replace') as file:", f"with open('brute_{idd}.txt', 'r', encoding='utf-8', errors='replace') as file:")
        idd += 1
print("готово")
