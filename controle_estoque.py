#!/usr/bin/env python3.5

import datetime
import tkinter
import sqlite3
from tkinter import ttk
from sqlite3 import Error
from tkinter.ttk import *
from tkinter import messagebox


def search(treeview, comparevalue):
    # checa se valor ja exite na tabela Treeview
    children = treeview.get_children('')
    for child in children:
        values = treeview.item(child, 'values')
        if comparevalue[4] == values[4] and str(comparevalue[0]) == str(values[0]):
            return True
    return False


def updateProduto():
    # produtos são colocados na tabela da GUI
    # pega dados do Produto no sql
    conn = sqlite3.connect("estoqueRe.db")
    # create cursor
    cur = conn.cursor()
    cur.execute("SELECT nome_produto, recipiente, valorCritico, estoque, ID FROM Produto")
    rows = cur.fetchall()

    # deleta tudo na treeview
    for i in tabelaProdutoTree.get_children():
        tabelaProdutoTree.delete(i)

    # atualiza os dados
    for i in rows:
        cur.execute("SELECT COUNT(*) FROM UnidadeE WHERE ID =" + str(i[4]))
        unidadesProdutoE = cur.fetchall()
        cur.execute("SELECT COUNT(*) FROM UnidadeS WHERE ID =" + str(i[4]))
        unidadesProdutoS = cur.fetchall()
        novoEstoque = unidadesProdutoE[0][0] - unidadesProdutoS[0][0]
        novoEstoqueint = int(novoEstoque)
        novoEstoqueStr = str(novoEstoqueint)
        cur.execute("UPDATE Produto SET estoque=" + novoEstoqueStr + " WHERE ID=" + str(i[4]))

    conn.commit()
    conn.close()

    # pega os produtos atualizados
    conn = sqlite3.connect("estoqueRe.db")
    cur = conn.cursor()
    cur.execute("SELECT nome_produto, recipiente, valorCritico, estoque, ID FROM Produto")
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for i in rows:
        if i[3] <= i[2]:
            tabelaProdutoTree.insert('', 'end', values=i, tags="crit")
            tabelaProdutoTree.tag_configure("crit", background='red')
        else:
            tabelaProdutoTree.insert('', 'end', values=i, tags="Ncrit")
            tabelaProdutoTree.tag_configure("Ncrit", background='white')


def submitProduto(NomeProduto, TipoRecipiente, ValorCritico, window):
    # adiciona um produto ao sql
    conn = None
    try:
        conn = sqlite3.connect("estoqueRe.db")
        cur = conn.cursor()

        # insert into table
        if len(NomeProduto.get()) <= 0 or len(TipoRecipiente.get()) <= 0 or len(ValorCritico.get()) <= 0 or type(NomeProduto.get()) != str or type(TipoRecipiente.get()) != str:
            messagebox.showwarning("Atenção", "Os dados inseridos para criação do produto não correspondem ao tipo correto")
        else:
            cur.execute("SELECT * FROM Produto")
            IDproduto = len(cur.fetchall())

            cur.execute("INSERT INTO Produto VALUES (:nome_produto, :recipiente, :valorCritico, :estoque, :ID)",
                        {
                            'nome_produto': NomeProduto.get(),
                            'recipiente': TipoRecipiente.get(),
                            'valorCritico': ValorCritico.get(),
                            'estoque': 0,
                            'ID': IDproduto
                        }
                        )
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.commit()
            conn.close()
            updateProduto()
            window.destroy()


