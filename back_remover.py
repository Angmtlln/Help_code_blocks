import cv2
import numpy as np


def remove_bg_with_grabcut(image_path, output_path):
    """
    Убрать белый фон вокруг объекта

    :param image_path: путь до фото
    :param output_path:  результат фотографии без белого фона

    """
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    mask = np.zeros((h, w), dtype=np.uint8)

    rect = (10, 10, w - 20, h - 20)

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    cv2.grabCut(img, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    final_mask = np.where((mask == 2) | (mask == 0), 0, 255).astype('uint8')
    final_mask = cv2.GaussianBlur(final_mask, (5, 5), 0)

    b, g, r = cv2.split(img)
    rgba = [b, g, r, final_mask]
    result = cv2.merge(rgba)

    cv2.imwrite(output_path, result)


remove_bg_with_grabcut('clean/aiease_1751276239086.png', 'battery_no_bg.png')