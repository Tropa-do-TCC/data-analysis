from typing import List
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from Landmark import Landmark
from Plot import Plot

class PlotLandmarks:
    def load_landmarks(self, filename: str, search_file_name: list) -> List[Landmark]:
        with open(filename, 'r') as file:
            ct_name = filename.split('/')[-1]

            if ct_name.split('_')[0] in search_file_name:
                lines = file.readlines()

                landmarks = []
                for line in lines:
                    line = line.strip('\n').split(' ')
                    landmarks.append(Landmark(float(line[0]), float(line[1]), float(line[2]), ct_name))

                return landmarks

    def load_cts(self, filename: str) -> List[str]:
        with open(filename, 'r') as file:
            lines = file.readlines()
            cts = []
            for line in lines:
                line = line.replace(' ', '').strip('\n')
                cts.append(line)
        return cts

    def load_all(self, directory_name: str, search_files: str) -> List[Landmark]:
        filenames = os.listdir(directory_name)
        search_files_name = self.load_cts(search_files)

        landmarks = []
        for filename in filenames:
            landmark_path = f"{directory_name}/{filename}"
            ct_data = self.load_landmarks(landmark_path, search_files_name)
            if ct_data:
                landmarks = landmarks + ct_data

        return landmarks

    def show(self):
        landmarks = self.load_all("./landmarks_from_ct", './teste/list_to_train')

        x = [landmark.x for landmark in landmarks]
        y = [landmark.y for landmark in landmarks]
        z = [landmark.z for landmark in landmarks]
        ct_names = [landmark.ct_name for landmark in landmarks]

        Plot(x, y, z, ct_names).plot_ply()