def janelaProduto():
    # cria a janela para criar um novo produto
    newWindow = tkinter.Toplevel()
    newWindow.title("Criar novo produto")
    newWindow.geometry("400x300")

    entryNomeProduto = tkinter.Entry(newWindow, width=30)
    entryNomeProduto.grid(row=0, column=1, padx=10, pady=10)
    labelNomeProduto = tkinter.Label(newWindow, text="Nome do produto: ")
    labelNomeProduto.grid(row=0, column=0, padx=10, pady=10)

    entryTipoRecipiente = tkinter.Entry(newWindow, width=30)
    entryTipoRecipiente.grid(row=1, column=1, padx=10, pady=10)
    labelTipoRecipiente = tkinter.Label(newWindow, text="Unidade: ")
    labelTipoRecipiente.grid(row=1, column=0, padx=10, pady=10)

    entryValorCritico = tkinter.Entry(newWindow, width=30)
    entryValorCritico.grid(row=2, column=1, padx=10, pady=10)
    labelValorCritico = tkinter.Label(newWindow, text="Valor critico: ")
    labelValorCritico.grid(row=2, column=0, padx=10, pady=10)

    buttonCancela = tkinter.Button(newWindow, text="Cancelar", command=newWindow.destroy)
    buttonCancela.grid(row=5, column=0, padx=10, pady=140, ipadx=50)
    buttonSubmit = tkinter.Button(newWindow, text="OK", command=lambda: submitProduto(entryNomeProduto, entryTipoRecipiente, entryValorCritico, newWindow))
    buttonSubmit.grid(row=5, column=1, padx=10, pady=140, ipadx=50)


def janelaAdicionar():
    # cria janela para adicionar unidades ao produto
    def nomeJanela(optionNomes):
        def nomeSubmit(nome):
            optionNomes["menu"].add_command(label=nome, command=tkinter._setit(clicked, nome))
            nameWindow.destroy()

        nameWindow = tkinter.Toplevel()
        nameWindow.title("Nome")
        nameWindow.geometry("270x100")

        nomeEntry = tkinter.Entry(nameWindow, width=20)
        nomeEntry.grid(row=0, column=1, padx=10, pady=10)
        nomeLabel = tkinter.Label(nameWindow, text="Nome: ")
        nomeLabel.grid(row=0, column=0, padx=10, pady=10)

        buttonSubmit = tkinter.Button(nameWindow, text="OK", command=lambda: nomeSubmit(nomeEntry.get()))
        buttonSubmit.grid(row=1, column=1, padx=10, pady=10, ipadx=20)
        buttonCancela = tkinter.Button(nameWindow, text="Cancelar", command=lambda: nameWindow.destroy)
        buttonCancela.grid(row=1, column=0, padx=10, pady=10, ipadx=20)

    conn = sqlite3.connect("estoqueRe.db")
    cur = conn.cursor()
    nomes = []
    duplicates = []
    produtoSelecionado = select_item(tabelaProdutoTree)

    if len(produtoSelecionado) > 0:
        cur.execute("SELECT funEntrada FROM UnidadeE")
        nomeTabela = cur.fetchall()
        for nome in nomeTabela:
            nomes.append(nome[0])
        cur.execute("SELECT funSaida FROM UnidadeS")
        nomeTabelaS = cur.fetchall()
        for nome in nomeTabelaS:
            nomes.append(nome[0])

        nomes.append("nenhum")
        for i in nomes:
            if i not in duplicates:
                duplicates.append(i)

        newWindow = tkinter.Toplevel()
        newWindow.title("Adicionar unidades")
        newWindow.geometry("370x200")

        entryValidade = tkinter.Entry(newWindow, width=30)
        entryValidade.grid(row=0, column=1, padx=10, pady=10)
        labelValidade = tkinter.Label(newWindow, text="Validade (dd/mm/aaaa): ")
        labelValidade.grid(row=0, column=0, padx=10, pady=10)

        entryQuantidade = tkinter.Entry(newWindow, width=10)
        entryQuantidade.grid(row=1, column=1, padx=10, pady=10)
        labelQuantidade = tkinter.Label(newWindow, text="Quantidade: ")
        labelQuantidade.grid(row=1, column=0, padx=10, pady=10)

        clicked = tkinter.StringVar(newWindow)
        optionNomes = tkinter.OptionMenu(newWindow, clicked, *duplicates)
        clicked.set("nenhum")
        optionNomes.grid(row=2, column=1, padx=10, pady=10, ipadx=50)
        buttonNome = tkinter.Button(newWindow, text="Novo Nome", command=lambda: nomeJanela(optionNomes))
        buttonNome.grid(row=2, column=0, padx=10, pady=10, ipadx=30)

        buttonCancelaO = tkinter.Button(newWindow, text="Cancelar", command=lambda: newWindow.destroy())
        buttonCancelaO.grid(row=3, column=0, padx=10, pady=30, ipadx=30)
        buttonSubmitO = tkinter.Button(newWindow, text="OK", command=lambda: submitAdicionar(entryValidade.get(), clicked.get(), produtoSelecionado[0][4], entryQuantidade.get(), newWindow))
        buttonSubmitO.grid(row=3, column=1, padx=10, pady=30, ipadx=30)
        conn.close()
    else:
        messagebox.showwarning("Aviso", "Selecione um produto para adicionar unidades")


