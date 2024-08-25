import cv2 as cv
import numpy as np

# List of image paths for the gear samples
image_paths = [
    r'C:\Users\peter\PeterMina_alexeagles_phase1\Task 2 Gear Inspection System\sample2.jpg',
    r'C:\Users\peter\PeterMina_alexeagles_phase1\Task 2 Gear Inspection System\sample3.jpg',
    r'C:\Users\peter\PeterMina_alexeagles_phase1\Task 2 Gear Inspection System\sample4.jpg',
    r'C:\Users\peter\PeterMina_alexeagles_phase1\Task 2 Gear Inspection System\sample5.jpg'
]

# Load the ideal gear image
ideal_img = cv.imread(r'C:\Users\peter\PeterMina_alexeagles_phase1\Task 2 Gear Inspection System\ideal.jpg')

if ideal_img is None:
    print("Error: Ideal gear image could not be loaded. Check the file path.")
    exit()

for i, path in enumerate(image_paths):
    # Load the sample image
    sample_img = cv.imread(path)

    if sample_img is None:
        print(f"Error: Sample image {i+1} could not be loaded. Check the file path.")
        continue

    cv.imshow('Ideal Gear', ideal_img)
    cv.imshow(f'Sample Gear {i+1}', sample_img)
    ####
    ############################################################
    # Convert the images to grayscale then threshold them to separate the gear teeth from the background
    gray_ideal = cv.cvtColor(ideal_img, cv.COLOR_BGR2GRAY)
    gray_sample = cv.cvtColor(sample_img, cv.COLOR_BGR2GRAY)
    # cv.imshow('grayscale ideal gear', gray_ideal)
    # cv.imshow('grayscale sample gear', gray_sample)
    ret, thresh_ideal = cv.threshold(gray_ideal, 127, 255, cv.THRESH_BINARY)
    ret, thresh_sample = cv.threshold(gray_sample, 127, 255, cv.THRESH_BINARY)
    # cv.imshow('threshold ideal gear', thresh_ideal)
    # cv.imshow('threshold sample gear', thresh_sample)
    ####
    ############################################################
    # xor the two thresholded images to get the differences
    bitwise_xor = cv.bitwise_xor(thresh_ideal, thresh_sample)
    cv.imshow(f'Bitwise XOR - Sample {i+1}', bitwise_xor)
    ####
    ############################################################
    # Get contours from the XOR image
    contours, hierarchy = cv.findContours(bitwise_xor, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # calculate the area of each contour and count the number of broken and worn teeth
    broken_teeth = 0
    worn_teeth = 0
    for cnt in contours:
        area = cv.contourArea(cnt)
        if area < 600 and area > 0:
            if 550 - area < 90:
                broken_teeth += 1
            elif 10 < area < 490:
                worn_teeth += 1

    print(f"Sample {i+1}:")
    print(f"Number of broken teeth: {broken_teeth}")
    print(f"Number of worn teeth: {worn_teeth}")

    # Wait for a key press to close the current window and proceed to the next
    cv.waitKey(0)
    cv.destroyAllWindows()

cv.waitKey(0)
cv.destroyAllWindows()
