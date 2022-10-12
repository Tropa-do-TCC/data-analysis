class Landmark:
    def __init__(self, x: float, y: float, z: float, ct_name:str = ''):
        self.x = x
        self.y = y
        self.z = z
        self.ct_name = ct_name

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"