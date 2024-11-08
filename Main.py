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
                k_a: int = 1, k_b: int = 100,):
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

    def plot_serie(self, axis):
        axis.scatter(self.x_samples, self.y_container)
        axis.plot(self.x_samples, self.y_container)



def pSeries(k):
    return 1 / (k*k)

BasicPower = PowerSerie(cn=pSeries, center=5)
x_container, y_container = BasicPower.compute(x_a=3, x_b=7, k_a=1, k_b=100)

# plot
fig, axis = plt.subplots(1, 1)

BasicPower.plot_serie(axis)

plt.show()