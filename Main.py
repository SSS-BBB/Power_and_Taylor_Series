import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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

class PowerSerieWithAnim():

    def __init__(self, cn: callable, anim_plot,
                 center: int = 0, power: float = 1, 
                 x_a: float = -10, x_b: float = 10, x_step: float = 1,
                k_a: int = 0, k_b: int = 100, total_frames: int = -1):
        self.cn = cn
        self.anim_plot = anim_plot
        self.center = center
        self.power = power

        self.x_min = x_a
        self.x_max = x_b
        if x_a > x_b:
            self.x_min = x_b
            self.x_max = x_a

        self.k_start = k_a
        self.k_end = k_b
        if k_a > k_b:
            self.k_start = k_b
            self.k_end = k_a

        self.x_step = x_step

        self.x_samples = np.arange(self.x_min, self.x_max + x_step, x_step)

        # init all value to 0 before summing up
        self.y_container = []
        for _ in self.x_samples:
            self.y_container.append(0)

        self.k_f = self.k_start # current k in each frame

        # calculate k step for each frmae
        # example: k = 1 - 100, total_frames = 10, then k_step = 10

        if total_frames <= 0:
            total_frames = self.k_end - self.k_start

        k_by_frame = (self.k_end - self.k_start) / total_frames
        self.k_step = math.ceil(k_by_frame)
        self.total_frames = total_frames


    def compute(self, frame):
        if self.k_f > self.k_end:
            return self.anim_plot

        # update value
        for i in range(self.x_samples.size):
            for k in range(self.k_f, self.k_f + self.k_step):
                x = self.x_samples[i]
                self.y_container[i] += self.cn(k) * math.pow((x - self.center), k * self.power)

        # plot
        self.anim_plot.set_data(self.x_samples, np.array(self.y_container))

        self.k_f += self.k_step

        return self.anim_plot

class TaylorSerie(PowerSerie):
    
    def __init__(self, fk_x0: callable, center = 0):
        cn = lambda k:  fk_x0(k, center) / math.factorial(k)
        super().__init__(cn, center, 1)

# Power = PowerSerie(cn = lambda k: math.pow(-1, k) / (math.pow(4, k)*(k + 5)), center=1)
# Power.compute(x_a=-4, x_b=6)

# plot
fig, axis = plt.subplots()

# Power.plot_serie(axis)

# def fk(k, x0):
#     remainder = k % 4
#     if remainder == 0:
#         return math.sin(x0)
#     elif remainder == 1:
#         return math.cos(x0)
#     elif remainder == 2:
#         return -math.sin(x0)

#     return -math.cos(x0)

# Taylor = PowerSerie(cn=lambda k: math.pow(-1, k+1) / k, center=1)

# Taylor.compute(x_a=0.1, x_b=2, x_step=0.1, k_a=1, k_b=5)
# Taylor.plot_serie(axis, label="Series")

# axis.plot(Taylor.x_samples, np.log(Taylor.x_samples), label="Function")

# anim plot
anim_plot, = axis.plot([], [])
Taylor = PowerSerieWithAnim(cn=lambda k: 1 / math.factorial(k), 
                            center=0, anim_plot=anim_plot,
                            k_a=1, k_b=50, x_a=-10, x_b=10, x_step=1)

axis.plot(Taylor.x_samples, np.exp(Taylor.x_samples), label="Function", linewidth=0.75) # plot real function

anim = FuncAnimation(fig=fig, func=Taylor.compute, frames=Taylor.total_frames, interval=300)

anim.save("Taylor_Series.gif")

axis.legend()
plt.show()