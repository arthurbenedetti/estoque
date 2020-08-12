import tkinter as tk
from tkinter import ttk


class MainView(tk.Frame):

    def __init__(self, root, controller):
        tk.Frame.__init__(self, root)
        self.root = root
        self.controller = controller

        self.buttons = []
        self.tables = {}
        self.children = {}

        self.grid(sticky="nsew")
        self.loadGraphics()

    def createButtons(self):
        self.buttons.append(tk.Button(self.root, text="Criar Novo Produto", command=lambda: self.controller.createNewProduct()))
        self.buttons.append(tk.Button(self.root, text="Adicionar Unidades", command=lambda: self.controller.addUnitsToProduct()))
        self.buttons.append(tk.Button(self.root, text="Remover Unidades", command=lambda: self.controller.removeUnitsFromProduct()))
        self.buttons.append(tk.Button(self.root, text="Excluir Produto", command=lambda: self.controller.deleteProduct()))

    def loadButtons(self):
        for index, button in enumerate(self.buttons):
            button.grid(row=0, column=index, padx=0, pady=10)

    def createTables(self):
        self.tables['products'] = {'frame': tk.LabelFrame(self.root, text="Produtos", height=300, width=400),
                                   'tree': None}
        self.tables['products']['tree'] = ttk.Treeview(self.tables['products']['frame'], columns=(1, 2, 3, 4, 5), show="headings", height="13")

    def loadTables(self):
        self.tables['products']['frame'].grid(row=1, columnspan=4, padx=10, pady=10)
        self.tables['products']['tree'].pack()

        self.tables['products']['tree'].heading(1, text="Nome do Produto")
        self.tables['products']['tree'].heading(2, text="Tipo do Recipiente")
        self.tables['products']['tree'].heading(3, text="Valor Crítico")
        self.tables['products']['tree'].heading(4, text="Estoque Atual")
        self.tables['products']['tree'].heading(5, text="ID")

        scroll = ttk.Scrollbar(self.root, orient='vertical', command=self.tables['products']['tree'])
        scroll.place(x=971, y=75, height=283)

        self.tables['products']['tree'].bind('<ButtonRelease-1>', lambda Treeview: self.select_item(self.tables['products']['tree']))

    def setupRootFrame(self):
        self.root.title("Controle de Estoque - HU")
        self.root.geometry("1000x380")

        for col in range(4):
            self.root.grid_columnconfigure(col, weight=1)

    def loadGraphics(self):
        self.setupRootFrame()

        self.createButtons()
        self.loadButtons()
        self.createTables()
        self.loadTables()

    def select_item(self, treeview):
        """Selects line in table of type treeview"""
        treeItems = treeview.selection()
        wholeData = []
        for item in treeItems:
            wholeData.append(treeview.item(item)['values'])
        return wholeData


if __name__ == "__main__":
    pass
