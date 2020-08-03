import datetime 
import tkinter 
import sqlite3
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox # importa bibliotecas
from tkinter import simpledialog


def search(treeview, comparevalue):
	#checa se valor ja exite na tabela Treeview
    children = treeview.get_children('')
    for child in children:
        values = treeview.item(child, 'values')
        if comparevalue[4]==values[4] and str(comparevalue[0])==str(values[0]):
            return True
    return False

def updateProduto():
	#produtos são colocados na tabela da GUI
	#pega dados do Produto no sql
	conn = sqlite3.connect("estoqueRe.db")
	#create cursor
	cur = conn.cursor()
	cur.execute("SELECT nome_produto, recipiente, valorCritico, estoque, ID FROM Produto")
	rows = cur.fetchall()
	

	# deleta tudo na treeview
	for i in tabelaProdutoTree.get_children():
		tabelaProdutoTree.delete(i)

    #atualiza os dados
	for i in rows:
		
		cur.execute("SELECT COUNT(*) FROM UnidadeE WHERE ID =" + str(i[4]))
		unidadesProdutoE = cur.fetchall()
		cur.execute("SELECT COUNT(*) FROM UnidadeS WHERE ID =" + str(i[4]))
		unidadesProdutoS = cur.fetchall()
		novoEstoque = unidadesProdutoE[0][0] - unidadesProdutoS[0][0]
		novoEstoqueint = int(novoEstoque)
		novoEstoqueStr = str(novoEstoqueint)
		cur.execute("UPDATE Produto SET estoque=" + novoEstoqueStr + " WHERE ID="+str(i[4]))
	conn.commit()
	conn.close()

	

	#pega os produtos atualizados
	conn = sqlite3.connect("estoqueRe.db")
	cur = conn.cursor()
	cur.execute("SELECT nome_produto, recipiente, valorCritico, estoque, ID FROM Produto")
	rows = cur.fetchall()
	conn.commit()
	conn.close()

	for i in rows:
		if i[3] <= i[2]:
			tabelaProdutoTree.insert('','end',values=i, tags="crit")
			tabelaProdutoTree.tag_configure("crit", background='red')
		else:
			tabelaProdutoTree.insert('','end',values=i, tags="Ncrit")
			tabelaProdutoTree.tag_configure("Ncrit", background='white')

def JanelaAviso(texto, tamanho):
	#janela de aviso com botao de ok
	def avisoDestroy():
		podeIr = True
		okClicado = True
		warningwindow.destroy()
		return okClicado
		
		
	def on_closing():
		podeIr = True
		okClicado = False
		warningwindow.destroy()
		return okClicado
		
		
	podeIr = False
	warningwindow = tkinter.Toplevel()
	warningwindow.title("Dados errados")
	warningwindow.geometry(tamanho)
	labelErro = tkinter.Label(warningwindow, text=texto)
	labelErro.grid(row=0, column=0, padx=10, pady=10)
	botaoOK = tkinter.Button(warningwindow, text="OK", command=lambda: avisoDestroy())
	botaoOK.grid(row=1, column=0, padx=10, pady=10, ipadx=40)
	warningwindow.protocol("WM_DELETE_WINDOW", on_closing)
	warningwindow.wait_variable(podeIr)



	
	
	

def submitProduto(NomeProduto, TipoRecipiente, ValorCritico, window):
	#adiciona um produto ao sql
	conn = sqlite3.connect("estoqueRe.db")
	#create cursor
	cur = conn.cursor()
	test = False
	try:
		int(ValorCritico.get())
	except:
		test = True
	#insert into table
	if len(NomeProduto.get()) <= 0 or len(TipoRecipiente.get()) <= 0 or len(ValorCritico.get()) <= 0 or type(NomeProduto.get()) != str or type(TipoRecipiente.get()) != str or test:
		JanelaAviso("os dados oferecidos para criar o produto nao correspondem ao tipo correto", "430x200")
	else:
		cur.execute("SELECT * FROM Produto")
		IDproduto = len(cur.fetchall())

		cur.execute("INSERT INTO Produto VALUES (:nome_produto, :recipiente, :valorCritico, :estoque, :ID)",
			{
				'nome_produto' : NomeProduto.get(),
				'recipiente' : TipoRecipiente.get(),
				'valorCritico' :ValorCritico.get(),
				'estoque': 0,
				'ID': IDproduto
			}
		)
		conn.commit()
		conn.close()
		updateProduto()
		
		window.destroy()

	
