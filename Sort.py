import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import logging
import shutil
import concurrent.futures


class FileSorter:
    CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
    TRANSLATION = (
        "a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
        "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

    MAP = {}

    for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        MAP[ord(cirilic)] = latin
        MAP[ord(cirilic.upper())] = latin.upper()

    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.EXTENSIONS = set()
        self.UNKNOWN = set()
        self.FOLDERS = []

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def scan_folder(self, folder):
        num_threads = os.cpu_count()  # Отримуємо кількість ядер на машині
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for item in folder.iterdir():
                if item.is_dir():
                    if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'others'):
                        self.FOLDERS.append(item)
                        executor.submit(self.scan_folder, item)
                    continue

                ext = self.get_extension(item.name)
                full_name = folder / item.name
                if not ext:
                    executor.submit(self.handle_file, full_name, self.source_folder / 'others')
                else:
                    handler_name = f"handle_{ext.lower()}"
                    handler = getattr(self, handler_name, self.handle_file)
                    executor.submit(handler, full_name, self.source_folder / ext.lower())

    def normalize(self, name):
        string = name.translate(self.MAP)
        translated_name = re.sub(r'[^a-zA-Z.0-9_]', '_', string)
        return translated_name

    def handle_file(self, file_name, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        translated_name = self.normalize(file_name.name)
        new_path = target_folder / translated_name
        file_name.replace(new_path)

    def handle_archive(self, file_name, target_folder):
        folder_for_file = target_folder / self.normalize(file_name.stem)
        folder_for_file.mkdir(exist_ok=True, parents=True)

        try:
            shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
        except shutil.ReadError:
            print(f'Error during unpacking archive {file_name}')
            return
        file_name.unlink()

    def handle_image(self, file_name, target_folder):
        self.handle_file(file_name, target_folder)

    def handle_audio(self, file_name, target_folder):
        self.handle_file(file_name, target_folder)

    def handle_video(self, file_name, target_folder):
        self.handle_file(file_name, target_folder)

    def handle_documents(self, file_name, target_folder):
        self.handle_file(file_name, target_folder)

    def core(self):
        self.scan_folder(self.source_folder)

        for folder in self.FOLDERS[::-1]:
            try:
                folder.rmdir()
            except OSError:
                print(f'Error during remove folder {folder}')


def get_user_input():
    while True:
        folder_path = input("Введіть шлях до папки для сортування: ")
        path = Path(folder_path)
        if path.exists() and path.is_dir():
            return path
        else:
            print("Шлях не існує або не є папкою. Спробуйте ще раз.")


if __name__ == "__main__":
    source_folder = get_user_input()
    file_sorter = FileSorter(source_folder)
    file_sorter.core()
    print("Сортування завершено успішно.")
