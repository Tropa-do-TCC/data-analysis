from os import listdir
from os.path import isfile, join
import glob
import numpy as np
import math
from pdb import set_trace

class DataAnalasys:

    def __init__(self) -> None:
        self.path_to_predicted_landmarks = "./results/landmarks/test/"
        self.path_to_original_landmarks = "./landmarks_from_ct/"

    def get_landmarks(self, read_file: str) -> dict:
        try:
            landmark_number = 0
            landmarks = {}
            with open(read_file, 'r') as file:
                for row in file:
                    row = row.split()
                    landmarks[landmark_number] = list(map(float, row))
                    landmark_number += 1
                return landmarks
        except Exception as ex:
            print(ex)

    def calculate_mae(self, original_landmarks: dict, predicted_landmarks: dict) -> float:
        result = []
        for key, value in original_landmarks.items():
            ol_x, ol_y, ol_z = value
            pl_x, pl_y, pl_z = predicted_landmarks[key]
            result.append(math.dist([ol_x, ol_y, ol_z], [pl_x, pl_y, pl_z]))
        return np.mean(result)

    def main(self):
        predicted_landmarks_files = glob.glob(self.path_to_predicted_landmarks + "*.txt")
        result = []
        try:
            for predicted_file in predicted_landmarks_files:
                file_name = predicted_file.split('/')[-1]
                original_file_name = self.path_to_original_landmarks + file_name
                original_landmarks = self.get_landmarks(original_file_name)
                predicted_landmarks = self.get_landmarks(predicted_file)
                print(self.calculate_mae(original_landmarks, predicted_landmarks))
        except Exception as ex:
            print(ex)

DataAnalasys().main()