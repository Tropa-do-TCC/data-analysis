from typing import List
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from Landmark import Landmark
from Plot import Plot

class PlotLandmarks:
    def load_landmarks(self, filename: str) -> List[Landmark]:
        with open(filename, 'r') as file:

            ct_name = filename.split('/')[-1]

            lines = file.readlines()

            landmarks = []
            for line in lines:
                line = line.strip('\n').split(' ')
                landmarks.append(Landmark(float(line[0]), float(line[1]), float(line[2]), ct_name))

            return landmarks

    def load_all(self, directory_name: str, limit: int = 500) -> List[Landmark]:
        filenames = os.listdir(directory_name)

        landmarks = []
        i = 0
        for filename in filenames:
            if i == limit:
                break
            landmarks = landmarks + self.load_landmarks(f"{directory_name}/{filename}")
            i += 1

        return landmarks

    def show(self):
        landmarks = self.load_all(f"./landmarks_from_ct")

        x = [landmark.x for landmark in landmarks]
        y = [landmark.y for landmark in landmarks]
        z = [landmark.z for landmark in landmarks]
        ct_names = [landmark.ct_name for landmark in landmarks]

        Plot(x, y, z, ct_names).plot_ply()