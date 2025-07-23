from docx import Document

def highlight_word_in_place(file_path, word_to_highlight, output_file, spaces=1):
    """
    Выделяет символы искомого слова, добавляя пробелы с двух сторон, сохраняя их положение в тексте.

    :param file_path: Путь к входному Word-документу.
    :param word_to_highlight: Слово, символы которого нужно выделить.
    :param output_file: Путь для сохранения обработанного документа.
    :param spaces: Количество пробелов с каждой стороны символа.
    """
    # Открыть документ
    doc = Document(file_path)
    spacer = ' ' * spaces  # Пробелы для добавления с двух сторон

    for paragraph in doc.paragraphs:
        new_text = ""
        match_index = 0  # Индекс текущего символа в искомом слове

        for char in paragraph.text:
            # Если символ совпадает с текущей частью слова
            if match_index < len(word_to_highlight) and char == word_to_highlight[match_index]:
                new_text += spacer + char + spacer  # Добавляем пробелы вокруг символа
                match_index += 1  # Переход к следующему символу слова
            else:
                new_text += char  # Символ остаётся без изменений

        # Заменить текст абзаца обновлённым
        paragraph.clear()  # Очистить текущий текст абзаца
        paragraph.add_run(new_text)  # Добавить обработанный текст

    # Сохранить результат
    doc.save(output_file)

# Пример использования
input_file = "input.docx"
output_file = "output.docx"
highlight_word = "молот"  # Слово для выделения
spaces_between_chars = 2  # Количество пробелов с каждой стороны

highlight_word_in_place(input_file, highlight_word, output_file, spaces_between_chars)
print(f"Обработанный файл сохранён как {output_file}.")
