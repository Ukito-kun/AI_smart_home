import time
class PID: # Пропорционально Интегрально Дифференциальный Регулятор. лучше почитать в интернете об этом
  def __init__(self, Kp, Ki, Kd, dt):
    self.Kp = Kp
    self.Ki = Ki
    self.Kd = Kd
    self.dt = dt

    self.integral = 0.0
    self.prev_error = 0.0

  def update(self, setpoint, measured_value):
    error = setpoint - measured_value

    # Пропорциональная часть
    P = self.Kp * error

    # Интегральная часть
    self.integral += error * self.dt
    I = self.Ki * self.integral

    # Дифференциальная часть
    derivative = (error - self.prev_error) / self.dt
    D = self.Kd * derivative

    self.prev_error = error

    # Итоговое управляющее воздействие
    output = P + I + D
    return output
