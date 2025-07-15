import numpy as np
import cv2
from utils import Placer
from naklon import Naclonyator
from PIL import Image
from time import time
from math import floor
from random import randint as rnd

# Загрузка изображения с прозрачностью (альфа-канал)
img = cv2.imread('mask_.png', cv2.IMREAD_UNCHANGED)

# Загрузка фонового изображения (досок)
doski = Image.open('doska_.png')
mask = img[:, :, -1] == 0
inpaint = np.zeros_like(mask, dtype='uint8')

img = img[:, :, :3]
h, w = mask.shape
bg = np.zeros_like(img)

# Опорные точки для трансформации (вероятно, углы области размещения)
pts = [(367.0, 900.0), (343.0, 653.0), (581.0, 629.0), (796.0, 816.0)]

placer = Placer(pts)
naklonyator = Naclonyator(doski)

t = time()

Y, X = mask.nonzero()
used = set()


# Основной цикл обработки каждого пикселя объекта
for x, y in zip(X, Y):
    if bg[y, x].sum() > 1:
        continue

    # Получаем новые координаты после трансформации
    x, y = placer.get_pos(x, y)
    x = floor(x)
    d = x % 2 * 0.5
    y = floor(y - d) + d

    # Пропускаем уже использованные позиции
    if (x, y) in used:
        continue
    used.add((x, y))  # Добавляем позицию в использованные

    # Получаем 4 точки для трансформации
    points = np.array([
        placer.get(x, y),
        placer.get(x, y + 1),
        placer.get(x + 1, y + 1),
        placer.get(x + 1, y)
    ])

    # Применяем трансформацию/наклон к области
    placed, (x, y, X, Y) = naklonyator.naklonyat(points, (w, h))
    bg[y:Y, x:X] = np.maximum(bg[y:Y, x:X], placed)

# Генерация полигонов для заполнения областей
for x, y in used:
    polygons = []
    area = 0

    while area < 0.2:
        x1, x2 = sorted((rnd(1, 9) / 10, rnd(1, 9) / 10))
        y1, y2 = sorted((rnd(1, 9) / 10, rnd(1, 9) / 10))
        area += (y2 - y1) * (x2 - x1)
        polygons.append((x1 + x, y1 + y, x2 + x, y2 + y))

    # Трансформируем координаты полигонов
    polygons = [
        (placer.get(x, y), placer.get(x, Y),
         placer.get(X, Y), placer.get(X, y))
        for x, y, X, Y in polygons
    ]
    [cv2.fillPoly(inpaint, [polygon], (255, 255, 255))
     for polygon in np.array(polygons)]

print(time() - t)

inpaint[np.invert(mask)] = 0
img[mask] = bg[mask]

# Сохранение результатов
cv2.imwrite('asd.jpg', img)  # Основное обработанное изображение
cv2.imwrite('test_mask.png', inpaint)  # Маска для инпаинтинга