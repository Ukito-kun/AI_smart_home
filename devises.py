if True:                                      # для сворачивания. 6 строк выглядят немного громоздко
  import time, random, datetime                             # Для теста и тп
  from abc import ABC, abstractclassmethod                  # Для шаблонных классов и невозможности создания их объектов.
  from dataclasses import dataclass                         # Для создания классов данных вместо словарей
  from enum import Enum, auto, IntEnum, global_enum,unique  # Для перечислений (состояния, типы, комнаты)   
  from math import cos, sin, radians                        # Математические функции для симуляции погоды
  from typing import NamedTuple, Literal, Any               # Для типизированных кортежей (структур данных)

''' Ctrl + K, Ctrl + J;  Ctrl + K, Ctrl + 0'''
def pr(state):print(state, type(state))
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
  a, b = 3 / 2, 1 / 4
  temp = a * (sin(b * t / 10) + cos(b * t / 5) + sin(b * t / 2)) + shift
  return temp if not r else round(temp, r)
def light(t: int, r: int = 0, shift: int = 0):
  """Симуляция изменения уровня освещенности в течение времени."""
  a,b = 2.5, 3.82
  l_val = a * sin(t / b) + shift
  return l_val if not r else round(l_val, r)

class SensorInfo(NamedTuple):
  """Струкха данных для информации о датчике."""

  sensor_id: int
  data: int
  is_active: bool
class DEVS(NamedTuple):
  """Связка ID устройства и его типа."""

  device_is: int
  dev_type: Device_type
@unique
class Months(IntEnum):
  JAN = 1;     FEB = 2;      MARCH = 3;      APR = 4
  MAY = 5;     JUN = 6;      JUL = 7;        AUG = 8
  SEPT = 9;    OCT = 10;     NOV = 11;       DEC = 12
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
@global_enum
class Caffes(Enum):
  ESSPRESSO = auto();     DOUBLE_ESSPRESSO = auto();      AMERICANO = auto()
  RISTRETTO = auto();     CAPPUCCINO = auto();            LATTE = auto()
  FLAT_WHITE = auto();    MOCHACHINO = auto();            DECAF = auto()
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
@global_enum
class Devices(Enum):
  """Перечисление всех физических устройств умного дома."""
  SENSOR_TEMP = auto();   WINDOW = auto();    LED = auto()
  SOCKET = auto();        FAN = auto();       SMART_DOOR = auto()
  KOFFEE = auto();        KETTLE = auto();    RGB_LED = auto()
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
@global_enum
class Rooms(Enum):
  """Перечисление комнат в доме."""
  LIVING = auto();        BATHROOM = auto();      BEDROOM = auto()
  KITCHEN = auto();       STREET = auto();        HALLWAY = auto()
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
@global_enum
class States(Enum):
  """Возможные состояния устройств."""
  NON = auto()
  CLOSE = auto();       OPEN = auto()
  OFF = auto();         ON = auto()
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
@unique
class WindowOpened(Enum):
  CLOSED = 0      # Закрыто
  MICRO_VTNT = 1  # Микропровертивание/щелевое проветр ивание
  TILT = 2        # Откидное проветривание - сверху открвается 
  TURN = 3        # Нараспашку. полностью открыто.
  @classmethod
  def get_values(obj):
    return [i.name for i in obj]
class Verbs(Enum):
  OPEN = auto(); CLOSE = auto(); ON = auto(); OFF = auto()
  HEATING = auto(); BOILING = auto(); SETCOLOR = auto()
  SETSPEED = auto(); LOCK = auto(); UNLOCK = auto()
  SETBRIGHTNESS = auto()

