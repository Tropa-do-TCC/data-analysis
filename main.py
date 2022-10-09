from typing import List
import os
import matplotlib.pyplot as plt


class Landmark:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"


def load_landmarks(filename: str) -> List[Landmark]:
    file = open(filename, 'r')

    lines = file.readlines()

    landmarks = []
    for line in lines:
        line = line.strip('\n').split(' ')
        landmarks.append(Landmark(float(line[0]), float(line[1]), float(line[2])))

    return landmarks


def load_all(directory_name: str) -> List[Landmark]:
    filenames = os.listdir(directory_name)

    landmarks = []
    i = 0
    for filename in filenames:
        if i == 500:
            break
        landmarks = landmarks + load_landmarks(f"{directory_name}/{filename}")
        i += 1

    return landmarks


def plot_ply(x, y, z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c=y, marker='o', s=3)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()


def main():
    landmarks = load_all(f"./points")

    for landmark in landmarks:
        print(landmark)

    x = [landmark.x for landmark in landmarks]
    y = [landmark.y for landmark in landmarks]
    z = [landmark.z for landmark in landmarks]

    plot_ply(x, y, z)


if __name__ == '__main__':
    main()
