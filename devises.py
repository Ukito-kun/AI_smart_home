from dataclasses import dataclass  # Для создания классов данных вместо словарей
from enum import Enum, auto  # Для перечислений (состояния, типы, комнаты)
from math import cos, sin  # Математические функции для симуляции погоды
from typing import NamedTuple  # Для типизированных кортежей (структур данных)


def pogoda(t: int, r: int = 0):
  """Симуляция уличной температуры с помощью синусоид и косинусов.

  График можно посмотреть в любом онлайн-калькуляторе по формуле: y = 1.5 *
  (sin(x/40) + cos(x/20) + sin(x/8)) + 25
  """
  a = 3 / 2
  b = 1 / 4
  temp = a * (sin(b * t / 10) + cos(b * t / 5) + sin(b * t / 2)) + 25
  return temp if not r else round(temp, r)


def light(t: int, r: int = 0):
  """Симуляция изменения уровня освещенности в течение времени."""
  a = 2.5
  b = 3.82
  l_val = a * sin(t / b)
  return l_val if not r else round(l_val, r)


class SensorInfo(NamedTuple):
  """Струкха данных для информации о датчике."""

  sensor_id: int
  data: int
  is_active: bool


class Sensors(Enum):
  """Перечисление доступных датчиков в системе."""

  NON = SensorInfo(0, 0, False)
  TEMP = SensorInfo(1, 26, True)
  LIGHT = SensorInfo(2, 0, True)
  CONTACT = SensorInfo(3, 0, True)
  SMART_DOOR = SensorInfo(4, 0, True)


class Device_type(Enum):
  """Типы устройств для категоризации логики управления."""

  SENSOR = auto()
  OC_DEV = auto()  # Open/Close (открываемые: окна, двери)
  OO_DEV = auto()  # On/Off (включаемые: лампы, розетки, вентиляторы)


class DEVS(NamedTuple):
  """Связка ID устройства и его типа."""

  device_is: int
  dev_type: Device_type


class Devices(Enum):
  """Перечисление всех физических устройств умного дома."""

  SENSOR = DEVS(0, Device_type.SENSOR)
  WINDOW = DEVS(1, Device_type.OC_DEV)
  LED = DEVS(2, Device_type.OO_DEV)
  SOCKET = DEVS(3, Device_type.OO_DEV)
  FAN = DEVS(4, Device_type.OO_DEV)


# Группы устройств по принципу работы (для проверки валидности команд)
OCobj = Devices.WINDOW
OOobj = (Devices.LED, Devices.SOCKET, Devices.FAN)


class Rooms(Enum):
  """Перечисление комнат в доме."""

  LIVING = auto()  # Гостиная
  DINING = auto()  # Столовая
  BEDROOM = auto()  # Спальня
  KITCHEN = auto()  # Кухня


class States(Enum):
  """Возможные состояния устройств."""

  NON = auto()  # Состояние не задано (для предотвращения ошибок)
  CLOSE = auto()  # Закрыто (для окон, дверей)
  OPEN = auto()  # Открыто (для окон, дверей)
  OFF = auto()  # Выключено (для ламп, розеток, вентиляторов)
  ON = auto()  # Включено (для ламп, розеток, вентиляторов)


@dataclass(init=False)
class Devs:
  """Класс устройства умного дома.

  Используем init=False, чтобы написать собственный конструктор для
  инкапсуляции (приватизации) полей через двойное подчеркивание.
  """

  __room: Rooms  # Комната, в которой находится устройство
  __device: Devices  # Тип устройства
  __state: States  # Текущее состояние устройства

  def __init__(
      self, room: Rooms, device: Devices, state: States = States.NON
  ):
    self.__room = room
    self.__device = device

    # Защита от дурака: проверяем, соответствует ли переданное состояние типу устройства
    if ((self.__device.value.dev_type == Device_type.OC_DEV) and (
        state in (States.OPEN, States.CLOSE)
    )) or ((self.__device.value.dev_type == Device_type.OO_DEV) and (
        state in (States.ON, States.OFF)
    )):
      self.__state = state
    else:
      # Если состояние передано некорректно или по умолчанию (NON),
      # назначаем базовое безопасное состояние в зависимости от типа устройства
      if self.__device.value.dev_type == Device_type.OC_DEV:
        self.__state = States.CLOSE
      else:
        self.__state = States.OFF

  # Свойства (геттеры) для безопасного чтения закрытых (private) полей извне
  @property
  def state(self) -> States:
    return self.__state

  @property
  def room(self) -> Rooms:
    return self.__room

  @property
  def device(self) -> Devices:
    return self.__device

  def Open(self):
    """Открытие устройства (доступно только для OC_DEV, например, окон)."""
    if self.__device.value.dev_type == Device_type.OC_DEV:
      self.__state = States.OPEN
    else:
      raise ValueError(f"Func Open need device from {OCobj}")

  def Close(self):
    """Закрытие устройства (доступно только для OC_DEV)."""
    if self.__device.value.dev_type == Device_type.OC_DEV:
      self.__state = States.CLOSE
    else:
      raise ValueError(f"Func Close need device from {OCobj}")

  def On(self):
    """Включение устройства (доступно только для OO_DEV, например, ламп)."""
    if self.__device.value.dev_type == Device_type.OO_DEV:
      self.__state = States.ON
    else:
      raise ValueError(f"Func On need device from {OOobj}")

  def Off(self):
    """Выключение устройства (доступно только для OO_DEV)."""
    if self.__device.value.dev_type == Device_type.OO_DEV:
      self.__state = States.OFF
    else:
      raise ValueError(f"Func Off need device from {OOobj}")

  def __str__(self) -> str:
    """Красивое строковое представление объекта для удобного вывода в лог."""
    return f"{self.__room.name} | {self.__device.name} | {self.__state.name}"


if __name__ == "__main__":
  # Тестирование работы классов и защиты от дурака
  Kitchen_window = Devs(Rooms.KITCHEN, Devices.WINDOW, States.CLOSE)

  print("ROOM    | DEVICE | STATE")
  print("-" * 25)
  print(str(Kitchen_window))  # Выведет состояние окна на кухне
  print(
      str(Devs(Rooms.BEDROOM, Devices.FAN))
  )  # Выведет вентилятор в спальне (по умолчанию OFF)
  print(Kitchen_window.__str__())
  print(str(Kitchen_window))
