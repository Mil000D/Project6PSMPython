import math
import matplotlib.pyplot as plot
import matplotlib.animation as animation

x = []
v = []
y = []
a = []
Ek = []
Ep = []
Et = []
t = []
yy = []


# Calculates data needed to create simulation of a string
# for specified parameters
def calculations(rows: int, n: int, dt: float) -> None:
    l = math.pi
    dx = l / n

    t.append(0)
    for i in range(rows - 1):
        t.append(t[i] + dt)

    for i in range(n + 1):
        x.append(i * dx)
        v.append(0)
        if i == 0 or i == n:
            y.append(0)
        else:
            y.append(math.sin(x[i]))

    for i in range(n + 1):
        if i == 0 or i == n:
            a.append(0)
        else:
            a.append((y[i + 1] - 2 * y[i] + y[i - 1]) / math.pow(dx, 2))

    Ek.append(0)
    for i in range(n + 1):
        Ek[0] += dx * math.pow(v[i], 2) / 2

    Ep.append(0)
    for i in range(n):
        Ep[0] += math.pow(y[i + 1] - y[i], 2) / (2 * dx)

    Et.append(Ep[0] + Ek[0])
    y_copy = y.copy()
    yy.append(y_copy)

    for i in range(1, rows):
        y2 = []
        for j in range(n + 1):
            if j != 0 and j != n:
                y2.append(y[j] + v[j] * dt / 2)
            else:
                y2.append(0)
        for j in range(n + 1):
            if j != 0 and j != n:
                v2 = v[j] + a[j] * dt / 2
                a2 = (y2[j + 1] - 2 * y2[j] + y2[j - 1]) / math.pow(dx, 2)
                y[j] += v2 * dt
                v[j] += a2 * dt
        y_copy = y.copy()
        yy.append(y_copy)
        for j in range(n + 1):
            if j != 0 and j != n:
                a[j] = (y[j + 1] - 2 * y[j] + y[j - 1]) / dx ** 2

        Ek.append(0)
        for j in range(n + 1):
            Ek[i] += dx * (math.pow(v[j], 2)) / 2

        Ep.append(0)
        for j in range(n):
            Ep[i] += (math.pow(y[j + 1] - y[j], 2)) / (2 * dx)

        Et.append(Ep[i] + Ek[i])


# Function that displays Energy plot and simple animation of motion of a string
# using data calculated in calculations function
def show_plots(n: int) -> None:
    data = [(Ek, 'Ek'), (Ep, 'Ep'), (Et, 'Et')]
    for d in data:
        plot.plot(t, d[0], label=d[1])

    plot.xlabel('T')
    plot.ylabel('Energy')
    plot.title('Energy Plot')

    plot.legend()

    fig = plot.figure()
    ax = fig.add_subplot(111)

    line, = ax.plot([], [])

    ax.set_xlim(0, n)
    ax.set_ylim(-1, 1)

    def update(frame):
        line.set_data([], [])

        line.set_data(range(n + 1), yy[frame])

        return line,

    animate = animation.FuncAnimation(fig, update, frames=len(yy), interval=100, blit=True)
    plot.show()


# Specify number of rows, n (number of points) and dt
rows_ = 60
n_ = 20
dt_ = 0.1
calculations(rows_, n_, dt_)
show_plots(n_)
