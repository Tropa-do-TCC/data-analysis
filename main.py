from DataAnalysis import DataAnalysis
from PlotLandmarks import PlotLandmarks
from excel import Excel
from pdb import set_trace
from PlotAccuracy import show

def main():
    #print(f"Calculando MAE")
    network_data, ct_data, ct_errors, original_landmarks, predicted_landmarks = DataAnalysis().data_analysis()
    show(original_landmarks, predicted_landmarks)
    #print(f'Mostrando grafico')
    #PlotLandmarks().show()
    #excel = Excel()
    #excel.generate_header()
    #excel.generate_excel(ct_data, ct_errors, network_data)

if __name__ == '__main__':
    main()