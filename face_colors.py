import imageio
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import colorsys


def get_predominant_color(img) -> [int, int, int]:
    colors, count = np.unique(img.reshape(-1,img.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()].tolist()

def get_face_colors(face_img, cell_coord: list[list[list[int, int]]], pad, labels=None):
    face_colors: list = [[],[],[]]
    for i in range(len(cell_coord)-1):
        for j in range(len(cell_coord[i])-1):
            cell_img = np.array(
                face_img[
                    cell_coord[i][j][1]+pad:cell_coord[i+1][j][1]-pad,
                    cell_coord[i][j][0]+pad:cell_coord[i][j+1][0]-pad,
                ]
            )
            if labels:
                plt.title(labels[i][j])
            plt.imshow(cell_img)
            plt.show()
            face_colors[i].append(get_predominant_color(cell_img))

    return face_colors

def rgb_to_hls(colors):
    hls = [[], [], []]
    for i, row in enumerate(colors):
        for color in row:
            hls[i].append([round(c*255, 2) for c in colorsys.rgb_to_hls(*[c/255 for c in color])])
    return hls


def find_colors(image, coordinates):
    img = imageio.imread(image)
    colors = get_face_colors(img, coordinates, 20)
    hls = rgb_to_hls(colors)

    return hls

def show_colors(image, coordinates, labels):
    img = imageio.imread(image)
    get_face_colors(img, coordinates, 20, labels=labels)
