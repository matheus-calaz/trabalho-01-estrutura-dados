import os
from jogo import JogoSame

def ler_inteiro(mensagem: str, minimo: int, maximo: int) -> int:
    while True:
        try:
            valor = int(input(mensagem))
            if minimo <= valor <= maximo:
                return valor
            print(f"Por favor, insira um valor entre {minimo} e {maximo}.")
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")

def imprimir_tabuleiro(matriz):
    cores_ansi = {
        0: '\033[0m',   # Vazio
        1: '\033[91m',  # Vermelho
        2: '\033[92m',  # Verde
        3: '\033[94m',  # Azul
        4: '\033[93m',  # Amarelo
        5: '\033[95m',  # Magenta
        6: '\033[96m'   # Ciano
    }
    reset = '\033[0m'
    
    print("\n   " + " ".join([f"{c+1:2}" for c in range(len(matriz[0]))]))
    print("  " + "-" * (len(matriz[0]) * 3 + 1))
    
    for i, linha in enumerate(matriz):
        linha_str = f"{i+1:2}| "
        for bloco in linha:
            if bloco == 0:
                linha_str += " . "
            else:
                linha_str += f"{cores_ansi[bloco]} ■ {reset}"
        print(linha_str)
    print()

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    limpar_tela()
    print("="*30)
    print("          JOGO SAME")
    print("="*30)

    # tamanho e cores tabuleiro
    linhas = ler_inteiro("Digite o número de linhas (10 a 20): ", 10, 20)
    colunas = ler_inteiro("Digite o número de colunas (10 a 60): ", 10, 60)
    cores = ler_inteiro("Digite o número de cores (3 a 6): ", 3, 6)

    jogo = JogoSame(linhas, colunas, cores)

    while True:
        limpar_tela()
        print("=== JOGO SAME ===")
        imprimir_tabuleiro(jogo.matriz)

        fim, resultado = jogo.verificar_fim_de_jogo()
        if fim:
            if resultado == "VITORIA":
                print("\n🏆 PARABÉNS! Você venceu limpando todo o tabuleiro!")
            else:
                print("\n💀 FIM DE JOGO! Não é possível realizar mais jogadas (Você perdeu).")
            break

        print("OPÇÕES:")
        print(" - Jogar: Digite a Linha e a Coluna separados por espaço (ex: 4 6)")
        print(" - Desfazer: Digite 'U'")
        print(" - Sair: Digite 'S'")
        entrada = input("\nSua jogada: ").strip().upper().split()

        if not entrada:
            continue

        if entrada[0] == 'U':
            if not jogo.desfazer_jogada():
                input("Nenhuma jogada para desfazer! Pressione Enter para continuar...")
        elif entrada[0] == 'S':
            print("Jogo encerrado.")
            break
        elif len(entrada) == 2 and entrada[0].isdigit() and entrada[1].isdigit():
            l = int(entrada[0]) - 1
            c = int(entrada[1]) - 1

            if 0 <= l < jogo.linhas and 0 <= c < jogo.colunas:
                if not jogo.realizar_jogada(l, c):
                    input("Jogada Inválida! Selecione um bloco com vizinhos da mesma cor. Pressione Enter...")
            else:
                input("Coordenadas fora do tabuleiro! Pressione Enter...")
        else:
            input("Comando inválido! Pressione Enter para continuar...")

if __name__ == "__main__":
    main()