from DataAnalysis import DataAnalysis
from PlotLandmarks import PlotLandmarks

def main():
    print(f"Calculando MAE")
    DataAnalysis().data_analysis()
    print(f'Mostrando grafico')
    PlotLandmarks().show()

if __name__ == '__main__':
    main()