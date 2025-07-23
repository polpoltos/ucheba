from docx import Document
from docx.shared import RGBColor


def highlight_letters_across_paragraphs(input_file, output_file, target_word, color=(255, 0, 0)):
    """
    Выделяет буквы целевого слова в тексте Word-документа, даже если они разбросаны по строкам.

    :param input_file: Путь к входному файлу Word (например, "input.docx").
    :param output_file: Путь к выходному файлу Word (например, "output.docx").
    :param target_word: Слово, которое нужно выделить.
    :param color: Цвет текста (RGB-кортеж, например, (255, 0, 0) для красного).
    """
    # Загружаем документ
    doc = Document(input_file)

    # Преобразуем целевое слово в список символов
    target_letters = list(target_word.lower())
    letter_index = 0  # Индекс текущей буквы целевого слова

    # Обрабатываем каждый абзац
    for paragraph in doc.paragraphs:
        new_runs = []  # Список для нового содержимого абзаца

        # Обходим все "ранги" (части текста с одинаковым стилем) в абзаце
        for run in paragraph.runs:
            new_text = []  # Буфер для нового текста без изменений

            for char in run.text:
                # Если текущая буква совпадает с символом целевого слова
                if letter_index < len(target_letters) and char.lower() == target_letters[letter_index]:
                    # Создаём новый run с выделением символа
                    highlighted_run = (char, RGBColor(*color))
                    new_runs.append(highlighted_run)
                    letter_index += 1  # Переходим к следующей букве целевого слова
                else:
                    # Добавляем символ без изменений
                    regular_run = (char, None)
                    new_runs.append(regular_run)

            # Если не завершили целевое слово, переходим к следующему фрагменту
            if letter_index >= len(target_letters):
                # Найдено всё слово — сбрасываем индекс
                letter_index = 0

        # Очищаем текст абзаца
        paragraph.clear()

        # Вставляем новые фрагменты с выделением
        for char, char_color in new_runs:
            run = paragraph.add_run(char)
            if char_color:
                run.font.color.rgb = char_color

    # Сохраняем изменения в новый файл
    doc.save(output_file)
    print(f"Файл успешно сохранён: {output_file}")


# Пример использования
if __name__ == "__main__":
    input_file = "Вход.docx"  # Путь к входному файлу Word
    output_file = "Выход.docx"  # Путь к выходному файлу Word
    target_word = "Мисс то"  # Слово для выделения
    color = (255, 0, 0)  # Красный цвет

    highlight_letters_across_paragraphs(input_file, output_file, target_word, color)
