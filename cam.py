#!/usr/bin/python
from picamera import PiCamera
from time import sleep
from skimage.measure import structural_similarity as ssim
import numpy as np
import cv2
from skimage import color
import time
import datetime

camera = PiCamera()

# Put your own directory here:
image_base = "/home/tero/cam/"
latest_image_path = image_base + "latest.jpg"
prev_image = None

threshold = 0.90

ind = 0
pix_per_detection = 2
detected_counter = 0

while True:
    camera.capture(latest_image_path)
    latest_image = cv2.imread(latest_image_path)
    if prev_image != None:
        prev_grey_image = color.rgb2gray(prev_image)
        latest_grey_image = color.rgb2gray(latest_image)
        sim = ssim(prev_grey_image, latest_grey_image)
        print "Similarity: ", sim
        if sim < threshold:
            detected_counter = pix_per_detection
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            cv2.imwrite(image_base + st + "_" + str(ind) + "_" + str(sim) + ".png", latest_image)
            cv2.imwrite(image_base + "latest_snap.png", latest_image)
            ind = ind + 1
            prev_image = latest_image
        elif detected_counter > 0:
            print "Detected counter: ", detected_counter
            detected_counter = detected_counter - 1
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
            cv2.imwrite(image_base + st + "_" + str(ind) + "_" + str(sim) + ".png", latest_image)
            ind = ind + 1
    else:
        prev_image = latest_image
