import imageio
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import colorsys


def get_predominant_color(img) -> [int, int, int]:
    colors, count = np.unique(img.reshape(-1,img.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()].tolist()

def get_face_colors(face_img, cell_coord: list[list[list[int, int]]], pad):
    face_colors: list = [[],[],[]]
    for i in range(len(cell_coord)-1):
        for j in range(len(cell_coord[i])-1):
            cell_img = np.array(
                face_img[
                    cell_coord[i][j][1]+pad:cell_coord[i+1][j][1]-pad,
                    cell_coord[i][j][0]+pad:cell_coord[i][j+1][0]-pad,
                ]
            )
            # plt.imshow(cell_img)
            # plt.show()
            # input()
            face_colors[i].append(get_predominant_color(cell_img))

    return face_colors

def rgb_to_hls(colors):
    hls = [[], [], []]
    for i, row in enumerate(colors):
        for color in row:
            hls[i].append([round(c*255, 2) for c in colorsys.rgb_to_hls(*[c/255 for c in color])])
    return hls


coordinates = [
    [[0, 0], [74, 0], [149, 0], [221, 0]],
    [[0, 76], [74, 76], [149, 76], [221, 76]],
    [[0, 151], [74, 151], [149, 151], [221, 151]],
    [[0, 221], [74, 221], [149, 221], [221, 221]],
]

img = imageio.imread("face_cube.jpeg")

colors = get_face_colors(img, coordinates, 20)
hls = rgb_to_hls(colors)

for row in hls:
    print(row)
