import re
import sys
import webbrowser
from random import randint
from time import *
import platform
import json
from tkinter import *
import requests
import subprocess
import psutil
import pywinusb.hid as hid
import tkinter as tk 
from tkinter import Tk, Button, filedialog, Frame
import shutil
from PIL import Image
from datetime import datetime
import os
import importlib.util
from pathlib import Path
user = 'user1'
size = os.get_terminal_size()
w = size.columns
def list_processes():
    print("Список текущих процессов:")
    print(f"{'PID':<10}{'Имя процесса'}")
    print("-" * 30)
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            print(f"{proc.info['pid']:<10}{proc.info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            # Если процесс исчез или доступ запрещён, пропускаем его
            continue

def search_processes(keyword):
    print(f"Поиск процессов, содержащих '{keyword}' в имени:")
    print(f"{'PID':<10}{'Имя процесса'}")
    print("-" * 30)
    found = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if keyword.lower() in proc.info['name'].lower():
                print(f"{proc.info['pid']:<10}{proc.info['name']}")
                found = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    if not found:
        print("Процессы не найдены.")

def terminate_process(pid):
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        process.terminate()  # Отправляем сигнал на завершение
        print(f"Процесс '{process_name}' (PID: {pid}) успешно завершён.")
    except psutil.NoSuchProcess:
        print(f"Процесс с PID {pid} не найден.")
    except psutil.AccessDenied:
        print(f"Нет прав для завершения процесса с PID {pid}.")
    except Exception as e:
        print(f"Ошибка при завершении процесса: {e}")

def print_red(text):
    red_color = "\033[38;5;196m" 
    reset_color = "\033[0m"
    print(f"{red_color}{text}{reset_color}")
def list_directory(path="."):
    return os.listdir(path)
context = {}  # Для локальных переменных ($i)
global_vars = {}  # Для глобальных переменных (@x)
now = datetime.now()
current_date = now.strftime("%d.%m.%Y")      
current_time = now.strftime("%H:%M:%S")     
current_weekday = now.strftime("%A")
def find_file(filename, search_path):
    result = {
        "Наличие файла": False,
        "Файл находится в папке": []
    }
    for root, dirs, files in os.walk(search_path):
        if filename in files:
            result["Наличие файла"] = True
            result["Файл находится в папке"].append(root)
    return result
def find_files_by_extension(extension, search_path):
    found_files = []

    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))
    return found_files
def find_file_case_insensitive(filename, search_path):
    result = {
        "Наличие файла": False,
        "Файл находится в папке": []
    }
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if file.lower() == filename.lower():
                result["Наличие файла"] = True
                result["Файл находится в папке"].append(root)
    return result
def find_files_by_pattern(pattern, search_path):
    found_files = []

    regex = re.compile(pattern)
    for root, dirs, files in os.walk(search_path):
        for file in files:
            if regex.match(file):
                found_files.append(os.path.join(root, file))
    return found_files
def find_file_with_depth_limit(filename, search_path, max_depth):
    result = {
        "Наличие файла": False,
        "Файл находится в папке": []
    }
    for root, dirs, files in os.walk(search_path):
        depth = root[len(search_path) + len(os.path.sep):].count(os.path.sep)
        if depth > max_depth:
            del dirs[:]  # Прекратить обход поддиректорий
            continue
        if filename in files:
            result["Наличие файла"] = True
            result["Файл находится в папке"].append(root)
    return result
def list_files_in_folder(folder_path):
    try:
        items = os.listdir(folder_path)
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]
        if files:
            print('Наличие папки: True')
            print("Файлы в папке:")
            for file in files:
                print('-', file)
        else:
            print('Наличие папки: True')
            print("В папке нет файлов.")
    except FileNotFoundError:
        print(f"Наличие папки: False")
        print('Папка не найдена')
    except Exception as e:
        print(f"Произошла ошибка: {e}")
def main_menu():
    print("=" * len('>>> 4   - Поиск файлов по регулярному выражению'))
    print(">>> 1   - Поиск файла по имени")
    print(">>> 2   - Поиск файлов по расширению")
    print(">>> 3   - Поиск файла без учета регистра")
    print(">>> 4   - Поиск файлов по регулярному выражению")
    print(">>> 5   - Поиск файла с ограничением глубины")
    print(">>> 6   - Поиск папки по имени")
    print(">>> ex  - Выход")
    print("=" * len('>>> 4   - Поиск файлов по регулярному выражению'))
def file_finder():
    print('''
.---..-..-.   .---. .---..-..-..-..--. .---..---. 
| |- | || |__ | |-  | |- | || .` || \ || |- | |-< 
`-'  `-'`----'`---' `-'  `-'`-'`-'`-'-'`---'`-'`-' ''')
    while True:
        main_menu()
        choice = input("FILEFINDER> ")
        if choice == "1":
            # Поиск файла по имени
            file_to_find = input("Введите имя файла: ")
            path_to_search = input("Введите путь для поиска (например, '.'): ")
            result = find_file(file_to_find, path_to_search)
            print(f"Наличие файла: {result['Наличие файла']}")
            if result["Наличие файла"]:
                print("Файл находится в папке:")
                for folder in result["Файл находится в папке"]:
                    print(f"- {folder}")
            else:
                print("Файл не найден.")
        elif choice == "2":
            # Поиск файлов по расширению
            extension_to_find = input("Введите расширение файла (например, '.txt'): ")
            path_to_search = input("Введите путь для поиска (например, '.'): ")
            found_files = find_files_by_extension(extension_to_find, path_to_search)
            if found_files:
                print(f"Найдены файлы с расширением '{extension_to_find}':")
                for file_path in found_files:
                    print(f"- {file_path}")
            else:
                print(f"Файлы с расширением '{extension_to_find}' не найдены.")

        elif choice == "3":
            # Поиск файла без учета регистра
            file_to_find = input("Введите имя файла: ")
            path_to_search = input("Введите путь для поиска (например, '.'): ")
            result = find_file_case_insensitive(file_to_find, path_to_search)
            print(f"Наличие файла: {result['Наличие файла']}")
            if result["Наличие файла"]:
                print("Файл находится в папке:")
                for folder in result["Файл находится в папке"]:
                    print(f"- {folder}")
            else:
                print("Файл не найден.")
        elif choice == "4":
            # Поиск файлов по регулярному выражению
            pattern_to_find = input("Введите регулярное выражение (например, '^log.*\\.txt$'): ")
            path_to_search = input("Введите путь для поиска (например, '.'): ")
            found_files = find_files_by_pattern(pattern_to_find, path_to_search)
            if found_files:
                print("Найдены файлы, соответствующие шаблону:")
                for file_path in found_files:
                    print(f"- {file_path}")
            else:
                print("Файлы, соответствующие шаблону, не найдены.")
        elif choice == "5":
            # Поиск файла с ограничением глубины
            file_to_find = input("Введите имя файла: ")
            path_to_search = input("Введите путь для поиска (например, '.'): ")
            try:
                max_depth = int(input("Введите максимальную глубину поиска: "))
            except ValueError:
                print("Ошибка: глубина должна быть числом.")
                continue
            result = find_file_with_depth_limit(file_to_find, path_to_search, max_depth)
            print(f"Наличие файла: {result['Наличие файла']}")
            if result["Наличие файла"]:
                print("Файл находится в папке:")
                for folder in result["Файл находится в папке"]:
                    print(f"- {folder}")
            else:
                print("Файл не найден.")
        elif choice == "6":
            folder = input("Введите путь к папке: ")
            list_files_in_folder(folder)
        elif choice == "ex":
            # Выход из программы
            print("Завершение работы программы.")
            break

        else:
            print("Ошибка: неверный выбор. Пожалуйста, выберите число от 1 до 6.")
        print("\n")
