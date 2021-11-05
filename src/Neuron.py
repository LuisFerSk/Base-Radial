from numpy import linalg, append, ones
from Funtions import CalculateOutput, LinearError, ActivationFunction, EuclideanDistance, ErrorG


class Neuron:
    def __init__(self, ejercicio, entradas, salidas, basesRadiales):
        self.Salidas = salidas
        self.Entradas = entradas
        self.Ejercicio = ejercicio
        self.matrizErrores = [[0.1, 0.1]]
        self.BasesRadiales = basesRadiales

    def Train(self, errorMaximo, funcionActivacion):
        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(
                EuclideanDistance(entradas, self.BasesRadiales))

        activacion = ActivationFunction(
            funcionActivacion, distanciasEuclidianas)
        matrizInterpolacion = ones((len(activacion), 1))
        matrizInterpolacion = append(matrizInterpolacion, activacion, axis=1)
        interp = linalg.lstsq(matrizInterpolacion, self.Salidas, rcond=-1)[0]

        salidas = CalculateOutput(matrizInterpolacion, interp)

        (errorLineal, entrenamiento) = LinearError(
            self.Salidas, salidas)

        errorG = ErrorG(errorLineal)

        self.matrizErrores.append([errorMaximo, errorG])

        return (errorG <= errorMaximo, entrenamiento, self.matrizErrores, matrizInterpolacion, errorG)
