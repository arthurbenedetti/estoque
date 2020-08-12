import peewee as pw

db = pw.SqliteDatabase("estoque.db")


class BaseModel(pw.Model):
    class Meta:
        database = db


class Produto(BaseModel):
    idProduto = pw.IntegerField()
    nome = pw.CharField()
    tipoEmbalagem = pw.CharField()
    valorCritico = pw.IntegerField(0)
    valorAtual = pw.IntegerField()


class Funcionario(BaseModel):
    idFuncionario = pw.IntegerField()
    nome = pw.CharField()
    cargo = pw.CharField()


class Lote(BaseModel):
    idLote = pw.IntegerField()
    codigo = pw.CharField()
    dataExpiracao = pw.DateField()


class RegistroEntrada(BaseModel):
    idRegEntrada = pw.IntegerField()
    idFuncionario = pw.ForeignKeyField(Funcionario, backref='registroEntrada')
    idLote = pw.ForeignKeyField(Lote, backref='registroEntrada')
    idProduto = pw.ForeignKeyField(Produto, backref='registroEntrada')
    dataEntrada = pw.DateField()
    quantidade = pw.IntegerField()


class RegistroSaida(BaseModel):
    idRegSaida = pw.IntegerField()
    idFuncionario = pw.ForeignKeyField(Funcionario, backref='registroSaida')
    idLote = pw.ForeignKeyField(Lote, backref='registroSaida')
    idProduto = pw.ForeignKeyField(Produto, backref='registroSaida')
    dataSaida = pw.DateField()
    quantidade = pw.IntegerField()


def create_tables():
    with db:
        db.create_tables([Produto, Funcionario, Lote, RegistroEntrada, RegistroSaida])


# cloroquina = Produto(idProduto=0, nome="cloroquina", tipoEmbalagem="caixa com 10", valorCritico=2, valorAtual=0)
# cloroquina.save()

# paracetamol = Produto(idProduto=1, nome="paracetamol", tipoEmbalagem="caixa com 5", valorCritico=10, valorAtual=0)
# paracetamol.save()

# joao = Funcionario(idFuncionario=0, nome="João", cargo="gerente")
# joao.save()

# loteX = Lote(idLote=0, codigo="123XYZ", dataExpiracao=date(2021, 9, 1))
# loteX.save()

# entraCloroquina = RegistroEntrada(idRegEntrada=0, idFuncionario=joao.idFuncionario, idLote=loteX.idLote, idProduto=cloroquina.idProduto, dataEntrada=date(2020, 8, 7), quantidade=10)
# entraCloroquina.save()

# entraParacetamol = RegistroEntrada(idRegEntrada=0, idFuncionario=joao.idFuncionario, idLote=loteX.idLote, idProduto=paracetamol.idProduto, dataEntrada=date(2020, 6, 9), quantidade=20)
# entraParacetamol.save()

# saiCloroquina = RegistroSaida(idRegSaida=0, idFuncionario=joao.idFuncionario, idLote=loteX.idLote, idProduto=cloroquina.idProduto, dataSaida=date(2020, 8, 7), quantidade=5)
# saiCloroquina.save()

# joao.cargo = "chefe"
# joao.update(cargo=joao.cargo).execute()

# got = Funcionario.get(Funcionario.nome == "João")
# print(got.nome, got.cargo)
