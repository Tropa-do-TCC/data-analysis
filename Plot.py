from typing import List
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from Landmark import Landmark


class Plot:

    def __init__(self, x, y, z, ct_names) -> None:
        self.x = x
        self.y = y
        self.z = z
        self.ct_names = ct_names
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')

    def distance(self, x_point, y_point, z_point, event):
        # Project 3d data space to 2d data space
        x2, y2, _ = proj3d.proj_transform(
            x_point, y_point, z_point, plt.gca().get_proj())
        # Convert 2d data space to 2d screen space
        x3, y3 = self.ax.transData.transform((x2, y2))

        return np.sqrt((x3 - event.x)**2 + (y3 - event.y)**2)

    def calcClosestDatapoint(self, event):
        """"Calculate which data point is closest to the mouse position."""
        distances = [self.distance(
            self.x[i], self.y[i], self.z[i], event) for i in range(len(self.x))]
        return np.argmin(distances)

    def onMouseMotion(self, event):
        """Event that is triggered when mouse is moved. Shows text annotation over data point closest to mouse."""
        closestIndex = self.calcClosestDatapoint(event)
        self.annotatePlot(closestIndex)

    def annotatePlot(self, index):
        # If we have previously displayed another label, remove it first
        if hasattr(self, 'label'):
            self.label.remove()
        # Get data point from array of points X, at position index
        x2, y2, _ = proj3d.proj_transform(
            self.x[index], self.y[index], self.z[index], self.ax.get_proj())
        self.label = plt.annotate(self.ct_names[index],
                                  xy=(x2, y2), xytext=(-20, 20), textcoords='offset points', ha='right', va='bottom',
                                  bbox=dict(boxstyle='round,pad=0.5',
                                            fc='yellow', alpha=0.5),
                                  arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        self.fig.canvas.draw()

    def plot_ply(self):
        self.ax.scatter(self.x, self.y, self.z, c=self.y, marker='o', s=3)

        tmp_planes = self.ax.zaxis._PLANES
        self.ax.zaxis._PLANES = (tmp_planes[2], tmp_planes[3],
                                 tmp_planes[0], tmp_planes[1],
                                 tmp_planes[4], tmp_planes[5])

        self.ax.set_xlabel('X Label')
        self.ax.set_ylabel('Y Label')
        self.ax.zaxis.set_rotate_label(False)
        self.ax.set_zlabel('Z Label', rotation=90)

        self.fig.canvas.mpl_connect('motion_notify_event', self.onMouseMotion)
        plt.show()
