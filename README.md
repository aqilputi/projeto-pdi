# projeto-pdi
Projeto final da disciplina de PDI

# Solucionador de Cubo Mágico utilizando processamento de imagens
Estudantes:

Fernando Akio Tutume de Salles Pucci fernandopucci@usp.br 8957197

Vitor Kodhi Teruya kodhiteruya@usp.br 10284441

Yan Crisóstomo Rohwedder yanrohwedder@usp.br 9779263



O objetivo principal do projeto consiste em desenvolver um conversor de imagens para resolução de cubo mágico utilizando seis imagens como entrada, uma para cada face do cubo.

As imagens utilizadas neste projeto são fotos tiradas pelos próprios integrantes. Cada imagem contém uma face do cubo mágico, sendo assim, são necessárias seis fotos como entrada para podermos solucionar o cubo mágico. Exemplo de imagem para entrada:

Primeiramente, tiramos uma foto de cada face de um cubo mágico embaralhado e utilizamos elas para o reconhecimento do estado do cubo. Cada imagem é transformada para gray scale, depois é utilizado o filtro Gaussiano para aplicar Blur na imagem. Depois é utilizado o Canny Edge Detector, para detecção de bordas. E por último, é utilizado o Hough Transform para identificação de linhas, assim podemos encontrar os vértices. Com isso feito, podemos utilizar essa nova imagem para separar a imagem original em 9 imagens diferentes, uma para cada peça da face. Com a imagem de cada peça de cada face, criamos uma margem interna, onde retiramos as partes mais externas da imagem para podermos reduzir o ruído. Após isso, podemos finalmente fazer uma média da cor de todos os pixels dessa imagem. Como essa cor vai estar em RGB, precisamos convertê-la para HSL, para depois podermos comparar a cor obtida com valores de cores que já conhecemos, assim podemos aplicar uma label para cada cor. Tendo o cubo mágico em forma de labels, podemos então usar um algoritmo de resolução de cubo mágico pronta da internet para resolver o cubo mágico.

Por se tratar de uma entrega parcial, o código é apenas um protótipo, com intuito de mostrar sua funcionalidade, por isso, o código não está bem organizado nem muito comentado. Abaixo temos as imagens resultantes de cada etapa do processo de conversão:
