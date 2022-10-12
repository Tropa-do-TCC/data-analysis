import xlsxwriter

class Excel:
    def __init__(self) -> None:
        self.workbook = xlsxwriter.Workbook('Expenses02.xlsx')
        self.worksheet = self.workbook.add_worksheet()

    def generate_excel(self, ct_data: dict, network_data: dict) -> None:
        col = 1
        row = 0
        for key, value in ct_data.items():
            row = 0
            ed = value['euclidean_distance']
            self.worksheet.write(row, col, key)
            row = 2
            for i in range(9):
                print(ed[8])
                self.worksheet.write(row, col, ed[i])
                row += 1
            self.worksheet.write(row, col, value['mae'])
            col += 1

        self.worksheet.write(row + 2, 1, network_data['eigvec_per'])
        self.worksheet.write(row + 3, 1, network_data['box_size'])
        self.worksheet.write(row + 4, 1, network_data['max_test_steps'])
        self.worksheet.write(row + 5, 1, network_data['num_random_init'])
        self.worksheet.write(row + 6, 1, network_data['predict_mode'])
        self.worksheet.write(row + 7, 1, network_data['shape_model_file'])
        self.workbook.close()

    def generate_header(self):
        row = 1
        col = 0
        self.worksheet.write(row, col, 'Distancia euclidiana')
        self.worksheet.write(row+1, col, 'P1')
        self.worksheet.write(row+2, col, 'P2')
        self.worksheet.write(row+3, col, 'P3')
        self.worksheet.write(row+4, col, 'P4')
        self.worksheet.write(row+5, col, 'P5')
        self.worksheet.write(row+6, col, 'P6')
        self.worksheet.write(row+7, col, 'P7')
        self.worksheet.write(row+8, col, 'P8')
        self.worksheet.write(row+9, col, 'P9')
        self.worksheet.write(row+10, col, 'MAE')
        self.worksheet.write(row+12, col, 'eigvec_per')
        self.worksheet.write(row+13, col, 'box_size')
        self.worksheet.write(row+14, col, 'max_test_steps')
        self.worksheet.write(row+15, col, 'num_random_init')
        self.worksheet.write(row+16, col, 'predict_mode')
        self.worksheet.write(row+17, col, 'shape_model_file')
