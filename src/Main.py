import tkinter as tk
import tkinter.ttk as ttk
import ViewsControl as vc
from Neuron import Neuron
from tkinter import filedialog
from pandas.core.frame import DataFrame
from tkinter import messagebox as MessageBox
from Funtions import ReadData, GenerateRadialBase, SaveResults

entrenar = None


def Event_btnData():
    global entrenar

    (ejercicio, matrix, entradas, salidas, basesRadiales, funcionActivacion,
        neuronas, error) = ReadData(filedialog.askopenfilename())

    entErrorMaximo.delete(0, tk.END)
    entErrorMaximo.insert(0, error)
    entNeuronas.delete(0, tk.END)
    entNeuronas.insert(0, neuronas)
    cobBoxFuncionSalida.delete(0, tk.END)
    cobBoxFuncionSalida.insert(0, funcionActivacion)

    treeView = ttk.Treeview(frameData)
    vc.Grid(treeView, frameData)
    vc.Table(treeView, matrix)

    if len(basesRadiales) == 0:
        btnInicializar['state'] = tk.NORMAL
    else:
        btnEntrenar['state'] = tk.NORMAL

    entrenar = Neuron(ejercicio, entradas, salidas, basesRadiales)

    vc.ClearFrame(frameBasesRadiales)
    vc.ClearFrame(frameSimulacionMatriz_1)
    vc.ClearFrame(frameSimulacionMatriz_2)
    vc.ClearFrame(frameSimulacion)
    vc.ClearFrame(frameEntranamiento)


def Event_btnInicializar():
    entrenar.BasesRadiales = GenerateRadialBase(entrenar.Entradas.min(),
                                                entrenar.Entradas.max(), int(entNeuronas.get()), len(entrenar.Entradas[0]))

    treeView = ttk.Treeview(frameBasesRadiales)
    vc.Grid(treeView, frameBasesRadiales)
    vc.Table(treeView, DataFrame(entrenar.BasesRadiales, columns=[
        'X' + str(x+1) for x in range(len(entrenar.BasesRadiales[0]))]))

    btnEntrenar['state'] = tk.NORMAL
    btnInicializar['state'] = tk.DISABLED


def Event_btnEntrenar():
    btnEntrenar['state'] = tk.DISABLED

    (flag, entrenamiento, vsErrores, interp, errorG) = entrenar.Train(
        float(entErrorMaximo.get()), cobBoxFuncionSalida.get())

    treeView = ttk.Treeview(frameSimulacionMatriz_1)
    vc.Grid(treeView, frameSimulacionMatriz_1)
    vc.Table(treeView, DataFrame(interp, columns=[
        'X0'] + ['FA' + str(i+1) for i in range(len(interp[0]) - 1)]))

    treeView = ttk.Treeview(frameSimulacionMatriz_2)
    vc.Grid(treeView, frameSimulacionMatriz_2)
    vc.Table(treeView, DataFrame(entrenar.Salidas, columns=[
        'YD' + str(i+1) for i in range(len(entrenar.Salidas[0]))]))

    vc.Graph(frameEntranamiento, entrenamiento)

    vc.Graph(frameSimulacion, vsErrores, False)

    btnInicializar['state'] = tk.NORMAL


def Event_btnGuardar():
    SaveResults(entrenar.Ejercicio, 'out', entrenar.Entradas, entrenar.Salidas,
                entrenar.BasesRadiales, cobBoxFuncionSalida.get(
                ), entErrorMaximo.get(), entNeuronas.get())
    MessageBox.showinfo(
        'EXITO!', '¡Se ha guardado el entranmiento sastifactoriamente!')
    filemenu.entryconfig(index="Guardar", state="disabled")


if __name__ == '__main__':
    root = tk.Tk()
    root.title("base radial")
    root.resizable(0, 0)
    root.geometry("1100x600")
    root.winfo_screenheight()
    root.winfo_screenwidth()

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Cargar datos", command=Event_btnData)
    filemenu.add_command(label="Guardar", command=Event_btnGuardar)
    filemenu.entryconfig(index="Guardar", state="disabled")
    filemenu.add_separator()
    filemenu.add_command(label="Salir", command=root.quit)

    menubar.add_cascade(label="Archivos", menu=filemenu)

    frameMain = tk.Frame(master=root, width=1100,
                         height=600, background="#e3e3e3")
    frameMain.place(relx=.0, rely=.0)

    frameConfig = tk.LabelFrame(frameMain, text="Configuración de la red")
    frameConfig.place(relx=.01, rely=.02, width=300, height=150)

    tk.Label(frameConfig, text="Error:").place(relx=.01, rely=.01)
    entErrorMaximo = tk.Entry(frameConfig, width=23)
    entErrorMaximo.place(relx=.5, rely=.01)
    entErrorMaximo.insert(0, 0.001)

    tk.Label(frameConfig, text="Número centros radiales:",
             ).place(relx=.01, rely=.2)
    entNeuronas = tk.Entry(frameConfig, width=23)
    entNeuronas.place(relx=.5, rely=.2)
    entNeuronas.insert(0, 0)

    tk.Label(frameConfig, text="Funcion de salida:",
             ).place(relx=.01, rely=.4)
    cobBoxFuncionSalida = ttk.Combobox(frameConfig)
    cobBoxFuncionSalida["values"] = [
        'BASERADIAL']
    cobBoxFuncionSalida.place(relx=.5, rely=.4)
    cobBoxFuncionSalida.insert(0, "BASERADIAL",)

    btnInicializar = tk.Button(frameConfig, text="Inicializar red", state=tk.DISABLED, command=Event_btnInicializar,
                               relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
    btnInicializar.place(relx=.01, rely=.75, width=143)

    btnEntrenar = tk.Button(frameConfig, text="Entrenar", state=tk.DISABLED, command=Event_btnEntrenar,
                            relief="flat", overrelief="flat", bg="#e3e3e3", borderwidth=2)
    btnEntrenar.place(relx=.5, rely=.75, width=143)

    frameData = tk.LabelFrame(frameMain, text="Datos de entrada")
    frameData.place(relx=.01, rely=.285, width=300, height=135)

    frameBasesRadiales = tk.LabelFrame(frameMain, text="Base radiales")
    frameBasesRadiales.place(relx=.01, rely=.52, width=300, height=135)

    frameConfigSimulacion = tk.LabelFrame(
        frameMain, text="Matriz de interpolación")
    frameConfigSimulacion.place(relx=.01, rely=.76, width=300, height=135)

    frameSimulacionMatriz_1 = tk.Frame(frameConfigSimulacion)
    frameSimulacionMatriz_1.place(relx=0, rely=.01, width=252, height=115)

    frameSimulacionMatriz_2 = tk.Frame(frameConfigSimulacion)
    frameSimulacionMatriz_2.place(relx=.86, rely=.01, width=40, height=115)

    frameEntranamiento = tk.LabelFrame(
        frameMain, text="Entrenamiento")
    frameEntranamiento.place(relx=.29, rely=.02, width=770, height=283)

    frameSimulacion = tk.LabelFrame(
        frameMain, text="Vs Error")
    frameSimulacion.place(relx=.29, rely=.513, width=770, height=283)

    root.mainloop()
