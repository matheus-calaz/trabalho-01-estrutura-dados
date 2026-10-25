from __future__ import annotations
from dataclasses import dataclass
from copy import deepcopy

@dataclass
class item:
    valor: any

# LISTA LIGADA: Para armazenar a região
class no_lista:
    def __init__(self, x: item):
        self.dado: item = x
        self.prox: no_lista | None = None

class lista_ligada:
    def __init__(self):
        self.primeiro: no_lista | None = None
        self.ultimo: no_lista | None = None
        self.tamanho: int = 0

    def vazia(self) -> bool:
        return self.primeiro is None

    def insere_fim(self, x: item) -> bool:
        novo = no_lista(deepcopy(x))
        if self.vazia():
            self.primeiro = novo
        else:
            self.ultimo.prox = novo
        self.ultimo = novo
        self.tamanho += 1
        return True

# PILHA DINÂMICA: Para o Histórico
class no_pilha:
    def __init__(self, x: item):
        self.dado: item = x
        self.prox: no_pilha | None = None

class pilha_dinamica:
    def __init__(self):
        self.topo: no_pilha | None = None
  
    def vazia(self) -> bool:
        return self.topo is None

    def empilha(self, x: item):
        novo = no_pilha(deepcopy(x))
        novo.prox = self.topo
        self.topo = novo

    def desempilha(self):
        if self.vazia():
            raise ValueError('Pilha Vazia')
        rem = self.topo
        self.topo = self.topo.prox
        rem.prox = None

    def elemento_topo(self) -> item:
        if self.vazia():
            raise ValueError('Pilha Vazia')
        return deepcopy(self.topo.dado)

# FILA DINÂMICA COM SENTINELA: Para Busca
class no_fila:
    def __init__(self, x: item):
        self.dado: item = x
        self.prox: no_fila | None = None

class fila_dinamica:
    def __init__(self):
        # Nó sentinela
        self.primeiro = no_fila(item(None))
        self.ultimo = self.primeiro
  
    def vazia(self) -> bool:
        return self.primeiro.prox is None

    def enfileira(self, x: item):
        novo = no_fila(deepcopy(x))
        self.ultimo.prox = novo
        self.ultimo = novo
        
    def desenfileira(self):
        if self.vazia():
            raise ValueError('Fila vazia')
        rem = self.primeiro.prox
        self.primeiro.prox = rem.prox
        # Se removeu o último elemento, ajusta o ponteiro último para a sentinela
        if rem == self.ultimo:
            self.ultimo = self.primeiro
        rem.prox = None
            
    def obtem_primeiro(self) -> item:
        if self.vazia():
            raise ValueError('Fila vazia')
        return deepcopy(self.primeiro.prox.dado)