def submitAdicionar(entryValidade, clicked, produtoSelecionadoID, quantidade, janelaAdicionar):
    # adiciona dados das entradas de unidades ao SQL
    testQuantidade = False
    try:
        quantidadeInt = int(quantidade)
    except:
        testQuantidade = True

    testValidade = False
    try:
        validade = datetime.datetime.strptime(entryValidade, '%d/%m/%Y')
    except:
        testValidade = True
    hoje = datetime.datetime.today()

    if len(entryValidade) <= 0 or len(clicked) <= 0 or len(quantidade) <= 0 or testQuantidade or testValidade:
        messagebox.showwarning("Aviso", "Os dados oferecidos para adicionar unidades não correspondem aos tipos corretos")
    elif validade < hoje:
        messagebox.showerror("Erro", "Não é possível registrar entrada de um produto vencido")
    else:
        conn = sqlite3.connect("estoqueRe.db")
        cur = conn.cursor()
        hojeStr = hoje.strftime("%d/%m/%Y")
        for i in range(quantidadeInt):
            cur.execute("INSERT INTO UnidadeE VALUES (:validade, :dataEntrada, :funEntrada, :ID)",
                        {
                            'validade': entryValidade,
                            'dataEntrada': hojeStr,
                            'funEntrada': clicked,
                            'ID': produtoSelecionadoID
                        })
        conn.commit()
        conn.close()
        updateProduto()
        janelaAdicionar.destroy()


def select_item(Treeview):
    # seleciona linha em tabela do tipo treeview
    Treeitems = Treeview.selection()
    wholeData = []
    for ite in Treeitems:
        wholeData.append(Treeview.item(ite)['values'])
    return wholeData

