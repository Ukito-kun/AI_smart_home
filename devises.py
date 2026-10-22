''' Ctrl + K, Ctrl + J;  Ctrl + K, Ctrl + 0'''
import time, random                       # Для теста и тп
from abc import ABC, abstractclassmethod  # Для шаблонных классов и невозможности создания их объектов.
from dataclasses import dataclass         # Для создания классов данных вместо словарей
from enum import Enum, auto               # Для перечислений (состояния, типы, комнаты)
from math import cos, sin, radians        # Математические функции для симуляции погоды
from typing import NamedTuple             # Для типизированных кортежей (структур данных)

def crt3_8(val:int) :
  return ((val + 1) * (val + 1) * val) >> 16

def HUE(hue:int, brightness:int):
  while hue > 255:
    hue -= 255
  while hue < 0:
    hue += 255
  if hue >= 170:
    hue = (hue - 170) * 3
    r = 255 - hue
    g = 0
    b = hue
  elif hue >= 85:
    hue = (hue - 85) * 3
    r = 0
    g = hue
    b = 255 - hue
  else:
    hue = (hue - 0) * 3
    r = hue
    g = 255 - hue
    b = 0
  r = crt3_8(r)
  g = crt3_8(g)
  b = crt3_8(b)
  return (r, g, b)

def pogoda(t: int, r: int = 0, shift: int = 25):
  """Симуляция уличной температуры с помощью синусоид и косинусов.

  График можно посмотреть в любом онлайн-калькуляторе по формуле: y = 1.5 *
  (sin(x/40) + cos(x/20) + sin(x/8)) + 25
  """
  a = 3 / 2
  b = 1 / 4
  temp = a * (sin(b * t / 10) + cos(b * t / 5) + sin(b * t / 2)) + shift
  return temp if not r else round(temp, r)

def light(t: int, r: int = 0, shift: int = 0):
  """Симуляция изменения уровня освещенности в течение времени."""
  a = 2.5
  b = 3.82
  l_val = a * sin(t / b) + shift
  return l_val if not r else round(l_val, r)

class Months(Enum):
  JAN = auto();     FEB = auto();     MARCH = auto();     MAY = auto();
  APR = auto();     JUN = auto();     JUL = auto();       AUG = auto()
  SEPT = auto();    OCT = auto();     NOV = auto();       DEC = auto()
  def __int__(month:Months):
    return month.value

class SensorInfo(NamedTuple):
  """Струкха данных для информации о датчике."""

  sensor_id: int
  data: int
  is_active: bool

class DEVS(NamedTuple):
  """Связка ID устройства и его типа."""

  device_is: int
  dev_type: Device_type

class Caffes(Enum):
  ESSPRESSO = auto()
  DOUBLE_ESSPRESSO = auto()
  AMERICANO = auto()
  RISTRETTO = auto()
  CAPPUCCINO = auto()
  LATTE = auto()
  LATTE_MACCHIATO = auto()
  FLAT_WHITE = auto()
  MOCHACHINO = auto()
  DECAF = auto()

class Devices(Enum):
  """Перечисление всех физических устройств умного дома."""
  SENSOR_TEMP = auto()
  WINDOW = auto()
  LED = auto()
  SOCKET = auto()
  FAN = auto()
  SMART_DOOR = auto()
  KOFFEE = auto()
  KETTLE = auto()
  RGB_LED = auto()

class Rooms(Enum):
  """Перечисление комнат в доме."""

  LIVING = auto()   # Гостиная
  DINING = auto()   # Столовая
  BEDROOM = auto()  # Спальня
  KITCHEN = auto()  # Кухня
  STREET = auto()   # Улица
  HALLWAY = auto()  # Прихожая

class States(Enum):
  """Возможные состояния устройств."""

  NON = auto()  # Состояние не задано (для предотвращения ошибок)
  CLOSE = auto()  # Закрыто (для окон, дверей)
  OPEN = auto()  # Открыто (для окон, дверей)
  OFF = auto()  # Выключено (для ламп, розеток, вентиляторов)
  ON = auto()  # Включено (для ламп, розеток, вентиляторов)

