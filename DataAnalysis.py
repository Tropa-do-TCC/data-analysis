from pdb import set_trace
from os import listdir
from os.path import isfile, join
import glob
import numpy as np
import math
from sklearn.metrics import mean_absolute_error as mae
from scipy.spatial import distance

class DataAnalysis:

    def __init__(self) -> None:
        self.path_to_infer = './teste/infer.py'
        self.path_to_train = './teste/train.py'
        self.path_to_predicted_landmarks = "./teste/results/landmarks/test/"
        self.path_to_original_landmarks = "./landmarks_from_ct/"
        self.path_to_dist_error = "./teste/results/dist_err/"

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

    def get_error(self, file: str):
        result = {}
        is_pixel = True
        with open(file, 'r') as file:
            for row in file:
                row = row.strip('\n')
                if row.split('(')[-1] == 'mm)': is_pixel = False
                row = row.split(':')
                if row[0] in ['Mean', 'Standard deviation']:
                    type = 'pixel' if is_pixel else 'mm'
                    name = f'{row[0]} {type}'
                    result[name] = row[1].replace(' ', '')
        return result


    def calculate_euclidean_distance(self, original_landmarks: dict, predicted_landmarks: dict) -> float:
        result = []
        for key, value in original_landmarks.items():
            ol_x, ol_y, ol_z = value
            pl_x, pl_y, pl_z = predicted_landmarks[key]
            #result.append(math.dist([ol_x, ol_y, ol_z], [pl_x, pl_y, pl_z]))
            result.append(distance.euclidean((ol_x, ol_y, ol_z), (pl_x, pl_y, pl_z)))
        return result

    def calculate_euclidean_mean(self, euclidean_distance: list) -> float:
        return np.mean(euclidean_distance)

    def infer_data(self):
        result = {}
        with open(self.path_to_infer, 'r') as file:
            for line in file:
                line = line.strip('\n').replace(' ', '').split("=")
                if line[0] in ['predict_mode', 'num_random_init', 'max_test_steps', 'box_size', 'eigvec_per']:
                    line[1] = line[1].split('#')[0]
                    result[line[0]] = float(line[1])
                    if line[0] == 'predict_mode':
                        break
        return result


    def train_data(self):
        result = {}
        with open(self.path_to_train, 'r') as file:
            for line in file:
                line = line.strip('\n').replace(' ', '').split("=")
                if line[0] in ['shape_model_file']:
                    line[1] = line[1].strip("'").strip(" ").split('/')[-1]
                    result[line[0]] = line[1].split('/')[-1]
        return result

    def accuracy(self, original_landmarks, predicted_landmarks, accepted_range = 3) -> float:
        positive_cases = 0
        for ct_name, landmarks in original_landmarks.items():
            for landmark_number, value in landmarks.items():
                ol_x, ol_y, ol_z = value
                pl_x, pl_y, pl_z = predicted_landmarks[ct_name][landmark_number]
                if math.dist([ol_x, ol_y, ol_z], [pl_x, pl_y, pl_z]) <= accepted_range:
                    positive_cases += 1
        return positive_cases / (len(original_landmarks) * 9)

    def data_analysis(self):
        predicted_landmarks_files = glob.glob(self.path_to_predicted_landmarks + "*.txt")
        result = {}
        all_original_landmarks = {}
        all_predicted_landmarks = {}
        ignored_files = ['CT-151_ps.txt', 'CT-408_ps.txt', 'CT-413_ps.txt', 'CT-415_ps.txt', 'CT-424_ps.txt', 'CT-426_ps.txt', 'CT-432_ps.txt']
        try:
            for predicted_file in predicted_landmarks_files:
                file_name = predicted_file.split('/')[-1]
                if file_name in ignored_files:
                    continue

                original_file_name = self.path_to_original_landmarks + file_name
                original_landmarks = self.get_landmarks(original_file_name)
                predicted_landmarks = self.get_landmarks(predicted_file)

                all_original_landmarks[file_name] = original_landmarks
                all_predicted_landmarks[file_name] = predicted_landmarks

                euclidean_distance = self.calculate_euclidean_distance(original_landmarks, predicted_landmarks)


                original_landmarks_join = sum(original_landmarks.values(), [])
                predicted_landmarks_join = sum(predicted_landmarks.values(), [])

                result[file_name] = {
                    'euclidean_distance': euclidean_distance,
                    'mean_euclidean_distance': self.calculate_euclidean_mean(euclidean_distance),
                    'mae': mae(original_landmarks_join, predicted_landmarks_join)
                }

            network_data = self.infer_data()
            network_data.update(self.train_data())

            errors_files = predicted_landmarks_files = glob.glob(self.path_to_dist_error + "*.txt")

            ct_errors = {}

            for predicted_file in errors_files:
                file_name = predicted_file.split('/')[-1]
                try:
                    file_name = file_name[file_name.index('CT-'):].split('.')[0]
                except:
                    file_name = "CT-" + file_name[file_name.index('-')+1:].split('.')[0]

                compare = file_name + '_ps.txt'
                if compare not in ignored_files:
                    ct_errors.setdefault(file_name, self.get_error(predicted_file))

            return  network_data, result, ct_errors, all_original_landmarks, all_predicted_landmarks
        except Exception as ex:
            print(ex)