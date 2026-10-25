import random
from copy import deepcopy
from estruturas import pilha_dinamica, fila_dinamica, lista_ligada, item

class JogoSame:
    def __init__(self, linhas: int, colunas: int, num_cores: int):
        self.linhas = linhas
        self.colunas = colunas
        self.num_cores = num_cores
        self.matriz = []
        self.historico = pilha_dinamica() 
        self.gerar_tabuleiro_inicial()

    def gerar_tabuleiro_inicial(self):
        for l in range(self.linhas):
            linha = []
            for c in range(self.colunas):
                linha.append(random.randint(1, self.num_cores))
            self.matriz.append(linha)

    def obter_regiao(self, l_inicio: int, c_inicio: int) -> lista_ligada:
        cor_alvo = self.matriz[l_inicio][c_inicio]
        regiao = lista_ligada() 
        
        if cor_alvo == 0:
            return regiao

        visitados = [[False for _ in range(self.colunas)] for _ in range(self.linhas)]
        
        fila_busca = fila_dinamica()
        fila_busca.enfileira(item((l_inicio, c_inicio)))
        visitados[l_inicio][c_inicio] = True

        while not fila_busca.vazia():
            it = fila_busca.obtem_primeiro()
            fila_busca.desenfileira()
            
            l_atual, c_atual = it.valor
            regiao.insere_fim(item((l_atual, c_atual)))

            vizinhos = [
                (l_atual - 1, c_atual), (l_atual + 1, c_atual),
                (l_atual, c_atual - 1), (l_atual, c_atual + 1)
            ]

            for vl, vc in vizinhos:
                if 0 <= vl < self.linhas and 0 <= vc < self.colunas:
                    if not visitados[vl][vc] and self.matriz[vl][vc] == cor_alvo:
                        visitados[vl][vc] = True
                        fila_busca.enfileira(item((vl, vc)))

        return regiao

    def realizar_jogada(self, linha: int, coluna: int) -> bool:
        regiao = self.obter_regiao(linha, coluna)

        # Regra: Uma região nunca tem um tamanho inferior a 2
        if regiao.tamanho < 2:
            return False

        # salva o estado na Pilha (deepcopy) para permitir desfazer
        estado_salvo = deepcopy(self.matriz)
        self.historico.empilha(item(estado_salvo))

        ptr = regiao.primeiro
        while ptr is not None:
            l, c = ptr.dado.valor
            self.matriz[l][c] = 0
            ptr = ptr.prox

        self.aplicar_gravidade()
        self.deslocar_colunas_vazias()

        return True

    def aplicar_gravidade(self):
        # Regra i: Os elementos que estão "acima" dos elementos da região eliminada "caem".
        for c in range(self.colunas):
            elementos_coluna = []
            for l in range(self.linhas - 1, -1, -1):
                if self.matriz[l][c] != 0:
                    elementos_coluna.append(self.matriz[l][c])

            idx = 0
            for l in range(self.linhas - 1, -1, -1):
                if idx < len(elementos_coluna):
                    self.matriz[l][c] = elementos_coluna[idx]
                    idx += 1
                else:
                    self.matriz[l][c] = 0

    def deslocar_colunas_vazias(self):
        # Regra ii: Quando uma coluna i fica sem elementos, a coluna i+1 se torna a coluna i
        colunas_validas = []
        for c in range(self.colunas):
            coluna_vazia = True
            for l in range(self.linhas):
                if self.matriz[l][c] != 0:
                    coluna_vazia = False
                    break
            if not coluna_vazia:
                colunas_validas.append(c)

        nova_matriz = [[0 for _ in range(self.colunas)] for _ in range(self.linhas)]
        for nova_c, c_original in enumerate(colunas_validas):
            for l in range(self.linhas):
                nova_matriz[l][nova_c] = self.matriz[l][c_original]

        self.matriz = nova_matriz

    def desfazer_jogada(self) -> bool:
        if self.historico.vazia():
            return False

        # Padrão TAD: obtem o topo, depois desempilha
        it = self.historico.elemento_topo()
        self.historico.desempilha()
        
        self.matriz = it.valor
        return True

    def verificar_fim_de_jogo(self) -> tuple[bool, str]:
        # Regra: Condições de término do jogo (Vitória ou Derrota)
        totalmente_zerado = True
        for l in range(self.linhas):
            for c in range(self.colunas):
                if self.matriz[l][c] != 0:
                    totalmente_zerado = False
                    break
        
        if totalmente_zerado:
            return (True, "VITORIA")

        # Verifica se ainda existe alguma região válida (>= 2 elementos iguais)
        for l in range(self.linhas):
            for c in range(self.colunas):
                if self.matriz[l][c] != 0:
                    regiao = self.obter_regiao(l, c)
                    if regiao.tamanho >= 2:
                        return (False, "EM_ANDAMENTO")

        return (True, "DERROTA")