class F:
  db = {}
  default = {}
  @classmethod
  def reg(cls, key, ds:States):
    def decorator(subclass):
      cls.db[key] = subclass
      cls.default[key] = ds
      return subclass
    return decorator
  
  @classmethod
  def make(cls, key, room:Rooms, state:States = States.NON):
    if state is States.NON:
      state = cls.default[key]
    return cls.db[key](room, state)

class Devs(ABC):
  """Класс устройства умного дома.
  Используем init=False, чтобы написать собственный конструктор для
  инкапсуляции (приватизации) полей через двойное подчеркивание.
  """
  _room: Rooms  # Комната, в которой находится устройство
  _device: Devices  # Тип устройства
  _state: States  # Текущее состояние устройства
  @abstractclassmethod
  def __init__(self, room: Rooms, device: Devices, state: States = States.NON):
    pass
  # Свойства (геттеры) для безопасного чтения закрытых (private) полей извне
  @property
  def state(self) -> States:
    return self._state

  @property
  def room(self) -> Rooms:
    return self._room

  @property
  def device(self) -> Devices:
    return self._device

  def __str__(self) -> str:
    """Красивое строковое представление объекта для удобного вывода в лог."""
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} |"

@F.reg('door', ds=States.CLOSE)
class door(Devs):
  _device = Devices.SMART_DOOR
  _locked: bool = False
  _pin: str

  def __init__(self, room: Rooms, pin:str = '1234', state: States = States.CLOSE):
    if state is States.NON:
      state = States.CLOSE
    if state not in (States.OPEN, States.CLOSE):
      raise AttributeError(f'Invalid type: {self._device} cannot be {state}ed')
    object.__setattr__(self, '_state', state)
    object.__setattr__(self, '_room', room)
    object.__setattr__(self, '_pin', pin)

  def change_pin(self, last_pin, new_pin) -> bool:
    if last_pin == self._pin:
      object.__setattr__(self, '_pin', new_pin)
      return 1
    return 0
    
  def Open(self, pin = '') -> bool:
    if not self._locked or (pin == self._pin and self._locked):
      object.__setattr__(self, '_state', States.OPEN)
      return 1
    return 0

  def Close(self, pin = '') -> bool:
    if not self._locked or (pin == self._pin and self._locked):
      object.__setattr__(self, '_state', States.CLOSE)
      return 1
    return 0

  def Lock(self, pin = '') -> bool:
    if pin == self._pin and (not self._locked):
      object.__setattr__(self, '_locked', True)
      return 1
    return 0

  def Unlock(self, pin = '') -> bool:
    if pin == self._pin and ( not self._locked):
      object.__setattr__(self, '_locked', False)
      return 1
    return 0
  
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {'locked' if self._locked else 'unlocked'}"

@F.reg('window', ds=States.CLOSE)
class window(Devs):
  _device = Devices.WINDOW
  def __init__(self, room: Rooms, state: States = States.CLOSE):
    if state not in (States.CLOSE, States.OPEN):
      raise AttributeError(f'Invalid type: {self._device} cannot be {state}ed')
    object.__setattr__(self, '_state', state)
    object.__setattr__(self, '_room', room)

  def Open(self) -> bool:
    object.__setattr__(self, '_state', States.OPEN)
    return 1

  def Close(self) -> bool:
    object.__setattr__(self, '_state', States.CLOSE)
    return 1

@F.reg('coffee', ds=States.NON)
class coffe(Devs):
  _device = Devices.KOFFEE
  _state:States = States.NON
  def __init__(self, room:Rooms, *args):
    object.__setattr__(self, '_room', room)
  def make_coffee(self, cafe:Caffes):
    time.sleep(2)
    return 1

