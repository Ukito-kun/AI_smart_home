# второй набросок кода

from dataclasses import dataclass   # для классов данных, используем вместо словарей
from enum import Enum, auto         # для перечислений состояний, типов, комнат
from math import sin, cos           # auto() автоматически выдает порядковый номер
from typing import NamedTuple

def pogoda(t:int, r: int = 0): # print(pogoda(0))
    a = 3/2
    b = 1/4
    temp = a* (sin(b*t/10) + cos(b*t/5) + sin(b*t/2)) + 25   # тут не описать. открыть нужно любой калькулятор графиков и вставить туда фомулу
    return temp if not r else round(temp, r)        # y = 2* (sin(x/20) + cos(x/10) + sin(x/4)) + 25  

def light(t:int, r: int = 0):
    a = 2.5
    b = 3.82
    light = a* (sin(t/b))
    return light

class SensorInfo(NamedTuple):
    sensor_id: int
    data: int
    is_active: bool
class Sensors(Enum):
    NON = SensorInfo(0, 0, False)
    TEMP = SensorInfo(1, 0, True)
    LIGHT = SensorInfo(2, 0, True)
    WIND = SensorInfo(3, 0, True)
    CONTACT = SensorInfo(4, 0, True)
    SMART_DOOR = SensorInfo(5, 0, True)

class Device_type(Enum):
    SENSOR = auto()
    OC_DEV = auto()
    OO_DEV = auto()
class DEVS(NamedTuple):
    device_is: int
    dev_type: Device_type

class Devices(Enum):    # Перечисления устройств
    SENSOR = DEVS(0, Device_type.SENSOR)
    WINDOW = DEVS(1, Device_type.OC_DEV)
    LED = DEVS(2, Device_type.OO_DEV)
    SOCKET = DEVS(3, Device_type.OO_DEV)
    FAN = DEVS(4, Device_type.OO_DEV)
OCobj = (Devices.WINDOW)
OOobj = (Devices.LED, Devices.SOCKET, Devices.FAN)
class Rooms(Enum):      # перечисление комнат
    LIVING = auto()     # Гостиная
    DINING = auto()     # столовая
    BEDROOM = auto()    # спальня
    KITCHEN = auto()    # кухня

class States(Enum):     # перечисление состояний
    NON = auto()        # Нет состояния. нужно для исключения некотоорых ошибок.
    CLOSE = auto()      # закрытою для окон, дверей и тп
    OPEN = auto()       # открыто для них же
    OFF = auto()        # выключенно. для розеток, ламп, вентиляторов
    ON = auto()         # включенно для них же

@dataclass(init = False) # нужно для класса с данными. init=False для того, что б самостоятельно создать ф-ию __init__
class Devs:             # иначе не получится создать приватные переменные.
    __room: Rooms        # комната.      _ для приватизации. :ROOMS для объявления типа данных, перечисленных выше.
    __device: Devices    # устройство    приватные должны быть, чтоб нельзя было изменить извне. например комнату и 
    __state: States      # состояние     устройство. иначе может быть, что из вентилятора в окно и окно будет выключено.

    def __init__(self, room:Rooms, device:Devices, state:States = States.NON):  # инициализация класса. self - внутренние
        self.__room = room       # данные переменной. в ней зранятся все данные, например комната, устройство, состояние
        self.__device = device   # тут мы присваиваем данные комнате и устройству
        
        if ((self.__device.value.dev_type == Device_type.OC_DEV) and (state in (States.OPEN, States.CLOSE))) or  \
            ((self.__device.value.dev_type == Device_type.OO_DEV) and (state in (States.ON, States.OFF))):
            # тут мы сравниваем, что бы не возникло ошибки - окно выключено и тп. in используем вместо множественного 
            # сравнения.
            self.__state = state # тут присваиваем внутренней переменной __state значение, если дверь и 
        else:                               # сделано так, что бы если не совпадает ни одно из верхних условий, 
            if self.__device.value.dev_type == Device_type.OC_DEV:       # не было ошибок, т.е. были созданы стандартными, например, если было 
                self.__state = States.CLOSE  # введено NON, мы поймем, что нужно ставить, если было введено неправильное,
            else:                           # например розетка открыта или окно включено, не было таких ошибок. так 
                self.__state = States.OFF    # называемая защита от дурака.

    @property
    def state(self) -> States:
        return self.__state
    @property
    def room(self) -> Rooms:
        return self.__room
    @property
    def device(self) -> Devices:
        return self.__device

    def Open(self):                      # создаем функцию, которой понадобятся внутренниее данные, вернет bool'евое значение
        if self.__device.value.dev_type == Device_type.OC_DEV:       # а именно True, если "успешно", False, если мы не ту функцию использовалиЮ или не 
            self.__state = States.OPEN   # получилоь (в реальном мире такое лучше делать). тут присваиваем статус. 
        else:
            raise f'Func Open need device from {OCobj}'
    
    def Close(self):                     # создаем аналогичную функцию для закрытия окон или дверей. тоже понадобятся данные, 
        if self.__device.value.dev_type == Device_type.OC_DEV:       # вернет булевое значение. 
            self.__state = States.CLOSE  # меняем статус
        else:
            raise f'Func Close need device from {OCobj}'

    def On(self):                        # теперь создаем функции для включения/выключения ламп, вентиляторов, розеток и тп.
        if self.__device.value.dev_type == Device_type.OO_DEV:       # сравниваем, входит ли в "открываемые/закрываемые"
            self.__state = States.ON
        else:
            raise f'Func On need device from {OOobj}'# если не входит в тот список, включаем, возвращаем "получилось"

    def Off(self):                       # выключение. 
        if self.__device.value.dev_type == Device_type.OO_DEV:       # сравниваем с открывающимися объектасм, если в нем:
            self.__state = States.OFF
        else:
            raise f'Func Off need device from {OOobj}'

    def __str__(self) -> str: # а тут мы возвращаем данные для вывода. иными способами будет сложно вывести все. придется это
        return f"{self.__room.name} | {self.__device.name} | {self.__state.name}" # же писать в каждом выводе, поэтому в функцию обернул.
                             # f' {ПЕРЕМЕННАЯ} ' форматирует переменные под строковой

if __name__ == '__main__':

    Kitchen_window = Devs(Rooms.KITCHEN,    # создаем объект окна на кухне. 
        Devices.WINDOW, States.CLOSE)       # состояние указывать не обязательно.
    print('ROOM    | DEVICE | STATE')       # это наш заголовок.
    print(str(Kitchen_window))              # выводим информацию про кухню: "KITCHEN | WINDOW | CLOSE"
    print(str(Devs(Rooms.BEDROOM, Devices.FAN)))  # выводим информацию о вентиляторе в спальне: "BEDROOM | FAN | OFF"
    print(Kitchen_window.__str__())
    print(str(Kitchen_window))

# Devs(__room=<Rooms.KITCHEN: 4>, __device=<Devices.WINDOW: 2>, __state=<States.CLOSE: 2>)
# KITCHEN | WINDOW | CLOSE
