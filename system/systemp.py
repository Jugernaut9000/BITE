import os
import psutil
import time
import threading
size = os.get_terminal_size()
w = size.columns 
# Флаг для остановки программы
stop_monitoring = False

def get_cpu_temperature():
    """Получение температуры процессора."""
    try:
        if os.name == 'nt':  # Windows
            return "N/A"  # На Windows требуются дополнительные инструменты
        else:  # Linux
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as file:
                temp = int(file.read()) / 1000
                return f"{temp:.1f}°C"
    except Exception as e:
        return "N/A"

def get_cpu_usage():
    """Получение загрузки процессора."""
    return f"{psutil.cpu_percent(interval=1)}%"

def get_memory_usage():
    """Получение использования оперативной памяти."""
    memory = psutil.virtual_memory()
    return f"{memory.percent}%"

def get_network_speed():
    """Получение скорости передачи данных в сети."""
    net_stats = psutil.net_io_counters()
    bytes_sent = net_stats.bytes_sent
    bytes_recv = net_stats.bytes_recv

    time.sleep(1)  # Ждём секунду для расчёта скорости

    new_net_stats = psutil.net_io_counters()
    new_bytes_sent = new_net_stats.bytes_sent
    new_bytes_recv = new_net_stats.bytes_recv

    upload_speed = (new_bytes_sent - bytes_sent) / 1_000_000  # МБ/с
    download_speed = (new_bytes_recv - bytes_recv) / 1_000_000  # МБ/с

    return f"Upload: {upload_speed:.2f} MB/s, Download: {download_speed:.2f} MB/s"

def clear_terminal():
    """Очистка терминала."""
    os.system('cls' if os.name == 'nt' else 'clear')

def monitor_system():
    """Мониторинг системы в реальном времени."""
    global stop_monitoring
    print("Начало мониторинга системы. Нажмите 'x', чтобы завершить.\n")

    while not stop_monitoring:
        try:
            cpu_temp = get_cpu_temperature()
            cpu_usage = get_cpu_usage()
            memory_usage = get_memory_usage()
            network_speed = get_network_speed()

            clear_terminal()

            print('='*w)
            print(f"Температура процессора: {cpu_temp}")
            print('-'*w)
            print(f"Загрузка процессора: {cpu_usage}")
            print('-'*w)
            print(f"Использование оперативной памяти: {memory_usage}")
            print('-'*w)
            print(f"Скорость передачи данных в сети: {network_speed}")
            print('='*w)
            time.sleep(1)  # Обновление каждую секунду

        except KeyboardInterrupt:
            print("\nМониторинг завершён.")
            break

def listen_for_exit():
    """Прослушивание ввода для выхода."""
    global stop_monitoring
    while True:
        user_input = input()
        if user_input.lower() == 'x':
            print("Завершение работы программы...")
            stop_monitoring = True
            break

def get_sys_temp():
    # Запуск мониторинга в отдельном потоке
    monitor_thread = threading.Thread(target=monitor_system)
    monitor_thread.start()

    # Запуск прослушивания ввода в основном потоке
    listen_for_exit()

    # Дожидаемся завершения потока мониторинга
    monitor_thread.join()
get_sys_temp()
