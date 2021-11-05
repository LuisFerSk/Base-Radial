from numpy import linalg, append
from Funtions import CalculateOutput, LinearError, ActivationFunction, EuclideanDistance, ErrorG


class Neuron:
    def __init__(self, ejercicio, entradas, salidas, basesRadiales):
        self.Salidas = salidas
        self.Entradas = entradas
        self.Ejercicio = ejercicio
        self.vsErrores = [[0.1, 0.1]]
        self.BasesRadiales = basesRadiales

    def Train(self, error_maximo, funcionActivacion):
        distanciasEuclidianas = []
        for entradas in self.Entradas:
            distanciasEuclidianas.append(
                EuclideanDistance(entradas, self.BasesRadiales))

        activacion = ActivationFunction(
            funcionActivacion, distanciasEuclidianas)
        matriz = [[1], [1], [1], [1]]
        matriz = append(matriz, activacion, axis=1)
        interp = linalg.lstsq(matriz, self.Salidas, rcond=-1)[0]

        salidas = CalculateOutput(matriz, interp)

        (errorLineal, entrenamiento) = LinearError(
            self.Salidas, salidas)

        errorG = ErrorG(errorLineal)

        self.vsErrores.append([error_maximo, errorG])

        return (errorG <= error_maximo, entrenamiento, self.vsErrores, matriz, errorG)
