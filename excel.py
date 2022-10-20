import xlsxwriter
import numpy as np

class Excel:
    def __init__(self) -> None:
        self.workbook = xlsxwriter.Workbook('Expenses02.xlsx')
        self.worksheet = self.workbook.add_worksheet()

    def generate_excel(self, ct_data: dict, ct_errors: dict, network_data: dict) -> None:
        col = 0
        row = 1
        media_geral = []
        for key, value in ct_data.items():
            col = 0
            ed = value['euclidean_distance']
            key = key.split("_")[0]
            self.worksheet.write(row, col, key)
            col += 1
            for i in range(9):
                self.worksheet.write(row, col, float("{:.3f}".format(ed[i])))
                media_geral.append(ed[i])
                col += 1
            self.worksheet.write(row, col, float("{:.3f}".format(value['mae'])))

            for label in ['Mean mm', 'Standard deviation mm', 'Mean pixel', 'Standard deviation pixel']:
                col += 1
                self.worksheet.write(row, col, float("{:.3f}".format(float(ct_errors[key][label]))))
            row += 1

        self.worksheet.write(1, col + 2, float("{:.3f}".format(np.mean(media_geral))))
        self.worksheet.write(1, col + 3, network_data['eigvec_per'])
        self.worksheet.write(1, col + 4, network_data['box_size'])
        self.worksheet.write(1, col + 5, network_data['max_test_steps'])
        self.worksheet.write(1, col + 6, network_data['num_random_init'])
        self.worksheet.write(1, col + 7, network_data['predict_mode'])
        self.worksheet.write(1, col + 8, network_data['shape_model_file'])
        self.workbook.close()

    def generate_header(self):
        header = ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'MAE', 'Mean mm',
                  'Standard deviation mm', 'Mean pixel', 'Standard deviation pixel', 'media geral', 'eigvec_per',
                  'box_size', 'max_test_steps', 'num_random_init', 'predict_mode', 'shape_model_file']
        row = 0
        col = 1
        for label in header:
            self.worksheet.write(row, col, label)
            col += 1
            if label == 'Standard deviation pixel': #label == "MAE":
                col += 1