import os
from PyPDF2 import PdfMerger


def merge_pdfs_in_folder(folder_path, output_filename='merged.pdf'):
    """
    Объединяет все PDF-файлы в указанной папке в один файл.

    :param folder_path: Путь к папке с PDF-файлами
    :param output_filename: Имя результирующего PDF-файла (по умолчанию 'merged.pdf')
    """
    # Проверяем существование папки
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"Папка '{folder_path}' не существует")

    # Получаем список PDF-файлов в папке (сортированный по имени)
    pdf_files = sorted([
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if f.lower().endswith('.pdf')
    ])

    # Проверяем наличие PDF-файлов
    if not pdf_files:
        raise FileNotFoundError(f"В папке '{folder_path}' не найдено PDF-файлов")

    # Объединяем файлы
    merger = PdfMerger()

    try:
        for pdf in pdf_files:
            merger.append(pdf)

        # Сохраняем результат
        merger.write(output_filename)
        return f"Успешно создан файл: {os.path.abspath(output_filename)}"

    finally:
        merger.close()


# Пример использования
if __name__ == "__main__":
    # Укажите путь к вашей папке с PDF-файлами
    folder = "./pdf"  # Замените на актуальный путь
    result = merge_pdfs_in_folder(folder)
    print(result)