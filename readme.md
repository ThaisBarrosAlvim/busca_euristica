# Visualização do problema de otimização de rota utilizando buscas heurísticas

Este código exemplifica o uso de buscas heurísticas em um problema de otimização de rota em uma malha rodoviária da Romênia. São implementados os algoritmos de busca gulosa e A*, que utilizam heurísticas diferentes para encontrar o caminho ótimo entre duas cidades.

### Malha rodoviária da Romênia

A malha rodoviária da Romênia é composta por diversas cidades conectadas por estradas. Para ilustrar a malha, é utilizado um gráfico onde cada cidade é representada por um ponto com suas coordenadas geográficas.

![Malha rodoviária da Romênia](https://raw.githubusercontent.com/ThaisBarrosAlvim/busca_euristica/master/plots/malha.png)

### Busca Gulosa

O algoritmo de busca gulosa utiliza como heurística a distância estimada em linha reta até o objetivo. Neste caso, o objetivo é a cidade de Bucareste. A busca gulosa percorre o caminho em direção à cidade que tem uma distancia mais próxima de Bucareste, sem levar em consideração a distancia local. 

![Busca Gulosa](https://raw.githubusercontent.com/ThaisBarrosAlvim/busca_euristica/master/plots/busca_g.png)

### Busca A*

O algoritmo A* utiliza como heurística a distância estimada mais a distância local. Neste caso, a distância local é levada em conta para tomar a decisão. A busca A* encontra o caminho ótimo em relação à busca gulosa.

![Busca A*](https://raw.githubusercontent.com/ThaisBarrosAlvim/busca_euristica/master/plots/busca_a.png)