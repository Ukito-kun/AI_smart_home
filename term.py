import os
import shutil
import sys
import threading

# Кроссплатформенная настройка ввода
IS_WINDOWS = os.name == "nt"

if IS_WINDOWS:
  import msvcrt

  os.system("")
else:
  import termios
  import tty

# Общие переменные и мьютекс для безопасного вывода
screen_lock = threading.Lock()
input_buffer = []
prompt_prefix = ">> "


def get_key():
  """Считывает ОДНО нажатие клавиши в реальном времени."""
  if IS_WINDOWS:
    ch = msvcrt.getwch()
    if ch in ("\x00", "\xe0"):
      msvcrt.getwch()
      return ""
    return ch
  else:
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
      tty.setraw(fd)
      ch = sys.stdin.read(1)
    finally:
      termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def get_term_size():
  """Возвращает текущие размеры терминала."""
  cols, rows = shutil.get_terminal_size((80, 24))
  return rows, cols


def init_terminal():
  """Инициализирует разделенный экран и область прокрутки."""
  rows, cols = get_term_size()
  sys.stdout.write(f"\033[1;{rows-1}r")
  sys.stdout.write("\033[2J")
  sys.stdout.flush()


def restore_terminal():
  """Возвращает настройки терминала в исходное состояние при выходе."""
  sys.stdout.write("\033[r")
  sys.stdout.write("\n")
  sys.stdout.flush()


def redraw_prompt():
  """Перерисовывает строку ввода внизу экрана."""
  rows, cols = get_term_size()
  current_text = "".join(input_buffer)
  display_text = (prompt_prefix + current_text)[: cols - 1]
  sys.stdout.write(f"\033[{rows};1H\033[2K{display_text}")
  sys.stdout.flush()


def print_log(message: str=''):
  """Выводит фоновое сообщение наверх, не портя строку ввода."""
  with screen_lock:
    rows, cols = get_term_size()
    sys.stdout.write(f"\033[s\033[{rows-1};1H\n{message}")
    sys.stdout.write("\033[u")
    redraw_prompt()
