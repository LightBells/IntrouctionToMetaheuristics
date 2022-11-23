import matplotlib

import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import functions as f
import utils.functools as ft

N = 1000 # Number of points in each dimension

if __name__ == "__main__":
    for metadatum in f.meta_informations:
        x = np.linspace(metadatum["lower_bound"], metadatum["upper_bound"], N)
        y = np.linspace(metadatum["lower_bound"], metadatum["upper_bound"], N)
        X, Y = np.meshgrid(x, y)

        partial = ft.get_partial_obj_fn(metadatum)
        unwrapped_function = ft.unwrap(partial)
        def function(x):
            return np.apply_along_axis(unwrapped_function, 1, x)

        Z = function(list(zip(X, Y)))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap=matplotlib.cm.coolwarm, linewidth=0, antialiased=False)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        plt.savefig("figures/" + metadatum["name"] + ".png")