class F:
  db = {}
  default = {}
  app = {}
  @classmethod
  def get_keys(cls):
    return [h for h in cls.db.keys()]
  @classmethod
  def reg(cls, key, ds:States):
    def decorator(subclass):
      cls.db[key] = subclass
      cls.default[key] = ds
      return subclass
    return decorator
  def get_rooms(self):
    return [h for h in self.app.keys()]
  def reg_room(self, room:str, room_type:Rooms):
    if not room in [h for h in self.app.keys()]:
      self.app[room] = {
        'kind': room_type, 
        'lst': {}
      }
    else: 
      raise ValueError('Wrong room')
  def pr(self):
    for i in self.app.keys():
      print(i, self.app[i])
  def control(self, room:str, name:str, verb:Verbs, value:States | int | (int, int, int) | str | None):
    dev = self.app.get(room).get('lst').get(name)
    if (value is None):
      if dev in (KETTLE, SENSOR_TEMP):
        pass
      else: raise ValueError('Wrong new status')
    if not room in [h for h in self.app.keys()]:
      raise ValueError('Wrong room')
    match verb:
      case Verbs.OPEN | Verbs.CLOSE: 
        if dev.device is SMART_DOOR:
          if type(value) is str:
            if verb is Verbs.OPEN:
              dev.Open(value)
            else: 
              dev.Close(value)
          else: raise TypeError('DOOR need str value')
        elif dev.device is WINDOW:
          if verb is Verbs.OPEN:
            dev.Open()
          else: 
            dev.Close()
      case Verbs.OFF | Verbs.ON: 
        if verb is Verbs.OFF:
          dev.OFF
        elif verb is Verbs.ON:
          if dev.device is FAN:
            if type(value) is int:
              dev.set_speed(value)
            else: raise TypeError('FAN need int value')
          elif dev.device is LED:
            print('IS GOOD')
            if type(value) is int:
              dev.set_brightness(value)
            else: raise TypeError('LED need int value')
      case Verbs.HEATING | Verbs.BOILING: 
        if dev.device is KETTLE:
          if verb is Verbs.HEATING:
            if type(value) is int:
              dev.heating(value)
            else: raise TypeError('HEATING need int value')
          elif verb is Verbs.BOILING:
            dev.boiling()
        else: raise AttributeError(f'\'{dev}\' object has no attribute \'{verb}\'')
      case Verbs.SETCOLOR: 
        if dev.device is RGB_LED:
          if type(value) is tuple:
            if type(value[0]) == type(value[1]) == type(value[2]) == int:
              dev.set_color(value)
            else: raise TypeError('SETCOLOR need tuple with 3 int (int, int, int)')
      case Verbs.SETBRIGHTNESS: 
        if dev.device is LED:
          if type(value) is int:
            dev.set_brightness(value)
          else: raise TypeError('SETBRIGHTNESS need int value')
        else: raise AttributeError(f'\'{dev}\' object has no attribute \'SETBRIGHTNESS\'')
      case Verbs.SETSPEED: 
        if dev.device is FAN:
          if type(value) is int:
            dev.set_brightness(value)
          else: raise TypeError('SETSPEED need int value')
        else: raise AttributeError(f'\'{dev}\' object has no attribute \'SETSPEED\'')
      case Verbs.LOCK | Verbs.UNLOCK: 
        if dev.device is SMART_DOOR:
          if type(value) is str:
            if verb is Verbs.LOCK:
              dev.Lock(value)
            elif verb is Verbs.UNLOCK:
              dev.Unlock(value)
          else: raise TypeError('door need str value - pin')
        else: raise AttributeError(f'\'{dev}\' object has no attribute \'{verb}\'')
  def create(self, key:str, name:str, room:str, state:States = States.NON):
    if not room in [h for h in self.app.keys()]:
      raise ValueError('Wrong room')
    
    if state is States.NON:
      state = self.default.get(key)
      if state is None:
        raise ValueError('Wrong key')
    c = self.db.get(key)(self.app.get(room).get('kind', None))
    if c is None:
      raise ValueError('Wrong key, room or state')
    self.app[room]['lst'][name] = c
    return c

