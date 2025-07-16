import cv2
import numpy as np
from random import randint as rnd

# Преобразует изображение в указанную четырёхугольную форму (перспективное искажение)
def doska_naklonyator(image, polygon, size):
    image = image.convert('RGBA')
    bbox = image.getbbox() # Определение ограничивающего прямоугольника непустой области
    cropped_image = image.crop(bbox)
    cropped_width, cropped_height = cropped_image.size
    image_np = np.array(cropped_image)

    # Задаём соответствие точек: polygon — куда вставляем, pts2 — откуда
    pts1 = np.float32(polygon)
    pts2 = np.float32(
        [[1, 1], [cropped_width - 1, 1], [cropped_width - 1, cropped_height - 1], [1, cropped_height - 1]])

    # Матрица перспективной трансформации и её применение
    matrix = cv2.getPerspectiveTransform(pts2, pts1)
    result = cv2.warpPerspective(image_np, matrix, size)
    return result

# Класс для многократного применения искажения к изображению
class Naclonyator:
    def __init__(self, image):
        image = image.convert('RGBA')
        bbox = image.getbbox()
        cropped_image = image.crop(bbox)
        self.image = np.array(cropped_image)[:, :, :3]
        h, w, _ = self.image.shape
        self.pts = np.float32(
            [[1, 1], [w - 1, 1], [w - 1, h - 1], [1, h - 1]])

    # Преобразование под указанный полигон
    def naklonyat(self, polygon, size):
        w, h = size

        # Определяем границы результирующего изображения
        x = [x for x, _ in polygon]
        y = [y for _, y in polygon]
        x, X = max(0, min(x)), min(max(x), w)
        y, Y = max(0, min(y)), min(max(y), h)

        # Сдвиг полигона в (0, 0) для корректной трансформации
        polygon = np.array(polygon) - np.array([x, y])

        matrix = cv2.getPerspectiveTransform(self.pts if rnd(0, 1) else np.concatenate((self.pts[2:], self.pts[:2])),
                                             np.float32(polygon))
        result = cv2.warpPerspective(self.image, matrix, (X - x, Y - y))
        return result, (x, y, X, Y)

