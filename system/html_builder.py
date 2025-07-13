import os
from rich import print as rprint
from rich.prompt import Prompt, IntPrompt
import importlib.util
import sys
com1 = 'newfkapp'
com2 = 'info'
com3 = 'runfkapp'
com4 = 'fkapps'
def run_flask_app(module_name):
    # Путь к файлу, предполагаем, что он в той же директории
    file_path = module_name

    # Динамическая загрузка модуля
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None:
        print(f"Не найден файл {file_path}")
        return

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Проверяем наличие атрибута app
    if not hasattr(module, 'app'):
        print(f"В файле {module_name}.py не найден объект 'app'")
        return

    flask_app = module.app
    flask_app.run(debug=False)
def create_flask_app():
    rprint('''[bold blue]__          __  _     _               
\ \        / / | |   | |              
 \ \  /\  / /__| |__ | |__   ___ _ __ 
  \ \/  \/ / _ \ '_ \| '_ \ / _ \ '__|
   \  /\  /  __/ |_) | |_) |  __/ |   
    \/  \/ \___|_.__/|_.__/ \___|_|   
======================================[/bold blue]''')
    rprint("[red]WARNING: Webber использует localhost, для создания более серьезных проектов используйте WSGI сервер[/red]")
    print('>>> newfkapp <имя .py файла> <имя .html файла> - создать новое flask приложение')
    print('>>> info <имя файла>                           - информация о flask приложении')
    print('>>> runfkapp <имя файла>                       - запустить flask приложение')
    print('>>> fkapps                                     - список flask приложений')
    print('>>> ex                                         - выйти')
    while True:
        sentence = Prompt.ask('[bold blue]WEBBER>[/bold blue] ')
        words = sentence.split() 
        if sentence == '':
            pass
        elif words[0] == com2:
            def show_app_info(filename: str):
                if not filename.endswith(".py"):
                    filename += ".py"
                if not os.path.exists(filename):
                    print(f"Файл '{filename}' не найден.")
                    return

                print(f"\nИнформация о приложении {filename}:\n")

                routes = []
                host = "не указан"
                port = "не указан"

                with open(filename, "r", encoding="utf-8") as f:
                    for line in f:
                        stripped_line = line.strip()

                        # Парсим маршруты @app.route(...)
                        if stripped_line.startswith("@app.route("):
                            if "'" in stripped_line or '"' in stripped_line:
                                start_quote = stripped_line.find("'")
                                end_quote = stripped_line.find("'", start_quote + 1)
                                if start_quote == -1:
                                    start_quote = stripped_line.find('"')
                                    end_quote = stripped_line.find('"', start_quote + 1)

                                if start_quote != -1 and end_quote != -1:
                                    route = stripped_line[start_quote + 1:end_quote]
                                    routes.append(route)
                                else:
                                    print("[Предупреждение] Не удалось извлечь маршрут из строки:", stripped_line)
                            else:
                                print("[Предупреждение] Маршрут без кавычек — пропущен:", stripped_line)

                        # Парсим app.run(...)
                        elif stripped_line.startswith("app.run("):
                            run_line = stripped_line[8:]  # Убираем 'app.run'
                            run_line = run_line.strip().lstrip("(").rstrip(")").strip()
                            params = [p.strip() for p in run_line.split(",") if p.strip()]

                            host_found = False
                            port_found = False

                            for param in params:
                                if "=" in param:
                                    key, value = param.split("=", 1)
                                    key = key.strip()
                                    value = value.strip().strip("'\"")

                                    if key == "host":
                                        host = value
                                        host_found = True
                                    elif key == "port":
                                        port = value
                                        port_found = True

                            if not host_found:
                                host = "не указан"
                            if not port_found:
                                port = "не указан"

                            break  # Нашли нужную строку — можно выйти

                # Вывод информации
                print("Декораторы (маршруты):")
                if routes:
                    for route in routes:
                        print(f" - {route}")
                else:
                    print("Маршруты не найдены.")

                print(f"\nХост: {host}")
                print(f"Порт: {port}")
            show_app_info(words[1])
        elif words[0] == com1:
            app_filename = words[1]
            html_path = words[2]

            # 3. Создаем файл
            if os.path.exists(app_filename):
                rprint(f"[yellow]Файл {app_filename} уже существует. Перезаписать? (y/n)[/yellow]")
                if input().lower() != "y":
                    rprint("[red]Отменено пользователем[/red]")
                    return

            with open(app_filename, "w", encoding="utf-8") as f:
                f.write("from flask import Flask, render_template_string\n\n")
                f.write("app = Flask(__name__)\n\n")

                rprint("\n[bold green]Начинаем добавлять маршруты[/bold green]")
                while True:
                    route_name = Prompt.ask("\nВведите имя декоратора (например '/'), или 'stop' для выхода")
                    if route_name.lower() == "stop":
                        break

                    func_name = Prompt.ask(f"Введите имя функции для маршрута '{route_name}' (например 'home')")

                    rprint(f"\n[blue]Введите функционал для {func_name} (введите 'nxtdr' чтобы закончить)[/blue]")
                    lines = []
                    while True:
                        line = input(". . . .")
                        if line.strip().lower() == "nxtdr":
                            break
                        lines.append(line)

                    # Записываем декоратор и функцию в файл
                    f.write(f"@app.route('{route_name}')\n")
                    f.write(f"def {func_name}():\n")
                    if lines:
                        for line in lines:
                            f.write(f"    {line}\n")
                    else:
                        f.write('    return "Hello World"\n')
                    f.write(f"    return render_template_string(open(r'{html_path}').read())\n\n")

                # 4. Хост и порт
                host = Prompt.ask("Введите хост", default="0.0.0.0")
                port = IntPrompt.ask("Введите порт", default=5000)

                # 5. Добавляем точку входа
                f.write(f"if __name__ == '__main__':\n")
                f.write(f"    app.run(host='{host}', port={port})\n")

            rprint(f"[bold green] Файл '{app_filename}' успешно создан![/bold green]")
        elif words[0] == 'ex':
            break
        elif words[0] == com3:
            run_flask_app(words[1])
        elif words[0] == com4:
            def list_apps():
                found_apps = []

                for filename in os.listdir('.'):
                    if filename.endswith('.py'):
                        is_flask_app = False
                        with open(filename, 'r', encoding='utf-8') as f:
                            for line in f:
                                # Простая проверка: есть ли создание экземпляра Flask
                                if ' = Flask(__name__)' in line.strip():
                                    is_flask_app = True
                                    break
                        if is_flask_app:
                            found_apps.append(filename)

                if found_apps:
                    for app in found_apps:
                        print(f" - {app}")
                else:
                    print("")
            list_apps()
