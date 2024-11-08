import numpy as np

class PowerSerie():

    cn = 1
    center = 0
    power = 1

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
        s_x = [] # s(x) -> list of summation of the serie for each x from x_list

        for _ in x_list:
            s_x.append(0) # init s(x) = 0 for all x

        for k in range(k_start, k_end + 1):
            for i in range(len(x_list)):
                x = x_list[i]
                s_x[i] += self.cn(k) * pow((x - self.center), k * self.power)

        return (x_list, s_x)
        

BasicPower = PowerSerie(cn=lambda k : 1/(k*k))
print(BasicPower.compute(x_a=0, x_b=5, k_a=1, k_b=5))