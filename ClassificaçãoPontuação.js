class TiroComArco {
    constructor() {
        this.pontuacoes = [];
    }

    registrarPontuacao(pontuacao) {
        this.pontuacoes.push(pontuacao);
    }

    aplicarPenalidade() {
        if (this.pontuacoes.length) {
            let maiorPontuacao = Math.max(...this.pontuacoes.filter(p => typeof p === 'number'));
            for (let i = 0; i < this.pontuacoes.length; i++) {
                if (this.pontuacoes[i] === maiorPontuacao) {
                    this.pontuacoes[i] = "M";
                    break;
                }
            }
        }
    }

    exibirPontuacoes() {
        let output = "";
        this.pontuacoes.forEach((pontuacao, index) => {
            output += `Flecha ${index + 1}: ${pontuacao}<br>`;
        });
        return output;
    }

    calcularSomaPontuacao() {
        return this.pontuacoes.reduce((sum, p) => sum + (typeof p === 'number' ? p : 0), 0);
    }
}

const tiroComArco = new TiroComArco();
const numeroFlechas = 72;

document.getElementById('adicionarPontuacao').addEventListener('click', () => {
    const pontuacoesDiv = document.getElementById('pontuacoes');
    for (let i = tiroComArco.pontuacoes.length; i < numeroFlechas; i++) {
        let pontuacao;
        while (true) {
            const pontuacaoInput = prompt(`Pontuação da flecha ${i + 1}:`);
            pontuacao = parseInt(pontuacaoInput);
            if (pontuacao >= 0 && pontuacao <= 10) {
                break;
            } else {
                alert("A pontuação deve ser um número entre 0 e 10.");
            }
        }
        tiroComArco.registrarPontuacao(pontuacao);
        pontuacoesDiv.innerHTML = tiroComArco.exibirPontuacoes();
    }
});

document.getElementById('calcularSoma').addEventListener('click', () => {
    const somaInicial = document.getElementById('somaInicial');
    somaInicial.innerHTML = `Soma total das pontuações registradas: ${tiroComArco.calcularSomaPontuacao()}`;
});

document.getElementById('cartaoSim').addEventListener('click', () => {
    document.getElementById('quantidadeCartoes').style.display = 'block';
});

document.getElementById('cartaoNao').addEventListener('click', () => {
    alert("Sem penalidades aplicadas.");
});

document.getElementById('aplicarPenalidade').addEventListener('click', () => {
    const quantidadeCartoes = parseInt(document.getElementById('inputCartoes').value);
    for (let i = 0; i < quantidadeCartoes; i++) {
        tiroComArco.aplicarPenalidade();
    }
    const pontuacoesFinais = document.getElementById('pontuacoesFinais');
    pontuacoesFinais.innerHTML = `Pontuações após aplicar as penalidades:<br>${tiroComArco.exibirPontuacoes()}`;
    const somaFinal = document.getElementById('somaFinal');
    somaFinal.innerHTML = `Soma total das pontuações após aplicar as penalidades: ${tiroComArco.calcularSomaPontuacao()}`;
});
