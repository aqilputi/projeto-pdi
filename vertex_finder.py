import imageio
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import colorsys

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

img = imageio.imread("face_cube.jpeg")
show_img_rgb(img)
gray = to_grayscale(img)
show_img(gray)
gaussian = gaussian_blur(gray)
show_img(gaussian)
edge = auto_canny(gaussian)
show_img(edge)

kernel = np.ones((3,3), np.uint8)
dilated = dilate(edge, kernel)
show_img(dilated)

minLineLength = 30
maxLineGap = 10
lines = cv.HoughLinesP(dilated,1,np.pi/180, 50)
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        print(x1, y1, x2, y2)
        cv.line(img,(x1,y1),(x2,y2),(0,255,0),2)

show_img_rgb(img)
