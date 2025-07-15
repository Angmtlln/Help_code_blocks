import cv2
import csv
import os

# Список для хранения координат точек, отмеченных пользователем
points = []

# Функция обработки событий мыши
def click(event, x, y, flags, param):
    # Если было нажатие левой кнопки мыши
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Clicked: {(x, y)}")

# Путь к папке с изображениями
folder_path = r"Z:\WORK FILES\test_carpet"

with open('cords.csv', 'w', newline='') as csvfile:
    # Определяем заголовки столбцов
    fieldnames = ['photo_name', 'cords_carpet']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Перебираем все файлы в указанной папке
    for i in os.listdir(folder_path):
        image_path = os.path.join(folder_path, i)

        if not os.path.isfile(image_path):
            continue

        # Загружаем изображение
        img = cv2.imread(image_path)
        if img is None:
            print(f"[WARNING] Невозможно открыть изображение: {image_path}")
            continue

        points = []
        # Отображаем изображение в окне
        cv2.imshow("image", img)
        cv2.setMouseCallback("image", click)

        # Бесконечный цикл ожидания 4 кликов
        while True:
            cv2.waitKey(1)
            if len(points) >= 4:
                break

        cv2.destroyWindow("image")
        writer.writerow({'photo_name': i, 'cords_carpet': str(points)})