'''lst = [{
  'Depiction': '1 kitchen, 1 bedroom, 1 bathroom',
  'kitchen1': {'kind': Rooms.KITCHEN,
  'lst': []
  },
  'bedroom1': {'kind': Rooms.BEDROOM,
  'lst': []
  },
  'bathroom1': {'kind': Rooms.BATHROOM,
  'lst': []
  } }]
'''
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
  def change_pin(self, last_pin:str, new_pin:str) -> bool:
    if last_pin == self._pin:
      object.__setattr__(self, '_pin', new_pin)
      return 1
    return 0
  def Open(self, pin:str = '') -> bool:
    if not self._locked or (pin == self._pin and self._locked):
      object.__setattr__(self, '_state', States.OPEN)
      return 1
    return 0
  def Close(self, pin:str = '') -> bool:
    if not self._locked or (pin == self._pin and self._locked):
      object.__setattr__(self, '_state', States.CLOSE)
      return 1
    return 0
  def Lock(self, pin:str = '') -> bool:
    if pin == self._pin and (not self._locked):
      object.__setattr__(self, '_locked', True)
      return 1
    return 0
  def Unlock(self, pin:str = '') -> bool:
    if pin == self._pin and (not self._locked):
      object.__setattr__(self, '_locked', False)
      return 1
    return 0
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {'locked' if self._locked else 'unlocked'}"
@F.reg('window', ds=States.CLOSE)
class window(Devs):
  _openedstate = WindowOpened.CLOSED
  _device = Devices.WINDOW
  def __init__(self, room: Rooms, state: States = States.CLOSE):
    if state not in (States.CLOSE, States.OPEN):
      raise AttributeError(f'Invalid type: {self._device} cannot be {state}ed')
    if state is States.OPEN:
       object.__setattr__(self, '_openedstate', WindowOpened.TURN)
    object.__setattr__(self, '_state', state)
    object.__setattr__(self, '_room', room)
    # print(self._room, self._state)
  def Open(self, val_of_open: WindowOpened = WindowOpened.TURN) -> bool:
    object.__setattr__(self, '_openedstate', val_of_open)
    object.__setattr__(self, '_state', States.OPEN)
    return 1
  def Close(self) -> bool:
    object.__setattr__(self, '_openedstate', WindowOpened.CLOSED)
    object.__setattr__(self, '_state', States.CLOSE)
    return 1
  def _str__(self) -> str:
    return f"{self._room:^10} | {self._device.name:^12} | {self._state.name:^10} | {self._openedstate.name:^10}"
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
    return f"{self._room:^10} | {self._device.name:^12} | {self._state.name:^10} | rgb: {self._r}, {self._g}, {self._b}"
  def hue(self, Hue:int, brightness:int):
    r, g, b = HUE(Hue, brightness)
    object.__setattr__(self, '_r', r)
    object.__setattr__(self, '_g', g)
    object.__setattr__(self, '_b', b)
    return 1
  def rgb(self, r:int, g:int, b:int):
    object.__setattr__(self, '_r', r)
    object.__setattr__(self, '_g', g)
    object.__setattr__(self, '_b', b)
    return 1
  def set_color(self, rgb:tuple | list):
    if type(rgb[0]) == type(rgb[1]) == type(rgb[2]) == int:
      object.__setattr__(self, '_r', rgb[0])
      object.__setattr__(self, '_g', rgb[1])
      object.__setattr__(self, '_b', rgb[2])
      return 1
    raise TypeError('Func rgb need tuple with 3 int (int, int, int)')
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
  def set_brightness(self, brightness:int):
    self.On()
    object.__setattr__(self, '_brightness', brightness)
  def __str__(self) -> str:
    return f"{self._room.name:^10} | {self._device.name:^12} | {self._state.name:^10} | {self._brightness:^10}" 
@F.reg('fan', ds=States.OFF)
class fan(OobjO):
  _device = Devices.FAN
  _speed:int = 0
  def set_speed(self, speed:int):
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

class VClock:
  def __init__(self, start_date:datetime.datetime):
    self._virt_start_time = start_date
    self._real_start_time = time.time()
    self.time_spd = 86400 // 240
  def get_current_time(self) -> datetime.datetime:
    real_elapsed = time.time() - self._real_start_time
    virtual_elapsed_seconds = real_elapsed * self.time_spd
    return self._virt_start_time + datetime.timedelta(seconds=virtual_elapsed_seconds)
  def set_time(self, new_data:datetime.datetime):
    self.start_virtual_time = new_date
    self.start_real_time = time.time()
  def shift_time(self, timedelta_obj: datetime.timedelta):
    """Сдвинуть время вперед или назад на определенный промежуток"""
    self.start_virtual_time += timedelta_obj
  def __str__(self) -> str:
    return f"{self.get_current_time().strftime('%Y-%m-%d %H:%M:%S')}"


''' переписать '''
if __name__ == "__main__":
  Appart = F()
  Appart.reg_room('Kitchen', KITCHEN)
  Appart.reg_room('Bedroom1', BEDROOM)
  Appart.reg_room('Street', STREET)
  print(Appart.get_rooms())
  print(F.get_keys())

  kit_wind = Appart.create('window','w1',  room='Kitchen', state=States.OPEN)
  bed_led = Appart.create('led', 'l1', room='Bedroom1', state=States.OFF)
  kit_ket = Appart.create('kettle', 'k1', room='Kitchen', state=States.NON)
  Appart.control('Bedroom1', 'l1', Verbs.ON, 100)
  print(f'\n{'ROOM':^10} | {'DEVISES':^12} | {'STATE':^10} | {'OTHERS':^10}')
  print(str(kit_wind))
  print(str(bed_led))
  print(str(rgb_led('Kitchen')))
  
  out_temp = Appart.create('temp_sensor', 'ts1', room='Street', state=States.NON)
  out_temp.get_temp(10)
  print(str(out_temp))
  
  virt_clock = VClock(datetime.datetime(2028, 5, 8, 14, 0))
  print(str(virt_clock))
  
  '''for i in range(5):
    time.sleep(i+1)
    print(f"{virt_clock.get_current_time().strftime('%Y-%m-%d %H:%M:%S')}")
  '''
  # Appart.pr()