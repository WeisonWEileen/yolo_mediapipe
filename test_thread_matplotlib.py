import threading
import numpy as np
import matplotlib.pyplot as plt

def plot_sine_wave(x, y):
    plt.plot(x, np.sin(y))
    plt.show()

x = np.linspace(0, 2*np.pi, 100)
threads = []
for i in range(4):
    t = threading.Thread(target=plot_sine_wave, args=(x, x+i*0.1))
    threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()
