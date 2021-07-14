import imageio
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import colorsys

import math

from face_colors import find_colors
from color_labelling import label_colors


def to_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size=5):
    return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

def auto_canny(image, sigma=0.845):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    print('V: ', v)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(image, 50, 70)
    print('yolooo')
    # return the edged image
    return edged

def laplacian_edge(image):
    dst = cv.Laplacian(image, cv.CV_16U, ksize=1)
    return cv.convertScaleAbs(dst)

def sobel_edge(image, scale, delta, axis='x'):
    if axis == 'x':
        grad = cv.Sobel(image, cv.CV_16U, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    if axis == 'y':
        grad = cv.Sobel(image, cv.CV_16U, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    return cv.convertScaleAbs(grad)

def image_lines(image):
    pass

def show_img(img):
    plt.imshow(img, cmap='gray')
    plt.show()

def show_img_rgb(img):
    plt.imshow(img)
    plt.show()

def dilate(img, kernel, iterations=1):
    return cv.dilate(img, kernel, iterations=iterations)


def erosion(img, kernel, iterations=2):
    return cv.erode(img, kernel, iterations=iterations)


def _is_mergeable(line, other, distance, debug=False):
    if debug:
        print(other)
    if abs(line[0][0] - other[0][0]) < distance \
       and abs(line[0][1] - other[0][1]) < distance \
       and abs(line[1][0] - other[1][0]) < distance \
       and abs(line[1][1] - other[1][1]) < distance:
        if debug:
            print("True")
        return True
    if abs(line[0][0] - other[1][0]) < distance \
       and abs(line[0][1] - other[1][1]) < distance \
       and abs(line[1][0] - other[0][0]) < distance \
       and abs(line[1][1] - other[0][1]) < distance:
        return True
    return False


def merge_lines(lines, distance, debug=False):
    for line in lines:
        for other in lines:
            if _is_mergeable(line, other, distance, debug) and line != other:
                if debug:
                    print(f"{line} -- {other}")
                lines.remove(other)
    return lines

def normalize_point(pt):
    normalized = [0, 0]
    normalized[0] = pt[0] if pt[0] > 0 else 0
    normalized[1] = pt[1] if pt[1] > 0 else 0
    return (normalized[0], normalized[1])

def hook_lines(lines, hook_size, threshold):
    hooked_lines = []
    for line in lines:
        x0 = line[0][0]
        x1 = line[1][0]
        y0 = line[0][1]
        y1 = line[1][1]
        if line[0][0] - line[1][0] > threshold:
            if line[0][0] > line[1][0]:
                x0 = line[0][0] + hook_size
                x1 = line[1][0] - hook_size
            else:
                x0 = line[0][0] - hook_size
                x1 = line[1][0] + hook_size
        if line[0][1] - line[1][1] > threshold:
            if line[0][1] > line[1][1]:
                y0 = line[0][1] + hook_size
                y1 = line[1][1] - hook_size
            else:
                y0 = line[0][1] - hook_size
                y1 = line[1][1] + hook_size
        hooked_lines.append(((x0, y0), (x1, y1)))
    return hooked_lines


def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    else:
        raise Exception('lines do not intersect')
    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        raise Exception('lines do not intersect')
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)

    return int(x), int(y)


def sort_points(points):
    sorted_points = []
    for p in points:
        sorted_points.append((p[0] + p[1]*222, p))
    sorted_points = sorted(sorted_points, key=lambda tup: tup[0])
    for i in range(4):
        sorted_points[4*i: 4*i+4] = sorted(sorted_points[4*i: 4*i+4], key=lambda tup: tup[1][0])
    return sorted_points


def create_vertex_matrix(points):
    points = sort_points(points)
    matrix = [[] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            matrix[i].append(list(points[i*4 + j][1]))
    return matrix
