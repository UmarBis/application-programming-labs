import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def read_image(file_path) -> np.ndarray:
    """
    Считывает изображение из файла.
    :param file_path: Путь к файлу изображения
    :return: Изображение как массив NumPy
    """
    image = cv2.imread(file_path)
    return image

def get_image_size(image) -> tuple:
    """
    Получает размер изображения.
    :param image: Изображение как массив NumPy
    :return: Размеры (высота, ширина)
    """
    height, width = image.shape[:2]
    return height, width

def display_image(image, title) -> None:
    """
    Отображает изображение с заданным заголовком.
    :param image: Изображение как массив NumPy
    :param title: Заголовок окна
    """
    cv2.imshow(title, image)
    cv2.waitKey(0)

def combine_images(image1, image2):
    """
    Объединяет 2 изображения
    :param image1: Изображение №1 как массив NumPy
    :param image2: Изображение №2 как массив NumPy
    """
    if image1.shape[0] != image2.shape[0]:
        res_image2 = cv2.resize(image2, (image2.shape[1], image1.shape[0]))

    combined_image = cv2.hconcat([image1, res_image2])
    return combined_image

def save_image(image, output) -> None:
    """
    Сохраняет изображение в файл.
    :param image: Изображение как массив NumPy
    :param output: Путь, куда нужно сохранить изображение
    """
    os.chdir(output)
    print(os.listdir(output))
    cv2.imwrite('combined_img.png', image)

def hist(img:np.ndarray)->tuple:
    """
    Создает гистограммы изображения c помощью библиотеки OpenCV
    :param img: изображение для анализа
    :return: Гистограммы трех цветов
    """
    b = cv2.calcHist([img], [0], None, [256], [0, 256])
    g = cv2.calcHist([img], [1], None, [256], [0, 256])
    r = cv2.calcHist([img], [2], None, [256], [0, 256])
    return b,g,r

def hist_show(b:np.ndarray, g:np.ndarray, r:np.ndarray)->None:
    """
    Отображает гистограммы для трех цветов с помощью библиотеки matplotlib
    :param b: Синяя гистограмма
    :param g: Зеленая гистограмма
    :param r: Красная гистограмма
    """
    plt.figure(figsize=(10, 5))
    plt.plot(b, label='Синяя линия', color='blue')
    plt.plot(g, label='Зеленая линия', color='green')
    plt.plot(r, label='Красная линия', color='red')
    plt.xlim([0, 256])
    plt.title('Гистограмма цвета изображения')
    plt.xlabel('Интенсивность цвета')
    plt.ylabel('Частота')
    plt.grid()
    plt.legend()
    plt.show()

def main():
    """
       :param image_path1: Путь к 1 файлу изображения
       :param image_path2: Путь ко 2 файлу изображения
       :param output_path: Путь для сохранения изображения
       """
    parser = argparse.ArgumentParser(description='Обработка изображения.')
    parser.add_argument('image_path1', type=str, help='Путь к 1 файлу изображения')
    parser.add_argument('image_path2', type=str, help='Путь ко 2 файлу изображения')
    parser.add_argument('output_path', type=str, help='Путь для сохранения изображения')

    args = parser.parse_args()

    try:
        # Считываем изображение
        image1 = read_image(args.image_path1)
        if image1 is None:
            raise ValueError(f"Failed to load image.")
        image2 = read_image(args.image_path2)
        if image2 is None:
            raise ValueError(f"Failed to load image.")

        # Вывод размеров изображений
        print(f"Size of Image 1: {get_image_size(image1)}")
        print(f"Size of Image 2: {get_image_size(image2)}")

        # Строим гистограмму
        b,g,r=hist(image1)
        hist_show(b,g,r)

        # Объединение изображений
        combined_image = combine_images(image1, image2)

        # Отображаем исходные изображения и результат.
        display_image(image1, title= 'Original image1')
        display_image(image2, title='Original image2')
        display_image(combined_image, title='Combined image')

        # Сохраняем изображение
        save_image(combined_image, args.output_path)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
   main()