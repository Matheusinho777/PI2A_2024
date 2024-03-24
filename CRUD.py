class Atleta:
    def __init__(self, nome, idade, nacionalidade, grupo):
        self.nome = nome
        self.idade = idade
        self.nacionalidade = nacionalidade
        self.grupo = grupo

class CadastroAtletas:
    def __init__(self):
        self.atletas = []

    def adicionar_atleta(self, atleta):
        self.atletas.append(atleta)

    def listar_atletas(self):
        for idx, atleta in enumerate(self.atletas, start=1):
            print(f"{idx}. Nome: {atleta.nome}, Idade: {atleta.idade}, Nacionalidade: {atleta.nacionalidade}, Grupo: {atleta.grupo}")

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

    def salvar_atletas(self, nome_arquivo):
        with open(nome_arquivo, "w") as arquivo:
            for atleta in self.atletas:
                arquivo.write(f"{atleta.nome},{atleta.idade},{atleta.nacionalidade},{atleta.grupo}\n")

    def carregar_atletas(self, nome_arquivo):
        self.atletas = []
        try:
            with open(nome_arquivo, "r") as arquivo:
                linhas = arquivo.readlines()
                for linha in linhas:
                    dados = linha.strip().split(",")
                    if len(dados) == 4:
                        nome, idade, nacionalidade, grupo = dados
                        self.adicionar_atleta(Atleta(nome, int(idade), nacionalidade, grupo))
        except FileNotFoundError:
            print("Arquivo não encontrado.")

# Adicionar um novo atleta
def adicionar_novo_atleta(cadastro):
    nome = input("Digite o nome do atleta: ")
    idade = int(input("Digite a idade do atleta: "))
    nacionalidade = input("Digite a nacionalidade do atleta: ")
    grupo = input("Digite o grupo que atleta está (ex: 1, 2, 3): ")
    novo_atleta = Atleta(nome, idade, nacionalidade, grupo)
    cadastro.adicionar_atleta(novo_atleta)
    print("Atleta adicionado com sucesso!")

# Deletar um atleta
def deletar_atleta(cadastro):
    nome = input("Digite o nome do atleta que deseja deletar: ")
    cadastro.deletar_atleta(nome)

# Main
def main():
    nome_arquivo = "atletas.txt"
    cadastro = CadastroAtletas()
    cadastro.carregar_atletas(nome_arquivo)
    while True:
        print("\n### MENU ###")
        print("1. Adicionar Atleta")
        print("2. Listar Atletas")
        print("3. Deletar Atleta")
        print("4. Salvar e Sair")

        opcao = input("\nDigite o número da opção desejada: ")

        if opcao == "1":
            adicionar_novo_atleta(cadastro)
        elif opcao == "2":
            cadastro.listar_atletas()
        elif opcao == "3":
            deletar_atleta(cadastro)
        elif opcao == "4":
            cadastro.salvar_atletas(nome_arquivo)
            print("Dados dos atletas salvos.")
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