def janelaProduto():
	#cria a janela para criar um novo produto
	newWindow = tkinter.Toplevel() 
	newWindow.title("Criar novo produto")
	newWindow.geometry("400x300")
	entryNomeProduto = tkinter.Entry(newWindow, width=30)
	entryNomeProduto.grid(row=0,column=1,padx=10, pady=10)
	entryTipoRecipiente = tkinter.Entry(newWindow, width=30)
	entryTipoRecipiente.grid(row=1,column=1,padx=10, pady=10)
	entryValorCritico = tkinter.Entry(newWindow, width=30)
	entryValorCritico.grid(row=2,column=1,padx=10, pady=10)
	labelNomeProduto = tkinter.Label(newWindow, text="Nome do produto: ")
	labelNomeProduto.grid(row=0,column=0,padx=10, pady=10)
	labelTipoRecipiente = tkinter.Label(newWindow, text="Unidade: ")
	labelTipoRecipiente.grid(row=1,column=0,padx=10, pady=10)
	labelValorCritico = tkinter.Label(newWindow, text="valor critico: ")
	labelValorCritico.grid(row=2,column=0,padx=10, pady=10)
	buttonCancela = tkinter.Button(newWindow, text="cancelar", command=newWindow.destroy)
	buttonCancela.grid(row=5,column=0,padx=10, pady=140, ipadx=50)
	buttonSubmit = tkinter.Button(newWindow, text="submit", command=lambda: submitProduto(entryNomeProduto, entryTipoRecipiente, entryValorCritico, newWindow))
	buttonSubmit.grid(row=5,column=1,padx=10, pady=140, ipadx=50)
	

def janelaAdicionar():
	#cria janela para adicionar unidades ao produto
	def nomeJanela(optionNomes):
		def nomeSubmit(nome):
			optionNomes["menu"].add_command(label=nome, command=tkinter._setit(clicked, nome))
			nameWindow.destroy()

		nameWindow = tkinter.Toplevel()
		nameWindow.title("Nome")
		nameWindow.geometry("250x100")

		nomeEntry = tkinter.Entry(nameWindow, width=20)
		nomeEntry.grid(row=0, column=1, padx=10, pady=10)
		nomeLabel = tkinter.Label(nameWindow, text="Nome: ")
		nomeLabel.grid(row=0, column=0, padx=10, pady=10)

		buttonSubmit = tkinter.Button(nameWindow, text="submit", command=lambda : nomeSubmit(nomeEntry.get()))
		buttonSubmit.grid(row=1, column=1, padx=10, pady=10, ipadx=20)
		buttonCancela =  tkinter.Button(nameWindow, text="cancela", command=lambda: nameWindow.destroy)
		buttonCancela.grid(row=1, column=0, padx=10, pady=10, ipadx=20)


	conn = sqlite3.connect("estoqueRe.db")
	cur = conn.cursor()
	nomes=[]
	duplicates=[]
	produtoSelecionado = select_item(tabelaProdutoTree)
	if len(produtoSelecionado) > 0:
		cur.execute("SELECT funEntrada FROM UnidadeE")
		nomeTabela = cur.fetchall()
		for nome in nomeTabela:
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
		labelValidade = tkinter.Label(newWindow, text="validade dd/mm/aaaa : ")
		labelValidade.grid(row=0, column=0, padx=10, pady=10)
		
		entryQuantidade = tkinter.Entry(newWindow, width=10)
		entryQuantidade.grid(row=1, column=1, padx=10, pady=10)
		labelQuantidade = tkinter.Label(newWindow, text="quantidade : ")
		labelQuantidade.grid(row=1, column=0, padx=10, pady=10)


		clicked = tkinter.StringVar(newWindow)
		optionNomes = tkinter.OptionMenu(newWindow, clicked, *duplicates)
		clicked.set("nenhum")
		optionNomes.grid(row=2, column=1, padx=10, pady=10, ipadx=50)
		buttonNome = tkinter.Button(newWindow, text="novo nome", command=lambda: nomeJanela(optionNomes))
		buttonNome.grid(row=2, column=0, padx=10, pady=10, ipadx=30)



		buttonCancelaO = tkinter.Button(newWindow, text="cancela", command=lambda :newWindow.destroy())
		buttonCancelaO.grid(row=3, column=0, padx=10, pady=30, ipadx=30)
		buttonSubmitO = tkinter.Button(newWindow, text="submit", command=lambda: submitAdicionar(entryValidade.get(), clicked.get(), produtoSelecionado[0][4], entryQuantidade.get(), newWindow))
		buttonSubmitO.grid(row=3, column=1, padx=10, pady=30, ipadx=30)
		conn.commit()
		conn.close()
	else:
		JanelaAviso("ops, selecione um produto antes de adicionar", "270x100")


	