def re():
    def read_code_from_file(file_path):
        if not os.path.exists(file_path):
            print(f"Ошибка: файл '{file_path}' не найден.")
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            return code
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
    def extract_dependencies(code):
        dependencies = set()
        # Находим строки с import или from
        for match in re.finditer(r"(?:import|from)\s+(\w+)", code):
            dependencies.add(match.group(1))
        return dependencies

    def check_and_install_module(module_name):
        try:
            __import__(module_name)
            print(f"Модуль '{module_name}' уже установлен.")
        except ImportError:
            print(f"Модуль '{module_name}' не найден. Установка...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
            print(f"Модуль '{module_name}' успешно установлен.")
    def execute_python_code(code):
        global_namespace = {}
        try:
            print("="*20+'Вывод'+'='*20)
            exec(code, global_namespace)
            print("Код выполнен успешно.")
        except Exception as e:
            print(f"\033[38;5;93mПроизошла ошибка при выполнении кода: {e}\033[0m")
        return global_namespace
    def call_function(global_namespace, function_name, *args, **kwargs):
        if function_name in global_namespace:
            func = global_namespace[function_name]
            if callable(func):
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    print(f"\033[38;5;93m0mОшибка при вызове функции '{function_name}': {e}\033[0m")
            else:
                print(f"'{function_name}' существует, но это не функция.")
        else:
            print(f"Функция '{function_name}' не найдена в коде.")
    def list_functions(global_namespace):
                functions = [name for name, obj in global_namespace.items() if callable(obj)]
                return functions
    file_name = f'system/Bite.py'
    code = read_code_from_file(file_name)
    if code is not None:
        global_namespace = execute_python_code(code)
        functions = list_functions(global_namespace)
        if functions:
            function_name = input("Введите имя функции для вызова (или нажмите Enter, чтобы пропустить): ").strip()
            if function_name:
                args_input = input("Введите позиционные аргументы через запятую (например, 1, 'hello'): ").strip()
                kwargs_input = input("Введите именованные аргументы через запятую (например, key1=value1, key2=value2): ").strip()
                args = []
                kwargs = {}
                if args_input:
                    args = [eval(arg.strip()) for arg in args_input.split(",")]
                if kwargs_input:
                    kwargs = dict(arg.split("=") for arg in kwargs_input.split(","))
                    kwargs = {k.strip(): eval(v.strip()) for k, v in kwargs.items()}
                call_function(global_namespace, function_name, *args, **kwargs)
com1 = 'run'
com2 = 'print'
com3 = 'jdi'
com4 = 'openweb'
com6 = 'randint'
com7 = 'box'
com8 = 'append'
com12 = 'find'
com17 = 'aperolfs'
com21 = 'divmod'
com31 = 'kt'
com32 = 'filefinder'
com33 = 'fix_ext'
com34 = 'outfold'
com35 = 'infold'
com37 = 'lf'
com39 = 'lproc'
com40 = 'sproc'
com41 = 'kproc'
com42 = 'rproc'
com45 = 'warehouse'
com46 = 'defcreator'
com47 = 'save'
com48 = 'for'
com49 = 'goat'
com50 = 'dl'
com51 = 'restusr'
com52 = 'webber'
google = 'https://google.ru/search?q='
wiki = 'https://ru.wikipedia.org/wiki/'
def menu():
    os.system('cls')
    print_red('''          ,---,                   ____    _____   _______   ______ 
  _    _,-'    `--,              |  _ \  |_   _| |__   __| |  ____|
 ( `-,'            `\            | |_) |   | |      | |    | |__
  \           ,    o \           |  _ <    | |      | |    |  __|
  /   ,       ;       \          | |_) |  _| |_     | |    | |____ 
 (_,-' \       `, _  ""/         |____/  |_____|    |_|    |______|
        `-,___ =='__,-'
              ````''')
    print('''                                 \033[38;5;196mB\033[0masic \033[38;5;196mI\033[0mnteractive \033[38;5;196mT\033[0merminal \033[38;5;196mE\033[0mnvironment
                                          by \033[38;5;18mJugernaut9000\033[0m''')
    print_red('-'*len('                                 Basic Interactive Terminal Environment'))
    print('\033[38;5;18mDirect link: https://github.com/Jugernaut9000/BITE.git\033[0m')
    print_red(f"Today is:"+' '*(38-len(f'Today is{current_weekday} {current_date} {current_time}'))+f"{current_weekday} {current_date} {current_time}")
    if current_weekday == 'Wednesday':
        print('Its wednesday, my dudes')
    print('Type "goat" to see the list of commands ')
def commands():
    print_red('MiniScript'+'-'*(w-10))
    print(f'>>> {com1}'+" "*(86-len(f'>>> {com1}'))+'- начать')
    print(f'>>> {com2} <текст>                                                                     - печать <текст>')
    print(f'>>> {com2} -jdi <переменная>                                                           - печать <jdi переменная>')
    print(f'>>> {com2} -box <название списка>                                                      - печать <список> c названием <название списка>')
    print(f'>>> {com2} <имя переменной>                                                            - печать <переменная>')
    print(f'>>> {com3} <lk, rk <ключ>, ek, <ключ>, <ключ> <запрос>, <ключ> == <значение переменной>> - работа с переменными как с ключами словаря и сохранением в json файл')
    print(f'>>> {com4} <ссылка>                                                                  - открытие ссылки')
    print(f'>>> {com7} <название списка>                                                             - создать список <название списка>')
    print(f'>>> {com8} <название списка> <элемент>                                                - добавление <элемент> в список <название списка>') 
    print(f'>>> {com47} <имя переменной> <значение переменной>                                       - создать временную переменную со значением <значение переменной>')
    print(f'>>> {com48} <перепенная> in <число или список>                                            - перебор <переменная> в <число или список>')
    print(f'>>> {com12} <слово которое нужно найти> <текст>                                          - найти <слово> в <текст>')
    print(f'>>> {com21} <число1> <число2>                                                          - поделить <число1> на <число2> с остатком')
    print(f'>>> contract if <условие>; <действие1> else; <действие2>                              - при выполнении условия выполняет <действие1> иначе выполняет <действие2>')
    print_red('Utility'+'-'*(w-7))
    print(f'>>> {com17}'+" "*(86-len(f'>>> {com17}'))+'- запуск файловой системы APEROLFs')
    print(f'>>> warehouse                                                                         - запуск программы WareHouse')
    print(f'>>> defcreator                                                                        - запук программы Defcreator')
    print(f'>>> filefinder                                                                        - запуск программы FileFinder')
    print(f'>>> webber                                                                            - запуск программы Webber')
    print_red('Files'+'-'*(w-5))
    print(f'>>> fix_ext <имя файла> <новое расширение>                                            - изменить текущее расширение файла')
    print(f'>>> outfold <путь к файлу>                                                            - вытащить файл из папки в которой он находится')
    print(f'>>> infold <путь к файлу> <путь к папке>                                              - добавить файл в папку')
    print(f'>>> {com37}                                                                                - дерево файлов')
    print(f'>>> dl <ссылка> <имя>                                                                 - скачать файл по ссылке и сохранить его под именем <имя>')
    print(f'>>> run_def <имя файла>                                                               - запуск .py файла с подробной работой с функциями')
    print_red('Os'+'-'*(w-2))
    print(f'>>> {com2} -components'+" "*(86-len(f'>>> {com2} -components'))+'- печать компонентов компьютера')
    print(f'>>> {com2} -usb'+" "*(86-len(f'>>> {com2} -usb'))+'- печать всех подключенных usb устройств ')
    print(f'>>> kt                                                                                - полная очистка терминала')
    print(f'>>> restusr <имя пользователя>                                                        - изменить пользователя')
    print(f'>>> goat                                                                              - список всех команд BiteOs')
    print(f'>>> re                                                                                - перезапуск программы')
    print(f'>>> saveses <имя сессии>                                                              - сохранить текущую сессию')
    print(f'>>> backup <имя сессии>                                                               - вернуть сессию')
    print(f'>>> lproc                                                                             - список всех процессов')
    print(f'>>> sproc <имя процесса / имя процесса>                                               - поиск процесса по PID или имени процесса')
    print(f'>>> kproc <PID процесса>                                                              - завершить просцесс')
    print(f'>>> rproc <название процесса>                                                         - запуск процесса <название процесса>')
def run_script():
    sentences = []
    stop_word = com1
    r = 0
    commands_path = Path(f"system/users/{user}/commands")
    commands_path.mkdir(parents=True, exist_ok=True)
    while True:
        sentence = input(f"\033[2mln:{r}\033[0m \033[38;5;196m{user}\033[38;5;196m@BITE> \033[0m")
        words = sentence.split()
        if sentence.lower() == stop_word:
            break
        elif sentence.lower() == 'goat':
            commands()
        elif sentence.lower() == 'kt':
            os.system('cls')
        elif sentence.lower() == 're':
            re()
        sentences.append(sentence)
        r += 1
    idx = 0
    for sentence in sentences:
        
        words = sentence.split() 
        if not sentence:
            idx += 1
            continue
        words = sentence.split()
        if not words:
            idx += 1
            continue
        command = words[0]
        if sentence == '':
            pass
        elif words and words[0].lower() == com17:
            print('\x1b[38;5;18m                             ,¿aaa¿,,\033[0m')
            print('\033[38;5;18m                             ▓▓▓▓▓▓▒▒\033[0m')
            print('\033[38;5;18m                             ▒▓▓▓▓▓▓▒\033[0m')
            print('\033[38;5;18m                             ▒▓▓▓▓▓▓▒\033[0m')
            print('\033[38;5;18m                             ▒▓▓▓▓▓██\033[0m')
            print('\033[38;5;18m                             ▒▓▓▓▓▓▓▒\033[0m')
            print('\033[37m                             ,,   ,;;\033[0m')
            print('\033[38;5;196m                            ]▒▒▒▒▒▒▒▒[\033[0m')
            print('\033[38;5;196m                            ╠▒▒▒▒▒▒▒▒▒\033[0m')
            print('\033[38;5;196m                            ║▒▒▒▒▒▒▒▒░\033[0m')
            print('\033[38;5;196m                            ▐▒▒▒▒▒▒▒▒Ç\033[0m')
            print('\033[38;5;196m                          ,@▒▒▒▒▒▒▒▒░░▒\033[0m')
            print('\033[38;5;196m                         @▒▒▒▒▒▒▒▒▒▒▒░;░N\033[0m')
            print('\033[38;5;196m                        ▐░▒▒▒▒▒▒▒▒▒▒▒▒▒▒░[\033[0m')
            print('\033[38;5;196m                        ▐░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░\033[0m')
            print('\033[38;5;196m                        ]░▒▒▒▒▒▒▒▒▒▒▒▒▒\033[38;5;18m▓█Γ\033[0m')
            print('\033[38;5;18m                        j▒▓▓▓██▓▓▓▒▓▒▓▒▓▓C\033[0m')
            print('\033[38;5;18m                        ▓▓▒▌▒\033[38;5;226mAPEROL\033[38;5;18m▓▒▒▓▓M\033[0m')
            print('\033[38;5;18m                        ▒▓▓▓▓▒▒█▒▓▓▀\033[38;5;196m▒\033[38;5;196m▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ▒▒▒▒\033[92m║║Ñ░▒▒»░\033[38;5;196m▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ▒▒▒▌▒\033[92m`>^ )╢▐\033[38;5;196m▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ▐░▒▒╢▒\033[92m^ (░▒║\033[38;5;196m▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                         ░▒▒▐▒\033[92m▄╓╓▄░\033[38;5;196m▒▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        j░▒▒▒╗\033[92m▒░░╓╖\033[38;5;196m▒▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ▐░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ╢░▒▓▒▒▒▒▒▒▒▒▒▒▒▒\033[0m')
            print('\033[38;5;196m                        ▒░▒▒▒▒▒▒▒▒▒▒▒▒▒▒W\033[0m')
            print('\033[38;5;196m                       j▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌\033[0m')
            print('\033[38;5;196m                        ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒┘\033[0m')
            print('\033[38;5;196m                             ``╙╙╙╙```\033[0m')
            print_red('''            _____   ______  _____    ____   _       ______    
     /\    |  __ \ |  ____||  __ \  / __ \ | |     |  ____|   
    /  \   | |__) || |__   | |__) || |  | || |     | |__  ___ 
   / /\ \  |  ___/ |  __|  |  _  / | |  | || |     |  __|/ __|
  / ____ \ | |     | |____ | | \ \ | |__| || |____ | |   \__ \\
 /_/    \_\|_|     |______||_|  \_\ \____/ |______||_|   |___/''')
            print('\033[38;5;196mA\033[0mdvanced \033[38;5;196mP\033[0merformance & \033[38;5;196mE\033[0mfficient \033[38;5;196mR\033[0mesource \033[38;5;196mO\033[0mrganization \033[38;5;196mL\033[0mayer \033[38;5;196mF\033[0mile \033[38;5;196ms\033[0mystem')
            class TextFileSystem:
                def __init__(self, base_dir=f"system/users/{user}/text_files"):
                    self.base_dir = base_dir
                    if not os.path.exists(self.base_dir):
                        os.makedirs(self.base_dir)
                def _get_filepath(self, filename):
                    return os.path.join(self.base_dir, filename)
                def create_file(self, filename, content=""):
                    filepath = self._get_filepath(filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Файл '{filename}' создан.")
                def read_file(self, filename):
                    filepath = self._get_filepath(filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            return f.read()
                    except FileNotFoundError:
                        print(f"Файл '{filename}' не найден.")
                        return None
                def write_file(self, filename, content):
                    filepath = self._get_filepath(filename)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Файл '{filename}' обновлён.")
                def append_to_file(self, filename, content):
                    filepath = self._get_filepath(filename)
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write(content)
                    print(f"Текст добавлен в файл '{filename}'.")
                def delete_file(self, filename):
                    filepath = self._get_filepath(filename)
                    try:
                        os.remove(filepath)
                        print(f"Файл '{filename}' удалён.")
                    except FileNotFoundError:
                        print(f"Файл '{filename}' не найден.")
                def list_files(self):
                    files = os.listdir(self.base_dir)
                    if files:
                        print("Файлы в системе:")
                        for file in files:
                            print(f">>> {file}")
                    else:
                        print("Нет созданных файлов.")
                    return files
                def rename_file(self, old_name, new_name):
                    old_path = self._get_filepath(old_name)
                    new_path = self._get_filepath(new_name)
                    try:
                        os.rename(old_path, new_path)
                        print(f"Файл '{old_name}' переименован в '{new_name}'.")
                    except FileNotFoundError:
                        print(f"Файл '{old_name}' не найден.")

                def file_exists(self, filename):
                    """Проверяет, существует ли файл."""
                    filepath = self._get_filepath(filename)
                    return os.path.isfile(filepath)

                def count_lines(self, filename):
                    """Считает количество строк в файле."""
                    filepath = self._get_filepath(filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            return sum(1 for line in f)
                    except FileNotFoundError:
                        print(f"Файл '{filename}' не найден.")
                        return 0

                def clear_file(self, filename):
                    filepath = self._get_filepath(filename)
                    try:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.truncate()
                        print(f"Файл '{filename}' очищен.")
                    except FileNotFoundError:
                        print(f"Файл '{filename}' не найден.")
                def input_text_until_done(self):
                    print("Введите текст (окончание ввода — строка 'done'):")
                    lines = []
                    while True:
                        line = input("")
                        if line.strip().lower() == "done":
                            break
                        lines.append(line)
                    return "\n".join(lines)
            def filesys():
                fs = TextFileSystem()
                print_red('='*len('>>> write <имя>                     - записать в файл (полностью перезапишет содержимое)'))
                print(">>> create <имя>                    - создать файл")
                print(">>> read <имя>                      - прочитать файл")
                print(">>> write <имя>                     - записать в файл (полностью перезапишет содержимое)")
                print(">>> append <имя>                    - добавить текст в конец файла")
                print(">>> delete <имя>                    - удалить файл")
                print(">>> lf                              - показать список файлов")
                print(">>> rename <старое имя> <новое имя> - переименовать файл")
                print(">>> exists <имя>                    - проверить существование файла")
                print(">>> count <имя>                     - посчитать строки в файле")
                print(">>> clear <имя>                     - очистить файл")
                print(">>> ex                              - выйти")
                print_red('='*len('>>> write <имя>                     - записать в файл (полностью перезапишет содержимое)'))
                while True:
                    command = input(f"\033[38;5;196m({user})APEROLFs> \033[0m").strip().split()
                    if not command:
                        continue
                    if command[0] == "ex":
                        print("Выход из системы.")
                        break
                    elif command[0] == "lf":
                        fs.list_files()
                    elif command[0] == "create" and len(command) == 2:
                        fs.create_file(command[1])
                    elif command[0] == "read" and len(command) == 2:
                        content = fs.read_file(command[1])
                        if content is not None:
                            print(f"\nСодержимое '{command[1]}':\n{content}")
                    elif command[0] == "write" and len(command) == 2:
                        text = fs.input_text_until_done()
                        fs.write_file(command[1], text)
                    elif command[0] == "append" and len(command) == 2:
                        text = fs.input_text_until_done()
                        fs.append_to_file(command[1], text)
                    elif command[0] == "delete" and len(command) == 2:
                        fs.delete_file(command[1])
                    elif command[0] == "rename" and len(command) == 3:
                        fs.rename_file(command[1], command[2])
                    elif command[0] == "exists" and len(command) == 2:
                        exists = fs.file_exists(command[1])
                        print(f"Наличие файла'{command[1]}':{'\033[38;5;196m True' if exists else '\033[38;5;93m False'}")
                    elif command[0] == "count" and len(command) == 2:
                        lines = fs.count_lines(command[1])
                        print(f"Количество строк в '{command[1]}': {lines}")
                    elif command[0] == "clear" and len(command) == 2:
                        fs.clear_file(command[1])
                    else:
                        print("\033[38;5;93mНеизвестная команда или неверное количество аргументов.\033[0m")
            filesys()
        elif words and words[0].lower() == com12:
            sentence = str(words[2:])
            index = sentence.find(words[1])
            print(index)
        elif words and words[0].lower() == com21:
            num1 = int(words[1])
            num2 = int(words[2])
            quot, rem = divmod(num1, num2)
            print(quot, rem)
        elif words and words[0].lower() == com31:
            pass
        elif words and words[0].lower() == com32:   
            file_finder() 
        elif words and words[0].lower() == com33:
            def change_file_extension():
                file_path = words[1]
                if not os.path.isfile(file_path):
                    print("\033[38;5;93mФайл не найден!")
                    return
                new_extension = words[2]
                if not new_extension.startswith('.'):
                    new_extension = '.' + new_extension  # Добавляем точку, если её нет
                base_name, old_extension = os.path.splitext(file_path)
                new_file_path = base_name + new_extension
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Файл успешно переименован! Теперь его имя >>> {new_file_path}")
                except Exception as e:
                    print(f"\033[38;5;93mОшибка при переименовании файла: {e}\033[0m")
            change_file_extension() 
        elif words and words[0].lower() == com34:
            def move_file_out_of_folder():
                file_path = words[1]
                absolute_file_path = os.path.abspath(file_path)
                if not os.path.isfile(absolute_file_path):
                    print("\033[38;5;93mФайл не найден!")
                    return
                folder_path = os.path.dirname(absolute_file_path)
                file_name = os.path.basename(absolute_file_path)
                new_file_path = os.path.join(os.path.dirname(folder_path), file_name)
                try:
                    shutil.move(absolute_file_path, new_file_path)
                    print(f"Файл успешно перемещен! Теперь его путь >>> {new_file_path}")
                except Exception as e:
                    print(f"\033[38;5;93mОшибка при перемещении файла: {e}\033[0m")
            move_file_out_of_folder()
        elif words and words[0].lower() == com35:
            def add_file_to_folder():
                file_path = '.'+words[1]
                folder_path = '.'+words[2]
                absolute_file_path = os.path.abspath(file_path)
                absolute_folder_path = os.path.abspath(folder_path)
                new_file_path = os.path.join(absolute_folder_path, os.path.basename(file_path))
                if os.path.isfile(absolute_file_path):
                    try:
                        shutil.move(absolute_file_path, new_file_path)
                        print(f"Файл успешно перемещен в папку! Теперь его путь >>> {new_file_path}")
                    except Exception as e:
                        print(f"\033[38;5;93mОшибка при перемещении файла: {e}\033[0m")
                else:
                    try:
                        os.makedirs(absolute_folder_path, exist_ok=True)
                        with open(new_file_path, 'w') as new_file:
                            new_file.write("")
                        print(f"Файл успешно создан в папке! Теперь его путь >>> {new_file_path}")
                    except Exception as e:
                        print(f"\033[38;5;93mОшибка при создании файла: {e}\033[0m")
            add_file_to_folder()
        elif words and words[0].lower() == com37:
            IGNORED_ITEMS = {
                ""
            }

            def format_size(size):
                """Форматирует размер файла"""
                for unit in ['Б', 'КБ', 'МБ', 'ГБ']:
                    if size < 1024:
                        return f"{size:.2f} {unit}".replace(".00", "")
                    size /= 1024
                return "0 Б"

            def print_directory_tree(start_path=".", prefix=""):
                """Рекурсивно выводит дерево проекта с фильтрацией"""
                start_path = Path(start_path)
                try:
                    entries = sorted(
                        [e for e in start_path.iterdir() if e.name not in IGNORED_ITEMS],
                        key=lambda x: (not x.is_dir(), x.name)
                    )
                except PermissionError:
                    return

                for i, path in enumerate(entries):
                    is_last = i == len(entries) - 1
                    connector = " └─> " if is_last else " ├─> "
                    current_prefix = prefix + ("    " if is_last else " │   ")

                    if path.is_dir():
                        print(f"{prefix}{connector} {path.name}/")
                        if not any(e for e in path.iterdir() if e.name not in IGNORED_ITEMS):
                            print(f"{current_prefix}   Папка пуста.")
                        else:
                            print_directory_tree(path, current_prefix)
                    else:
                        try:
                            size = format_size(path.stat().st_size)
                            print(f"{prefix}{connector} {path.name} ({size})")
                        except FileNotFoundError:
                            pass
            print('./')
            print_directory_tree()
        elif words and words[0].lower() == com39:
            list_processes()
        elif words and words[0].lower() == com40:
            keyword = words[1]
            if keyword:
                search_processes(keyword)
            else:
                print("Пустой запрос. Попробуйте снова.")
        elif words and words[0] == com41:
            try:
                pid = int(words[1])
                terminate_process(pid)
            except ValueError:
                print("\033[38;5;93mНекорректный PID. Введите число.\033[0m")
        elif words and words[0].lower() == com42:
            def open_application_and_show_pid(app_name):
                try:
                    # Запускаем приложение
                    if os.name == "nt":  # Windows
                        os.startfile(app_name)  # Запускаем файл/приложение
                    else:  # Linux/MacOS
                        os.system(f"xdg-open {app_name}" if os.uname().sysname != "Darwin" else f"open {app_name}")
                    
                    # Ищем процесс по имени приложения
                    found = False
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            if proc.info['name'].lower() in app_name.lower():
                                print(f"Приложение '{app_name}' успешно запущено.")
                                print(f"PID процесса: {proc.info['pid']}")
                                found = True
                                break
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                            continue
                    
                    if not found:
                        print(f"Не удалось найти PID для приложения '{app_name}'.\033[0m")
                
                except FileNotFoundError:
                    print(f"\033[38;5;93mОшибка: приложение '{app_name}' не найдено. Убедитесь, что путь указан правильно.\033[0m")
                except PermissionError:
                    print(f"\033[38;5;93mОшибка: недостаточно прав для запуска приложения '{app_name}'.")
                except Exception as e:
                    print(f"\033[38;5;93mПроизошла ошибка: {e}\033[0m")
            app_name = input("Введите имя или путь к приложению: ").strip()
            if app_name:
                open_application_and_show_pid(app_name)
            else:
                print("Имя приложения не может быть пустым.")
        elif words and words[0] == com45:
            
            # Путь к файлу для сохранения данных
            DATA_FILE = f"system/users/{user}/data_store.json"

            # Загрузка словаря из файла (если файл существует)
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data_store = json.load(file)
            else:
                data_store = {}
            def print_all_lists():
                """
                Выводит все списки из словаря data_store.
                Если файл данных не существует или словарь пуст, выводится соответствующее сообщение.
                """
                # Проверяем, существует ли файл
                if not os.path.exists(DATA_FILE):
                    print("Файл данных не найден. Нет сохраненных списков.")
                    return

                # Загружаем данные из файла
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    try:
                        data_store = json.load(file)
                    except json.JSONDecodeError:
                        print("Ошибка чтения файла данных. Файл поврежден или пуст.")
                        return

                # Проверяем, есть ли списки в словаре
                if not data_store:
                    print("Словарь пуст. Нет сохраненных списков.")
                    return

                # Выводим все списки
                print("Списки в хранилище:")
                for list_name, list_content in data_store.items():
                    print(f"'{list_name}': {list_content}")
            def load_data():
                if not os.path.exists(DATA_FILE):
                    return {}
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as file:
                        return json.load(file)
                except (json.JSONDecodeError, FileNotFoundError):
                    return {}
            def save_data(data_store):
                """
                Сохраняет словарь data_store в файл.
                """
                with open(DATA_FILE, "w", encoding="utf-8") as file:
                    json.dump(data_store, file, ensure_ascii=False, indent=4)
            def createbox(command):
                try:
                    # Разбиваем команду на части
                    parts = command.split()
                    if len(parts) < 3:
                        print("\033[38;5;93mНеверный формат команды. Пример: createbox 5 box +enumerate\033[0m")
                        return

                    count = int(parts[1])  # Количество списков
                    base_name = parts[2]   # Базовое имя списка
                    mode = parts[3] if len(parts) > 3 else "+enumerate"  # Режим нумерации

                    if count <= 0:
                        print("Количество списков должно быть больше 0.")
                        return

                    # Загружаем текущие данные
                    data_store = load_data()

                    for i in range(1, count + 1):
                        if mode == "+enumerate":
                            # Простая нумерация (1, 2, 3...)
                            list_name = f"{base_name}{i}"
                        elif mode == "+roman":
                            # Римские цифры (I, II, III...)
                            roman_numerals = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
                                            "XI", "XII", "XIII", "XIV", "XV", "XVI", "XVII", "XVIII", "XIX", "XX",
                                            "XXI", "XXII", "XXIII", "XXIV", "XXV", "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
                                            "XXXI", "XXXII", "XXXIII", "XXXIV", "XXXV", "XXXVI", "XXXVII", "XXXVIII", "XXXIX", "XL",
                                            "XLI", "XLII"]
                            list_name = f"{base_name}{roman_numerals[i]}"
                        elif mode == "+letters":
                            # Буквы латинского алфавита (A, B, C...)
                            letter = chr(64 + i)  # Преобразуем число в букву (A=1, B=2, ...)
                            list_name = f"{base_name}{letter}"
                        elif mode == "+random":
                            # Случайный порядок (используем uuid для уникальности)
                            import uuid
                            random_suffix = str(uuid.uuid4())[:8]  # Первые 8 символов UUID
                            list_name = f"{base_name}_{random_suffix}"
                        else:
                            # По умолчанию: простая нумерация
                            list_name = f"{base_name}{i}"

                        # Добавляем список в хранилище
                        data_store[list_name] = []

                    # Сохраняем обновленные данные
                    save_data(data_store)
                    print(f"Создано {count} списков с названием {base_name}.")

                except ValueError:
                    print("Неверный формат числа. Укажите целое число для количества списков.")
                except Exception as e:
                    print(f"Произошла ошибка при создании списков: {e}")
            def delete_list(list_name):
                """
                Удаляет список по имени.
                Пример команды: delete list1
                """
                data_store = load_data()

                if list_name in data_store:
                    del data_store[list_name]
                    save_data(data_store)
                    print(f"Список '{list_name}' удален.")
                else:
                    print(f"Список '{list_name}' не найден.")

            def delete_range(start, end):
                data_store = load_data()

                # Получаем все ключи (имена списков) из словаря
                all_lists = list(data_store.keys())

                # Проверяем, что диапазон корректен
                if start < 1 or end > len(all_lists) or start > end:
                    print("Неверный диапазон. Убедитесь, что индексы находятся в пределах существующих списков.")
                    return

                # Удаляем списки в диапазоне
                deleted_count = 0
                for i in range(start - 1, end):  # Индексация начинается с 0
                    list_name = all_lists[i]
                    del data_store[list_name]
                    deleted_count += 1

                if deleted_count > 0:
                    save_data(data_store)
                    print(f"Все списки с индекса {start} до {end} удалены.")
                else:
                    print("Нет списков для удаления в указанном диапазоне.")
            def process_command(command):
                """
                Обрабатывает команды box, append и print.
                :param command: строка с командой
                """
                # Разделяем команду на слова
                parts = command.split()
                
                if not parts:
                    print("\033[38;5;93mОшибка: пустая команда.\033[0m")
                    return

                # Определяем тип команды
                action = parts[0]

                if action == "box":
                    # Создаем новый список с именем из второго слова
                    if len(parts) < 2:
                        print("\033[38;5;93mОшибка: не указано имя списка.\033[0m")
                        return
                    list_name = parts[1]
                    if list_name in data_store:
                        print(f"Список '{list_name}' уже существует.")
                    else:
                        data_store[list_name] = []
                        print(f"Создан новый список: '{list_name}'.")
                        save_data(data_store)

                elif action == "inbox":
                    # Добавляем элементы в существующий список
                    if len(parts) < 3:
                        print("\033[38;5;93mОшибка: недостаточно аргументов для команды 'append'.\033[0m")
                        return
                    list_name = parts[1]
                    if list_name not in data_store:
                        print(f"\033[38;5;93mОшибка: список '{list_name}' не существует.\033[0m")
                    else:
                        # Все слова после второго добавляем в список
                        content = " ".join(parts[2:])  # Сохраняем как одну строку
                        data_store[list_name].append(content)
                        print(f"Добавлено в список '{list_name}': {content}")
                        save_data(data_store)

                elif action == "print":
                    # Выводим содержимое списка
                    if len(parts) < 3:
                        print("\033[38;5;93mОшибка: неверный формат команды 'print'. Используйте 'print <имя_списка>'.\033[0m")
                        return
                    list_name = parts[1]
                    if list_name not in data_store:
                        print(f"\033[38;5;93mОшибка: список '{list_name}' не существует.\033[0m")
                    else:
                        print(data_store[list_name])
                elif action == 'lb':
                    print_all_lists()
                elif action == 'rangebox':
                    createbox(command)  
                elif action == 'delete':
                    delete_list(parts[1]) 
                elif action == 'delrange':
                    start = int(parts[1])
                    end = int(parts[2])
                    delete_range(start, end)
                else:
                    print(f"Неизвестная команда: '{action}'.")
        
            def gradient_text(text, color_codes):
                result = ""
                for i, char in enumerate(text):
                    color = color_codes[i % len(color_codes)]
                    result += f"\033[38;5;{color}m{char}"
                result += "\033[0m"  # Сброс цвета
                return result


            # Определим градиент: от ярко-оранжевого к темно-коричневому
            gradient_colors = [214, 208, 172, 130, 94]  # от оранжевого к коричневому

            text = '''.-.-.-..---..---. .---..-. .-..----..-..-..---..---.
| | | || | || |-< | |- | |=| || || || || | \ \ | |- 
`-----'`-^-'`-'`-'`---'`-' `-'`----'`----'`---'`---' '''
            text2 = '='
            text3 = f'({user})WAREHOUSE> '
            print(gradient_text(text, gradient_colors))
            print((gradient_text(text2, gradient_colors))*len('>>> rangebox <количество списков> <базовое имя списка> <режим (+enumerate, +roman, +random, +letters)> - создание списков в количестве <количество списков> со структурированием <режим>'))
            print(">>> box <название>                                                                                     - создание списка с названием <название списка>")
            print(">>> inbox <название списка> <содержимое>                                                               - добавление <содержимое> в список <название списка> ")
            print(">>> print <название списка>                                                                            - написать содержимое списка <название списка> ")
            print(">>> lb                                                                                                 - содержимое всех списков")
            print('>>> rangebox <количество списков> <базовое имя списка> <режим (+enumerate, +roman, +random, +letters)> - создание списков в количестве <количество списков> со структурированием <режим>')
            print('>>> delete <название списка>                                                                           - удалить список <название списка>')
            print('>>> delrange <номер 1 списка> <номер 2 списка>                                                         - удалить все списки в диапазоне с <номер 1 списка> до <номер 2 списка>')
            print('>>> ex                                                                                                 - выход')
            print((gradient_text(text2, gradient_colors))*len('>>> rangebox <количество списков> <базовое имя списка> <режим (+enumerate, +roman, +random, +letters)> - создание списков в количестве <количество списков> со структурированием <режим>'))
            while True:
                try:
                    user_input = input(gradient_text(text3, gradient_colors))
                    if user_input == 'ex':
                        print("Выход из Warehouse")
                        break
                    process_command(user_input)
                except KeyboardInterrupt:
                    print("\nВыход из Warehouse")
                    break
        elif words and words[0] == com46:
            COMMANDS_DIR = f"system/users/{user}/commands"
            def save_command(command_name, command_code):
                if not os.path.exists(COMMANDS_DIR):
                    os.makedirs(COMMANDS_DIR)

                file_path = os.path.join(COMMANDS_DIR, f"{command_name}.py")
                try:
                    with open(file_path, "w", encoding="utf-8") as f:  # Явно указываем кодировку UTF-8
                        f.write(f"def {command_name}():\n")
                        for line in command_code.split("\n"):
                            f.write(f"    {line}\n")
                    print(f"Команда '{command_name}' успешно создана.")
                except Exception as e:
                    print(f"Ошибка при сохранении команды: {e}")

            def load_command(command_name):
                file_path = os.path.join(COMMANDS_DIR, f"{command_name}.py")
                if not os.path.exists(file_path):
                    print(f"Команда '{command_name}' не найдена.")
                    return None

                try:
                    # Динамический импорт модуля
                    module_name = f"commands.{command_name}"
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # Проверяем, есть ли функция с таким же именем, как у файла
                    if hasattr(module, command_name):
                        return getattr(module, command_name)
                    else:
                        print(f"Функция '{command_name}' не найдена в файле.")
                        return None
                except Exception as e:
                    print(f"Ошибка при загрузке команды: {e}")
                    return None
            def list_commands():
                if not os.path.exists(COMMANDS_DIR) or not os.listdir(COMMANDS_DIR):
                    print("Нет доступных команд.")
                    return
       
                for filename in os.listdir(COMMANDS_DIR):
                    if filename.endswith(".py"):
                        command_name = filename[:-3]  # Убираем расширение .py
                        print(f"- {command_name}")
    
            
            def createfunc():
                print('''\x1b[38;5;75m.--. .---..---. .---..---. .---..---..---..----..---. 
| \ \| |- | |-  | |  | |-< | |- | | |`| |'| || || |-< 
`-'-'`---'`-'   `---'`-'`-'`---'`-^-' `-' `----'`-'`-' \x1b[0m''')
                print('\x1b[38;5;75m=\x1b[0m'*w)
                print(">>> create <имя функции> - создать")
                print('>>> lс - список команд')
                print('>>> done - закончить писать функцию')
                print('>>> ex - выход')
                print('\x1b[38;5;75m=\x1b[0m'*w)
                while True:
                    try:
                        user_input = input(f"\x1b[38;5;75m({user})DEFCREATOR> \x1b[0m").strip()
                        words = user_input.split()
                        if user_input.lower() in ["ex", "quit"]:
                            print("Выход из программы.")
                            break

                        if words[0] == "create":
                            # Создание новой команды
                            command_name = words[1]
                            if not command_name.isidentifier():
                                print("\033[38;5;93mНекорректное имя команды. Используйте только буквы, цифры и символ '_'.\033[0m")
                                continue

                            print("Введите функционал команды, для завершения введите done, в конце кода вызовите вашу функцию для правильного выполнения кода:")
                            command_code = []
                            while True:
                                try:
                                    line = input()
                                    if line.strip() == "done":
                                        break
                                    command_code.append(line)
                                except UnicodeDecodeError as e:
                                    print(f"\033[38;5;93mОшибка ввода: {e}. Убедитесь, что вы используете корректные символы.\033[0m")
                                    continue
                            save_command(command_name, "\n".join(command_code))

                        elif words[0] == "lc":
                            
                            list_commands()

                        else:
                            # Выполнение существующей команды
                            command_function = load_command(user_input)
                            if command_function:
                                try:
                                    command_function()
                                except Exception as e:
                                    print(f"Ошибка при выполнении команды: {e}")
                    except UnicodeDecodeError as e:
                        print(f"Ошибка кодировки: {e}. Убедитесь, что вводимый текст соответствует UTF-8.")
            createfunc()
        elif words[0] == 'saveses':
            NOTES_FILE = f'system/users/{user}/backups.json'
            def load_backup():
                if os.path.exists(NOTES_FILE):
                    with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                        return json.load(f)
                return {}

            def save_notes(notes):
                with open(NOTES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, ensure_ascii=False, indent=4)

            def backup():
                notes = load_backup()

                key = words[1]

                print("Введите текст, который хотите сохранить:")
                notes[key] = sentences
                save_notes(notes)

                print(f"\nТекст сохранён под ключом '{key}' в файле '{NOTES_FILE}'.")
            backup()
        elif words[0] == 'backup':
            NOTES_FILE = f'system/users/{user}/backups.json'
            def load_backup():
                if os.path.exists(NOTES_FILE):
                    with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                        return json.load(f)
            notes = load_backup()
            key = words[1]
            for i in notes[key]:
                print(i)
        elif words[0] + '.py' in os.listdir(f"system/users/{user}/commands"):
            def read_code_from_file(file_path):
                """
                Читает содержимое файла и возвращает его как строку.
                :param file_path: Путь к файлу с кодом
                :return: Строка с кодом
                """
                if not os.path.exists(file_path):
                    print(f"Ошибка: файл '{file_path}' не найден.")
                    return None

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        code = file.read()
                    return code
                except Exception as e:
                    print(f"Ошибка при чтении файла: {e}")
                    return None

            def extract_dependencies(code):
                """
                Извлекает зависимости (импорты) из Python-кода.
                :param code: Строка с кодом
                :return: Список зависимостей
                """
                dependencies = set()
                # Находим строки с import или from
                for match in re.finditer(r"(?:import|from)\s+(\w+)", code):
                    dependencies.add(match.group(1))
                return dependencies

            def check_and_install_module(module_name):
                """
                Проверяет наличие модуля и устанавливает его, если он отсутствует.
                :param module_name: Название модуля
                """
                try:
                    __import__(module_name)
                    print(f"Модуль '{module_name}' уже установлен.")
                except ImportError:
                    print(f"Модуль '{module_name}' не найден. Установка...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                    print(f"Модуль '{module_name}' успешно установлен.")

            def execute_python_code(code):
                """
                Выполняет Python-код из строки и предоставляет доступ к глобальным переменным.
                :param code: Строка с кодом
                :return: Словарь глобальных переменных
                """
                global_namespace = {}
                try:
                    print("="*20+'Вывод'+'='*20)
                    exec(code, global_namespace)
                    print("Код выполнен успешно.")
                except Exception as e:
                    print(f"\033[38;5;93mПроизошла ошибка при выполнении кода: {e}\033[0m")
                return global_namespace

            def call_function(global_namespace, function_name, *args, **kwargs):
                if function_name in global_namespace:
                    func = global_namespace[function_name]
                    if callable(func):
                        try:
                            result = func(*args, **kwargs)
                        except Exception as e:
                            print(f"\033[38;5;93m0mОшибка при вызове функции '{function_name}': {e}\033[0m")
                    else:
                        print(f"'{function_name}' существует, но это не функция.")
                else:
                    print(f"Функция '{function_name}' не найдена в коде.")
            def list_functions(global_namespace):
                """
                Выводит список доступных функций из глобального пространства имён.
                :param global_namespace: Словарь глобальных переменных
                :return: Список имён функций
                """
                functions = [name for name, obj in global_namespace.items() if callable(obj)]
                return functions
            file_name = f'system/users/{user}/commands/' + words[0] + '.py'
            code = read_code_from_file(file_name)
            if code is not None:
                global_namespace = execute_python_code(code)
                functions = list_functions(global_namespace)
                if functions:
                    function_name = input("Введите имя функции для вызова (или нажмите Enter, чтобы пропустить): ").strip()
                    if function_name:
                        args_input = input("Введите позиционные аргументы через запятую (например, 1, 'hello'): ").strip()
                        kwargs_input = input("Введите именованные аргументы через запятую (например, key1=value1, key2=value2): ").strip()
                        args = []
                        kwargs = {}
                        if args_input:
                            args = [eval(arg.strip()) for arg in args_input.split(",")]
                        if kwargs_input:
                            kwargs = dict(arg.split("=") for arg in kwargs_input.split(","))
                            kwargs = {k.strip(): eval(v.strip()) for k, v in kwargs.items()}
                        call_function(global_namespace, function_name, *args, **kwargs)
        elif words and words[0] == 'run_def':
            def read_code_from_file(file_path):
                if not os.path.exists(file_path):
                    print(f"\033[38;5;93mОшибка: файл '{file_path}' не найден.\033[0m")
                    return None

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        code = file.read()
                    return code
                except Exception as e:
                    print(f"\033[38;5;93mОшибка при чтении файла: {e}\033[0m")
                    return None
            def extract_dependencies(code):
                dependencies = set()
                # Находим строки с import или from
                for match in re.finditer(r"(?:import|from)\s+(\w+)", code):
                    dependencies.add(match.group(1))
                return dependencies

            def check_and_install_module(module_name):
                try:
                    __import__(module_name)
                    print(f"Модуль '{module_name}' уже установлен.")
                except ImportError:
                    print(f"Модуль '{module_name}' не найден. Установка...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                    print(f"Модуль '{module_name}' успешно установлен.")

            def execute_python_code(code):
                global_namespace = {}
                try:
                    print("="*20+'Вывод'+'='*20)
                    exec(code, global_namespace)
                    print("Код выполнен успешно.")
                except Exception as e:
                    print(f"\033[38;5;93mПроизошла ошибка при выполнении кода: {e}\033[0m")
                return global_namespace

            def call_function(global_namespace, function_name, *args, **kwargs):
                if function_name in global_namespace:
                    func = global_namespace[function_name]
                    if callable(func):
                        try:
                            result = func(*args, **kwargs)
                        except Exception as e:
                            print(f"Ошибка при вызове функции '{function_name}': {e}")
                    else:
                        print(f"'{function_name}' существует, но это не функция.")
                else:
                    print(f"Функция '{function_name}' не найдена в коде.")
            def list_functions(global_namespace):
                functions = [name for name, obj in global_namespace.items() if callable(obj)]
                return functions
            file_name = words[1]
            code = read_code_from_file(file_name)
            if code is not None:
                global_namespace = execute_python_code(code)
                functions = list_functions(global_namespace)
                if functions:
                    function_name = input("Введите имя функции для вызова (или нажмите Enter, чтобы пропустить): ").strip()
                    if function_name:
                        args_input = input("Введите позиционные аргументы через запятую (например, 1, 'hello'): ").strip()
                        kwargs_input = input("Введите именованные аргументы через запятую (например, key1=value1, key2=value2): ").strip()
                        args = []
                        kwargs = {}
                        if args_input:
                            args = [eval(arg.strip()) for arg in args_input.split(",")]
                        if kwargs_input:
                            kwargs = dict(arg.split("=") for arg in kwargs_input.split(","))
                            kwargs = {k.strip(): eval(v.strip()) for k, v in kwargs.items()}
                        call_function(global_namespace, function_name, *args, **kwargs)
        elif words and words[0] == com50:
            url = words[1]
            response = requests.get(url)
            file_Path = words[2]
            if response.status_code == 200:
                with open(file_Path, 'wb') as file:
                    file.write(response.content)
                print('Файл успешно скачан')
            else:
                print('\033[38;5;93mНе получилось скачать файл\033[0m')
        elif command == "save" and len(words) >= 3:
            var_name = words[1]
            value_expr = ' '.join(words[2:])
            try:
                # Вычисляем выражение
                value = eval(value_expr, {}, context)
                # Сохраняем в глобальный контекст
                global_vars[var_name] = value
                print(f"[Переменная] @{var_name} = {value}")
            except Exception as e:
                print(f"[Ошибка save]: {e}")
            idx += 1
        elif command == "for":
            if len(words) >= 4 and words[2] == "in":
                var_name = words[1]
                count_or_list = ' '.join(words[3:])
                try:
                    count = int(count_or_list)
                    iterable = range(1, count + 1)
                except ValueError:
                    try:
                        iterable = eval(count_or_list, globals(), context)
                    except Exception as e:
                        print(f"[Ошибка разбора значения]: {e}")
                        idx += 1
                        continue

                idx += 1
                body = []
                while idx < len(sentences) and sentences[idx].startswith("b>"):
                    raw_line = sentences[idx][2:].strip()
                    body.append(raw_line)
                    idx += 1

                for value in iterable:
                    context[var_name] = value
                    for stmt in body:
                        # Подставляем локальную переменную ($i)
                        dynamic_stmt = stmt
                        for var in list(context.keys()):
                            dynamic_stmt = dynamic_stmt.replace(f"${var}", str(context[var]))
                        # Подставляем глобальную переменную (@x)
                        for var in list(global_vars.keys()):
                            dynamic_stmt = dynamic_stmt.replace(f"@{var}", str(global_vars[var]))

                        if dynamic_stmt.startswith("print"):
                            content = dynamic_stmt[len("print"):].strip()
                            try:
                                print(eval(content, {}, {**globals(), **context, **global_vars}))
                            except:
                                print(content)
                        else:
                            try:
                                exec(dynamic_stmt, {}, {**globals(), **context, **global_vars})
                            except Exception as e:
                                print(f"[Ошибка выполнения]: {e}")
            else:
                print('Ошибка синтаксиса')
            idx += 1

        # === print команда ===
        elif words and words[0].lower() == com2:
            def execute_print_command(words):
                output_parts = []

                i = 1
                while i < len(words):
                    word = words[i]

                    # Подстановка глобальной переменной @name
                    if word.startswith('@'):
                        var_name = word[1:]
                        if var_name in global_vars:
                            output_parts.append(str(global_vars[var_name]))
                        else:
                            output_parts.append(f"[Ошибка: Переменная '{var_name}' не найдена]")

                    # Флаг -jdi
                    elif word == '-jdi':
                        DATA_FILE = f"system/users/{user}/data.json"
                        def load_data():
                            if os.path.exists(DATA_FILE):
                                with open(DATA_FILE, "r", encoding="utf-8") as file:
                                    return json.load(file)
                            return {}
                        data = load_data()
                        key = words[i + 1] if i + 1 < len(words) else None
                        if key and key in data:
                            output_parts.append(f"{key}: {data[key]}")
                            i += 1  # Пропускаем ключ
                        else:
                            output_parts.append(f"Ключ '{key}' не найден.")
                            i += 1  # Пропускаем ключ

                    # Флаг -components
                    elif word == '-components':
                        output_parts.append(
                            f"Computer network name: {platform.node()}\n"
                            f"Machine type: {platform.machine()}\n"
                            f"Processor type: {platform.processor()}\n"
                            f"Platform type: {platform.platform()}\n"
                            f"Operating system: {platform.system()}\n"
                            f"OS release: {platform.release()}\n"
                            f"OS version: {platform.version()}"
                        )

                    # Флаг -usb
                    elif word == '-usb':
                        all_devices = hid.HidDeviceFilter().get_devices()
                        if not all_devices:
                            output_parts.append("USB-устройства не найдены.")
                        else:
                            for device in all_devices:
                                output_parts.append(
                                    f"Устройство: {device.product_name}"
                                    f"(Vendor ID: {device.vendor_id}, Product ID: {device.product_id})\n"
                                )

                    # Флаг -box
                    elif word == '-box':
                        DATA_FILE = f"system/users/{user}/data_store.json"
                        if os.path.exists(DATA_FILE):
                            with open(DATA_FILE, "r", encoding="utf-8") as file:
                                data_store = json.load(file)
                        else:
                            data_store = {}

                        if i + 1 < len(words):
                            list_name = words[i + 1]
                            if list_name in data_store:
                                output_parts.append(str(data_store[list_name]))
                            else:
                                output_parts.append(f"Список '{list_name}' не найден.")
                            i += 1
                        else:
                            output_parts.append("[Ошибка] Не указан имя списка после -box")

                    # Флаг -allbox
                    elif word == '-allbox':
                        DATA_FILE = f"system/users/{user}/data_store.json"
                        if os.path.exists(DATA_FILE):
                            with open(DATA_FILE, "r", encoding="utf-8") as file:
                                data_store = json.load(file)
                        else:
                            data_store = {}

                        if not data_store:
                            output_parts.append("Хранилище данных пустое.")
                        else:
                            result = "Все данные в хранилище:\n"
                            for k, v in data_store.items():
                                result += f"{k}: {v}\n"
                            output_parts.append(result.strip())

                    # Проверка на переменную или выражение
                    elif word in global_vars:
                        output_parts.append(str(global_vars[word]))

                    # По умолчанию — добавляем само слово
                    else:
                        output_parts.append(word)

                    i += 1

                full_output = ' '.join(output_parts)
                return full_output
            to_Print = execute_print_command(words)
            print(to_Print)
            idx += 1
        elif command == com3:
            DATA_FILE = f"system/users/{user}/data.json"

            def load_data():
                """Загружает данные из файла, если он существует."""
                if os.path.exists(DATA_FILE):
                    with open(DATA_FILE, "r", encoding="utf-8") as file:
                        return json.load(file)
                return {}

            def save_data(data):
                """Сохраняет данные в файл."""
                with open(DATA_FILE, "w", encoding="utf-8") as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

            def add_or_update_key(data):
                key, question = words[1], words[2:]
                if not key or not question:
                    print("Ключ и вопрос не могут быть пустыми.")
                    return
                value = input(f"{' '.join(question)} ").strip()
                if not value:
                    print("Значение не может быть пустым.")
                    return
                data[key] = value
                save_data(data)
                print(f"Значение '{value}' сохранено для ключа '{key}'.")

            def edit_key(data):
                key = input("Введите ключ для редактирования: ").strip()
                if key in data:
                    question = words[2:]
                    new_value = input(f"{' '.join(question)} ").strip()
                    if not new_value:
                        print("Значение не может быть пустым.")
                        return
                    data[key] = new_value
                    save_data(data)
                    print(f"Значение для ключа '{key}' обновлено на '{new_value}'.")
                else:
                    print(f"Ключ '{key}' не найден.")

            def remove_key(data):
                key = words[2]
                if key in data:
                    del data[key]
                    save_data(data)
                    print(f"Ключ '{key}' удалён.")
                else:
                    print(f"Ключ '{key}' не найден.")

            def list_keys(data):
                if data:
                    for key in data:
                        print(f"- {key}")
                else:
                    print("Словарь пуст.")

            data = load_data()
            choice = words[1]

            if choice == "ek":
                edit_key(data)
            elif choice == "rk":
                remove_key(data)
            elif choice == "lk":
                list_keys(data)
            elif len(words) >= 4 and words[2] == "==":
                data[words[1]] = words[3]
                save_data(data)
                print(f"Ключ '{words[1]}' добавлен.")
            else:
                add_or_update_key(data)

            idx += 1

        # === if условие ===
        elif command == "if":
            condition = ' '.join(words[1:])
            try:
                result = eval(condition, globals(), {**context, **global_vars})
            except Exception as e:
                print(f"[Ошибка условия]: {e}")
                idx += 1
                continue

            idx += 1
            body = []
            while idx < len(sentences) and sentences[idx].startswith("b>"):
                body.append(sentences[idx][2:].strip())
                idx += 1

            if result:
                for stmt in body:
                    formatted_stmt = stmt
                    for var in list(context.keys()):
                        formatted_stmt = formatted_stmt.replace(f"${var}", str(context[var]))
                    try:
                        if formatted_stmt.startswith("print"):
                            content = formatted_stmt[len("print"):].strip()
                            print(eval(content, globals(), {**context, **global_vars}))
                        else:
                            exec(formatted_stmt, {}, {**context, **global_vars})
                    except Exception as e:
                        print(f"[Ошибка выполнения]: {e}")
            else:
                # Пропуск блока
                while idx < len(sentences) and sentences[idx].startswith("b>"):
                    idx += 1
        elif words and words[0].lower() == com4:
            webbrowser.open(words[1])
        elif words and words[0].lower() == com6:
            r1 = int(words[1])
            r2 = int(words[2])
            r = randint(r1, r2)
            words_count = len(words)
            print(r)
        elif words and words[0].lower() == com8:
            DATA_FILE = f"system/users/{user}/data_store.json"
            def save_data(data_store):
                """
                Сохраняет словарь data_store в файл.
                """
                with open(DATA_FILE, "w", encoding="utf-8") as file:
                    json.dump(data_store, file, ensure_ascii=False, indent=4)
            # Загрузка словаря из файла (если файл существует)
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data_store = json.load(file)
            else:
                data_store = {}
            list_name = words[1]
            if list_name not in data_store:
                print(f"\033[38;5;93mОшибка: список '{list_name}' не существует.\033[0m")
            else:
                # Все слова после второго добавляем в список
                content = " ".join(words[2:])  # Сохраняем как одну строку
                data_store[list_name].append(content)
                print(f"Добавлено в список '{list_name}': {content}")
                save_data(data_store)
        elif words and words[0].lower() == com7:
            DATA_FILE = f"system/users/{user}/data_store.json"
            # Загрузка словаря из файла (если файл существует)
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    data_store = json.load(file)
            else:
                data_store = {}
            def save_data():
                """
                Сохраняет словарь data_store в файл.
                """
                with open(DATA_FILE, "w", encoding="utf-8") as file:
                    json.dump(data_store, file, ensure_ascii=False, indent=4)
            # Создаем новый список с именем из второго слова
            list_name = words[1]
            if list_name in data_store:
                print(f"Список '{list_name}' уже существует.")
                break
            else:
                data_store[list_name] = []
                print(f"Создан новый список: '{list_name}'.")
                save_data() 
                break
        elif words[0] == 'b>':
            pass
        elif words[0] == com51:
            # Открываем файл и читаем все строки
            with open('system/Bite.py', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # Меняем нужную строку
            with open('system/Bite.py', 'w', encoding='utf-8') as file:
                for line in lines:
                    if line.startswith('user ='):
                        file.write(f"user = '{words[1]}'\n")
                    else:
                        file.write(line)
            re()
        elif words[0] == 'goat':
            pass
        elif words[0] == com52:
            def read_code_from_file(file_path):
                if not os.path.exists(file_path):
                    print(f"\033[38;5;93mОшибка: файл '{file_path}' не найден.\033[0m")
                    return None

                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        code = file.read()
                    return code
                except Exception as e:
                    print(f"\033[38;5;93mОшибка при чтении файла: {e}\033[0m")
                    return None
            def extract_dependencies(code):
                dependencies = set()
                # Находим строки с import или from
                for match in re.finditer(r"(?:import|from)\s+(\w+)", code):
                    dependencies.add(match.group(1))
                return dependencies

            def check_and_install_module(module_name):
                try:
                    __import__(module_name)
                    print(f"Модуль '{module_name}' уже установлен.")
                except ImportError:
                    print(f"Модуль '{module_name}' не найден. Установка...")
                    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])
                    print(f"Модуль '{module_name}' успешно установлен.")

            def execute_python_code(code):
                global_namespace = {}
                try:
                    exec(code, global_namespace)
                except Exception as e:
                    print(f"\033[38;5;93mПроизошла ошибка при выполнении кода: {e}\033[0m")
                return global_namespace

            def call_function(global_namespace, function_name, *args, **kwargs):
                if function_name in global_namespace:
                    func = global_namespace[function_name]
                    if callable(func):
                        try:
                            result = func(*args, **kwargs)
                        except Exception as e:
                            print(f"Ошибка при вызове функции '{function_name}': {e}")
                    else:
                        print(f"'{function_name}' существует, но это не функция.")
                else:
                    print(f"Функция '{function_name}' не найдена в коде.")
            def list_functions(global_namespace):
                functions = [name for name, obj in global_namespace.items() if callable(obj)]
                return functions
            file_name = 'system/html_builder.py'
            code = read_code_from_file(file_name)
            if code is not None:
                global_namespace = execute_python_code(code)
                functions = list_functions(global_namespace)
                if functions:
                    function_name = 'create_flask_app'
                    if function_name:
                        args_input = ''
                        kwargs_input = ''
                        args = []
                        kwargs = {}
                        if args_input:
                            args = [eval(arg.strip()) for arg in args_input.split(",")]
                        if kwargs_input:
                            kwargs = dict(arg.split("=") for arg in kwargs_input.split(","))
                            kwargs = {k.strip(): eval(v.strip()) for k, v in kwargs.items()}
                        call_function(global_namespace, function_name, *args, **kwargs)
        elif words[0] == 'contract':
            def execute_print_command(words, global_vars, user):
                output_parts = []

                i = 1
                while i < len(words):
                    word = words[i]

                    # Подстановка глобальной переменной @name
                    if word.startswith('@'):
                        var_name = word[1:]
                        if var_name in global_vars:
                            output_parts.append(str(global_vars[var_name]))
                        else:
                            output_parts.append(f"[Ошибка: Переменная '{var_name}' не найдена]")

                    # Флаг -jdi
                    elif word == '-jdi':
                        DATA_FILE = f"system/users/{user}/data.json"
                        def load_data():
                            if os.path.exists(DATA_FILE):
                                with open(DATA_FILE, "r", encoding="utf-8") as file:
                                    return json.load(file)
                            return {}
                        data = load_data()
                        key = words[i + 1] if i + 1 < len(words) else None
                        if key and key in data:
                            output_parts.append(f"{key}: {data[key]}")
                            i += 1  # Пропускаем ключ
                        else:
                            output_parts.append(f"Ключ '{key}' не найден.")
                            i += 1  # Пропускаем ключ

                    # Флаг -components
                    elif word == '-components':
                        output_parts.append(
                            f"Computer network name: {platform.node()}\n"
                            f"Machine type: {platform.machine()}\n"
                            f"Processor type: {platform.processor()}\n"
                            f"Platform type: {platform.platform()}\n"
                            f"Operating system: {platform.system()}\n"
                            f"OS release: {platform.release()}\n"
                            f"OS version: {platform.version()}"
                        )

                    # Флаг -usb
                    elif word == '-usb':
                        all_devices = hid.HidDeviceFilter().get_devices()
                        if not all_devices:
                            output_parts.append("USB-устройства не найдены.")
                        else:
                            for device in all_devices:
                                output_parts.append(
                                    f"Устройство: {device.product_name} "
                                    f"(Vendor ID: {device.vendor_id}, Product ID: {device.product_id})\n"
                                )

                    # Флаг -box
                    elif word == '-box':
                        DATA_FILE = f"system/users/{user}/data_store.json"
                        if os.path.exists(DATA_FILE):
                            with open(DATA_FILE, "r", encoding="utf-8") as file:
                                data_store = json.load(file)
                        else:
                            data_store = {}

                        if i + 1 < len(words):
                            list_name = words[i + 1]
                            if list_name in data_store:
                                output_parts.append(str(data_store[list_name]))
                            else:
                                output_parts.append(f"Список '{list_name}' не найден.")
                            i += 1
                        else:
                            output_parts.append("[Ошибка] Не указано имя списка после -box")

                    # Флаг -allbox
                    elif word == '-allbox':
                        DATA_FILE = f"system/users/{user}/data_store.json"
                        if os.path.exists(DATA_FILE):
                            with open(DATA_FILE, "r", encoding="utf-8") as file:
                                data_store = json.load(file)
                        else:
                            data_store = {}

                        if not data_store:
                            output_parts.append("Хранилище данных пустое.")
                        else:
                            result = "Все данные в хранилище:\n"
                            for k, v in data_store.items():
                                result += f"{k}: {v}\n"
                            output_parts.append(result.strip())

                    # Проверка на переменную или выражение
                    elif word in global_vars:
                        output_parts.append(str(global_vars[word]))

                    # По умолчанию — просто текст
                    else:
                        output_parts.append(word)

                    i += 1

                full_output = ' '.join(output_parts)
                return full_output


            def execute_contract_command(words, global_vars, user):
                """
                Обрабатывает команду contract с поддержкой execute_print_command
                """
                if len(words) < 4 or 'if' not in words:
                    print("[Ошибка] Некорректный формат команды contract.")
                    return

                raw_code = ' '.join(words[1:])

                tokens = []
                current_block = ""
                i = 0
                while i < len(raw_code):
                    char = raw_code[i]

                    if char == ';':
                        if current_block.strip():
                            tokens.append(current_block.strip())
                            current_block = ""
                        i += 1
                    elif raw_code.startswith("else", i):
                        if current_block.strip():
                            tokens.append(current_block.strip())
                            current_block = ""
                        tokens.append("else")
                        i += 4
                    elif raw_code.startswith("if", i):
                        end_pos = raw_code.find(";", i)
                        if end_pos == -1:
                            end_pos = len(raw_code)
                        tokens.append(raw_code[i:end_pos].strip())
                        i = end_pos + 1
                    else:
                        current_block += char
                        i += 1

                if current_block.strip():
                    tokens.append(current_block.strip())

                python_code = []
                indent_level = 0

                for token in tokens:
                    if not token:
                        continue

                    # --- IF ---
                    if token.startswith("if "):
                        condition = token.split(" ", 1)[1]
                        condition = condition.replace("=", "==")
                        python_code.append("    " * indent_level + f"if {condition}:")
                        indent_level = 1

                    # --- ELSE ---
                    elif token == "else":
                        indent_level = 1
                        python_code.append("    " * (indent_level - 1) + "else:")
                        indent_level += 1

                    # --- PRINT ---
                    elif token.startswith("print "):
                        cmd_words = ["print"] + token[len("print"):].strip().split()

                        try:
                            printed_text = execute_print_command(cmd_words, global_vars, user)

                            # Экранируем кавычки и переводы строк
                            safe_text = printed_text.replace('"', '\\"').replace('\n', '\\n')

                            python_code.append("    " * indent_level + f'print("{safe_text}")')
                        except Exception as e:
                            python_code.append("    " * indent_level + f'# Ошибка при выполнении print: {e}')

                    # --- Неизвестная команда ---
                    else:
                        python_code.append("    " * indent_level + f'# [Неизвестная команда]: {token}')

                full_code = '\n'.join(python_code)

                try:
                    exec(full_code, {}, global_vars)
                except Exception as e:
                    print(f"\n Ошибка выполнения: {e}")
            command = sentence
            execute_contract_command(words, global_vars, user)
        else:
            if sentence not in sentences[start_index:end_index]:
                print(f'\033[2mln:{idx}\033[0m\033[38;5;93m ERROR: NO COMMAND "{sentence}" \033[0m')
            idx += 1
    run_script()
menu()
run_script()
