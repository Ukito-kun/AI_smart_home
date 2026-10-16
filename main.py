'''from devises import *
import threading, time, random
from math import sin, cos

def pogoda(t:int):
    temp = 2* (sin(t/20) + cos(t/10) + sin(t/4)) + 25  # тут не описать. открыть нужно любой калькулятор графиков и вставить туда фомулу
    return temp   # y = 2* (sin(x/20) + cos(x/10) + sin(x/4)) + 25  это очень красиво выглядит. подобрано было на угад =)

'''
import time
from queue import Queue
from threading import Thread

try:
    import readline
except ImportError:
    print("err")
    readline = None
# Рабочая функция потока (получает задачу, возвращает результат)

def inputer(to_inp_q: Queue, from_inp_q: Queue, worker_id: int):
    while True:
        i = input()
        if len(i) > 2:
            from_inp_q.put(i)
        if to_inp_q.get() != '!!!EXIT!!!':
            return 0
    return 1
def outputer(to_out_q: Queue, from_out_q: Queue, worker_id:int):
    while True:
        t = to_out_q.get()
        if t == '!!!EXIT!!!':
            return 0
        print(t)
    return 1
    

def worker(to_worker_queue: Queue, from_worker_queue: Queue, worker_id: int):
  while True:
    # Ожидаем задание от главного потока (или другого потока)
    data = to_worker_queue.get()

    print(
        f'[Поток {worker_id}] Получено задание: {data}', flush=True
    )

    if data == '!!!EXIT!!!':  # Сигнал для завершения работы
      to_worker_queue.task_done()
      break

    time.sleep(1)  # Имитация полезной работы (например, I/O-запрос)
    
    
    # Обрабатываем данные и отправляем ответ обратно
    response = f'Обработано [{data}] от потока {worker_id}'
    from_worker_queue.put(response)

    # Сообщаем очереди, что задача обработана
    to_worker_queue.task_done()


def main():
  # Создаем две очереди для двусторонней связи:
  # 1. request_queue — от главного потока к рабочему
  # 2. response_queue — от рабочего к главному потоку
  request_queue = Queue()
  response_queue = Queue()
  to_inp_q, to_out_q, from_inp_q, from_out_q = (Queue() for i in range(4))

  # Запускаем рабочий поток
  inp = Thread(
    target=inputer, args=(to_inp_q, from_inp_q, 2), daemon= True
  )
  out = Thread(
    target=outputer, args=(to_out_q, from_out_q, 3), daemon= True
    )
  t = Thread(
      target=worker, args=(request_queue, response_queue, 1), daemon=True
  )
  t.start()
  inp.start()
  out.start()

  # Отправляем данные в рабочий поток
  tasks = ['запрос_А', 'запрос_Б', 'запрос_В', ' 1', ' t ', 'exit', '4']
  for task in tasks:
    request_queue.put(task)

  # Считываем ответы из обратной очереди
  for _ in range(len(tasks)):
    result = response_queue.get()
    print(f'[Главный поток] Ответ: {result}', flush=True)
    response_queue.task_done()

  # Отправляем сигнал остановки потоку
  to_inp_q.put('!!!EXIT!!!')
  to_out_q.put('!!!EXIT!!!')
  t.join()
  out.join()
  inp.join()
  print('Работа завершена.')


if __name__ == '__main__':
  main()
