from tkinter.ttk import Style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def Graph(frame, data, flag=True):
    fig = Figure(figsize=(5, 4), dpi=100)

    if flag:
        fig.add_subplot(111).plot([fila[0] for fila in data], 'o', [
            fila[1] for fila in data], '^')
    else:
        fig.add_subplot(111).plot(
            [fila[0] for fila in data], '-',  [fila[1] for fila in data], '--')

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().place(relwidth=1, relheight=1)


def Grid(treeView, frame):
    style = Style(frame)
    style.configure(treeView, rowheight=100, highlightthickness=0, bd=0)
    treeView.place(relheight=1, relwidth=1)


def Table(treeView, Matriz):
    treeView.delete(*treeView.get_children())
    treeView["column"] = list(Matriz.columns)
    treeView["show"] = "headings"

    for column in treeView["columns"]:
        treeView.column(column=column, width=10, anchor='center')
        treeView.heading(column=column, text=column)

    Matriz_rows1 = Matriz.to_numpy().tolist()
    for row in Matriz_rows1:
        treeView.insert("", "end", values=row)
