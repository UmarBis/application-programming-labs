import csv
import argparse
import os
from typing import List
from icrawler.builtin import GoogleImageCrawler


def download_images(keyword: str, download_folder: str, num_images: int = 100) -> List[str]:
    """
    Скачивает изображения из Google по ключевому слову.
    :param keyword: Ключевое слово для поиска.
    :param download_folder: Папка для сохранения изображений.
    :param num_images: Макс количество изображений для скачивания.
    :return: Список путей к изображениям.
    """
    crawler = GoogleImageCrawler(storage={"root_dir": download_folder})
    crawler.crawl(keyword=keyword, max_num=num_images)

    image_paths = []
    for dirname, _, filenames in os.walk(download_folder):
        for filename in filenames:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                image_paths.append(os.path.join(dirname, filename))

    return image_paths

def save_annotations(image_paths: List[str], annotation_file: str):
    """
    Сохраняет аннотации изображений в CSV.
    :param image_paths: Список путей к изображениям.
    :param annotation_file: Путь к файлу, в котором будут сохранены аннотации.
    """
    with open(annotation_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['absolute_path', 'relative_path'])

        for image_path in image_paths:
            absolute_path = os.path.abspath(image_path)
            relative_path = os.path.relpath(image_path, start=os.path.dirname(annotation_file))
            writer.writerow([absolute_path, relative_path])

class ImageIterator:
    def __init__(self, annotation_file: str):
        """
        Инициализирует итератор изображений.
        :param annotation_file: Путь к файлу с аннотациями.
        """
        self.annotation_file = annotation_file
        self.image_paths = []
        self.current_index = 0
        self.load_annotations()

    def load_annotations(self):
        """Загружает аннотации изображений из CSV файла."""
        with open(self.annotation_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader)  # Пропустить заголовок
            self.image_paths = [row[0] for row in reader]

    def __iter__(self):
        """Возвращает объект итератора."""
        return self  # Возвращаем сам объект, чтобы он был итерируемым

    def __next__(self) -> str:
        """
        Возвращает следующий путь к изображению.
        :return: Путь к следующему изображению.
        :raises StopIteration: Если достигнут конец списка изображений.
        """
        if self.current_index < len(self.image_paths):
            image_path = self.image_paths[self.current_index]
            self.current_index += 1
            return image_path
        else:
            raise StopIteration

def main():
    """Основная функция для обработки аргументов и запуска программы."""
    parser = argparse.ArgumentParser(description="Скачивание изображений по ключевому слову.")
    parser.add_argument("keyword", type=str, help="Ключевое слово для поиска изображений")
    parser.add_argument("download_folder", type=str, help="Папка для загрузки изображений")
    parser.add_argument("annotation_file", type=str, help="Файл для сохранения аннотаций")

    args = parser.parse_args()

    keyword = args.keyword
    download_folder = args.download_folder
    annotation_file = args.annotation_file

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Скачивание изображений
    image_paths = download_images(keyword, download_folder)

    # Сохранение аннотаций
    save_annotations(image_paths, annotation_file)

    # Пример использования итератора
    image_iterator = ImageIterator(annotation_file)
    for image_path in image_iterator:
        print(image_path)

if __name__ == "__main__":
    main()