def janelaRemover():
    # cria janela para adicionar unidades ao produto
    def nomeJanela(optionNomes):
        def nomeSubmit(nome):
            optionNomes["menu"].add_command(label=nome, command=tkinter._setit(clicked, nome))
            nameWindow.destroy()

        nameWindow = tkinter.Toplevel()
        nameWindow.title("Nome")
        nameWindow.geometry("270x100")

        nomeEntry = tkinter.Entry(nameWindow, width=20)
        nomeEntry.grid(row=0, column=1, padx=10, pady=10)
        nomeLabel = tkinter.Label(nameWindow, text="Nome: ")
        nomeLabel.grid(row=0, column=0, padx=10, pady=10)

        buttonSubmit = tkinter.Button(nameWindow, text="OK", command=lambda: nomeSubmit(nomeEntry.get()))
        buttonSubmit.grid(row=1, column=1, padx=10, pady=10, ipadx=20)
        buttonCancela = tkinter.Button(nameWindow, text="Cancelar", command=lambda: nameWindow.destroy)
        buttonCancela.grid(row=1, column=0, padx=10, pady=10, ipadx=20)

    conn = sqlite3.connect("estoqueRe.db")
    cur = conn.cursor()
    nomes = []
    duplicates = []
    produtoSelecionado = select_item(tabelaProdutoTree)

    if len(produtoSelecionado) > 0:
        cur.execute("SELECT funEntrada FROM UnidadeE")
        nomeTabela = cur.fetchall()
        for nome in nomeTabela:
            nomes.append(nome[0])

        cur.execute("SELECT funSaida FROM UnidadeS")
        nomeTabelaS = cur.fetchall()
        for nome in nomeTabelaS:
            nomes.append(nome[0])


        nomes.append("nenhum")
        for i in nomes:
            if i not in duplicates:
                duplicates.append(i)

        newWindow = tkinter.Toplevel()
        newWindow.title("Remover unidades")
        newWindow.geometry("370x200")

        entryQuantidade = tkinter.Entry(newWindow, width=10)
        entryQuantidade.grid(row=1, column=1, padx=10, pady=10)
        labelQuantidade = tkinter.Label(newWindow, text="Quantidade: ")
        labelQuantidade.grid(row=1, column=0, padx=10, pady=10)

        clicked = tkinter.StringVar(newWindow)
        optionNomes = tkinter.OptionMenu(newWindow, clicked, *duplicates)
        clicked.set("nenhum")
        optionNomes.grid(row=2, column=1, padx=10, pady=10, ipadx=50)
        buttonNome = tkinter.Button(newWindow, text="Novo Nome", command=lambda: nomeJanela(optionNomes))
        buttonNome.grid(row=2, column=0, padx=10, pady=10, ipadx=30)

        buttonCancelaO = tkinter.Button(newWindow, text="Cancelar", command=lambda: newWindow.destroy())
        buttonCancelaO.grid(row=3, column=0, padx=10, pady=30, ipadx=30)
        buttonSubmitO = tkinter.Button(newWindow, text="OK", command=lambda: submitRemover(clicked.get(), produtoSelecionado[0][4], entryQuantidade.get(), newWindow))
        buttonSubmitO.grid(row=3, column=1, padx=10, pady=30, ipadx=30)
        conn.close()
    else:
        messagebox.showwarning("Aviso", "Selecione um produto para remover unidades")




    def oldest(items):
        return min(items)

    def submitRemover(clicked, produtoSelecionadoID, quantidade, janelaRemover):
        #remove unidades do sql 
        testQuantidade = False
        try:
            quantidadeInt = int(quantidade)
        except:
            testQuantidade = True

        conn = sqlite3.connect("estoqueRe.db")
        cur = conn.cursor()
        cur.execute("SELECT estoque FROM Produto WHERE ID = ?;", str(produtoSelecionadoID))
        estoquePro = cur.fetchall()
        estoqueProd = estoquePro[0][0]
        conn.commit()
        conn.close()


        hoje = datetime.datetime.today()
        if len(clicked) <= 0 or len(quantidade) <= 0 or testQuantidade:
            messagebox.showwarning("Aviso", "Os dados oferecidos para remover unidades não correspondem aos tipos corretos")
        elif quantidadeInt > estoqueProd:
            messagebox.showwarning("Aviso", "A quantidade removida é maior que o estoque")

        else:
            conn = sqlite3.connect("estoqueRe.db")
            cur = conn.cursor()
            hojeStr = hoje.strftime("%d/%m/%Y")
            cur.execute("SELECT validade FROM UnidadeE WHERE ID = ?;", str(produtoSelecionadoID))
            validadesEntrada = cur.fetchall()
            validadesStr = []
            for validade in validadesEntrada:
                validadesStr.append(validade[0])

            validades = []
            for validade in validadesStr:
                obj = datetime.datetime.strptime(validade, "%d/%m/%Y")
                validades.append(obj)

            for i in range(quantidadeInt):

                entryValidade = oldest(validades).strftime("%d/%m/%Y")




                cur.execute("INSERT INTO UnidadeS VALUES (:validade, :dataSaida, :funSaida, :ID)",
                            {
                                'validade': entryValidade,
                                'dataSaida': hojeStr,
                                'funSaida': clicked,
                                'ID': produtoSelecionadoID
                            })
            conn.commit()
            conn.close()
            updateProduto()
            janelaRemover.destroy()

#WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWaquiiiiiWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW


    
def submitJanelaRelatorio():
    produtoSelecionadoi = select_item(tabelaProdutoTree)
    produtoSelecionado = produtoSelecionadoi[0][4]
    if len(produtoSelecionadoi) > 0:

        newWindow = tkinter.Toplevel()
        newWindow.title("Histórico do produto")
        newWindow.geometry("850x530")
        tabelaHistoricoFrame = tkinter.LabelFrame(newWindow, text="Histórico entrada", height=200, width=300)
        tabelaHistoricoFrame.grid(row=1, columnspan=4, padx=(10,0), pady=10)
        tabelaHistoricoTree = ttk.Treeview(tabelaHistoricoFrame, columns=(1, 2, 3, 4), show="headings", height="10")
        tabelaHistoricoTree.pack()
        tabelaHistoricoTree.heading(1, text="Validade")
        tabelaHistoricoTree.heading(2, text="data entrada")
        tabelaHistoricoTree.heading(3, text="nome entrada")
        tabelaHistoricoTree.heading(4, text="id")
        scrollHistoricoProduto = ttk.Scrollbar(newWindow, orient="vertical", command=tabelaHistoricoTree.yview)
        scrollHistoricoProduto.grid(row=1, column=4, pady=(20,10), sticky='ns')

        tabelaHistorico1Frame = tkinter.LabelFrame(newWindow, text="Histórico saída", height=200, width=300)
        tabelaHistorico1Frame.grid(row=2, columnspan=4, padx=(10,0), pady=10)
        tabelaHistorico1Tree = ttk.Treeview(tabelaHistorico1Frame, columns=(1, 2, 3, 4), show="headings", height="10")
        tabelaHistorico1Tree.pack()
        tabelaHistorico1Tree.heading(1, text="Validade")
        tabelaHistorico1Tree.heading(2, text="data saida")
        tabelaHistorico1Tree.heading(3, text="nome saida")
        tabelaHistorico1Tree.heading(4, text="id")
        scrollHistorico1Produto = ttk.Scrollbar(newWindow, orient="vertical", command=tabelaHistorico1Tree.yview)
        scrollHistorico1Produto.grid(row=2, column=4, pady=(20,10), sticky='ns')

        for i in tabelaHistoricoTree.get_children():
            tabelaHistoricoTree.delete(i)
        for i in tabelaHistorico1Tree.get_children():
            tabelaHistorico1Tree.delete(i)

        conn = sqlite3.connect("estoqueRe.db")
        cur = conn.cursor()
        cur.execute("SELECT Validade, dataEntrada, funEntrada FROM UnidadeE WHERE ID = ?;", str(produtoSelecionado))
        rowsE = cur.fetchall()
        cur.execute("SELECT Validade, dataSaida, funSaida FROM UnidadeS WHERE ID = ?;", str(produtoSelecionado))
        rowsS = cur.fetchall()
        conn.commit()
        conn.close()

        rowsE.sort()
        rowsS.sort()
        superLista = []
        k = 0
        for i in rowsE:
            k+=1
            lista = list(i)
            lista.append(k)
            tabelaHistoricoTree.insert('', 'end', values=lista)
            
        j = 0
        for i in rowsS:
            j+=1
            lista = list(i)
            lista.append(j)
            tabelaHistorico1Tree.insert('', 'end', values=lista)



    else:
        messagebox.showwarning("Aviso", "Selecione um produto para ver o histórico")
        


    






