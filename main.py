'''
>>> Закрой окно 1
>>> добавить
  1 Kitchen
  2 Bedroom
  3 Living
>>> 2
 Что бы вы хотели добавить в {BEDROOM}
  1 LED
  2 FAN
  3 SOCKET
>>> 1
  Добавлена лампа в спальню
'''

'day.month hour:min                       '
'15.JUL 15:24'        '{day}.{month} {hour}:{minute}'
from devises import *
import threading
import time
import calendar

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
kitchen = {
  'led1':F.make('led', Rooms.KITCHEN, States.ON), 
  'window1':F.make('window', Rooms.KITCHEN), 
  'door1':F.make('door', Rooms.KITCHEN)
}
living = {
  'led1':F.make('led', Rooms.LIVING, States.ON), 
  'window1':F.make('window', Rooms.LIVING), 
  'door1':F.make('door', Rooms.LIVING)
}
bedroom = {
  'led1':F.make('led', Rooms.BEDROOM, States.ON), 
  'window1':F.make('window', Rooms.BEDROOM), 
  'door1':F.make('door', Rooms.BEDROOM)
}
def background_task():
  global living
  """Пример фонового процесса, который периодически шлет логи наверх."""
  step = 1
  print_log(f'{'ROOM':^10} | {'DEVISES':^12} | {'STATE':^10} | {'OTHERS':^10}\n')
  
  while True:
    # print_log(f"[ФОН] Шаг {step}: Фоновый процесс работает стабильно.")
    time.sleep(2)
    for i in living:
      print_log(str(living[i]))
      living['led1'].set_brightness(random.randint(1,100))
      if living['window1'].state == States.CLOSE:
        living['window1'].Open()
        living['door1'].Close()
      else: 
        living['window1'].Close()
        living['door1'].Open()
      #print_log(f"[ФОН] Шаг {step}: ФОН работает. Фоновых процессов: {random.randint(0, 100)}")
    print_log('')
    step += 1

def main():
  global living
  commands = ('help', 'status', 'exit')
  # 1. Инициализируем терминал (создаем область логов сверху и строку ввода внизу)
  init_terminal()

  print_log("=== Консольный интерфейс запущен ===")
  print_log(f"Введите команду {commands} и нажмите Enter.\n")

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
          
          match cmd_lower:
            case "exit":
              print_log("Завершение работы...")
              break
            case 'help':
              print_log(f'Доступные команды: {commands}')
            case _:
              if 'living' in cmd_lower:
                print_log(f'Что закрыть? {living.keys()}')
                while True:
                  i = ''
              print_log(f"Неизвестная команда: '{command}'")
          print_log(f'\n{'ROOM':^10} | {'DEVISES':^12} | {'STATE':^10} | {'OTHERS':^10}')
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
