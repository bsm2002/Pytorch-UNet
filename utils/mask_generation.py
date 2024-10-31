import cv2
import numpy as np
import glob
import multiprocessing as mp

def masking(file):
    image = cv2.imread(filename=file)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 1. Create red mask
    lower_red1 = np.array([0, 150, 0])  # High saturation and low value
    upper_red1 = np.array([10, 255, 200])

    lower_red2 = np.array([170, 150, 0])
    upper_red2 = np.array([180, 255, 200])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    red_mask = mask1 | mask2

    # 2. Refine mask (remove noise and close edges)
    kernel = np.ones((3, 3), np.uint8)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel, iterations=6)

    # 3. Find contours
    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 4. Create labeled mask image
    # Create an empty mask of the same size as the original image (initialized to 0)
    mask_image = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)

    # 5. Resize mask image by 2x
    mask_image = cv2.resize(mask_image, None, fx=2, fy=2, interpolation=cv2.INTER_AREA)

    # 6. Resize contours by 2x
    contours = [np.int32(cnt * 2) for cnt in contours]

    # 7. Fill the inside of the contours to label the area as 1
    cv2.drawContours(mask_image, contours, -1, color=1, thickness=cv2.FILLED)

    # Optional: Display mask image
    # cv2.imshow('Mask Image', mask_image * 255)  # Convert 1 to 255 for visualization
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Optional: Save mask image to data/masks folder
    cv2.imwrite('../data/masks/pore/' + file.split('/')[-1], mask_image * 255)

if __name__ == "__main__":
    files = glob.glob('../data/pore/*_pore.jpg')
    files = [file for file in files if 'org' not in file]   # Exclude files with 'org' in the filename

    pool = mp.Pool(processes=mp.cpu_count())
    pool.map(masking, files)
    pool.close()
    pool.join()