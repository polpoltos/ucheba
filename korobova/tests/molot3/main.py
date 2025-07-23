import zipfile
from docx import Document
from lxml import etree
import shutil
import os

def set_spacing_in_word(input_file, output_file, target_word, spacing_value):
    """
    Изменяет межсимвольный интервал для выбранных букв целевого слова в документе Word.

    :param input_file: Путь к входному файлу Word (например, "input.docx").
    :param output_file: Путь к выходному файлу Word (например, "output.docx").
    :param target_word: Слово, символы которого нужно найти и изменить интервал.
    :param spacing_value: Значение межсимвольного интервала (в единицах EMU, например, 200 для увеличения).
    """
    # Открываем документ
    doc = Document(input_file)
    target_letters = list(target_word)  # Разбиваем слово на символы
    letter_index = 0  # Индекс текущей буквы целевого слова

    # Обрабатываем абзацы и ранги
    for paragraph in doc.paragraphs:
        new_runs = []  # Буфер для новых run

        for run in paragraph.runs:
            run_text = run.text
            new_text = []  # Буфер для нового текста

            for char in run_text:
                # Проверяем, совпадает ли текущий символ с нужным
                if letter_index < len(target_letters) and char == target_letters[letter_index]:
                    # Увеличиваем межсимвольный интервал у этого символа
                    new_run = paragraph.add_run(char)
                    new_run._element.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}highlight_spacing", "true")
                    letter_index += 1
                else:
                    new_run = paragraph.add_run(char)
                new_text.append(new_run)

            # Если слово найдено, сбрасываем индекс
            if letter_index >= len(target_letters):
                letter_index = 0

            # Очищаем оригинальный run
            run.clear()

        # Добавляем новые runs в абзац
        for run in new_text:
            paragraph.runs.append(run)

    # Сохраняем документ с пометками
    temp_file = "temp.docx"
    doc.save(temp_file)

    # Редактируем XML-документ, чтобы задать межсимвольный интервал
    edit_spacing_in_xml(temp_file, output_file, spacing_value)

def edit_spacing_in_xml(input_file, output_file, spacing_value):
    """
    Редактирует XML-документ Word для изменения межсимвольного интервала.

    :param input_file: Путь к временному файлу Word.
    :param output_file: Путь к конечному файлу Word.
    :param spacing_value: Значение межсимвольного интервала (в единицах EMU).
    """
    # Распаковка docx-файла
    with zipfile.ZipFile(input_file, 'r') as zip_ref:
        zip_ref.extractall('temp_folder')

    # Путь к файлу document.xml внутри docx-архива
    document_path = 'temp_folder/word/document.xml'

    # Открытие XML-файла
    with open(document_path, "rb") as file:
        tree = etree.parse(file)

    # Пространство имён для XML
    namespace = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # Находим все элементы символов (<w:r>), у которых есть "highlight_spacing"
    for run in tree.xpath("//w:r[@w:highlight_spacing='true']", namespaces=namespace):
        # Удаляем наш пользовательский атрибут "highlight_spacing"
        del run.attrib["{http://schemas.openxmlformats.org/wordprocessingml/2006/main}highlight_spacing"]

        # Находим или создаём элемент <w:spacing>
        rPr = run.find("w:rPr", namespaces=namespace)  # Стиль текста
        if rPr is None:
            rPr = etree.SubElement(run, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr")

        spacing = rPr.find("w:spacing", namespaces=namespace)
        if spacing is None:
            spacing = etree.SubElement(rPr, "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}spacing")

        # Устанавливаем значение межсимвольного интервала
        spacing.set("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val", str(spacing_value))

    # Сохранение изменений в XML-файл
    tree.write(document_path, xml_declaration=True, encoding="UTF-8", standalone="yes")

    # Упаковка изменённого docx-файла
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        for foldername, subfolders, filenames in os.walk('temp_folder'):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, 'temp_folder')
                zip_ref.write(file_path, arcname)

    # Удаление временной папки
    shutil.rmtree('temp_folder')
    print(f"Файл с изменённым межсимвольным интервалом сохранён: {output_file}")

# Пример использования
if __name__ == "__main__":
    input_file = "begin.docx"  # Входной файл Word
    output_file = "end.docx"  # Выходной файл Word
    target_word = "секрет"  # Целевое слово
    spacing_value = 200  # Межсимвольный интервал (например, 200 единиц)

    set_spacing_in_word(input_file, output_file, target_word, spacing_value)