@F.reg('kettle', ds=States.NON)
class kettle(Devs):
  _device = Devices.KETTLE
  _state = States.NON
  def __init__(self, room:Rooms, *args):
    object.__setattr__(self, '_room', room)
  def boiling(self):
    time.sleep(45)
    return 1
  def heating(self, temp):
    time.sleep(temp-25)
    return 1

@F.reg('rgb_led', ds=States.OFF)
class rgb_led(Devs):
  _device = Devices.RGB_LED
  _r:int = 0
  _g:int = 0
  _b:int = 0
  def __init__(self, room:Rooms, state:States = States.OFF):
    object.__setattr__(self, '_state', state)
    object.__setattr__(self, '_room', room)
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | rgb: {self._r}, {self._g}, {self._b}"
  def hue(self, Hue:int, brightness:int):
    r, g, b = HUE(Hue, brightness)
    object.__setattr__(self, '_r', r)
    object.__setattr__(self, '_g', g)
    object.__setattr__(self, '_b', b)
    return 1
  def rgb(self, r, g, b):
    object.__setattr__(self, '_r', r)
    object.__setattr__(self, '_g', g)
    object.__setattr__(self, '_b', b)
    return 1

class OobjO(Devs, ABC):
  def __init__(self, room: Rooms, state: States = States.OFF):
    if state not in (States.ON, States.OFF):
      raise AttributeError(f'Invalid type: {self._device} cannot be {state}ed')
    object.__setattr__(self, '_room', room)
    object.__setattr__(self, '_state', state)
  
  def Off(self) -> bool:
    object.__setattr__(self, '_state', States.OFF)
    return 1

  def On(self) -> bool:
    object.__setattr__(self, '_state', States.ON)
    return 1

@F.reg('led', ds=States.OFF)
class led(OobjO):
  _device = Devices.LED
  _brightness:int = 0
  def set_brightness(self, brightness):
    object.__setattr__(self, '_brightness', brightness)
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {self._brightness:^10}" 
@F.reg('fan', ds=States.OFF)
class fan(OobjO):
  _device = Devices.FAN
  _speed:int = 0
  def set_speed(self, speed):
    object.__setattr__(self, '_speed', speed)
    return 1
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {self._speed:^10}"
@F.reg('socket', ds=States.OFF)
class socket(OobjO):
  _device = Devices.SOCKET

@F.reg('temp_sensor', ds=States.NON)
class temp_sensor(Devs):
  _device: Devices = Devices.SENSOR_TEMP
  _temp: int = pogoda(0, 2, 25)
  _state: States = States.NON
  def __init__(self, room:Rooms, *args):
    object.__setattr__(self, '_room', room)

  def get_temp(self, t:int = 0, month:Months = Months.SEPT):
    if self._room is Rooms.STREET:
      object.__setattr__(self, '_temp', pogoda(t, 2, round(- 50*sin(radians(30 * int(Months.JAN))), 2)))
    else:
      object.__setattr__(self, '_temp', self._temp + (random.random()*2 - 1))
      while not (20 < self._temp < 30):
        if self._temp <= 20:
          self._temp += 1
        elif self._temp >= 30:
          self._temp -= 1
    return self._temp

  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {self._temp:^10}"
    
if __name__ == "__main__":
  print(f'{'ROOM':^10} | {'DEVISES':^12} | {'STATE':^10} | {'OTHERS':^10}')
  kit_wind = F.make('window', room=Rooms.KITCHEN, state=States.OPEN)
  bed_led = F.make('led', room=Rooms.BEDROOM, state=States.OFF)
  kit_ket = F.make('kettle', room=Rooms.KITCHEN, state=States.NON)
  print(str(kit_wind))
  print(str(bed_led))
  print(str(rgb_led(Rooms.KITCHEN)))
  out_temp = F.make('temp_sensor', room=Rooms.STREET, state=States.NON)
  out_temp.get_temp(10)
  print(str(out_temp))