def submitAdicionar(entryValidade, clicked, produtoSelecionadoID, quantidade, janelaAdicionar):
	#adiciona dados das entradas de unidades ao SQL

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
	

	if len(entryValidade) <= 0 or len(clicked) <= 0 or len(quantidade) <= 0  or testQuantidade or testValidade:
		JanelaAviso("os dados oferecidos para adicionar unidades nao correspondem aos tipos corretos","470x100")
	elif validade < hoje:
		JanelaAviso("nao eh possivel fazer entrada de um produto vencido", "370x100")
	else:
		conn = sqlite3.connect("estoqueRe.db")
		cur = conn.cursor()
		hojeStr = hoje.strftime("%d/%m/%Y")
		for i in range(quantidadeInt):
			cur.execute("INSERT INTO UnidadeE VALUES (:validade, :dataEntrada, :funEntrada, :ID)",
				{
					'validade' : entryValidade,
					'dataEntrada': hojeStr,
					'funEntrada': clicked,
					'ID': produtoSelecionadoID
				}
			)
		conn.commit()
		conn.close()
		updateProduto()
		janelaAdicionar.destroy()

		

def janelaRemover():
	#cria nova janela
	newWindow = tkinter.Toplevel(root) 
	newWindow.title("remover")
	newWindow.geometry("200x200")

def select_item(Treeview):
	#seleciona linha em tabela do tipo treeview
	 Treeitems = Treeview.selection()
	 wholeData = []
	 for ite in Treeitems:
	 	wholeData.append(Treeview.item(ite)['values'])
	 return wholeData

def deleteProduto():
	produtoSelecionado = select_item(tabelaProdutoTree)
	if len(produtoSelecionado) > 0:
		var = tkinter.messagebox.askquestion('deletar produto','tem certeza que quer deletar o produto: '+ produtoSelecionado[0][0],icon = 'warning')
		if  var == 'yes':
			conn = sqlite3.connect("estoqueRe.db")
			cur = conn.cursor()
			produtoDelete = (produtoSelecionado[0][4],)
			cur.execute("DELETE FROM Produto WHERE ID = ?;", produtoDelete)
			cur.execute("DELETE FROM UnidadeE WHERE ID = ?;", produtoDelete)
			cur.execute("DELETE FROM UnidadeS WHERE ID = ?;", produtoDelete)
			conn.commit()
			conn.close()
			updateProduto()
			JanelaAviso("produto deletado","120x100")
			
			
			

		else:
			pass
		
	else:
		JanelaAviso("nenhum produto selecionado para ser deletado","280x100")


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



#create database
conn = sqlite3.connect("estoqueRe.db")
#create cursor
cur = conn.cursor()


#create table

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

#faz as mudancas
#cria janela
root = tkinter.Tk()
root.title('controle de estoque HU')
root.geometry("1000x380")

style = ttk.Style()
style.map('Treeview', foreground=fixed_map('foreground'),
  background=fixed_map('background'))

col_count, row_count = root.grid_size()
for col in range(4):
    root.grid_columnconfigure(col, weight=1)


botaoProduto = tkinter.Button(root, text="criar novo produto", command=lambda : janelaProduto() )
botaoProduto.grid(row=0, column=0, padx=0, pady=10)
botaoAdUnidade = tkinter.Button(root, text="adicionar unidades", command=lambda: janelaAdicionar())
botaoAdUnidade.grid(row=0, column=1, padx=0, pady=10)
botaoReUnidade = tkinter.Button(root, text="remover unidades", command=lambda: janelaRemover())
botaoReUnidade.grid(row=0, column=2, padx=0, pady=10)
botaoDeleteProduto = tkinter.Button(root, text="deletar produto", command=lambda: deleteProduto())
botaoDeleteProduto.grid(row=0, column=3, padx=0, pady=10)
cursorzito = cur.execute("SELECT nome_produto FROM Produto")
produto = cursorzito.fetchall()


tabelaProdutoFrame = tkinter.LabelFrame(root ,text="Produtos", height=300, width=400)
tabelaProdutoFrame.grid(row=1, columnspan=4, padx=10, pady=10)
tabelaProdutoTree = ttk.Treeview(tabelaProdutoFrame, columns=(1,2,3,4,5), show="headings", height="13")
tabelaProdutoTree.pack()
tabelaProdutoTree.heading(1, text="Nome produto")
tabelaProdutoTree.heading(2, text="Tipo recipiente")
tabelaProdutoTree.heading(3, text="ValorCritico")
tabelaProdutoTree.heading(4, text="Estoque")
tabelaProdutoTree.heading(5, text="ID")
scrollTabelaProduto = ttk.Scrollbar(root, orient="vertical", command=tabelaProdutoTree.yview)
scrollTabelaProduto.place(x=971, y=75, height=283)
tabelaProdutoTree.bind('<ButtonRelease-1>',lambda Treeview: select_item(tabelaProdutoTree))
conn.commit()
conn.close()
updateProduto()
root.mainloop()