def deleteProduto():
    produtoSelecionado = select_item(tabelaProdutoTree)
    if len(produtoSelecionado) > 0:
        var = tkinter.messagebox.askquestion('Excluir Produto', 'Tem certeza de que deseja excluir o produto: ' + produtoSelecionado[0][0], icon='warning')
        if var == 'yes':
            conn = sqlite3.connect("estoqueRe.db")
            cur = conn.cursor()
            produtoDelete = (produtoSelecionado[0][4],)
            cur.execute("DELETE FROM Produto WHERE ID = ?;", produtoDelete)
            cur.execute("DELETE FROM UnidadeE WHERE ID = ?;", produtoDelete)
            cur.execute("DELETE FROM UnidadeS WHERE ID = ?;", produtoDelete)
            conn.commit()
            conn.close()
            updateProduto()
            messagebox.showinfo("Aviso", "Produto excluído com sucesso")
    else:
        messagebox.showwarning("Aviso", "Selecione um produto para excluir")



def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if
            elm[:2] != ('!disabled', '!selected')]


if __name__ == "__main__":
    # create database
    conn = sqlite3.connect("estoqueRe.db")
    # create cursor
    cur = conn.cursor()

    # create table
    cur.execute("""CREATE TABLE IF NOT EXISTS Produto(
        nome_produto text,
        recipiente text,
        valorCritico integer,
        estoque integer,
        ID integer  )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS UnidadeE(
        validade text,
        dataEntrada text,
        funEntrada text,
        ID integer  )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS UnidadeS(
        validade text,
        dataSaida text,
        funSaida text,
        ID integer  )""")

    # faz as mudancas
    # cria janela
    root = tkinter.Tk()
    root.title('Controle de Estoque - HU')
    root.geometry("1000x380")

    style = ttk.Style()
    style.map('Treeview', foreground=fixed_map('foreground'),
            background=fixed_map('background'))

    col_count, row_count = root.grid_size()
    for col in range(5):
        root.grid_columnconfigure(col, weight=1)

    botaoProduto = tkinter.Button(root, text="Criar Novo Produto", command=lambda: janelaProduto())
    botaoProduto.grid(row=0, column=0, padx=10, pady=10)
    botaoAdUnidade = tkinter.Button(root, text="Adicionar Unidades", command=lambda: janelaAdicionar())
    botaoAdUnidade.grid(row=0, column=1, padx=10, pady=10)
    botaoReUnidade = tkinter.Button(root, text="Remover Unidades", command=lambda: janelaRemover())
    botaoReUnidade.grid(row=0, column=2, padx=10, pady=10)
    botaoDeleteProduto = tkinter.Button(root, text="Excluir Produto", command=lambda: deleteProduto())
    botaoDeleteProduto.grid(row=0, column=3, padx=10, pady=10)
    botaoEstatisticaProdutos = tkinter.Button(root, text="Histórico", command=lambda: submitJanelaRelatorio())
    botaoEstatisticaProdutos.grid(row=0, column=4, padx=10, pady=10)
    cursorzito = cur.execute("SELECT nome_produto FROM Produto")
    produto = cursorzito.fetchall()

    tabelaProdutoFrame = tkinter.LabelFrame(root, text="Produtos", height=300, width=400)
    tabelaProdutoFrame.grid(row=1, columnspan=5, padx=(10,0), pady=10)
    tabelaProdutoTree = ttk.Treeview(tabelaProdutoFrame, columns=(1, 2, 3, 4, 5), show="headings", height="13")
    tabelaProdutoTree.pack()
    tabelaProdutoTree.heading(1, text="Nome do Produto")
    tabelaProdutoTree.heading(2, text="Tipo do Recipiente")
    tabelaProdutoTree.heading(3, text="Valor Crítico")
    tabelaProdutoTree.heading(4, text="Estoque Atual")
    tabelaProdutoTree.heading(5, text="ID")
    scrollTabelaProduto = ttk.Scrollbar(root, orient="vertical", command=tabelaProdutoTree.yview)
    scrollTabelaProduto.grid(row=1, column=5, pady=(20,10), sticky='ns')
    tabelaProdutoTree.bind('<ButtonRelease-1>', lambda Treeview: select_item(tabelaProdutoTree))
    updateProduto()
    conn.commit()
    conn.close()
    root.mainloop()
