# второй набросок кода

from dataclasses import dataclass   # для классов данных, используем вместо словарей
from enum import Enum, auto         # для перечислений состояний, типов, комнат
                                    # auto() автоматически выдает порядковый номер

true = True  # я привык мелкими писать
false = False # тоже

class Devices(Enum):    # Перечисления устройств
    DOOR = auto()       # дверь 1
    WINDOW = auto()     # окно  2
    LED = auto()        # лапа  3   
    SOCKET = auto()     # розетка
    FAN = auto()        # вентилятор

OCobj = (Devices.WINDOW, Devices.DOOR)  # решил создать, чтобы не изменять в множстве мест. Open/Close Objects

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

@dataclass(init= False) # нужно для класса с данными. init=False для того, что б самостоятельно создать ф-ию __init__
class Devs:             # иначе не получится создать приватные переменные.
    _room: Rooms        # комната.      _ для приватизации. :ROOMS для объявления типа данных, перечисленных выше.
    _device: Devices    # устройство    приватные должны быть, чтоб нельзя было изменить извне. например комнату и 
    _state: States      # состояние     устройство. иначе может быть, что из вентилятора в окно и окно будет выключено.

    def __init__(self, room:Rooms, devise:Devices, state:States = States.NON):  # инициализация класса. self - внутренние
        self._room = room       # данные переменной. в ней зранятся все данные, например комната, устройство, состояние
        self._device = devise   # тут мы присваиваем данные комнате и устройству
        
        if (self._device in OCobj) & (state in (States.OPEN, States.CLOSE)):
            # тут мы сравниваем, что бы не возникло ошибки - окно выключено и тп. in используем вместо множественного 
            # сравнения.
            self._state = state # тут присваиваем внутренней переменной _state значение, если дверь и 
        elif (self._device not in OCobj) & (state in (States.ON, States.OFF)):
            self._state = state
        else:                               # сделано так, что бы если не совпадает ни одно из верхних условий, 
            if self._device in OCobj:       # не было ошибок, т.е. были созданы стандартными, например, если было 
                self._state = States.CLOSE  # введено NON, мы поймем, что нужно ставить, если было введено неправильное,
            else:                           # например розетка открыта или окно включено, не было таких ошибок. так 
                self._state = States.OFF    # называемая защита от дурака.

    def Open(self) -> bool:             # создаем функцию, которой понадобятся внутренниее данные, вернет bool'евое значение
        if self._device in OCobj:       # а именно True, если "успешно", False, если мы не ту функцию использовалиЮ или не 
            self._state = States.OPEN   # получилоь (в реальном мире такое лучше делать). тут присваиваем статус. 
            return True                 # возвращаем истину, значащую "получилось"
        else:                           # если не получилось
            return False                # возвращаем "не получилось"
    def Close(self) -> bool:            # создаем аналогичную функцию для закрытия окон или дверей. тоже понадобятся данные, 
        if self._device in OCobj:       # вернет булевое значение. 
            self._state = States.CLOSE  # меняем статус
            return True                 # возвращаем "получилось"
        else:                           # иначе
            return False                # возвращаем "не получилось"

    def On(self) -> bool:               # теперь создаем функции для включения/выключения ламп, вентиляторов, розеток и тп.
        if self._device in OCobj:       # сравниваем, входит ли в "открываемые/закрываемые"
            return False                # если да, возвращаем "не получилось", т.к. тип не правильный. мы сравниваем именно с 
        else:                           # этим списком, что бы не писать лишние буквы. в больших кодах поможет
            self._state = States.ON     # если не входит в тот список, включаем, возвращаем "получилось"
            return True                 
    def Off(self) -> bool:              # выключение. 
        if self._device in OCobj:       # сравниваем с открывающимися объектасм, если в нем:
            return False                # возвращаем ложь
        else:                           # иначе
            self._state = States.OFF    # выключаем,
            return True                 # возвращаем истину

    def state(self) -> States:  # функция для проверки статуса, можно, конечно, через Devs._state получить, но лучше взять за 
        return self._state      # привычку писать такие функции. в более сложных проектах пригодятся
    
    def pr(self) -> str:        # а тут мы возвращаем данные для вывода. иными способами будет сложно вывести все. придется это
        return f'{self._room} | {self._device} | {self._state}'.replace(    # же писать в каждом выводе, поэтому в функцию обернул.
            'Rooms.', '').replace('Devices.', '').replace('States.', '')    # f' {ПЕРЕМЕННАЯ} ' форматирует переменные под строковой
                                # формат для более красивого вывода. .replace(Т1, Т2) заменяет Т1 на Т2. они должны быть строками.
                                # тут мы их используем, что бы убрать лишние данные.
if __name__ == '__main__':

    Kitchen_window = Devs(Rooms.KITCHEN,    # создаем объект окна на кухне. 
        Devices.WINDOW, States.CLOSE)       # состояние указывать не обязательно.
    print('ROOM    | DEVICE | STATE')       # это наш заголовок.
    print(Kitchen_window.pr())              # выводим информацию про кухню: "KITCHEN | WINDOW | CLOSE"
    print(Devs(Rooms.BEDROOM, Devices.FAN).pr())  # выводим информацию о вентиляторе в спальне: "BEDROOM | FAN | OFF"
    print(Kitchen_window.pr())

# Devs(_room=<Rooms.KITCHEN: 4>, _device=<Devices.WINDOW: 2>, _state=<States.CLOSE: 2>)
# KITCHEN | WINDOW | CLOSE
