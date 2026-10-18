from devises import *
import threading
import time

# Импортируем всё необходимое из нашей библиотеки term_ui
from term import (
    get_key,
    init_terminal,
    input_buffer,
    print_log,
    redraw_prompt,
    restore_terminal,
    screen_lock,
)


def background_task():
  """Пример фонового процесса, который периодически шлет логи наверх."""
  step = 1
  while True:
    time.sleep(3)
    print_log(f"[ФОН] Шаг {step}: Фоновый процесс работает стабильно.")
    step += 1


def main():
  # 1. Инициализируем терминал (создаем область логов сверху и строку ввода внизу)
  init_terminal()

  print_log("=== Консольный интерфейс запущен ===")
  print_log("Введите команду ('help', 'status', 'exit') и нажмите Enter.\n")

  # 2. Запускаем фоновый поток
  sim_thread = threading.Thread(target=background_task, daemon=True)
  sim_thread.start()

  # 3. Первая отрисовка строки ввода
  with screen_lock:
    redraw_prompt()

  try:
    # 4. Главный цикл обработки клавиатуры
    while True:
      key = get_key()
      if not key:
        continue

      # Нажатие Enter (отправка команды)
      if key in ("\r", "\n"):
        command = "".join(input_buffer).strip()
        input_buffer.clear()

        with screen_lock:
          redraw_prompt()

        if command:
          print_log(f"[Пользователь]: {command}")
          cmd_lower = command.lower()
          
          if cmd_lower == "exit":
            print_log("Завершение работы...")
            break
          elif cmd_lower == "help":
            print_log("Доступные команды: help, status, exit")
          elif cmd_lower == "status":
            print_log("Статус: Все системы работают нормально.")
          else:
            print_log(f"Неизвестная команда: '{command}'")

      # Нажатие Backspace (удаление символа)
      elif key in ("\x08", "\x7f"):
        if input_buffer:
          input_buffer.pop()
          with screen_lock:
            redraw_prompt()

      # Экстренный выход (Ctrl+C)
      elif key == "\x03":
        break

      # Печатные символы
      elif ord(key) >= 32:
        input_buffer.append(key)
        with screen_lock:
          redraw_prompt()

  finally:
    # Обязательно восстанавливаем консоль при выходе
    restore_terminal()


if __name__ == "__main__":
  main()
