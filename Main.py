import numpy as np
import matplotlib.pyplot as plt
import math

class PowerSerie():

    center = 0
    power = 1

    x_samples = np.array([])
    y_container = np.array([])

    def __init__(self, cn: callable, center: int = 0, power: float = 1):
        self.cn = cn
        self.center = center
        self.power = power

    def compute(self, x_a: float = -10, x_b: float = 10, x_step: float = 1,
                k_a: int = 0, k_b: int = 100):
        x_min = x_a
        x_max = x_b
        if x_a > x_b:
            x_min = x_b
            x_max = x_a

        k_start = k_a
        k_end = k_b
        if k_a > k_b:
            k_start = k_b
            k_end = k_a

        x_list = np.arange(x_min, x_max + x_step, x_step) # list of all x that are used to calculate the function
        s = [] # s(x) -> list of summation of the serie for each x from x_list

        for x in x_list:
            s_x = 0
            for k in range(k_start, k_end + 1):
                s_x += self.cn(k) * math.pow((x - self.center), k * self.power)

            s.append(s_x)

        self.x_samples = x_list
        self.y_container = np.array(s)

        return (x_list, np.array(s))

    def plot_serie(self, axis, label=""):
        axis.scatter(self.x_samples, self.y_container)
        axis.plot(self.x_samples, self.y_container, label=label)

class TaylorSerie(PowerSerie):
    
    def __init__(self, fk_x0: callable, center = 0):
        cn = lambda k:  fk_x0(k, center) / math.factorial(k)
        super().__init__(cn, center, 1)

# Power = PowerSerie(cn = lambda k: math.pow(-1, k) / (math.pow(4, k)*(k + 5)), center=1)
# Power.compute(x_a=-4, x_b=6)

# plot
fig, axis = plt.subplots(1, 1)

# Power.plot_serie(axis)

def fk(k, x0):
    remainder = k % 4
    if remainder == 0:
        return math.sin(x0)
    elif remainder == 1:
        return math.cos(x0)
    elif remainder == 2:
        return -math.sin(x0)

    return -math.cos(x0)

TaylorSerie = TaylorSerie(fk)

TaylorSerie.compute()
TaylorSerie.plot_serie(axis, label="E Series")

axis.plot(TaylorSerie.x_samples, np.sin(TaylorSerie.x_samples), label="E Function")

axis.legend()
plt.show()