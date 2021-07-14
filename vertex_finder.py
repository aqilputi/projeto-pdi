import imageio
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import colorsys

import math

from face_colors import find_colors, show_colors
from color_labelling import label_colors


def to_grayscale(image):
    return cv.cvtColor(image, cv.COLOR_BGR2GRAY)

def gaussian_blur(img, kernel_size=5):
    return cv.GaussianBlur(img, (kernel_size, kernel_size), 0)

def auto_canny(image, sigma=0.33):
    # compute the median of the single channel pixel intensities
    v = np.median(image)
    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv.Canny(image, lower, upper)
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


img = imageio.imread("inputs/face_cube.jpeg")
show_img_rgb(img)
gray = to_grayscale(img)
show_img(gray)
gaussian = gaussian_blur(gray)
show_img(gaussian)
edge = auto_canny(gaussian)
show_img(edge)

kernel = np.ones((3,3), np.uint8)
dilated = dilate(edge, kernel)
kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
dilated = cv.filter2D(dilated, cv.CV_8U, kernel)
show_img(dilated)

line_points = []

def normalize_point(pt):
    normalized = [0, 0]
    normalized[0] = pt[0] if pt[0] > 0 else 0
    normalized[1] = pt[1] if pt[1] > 0 else 0
    return (normalized[0], normalized[1])

lines = cv.HoughLines(dilated, 1, np.pi/180, 170)
print(dilated.shape)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = math.cos(theta)
        b = math.sin(theta)
        x0 = a * rho
        y0 = b * rho
        pt1 = (int(x0 + img.shape[0]*(-b)), int(y0 + img.shape[1]*(a)))
        pt2 = (int(x0 - img.shape[0]*(-b)), int(y0 - img.shape[1]*(a)))
        pt1 = normalize_point(pt1)
        pt2 = normalize_point(pt2)
        line_points.append((pt1, pt2))


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


merged_lines = merge_lines(line_points, 30)
merged_lines = hook_lines(merged_lines, 20, 50)
for pt1, pt2 in merged_lines:
    print(pt1, pt2)
    cv.line(img, pt1, pt2, (0,0,255), 3, cv.LINE_AA)
    show_img_rgb(img)



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


lines = merged_lines.copy()

points = []

for line in lines:
    for other in lines:
        if other != line:
            try:
                p = line_intersect(line[0][0], line[0][1], line[1][0], line[1][1], other[0][0], other[0][1], other[1][0], other[1][1])
            except:
                pass
            else:
                points.append(p)
                img = cv.circle(img, p, radius=2, color=(0, 255, 255), thickness=5)
                show_img_rgb(img)

points = list(set(points))


def sort_points(points):
    sorted_points = []
    print(points)
    for p in points:
        sorted_points.append((p[0] + p[1]*222, p))
    sorted_points = sorted(sorted_points, key=lambda tup: tup[0])
    for i in range(4):
        sorted_points[4*i: 4*i+4] = sorted(sorted_points[4*i: 4*i+4], key=lambda tup: tup[1][0])
    return sorted_points


def create_vertex_matrix(points):
    points = sort_points(points)
    matrix = [[] for _ in range(4)]
    print(points)
    for i in range(4):
        for j in range(4):
            matrix[i].append(list(points[i*4 + j][1]))
    return matrix


vertexes = create_vertex_matrix(points)
hls = find_colors("inputs/face_cube.jpeg", vertexes)

labels = label_colors(hls)

show_colors("inputs/face_cube.jpeg", vertexes, labels)
