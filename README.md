# projeto-pdi
Projeto final da disciplina de PDI

# Solucionador de Cubo Mágico utilizando processamento de imagens
Estudantes:

Fernando Akio Tutume de Salles Pucci fernandopucci@usp.br 8957197

Vitor Kodhi Teruya kodhiteruya@usp.br 10284441

Yan Crisóstomo Rohwedder yanrohwedder@usp.br 9779263



O objetivo principal do projeto consiste em desenvolver um conversor de imagens para resolução de cubo mágico utilizando seis imagens como entrada, uma para cada face do cubo.

As imagens utilizadas neste projeto são fotos tiradas pelos próprios integrantes. Cada imagem contém uma face do cubo mágico, sendo assim, são necessárias seis fotos como entrada para podermos solucionar o cubo mágico. Exemplo de imagem de uma das faces como entrada:

<a href="https://github.com/aqilputi/projeto-pdi/blob/main/inputs/face_cube.jpeg"><img src="https://github.com/aqilputi/projeto-pdi/blob/main/inputs/face_cube.jpeg" width="250" height="250"/></a>

Primeiramente, tiramos uma foto de cada face de um cubo mágico embaralhado e utilizamos elas para o reconhecimento do estado do cubo. Cada imagem é transformada para gray scale:

<a href="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1.png"><img src="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1.png" width="500" height="500"/></a>

Depois é utilizado o filtro Gaussiano para aplicar Blur na imagem:

<a href="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_blur.png"><img src="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_blur.png" width="500" height="500"/></a>

Depois é utilizado o Canny Edge Detector, para detecção de bordas:

<a href="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_dilated.png"><img src="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_dilated.png" width="500" height="500"/></a>

E por último, é utilizado o Hough Transform para identificação de linhas, assim podemos encontrar os vértices:

<a href="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_lines.png"><img src="https://github.com/aqilputi/projeto-pdi/blob/main/outputs/Figure_1_lines.png" width="500" height="500"/></a>

### Coordenadas adquiridas de cada vértice
##### [0, 0], [74, 0], [149, 0], [221, 0]
##### [0, 76], [74, 76], [149, 76], [221, 76]
##### [0, 151], [74, 151], [149, 151], [221, 151]
##### [0, 221], [74, 221], [149, 221], [221, 221]



Com isso feito, podemos utilizar essa nova imagem para separar a imagem original em 9 imagens diferentes, uma para cada peça da face. Com a imagem de cada peça de cada face, criamos uma margem interna, onde retiramos as partes mais externas da imagem para podermos reduzir o ruído. Após isso, podemos finalmente fazer uma média da cor de todos os pixels dessa imagem. Como essa cor vai estar em RGB, precisamos convertê-la para HSL, para depois podermos comparar a cor obtida com valores de cores que já conhecemos, assim podemos aplicar uma label para cada cor. 

Repositório do solver: https://github.com/pglass/cube
```python
>>> from rubik.cube import Cube
>>> c = Cube("OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR")
>>> print(c)
    OOO
    OOO
    OOO
YYY WWW GGG BBB
YYY WWW GGG BBB
YYY WWW GGG BBB
    RRR
    RRR
    RRR
```


### Saída para o Solver
##### 'ygybwyrbobrbwwgwbbrwoworyggyrgrbrrwgybrgybwogoowoyoygo'

Tendo o cubo mágico em forma de labels, podemos então usar um algoritmo de resolução de cubo mágico pronta da internet para resolver o cubo mágico.

### Exemplo de Saída do Solver
##### ['B', 'B', 'B', 'E', 'L', 'Ei', 'Li', 'B']

Ver notação padrão de cubo mágico em:
https://ruwix.com/the-rubiks-cube/notation/

### Observações

Nós tiramos fotos em diversas condições, em ambiente com baixa luminosidade, com boa iluminação e com flash. Na maioria dos casos, o nosso algoritmo consegue detectar corretamente as cores de cada peça do cubo. Porém, quando o flash é usado, o cubo acaba refletindo muita luz, fazendo com que grande parte da peça fique totalmente branca, daí o nosso algoritmo acaba não conseguindo detectar a cor certa.

### Cargos

Fernando -> Ficou como o programador principal para implementação do código.

Vitor -> Ficou encarregado de tirar as fotos e de descobrir uma forma de calcular os valores das cores para identificação. Também ajudou na implementação do código e no Project Report.

Yan -> Ficou encarregado de fazer o Project Report, auxiliar na implementação do código e fazer a demonstração.
