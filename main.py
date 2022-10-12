from DataAnalysis import DataAnalysis
from PlotLandmarks import PlotLandmarks
from excel import Excel
from pdb import set_trace

def main():
    print(f"Calculando MAE")
    dataAnalysis = DataAnalysis()
    network_data, ct_data = dataAnalysis.data_analysis()
    #print(f'Mostrando grafico')
    #PlotLandmarks().show()
    excel = Excel()
    excel.generate_header()
    excel.generate_excel(ct_data, network_data)

if __name__ == '__main__':
    main()