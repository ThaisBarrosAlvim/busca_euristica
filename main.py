from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt


class Cidade:
    def __init__(self, nome, coordenadas: Optional[tuple] = None):
        self.nome = nome
        self.coordenadas = coordenadas

    def __repr__(self):
        return self.nome

    def __str__(self):
        return self.nome

    def __eq__(self, other):
        return self.nome == other.nome

    def __hash__(self):
        return hash(self.nome)


class Grafo:
    def __init__(self):
        self.vertices = {}

    def adicionar_vertice(self, cidade: Cidade, distancia_objetivo: int = 0):
        self.vertices[cidade] = {'dist_obj': distancia_objetivo, 'proximas': []}

    def adicionar_aresta(self, cidade1: Cidade, cidade2: Cidade, distancia_local: int):
        self.vertices[cidade1]['proximas'].append((cidade2, distancia_local))
        self.vertices[cidade2]['proximas'].append((cidade1, distancia_local))

    def busca_gulosa(self, origem: Cidade, destino: Cidade):
        caminho = [origem]
        distancia = 0
        atual = origem
        while atual != destino:
            proximo = min(self.vertices[atual]['proximas'], key=lambda x: self.vertices[x[0]]['dist_obj'])
            if proximo is None:
                return None
            distancia += proximo[1]
            caminho.append(proximo[0])
            atual = proximo[0]
        return caminho, distancia

    def busca_a_estrela(self, origem: Cidade, destino: Cidade):
        caminho = [origem]
        distancia = 0
        atual = origem
        while atual != destino:
            proximo = min(self.vertices[atual]['proximas'], key=lambda x: x[1] + self.vertices[x[0]]['dist_obj'])
            if proximo is None:
                return None
            distancia += proximo[1]
            caminho.append(proximo[0])
            atual = proximo[0]
        return caminho, distancia

    @classmethod
    def carrega_csv(cls, cidades_csv, arestas_csv) -> 'Grafo':
        grafo = Grafo()

        # Adicionar as cidades
        cidades = pd.read_csv(cidades_csv, skiprows=0)
        for cidade in cidades.itertuples():
            grafo.adicionar_vertice(Cidade(cidade[1], (cidade[2], cidade[3])), cidade[4])

        # Adicionar as arestas
        arestas = pd.read_csv(arestas_csv, skiprows=0)
        for aresta in arestas.itertuples():
            grafo.adicionar_aresta(Cidade(aresta[1]), Cidade(aresta[2]), aresta[3])

        return grafo

    def visualiza_cidades(self, titulo, subtitulo=None, caminho=None):
        if caminho is not None:
            caminho = [cidade.nome for cidade in caminho]

        # Obter as coordenadas das cidades
        coords = {}
        for v in self.vertices:
            coords[v.nome] = v.coordenadas

        # Criar uma lista com todas as arestas
        arestas = []
        for cidade1 in self.vertices:
            for cidade2, dist_local in self.vertices[cidade1]['proximas']:
                arestas.append((cidade1.nome, cidade2.nome, dist_local))

        # Criar o gráfico
        plt.suptitle(titulo)
        if subtitulo is not None:
            plt.title(subtitulo)

        # Definir a escala do gráfico
        min_x = min(coords.values(), key=lambda x: x[0])[0]
        max_x = max(coords.values(), key=lambda x: x[0])[0]
        min_y = min(coords.values(), key=lambda x: x[1])[1]
        max_y = max(coords.values(), key=lambda x: x[1])[1]
        pad = 50
        plt.xlim(min_x - pad, max_x + pad)
        plt.ylim(min_y - pad, max_y + pad)

        # Plotar as arestas como linhas
        for cidade1_nome, cidade2_nome, dist_local in arestas:
            x1, y1 = coords[cidade1_nome]
            x2, y2 = coords[cidade2_nome]

            plt.plot([x1, x2], [y1, y2], '-', color='gray', alpha=0.5)

            # Adicionar a distância entre as cidades
            xc = (x1 + x2) / 2
            yc = (y1 + y2) / 2
            plt.text(xc, yc, str(dist_local), fontsize=6)

        if caminho is not None:
            # Plotar o caminho como linhas
            for i in range(len(caminho) - 1):
                cidade1_nome = caminho[i]
                cidade2_nome = caminho[i + 1]
                x1, y1 = coords[cidade1_nome]
                x2, y2 = coords[cidade2_nome]
                plt.plot([x1, x2], [y1, y2], '-', color='blue', alpha=0.5)

        # Plotar as cidades como pontos
        for cidade, coord in coords.items():
            if caminho is not None and cidade in caminho:
                plt.plot(coord[0], coord[1], 'sb')
            else:
                plt.plot(coord[0], coord[1], 'sr')
            plt.text(coord[0] + 10, coord[1] + 10, cidade, fontsize=8)

        plt.show()


def main():
    # Criar o grafo da Romênia
    grafo_romenia = Grafo.carrega_csv('data/cidades_romenia.csv', 'data/arestas_romenia.csv')
    grafo_romenia.visualiza_cidades('Malha rodoviária da Romênia')

    # Busca Gulosa
    caminho_g, distancia_g = grafo_romenia.busca_gulosa(Cidade('Arad'), Cidade('Bucharest'))
    print(f'Busca Gulosa\nCaminho: {"->".join(map(str, caminho_g))}\nDistância: {distancia_g} milhas\n\n')
    grafo_romenia.visualiza_cidades('Malha rodoviária da Romênia',
                                    f'Caminho percorrido pela Busca Gulosa com Distancia total de: {distancia_g}',
                                    caminho_g)

    # Busca A*
    caminho_a, distancia_a = grafo_romenia.busca_a_estrela(Cidade('Arad'), Cidade('Bucharest'))
    print(f'Busca A*\nCaminho: {"->".join(map(str, caminho_a))}\nDistância: {distancia_a} milhas')
    grafo_romenia.visualiza_cidades('Malha rodoviária da Romênia',
                                    f'Caminho percorrido pela Busca A* com Distancia total de: {distancia_a}',
                                    caminho_a)


if __name__ == '__main__':
    main()
