import json
import os
from random import choice, randrange, uniform

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from chronus.domain.Run import Run


def fake_data() -> list[Run]:
    # check if data set is cached in file
    file_path = "/home/anders/projects/chronus/out/chronus_fake_run.json"
    if os.path.isfile(file_path):
        data = json.load(open(file_path))
        return [Run.from_dict(d) for d in data]

    runs = []
    fan_speeds = [1000, 1500, 2000, 2500]
    cpu_temps = [50.0, 60.0, 70.0, 80.0]
    cpu_cores = [1, 2, 4, 8, 16, 32, 48, 64]
    gflops_range = (10.0, 500.0)
    watts_range = (50, 250)
    for i in range(50):
        watts = randrange(*watts_range)
        core_count = choice(cpu_cores)
        core_frequency = uniform(1, 3.6)
        gflops = core_count * core_frequency
        runs.append(Run(0, 0, core_count, core_frequency, int(gflops), watts))

    # save data for caching
    json.dump([r.to_dict() for r in runs], open(file_path, "w"))

    return runs


def plot_energy():
    data = fake_data()
    # 3d plot with watt, gflops, cpu cores

    x = [r.watts for r in data]
    y = [r.cpu_cores for r in data]
    z = [r.gflops for r in data]

    # Plot the 3D scatter plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z, c=z, cmap="hot", marker="o")
    ax.set_xlabel("Watts")
    ax.set_ylabel("Core Count")
    ax.set_zlabel("GFLOPS")
    plt.show()
