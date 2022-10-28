import matplotlib.pyplot as plt
import math

def accuracy(original_landmarks, predicted_landmarks, accepted_range = 3) -> float:
        positive_cases = 0
        for ct_name, landmarks in original_landmarks.items():
            for landmark_number, value in landmarks.items():
                ol_x, ol_y, ol_z = value
                pl_x, pl_y, pl_z = predicted_landmarks[ct_name][landmark_number]
                if math.dist([ol_x, ol_y, ol_z], [pl_x, pl_y, pl_z]) <= accepted_range:
                    positive_cases += 1
        return positive_cases / (len(original_landmarks) * 9)

def show(original_landmarks, predicted_landmarks):
    area_array = []
    accuracy_array = []
    for area in range(1, 30):
        accuracy_array.append(accuracy(original_landmarks, predicted_landmarks, area))
        area_array.append(area)
    plt.plot(area_array, accuracy_array)
    plt.title('Range Vs Accuracy')
    plt.xlabel('Range')
    plt.ylabel('Accuracy')
    plt.show()