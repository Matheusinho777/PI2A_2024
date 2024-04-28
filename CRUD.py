import pymysql
class Atleta:
    def __init__(self, nome, idade, nacionalidade, colocacao):
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade
        self.colocacao = colocacao

class CadastroAtletas:
    def __init__(self):
        self.atletas = []

    def adicionar_atleta(self, atleta):
        self.atletas.append(atleta)

    def listar_atletas(self):
        colocacao_atletas = sorted(self.atletas, key=lambda atleta: atleta.colocacao)
        for idx, atleta in enumerate(colocacao_atletas, start=1):
            print(f"{idx}º Colocado - Nome: {atleta.nome}, Idade: {atleta.idade}, Nacionalidade: {atleta.nacionalidade}, Colocação: {atleta.colocacao}")

    def buscar_atleta(self, nome):
        for atleta in self.atletas:
            if atleta.nome == nome:
                return atleta
        return None

    def deletar_atleta(self, nome):
        atleta = self.buscar_atleta(nome)
        if atleta:
            self.atletas.remove(atleta)
            print("Atleta removido com sucesso!")
        else:
            print("Atleta não encontrado.")

    def atualizar_atleta(self, nome, novo_nome, nova_idade, nova_nacionalidade, nova_colocacao):
        atleta = self.buscar_atleta(nome)
        if atleta:
            atleta.nome = novo_nome
            atleta.idade = nova_idade
            atleta.nacionalidade = nova_nacionalidade
            atleta.colocacao = nova_colocacao
            print("Atleta atualizado com sucesso!")
        else:
            print("Atleta não encontrado.")

    def salvar_atletas(self, connection):
        try:
            with connection.cursor() as cursor:
                for atleta in self.atletas:
                    sql = "INSERT INTO classificacao (nome, idade, nacionalidade, colocacao) VALUES (%s, %s, %s, %s)"
                    cursor.execute(sql, (atleta.nome, atleta.idade, atleta.nacionalidade, atleta.colocacao))
            connection.commit()
            print("Dados dos atletas salvos no banco de dados.")
        except pymysql.Error as e:
            print(f"Erro ao salvar dados dos atletas: {e}")

    def carregar_atletas(self, nome_arquivo):
        self.atletas = []
        try:
            with open(nome_arquivo, "r") as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    dados = linha.strip().split(",")
                    if len(dados) == 4:
                        nome, idade, nacionalidade, colocacao = dados
                        self.adicionar_atleta(Atleta(nome, int(idade), nacionalidade, colocacao))
        except FileNotFoundError:
            print("Arquivo não encontrado.")

class classificaçãoAtleta:
    def __init__(self, etapa, pontuacao, pontuacaoTiros,  ):
        self.etapa = etapa
        self.pontuacao = pontuacao
        self.pontuacaoTiros = pontuacaoTiros

    def tipo_etapa(self, etapa):
        fase = input("Escolha qual fase o atleta está jogando: \n(1) Fase Classificatória\n(2) Fase Eliminatória")
        if fase == "1":
            self.etapa = "Classificatória"
            print("Ok! vamos prosseguir com a etapa {}".format(self.etapa))
        elif fase == "2":
            self.etapa = "Eliminatória"
            print("Ok! vamos prosseguir com a etapa {}".format(self.etapa))
        else:
            print("Digite uma opção válida de fase...")
            return
        return etapa


def adicionar_novo_atleta(cadastro):
    nome = input("Digite o nome do atleta: ")
    idade = int(input("Digite a idade do atleta: "))
    nacionalidade = input("Digite a nacionalidade do atleta: ")
    colocacao = input("Digite a colocação do atleta (ex: 1º, 2º, 3º): ")
    novo_atleta = Atleta(nome, idade, nacionalidade, colocacao)
    cadastro.adicionar_atleta(novo_atleta)
    print("Atleta adicionado com sucesso!")

def deletar_atleta(cadastro):
    nome = input("Digite o nome do atleta que deseja deletar: ")
    cadastro.deletar_atleta(nome)

def atualizar_atleta(cadastro):
    nome = input("Digite o nome do atleta que deseja atualizar: ")
    novo_nome = input("Digite o novo nome do atleta: ")
    nova_idade = int(input("Digite a nova idade do atleta: "))
    nova_nacionalidade = input("Digite a nova nacionalidade do atleta: ")
    nova_colocacao = input("Digite a nova colocação do atleta (ex: 1º, 2º, 3º): ")
    cadastro.atualizar_atleta(nome, novo_nome, nova_idade, nova_nacionalidade, nova_colocacao)

def main():
    connection = pymysql.connect(
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-2480cbc6-iesb-pi2a2024.h.aivencloud.com",
        password="AVNS_FhpJunTAM7Hz3pU4pIM",
        port=22150,
        user="avnadmin",
    )
    nome_arquivo = "atletas.txt"
    cadastro = CadastroAtletas()
    cadastro.carregar_atletas(nome_arquivo)
    while True:
        print("\n### MENU ###")
        print("1. Adicionar Atleta")
        print("2. Classificação dos Atletas")
        print("3. Deletar Atleta")
        print("4. Atualizar Atleta")
        print("5. Salvar e Sair")

        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            adicionar_novo_atleta(cadastro)
        elif opcao == "2":
            cadastro.listar_atletas()
        elif opcao == "3":
            deletar_atleta(cadastro)
        elif opcao == "4":
            atualizar_atleta(cadastro)
        elif opcao == "5":
            cadastro.salvar_atletas(connection)
            print("Dados dos atletas salvos.")
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
