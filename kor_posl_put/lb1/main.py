import tkinter as tk
from tkinter import ttk, messagebox
import os

# База знаний (правила)
rules = [
    {
        "conditions": {
            "Головная_боль": "да",
            "Головокружение": "да",
            "Запоры": "да",
            "Метеоризм": "да",
            "Постоянные_или_схваткообразные_боли_в_области_желудка": "да",
            "Рвота": "да",
            "Слабость": "да",
            "Сухость_во_рту": "да",
            "Тошнота": "да"
        },
        "conclusion": "ботулизм"
    },
    {
        "conditions": {
            "Лихорадка": "да",
            "Температура": "да",
            "Обильный_пот": "да",
            "Ознобы": "да",
            "Увеличение_лимфоузлов": "да",
            "Сухость_во_рту": "да",
            "Жажда": "да",
            "Боли_в_мыщцах,костях,суставах": "да"
        },
        "conclusion": "бруцеллез"
    },
    {
        "conditions": {
            "Слабость": "да",
            "Познабливание": "да",
            "Бессонница": "да",
            "Температура": "да",
            "Головная_боль": "да",
            "Боли_в_глазах": "да",
            "Рвота": "да",
            "Лицо,шея,верхние_отделы_груди_и_спины_гиперемированы": "да"
        },
        "conclusion": "геморрагическая_лихорадка_с_почечным_синдромом(ГЛПС)"
    },
    {
        "conditions": {
            "Температура": "да",
            "Недомогание": "да",
            "Слабость": "да",
            "Потеря_аппетита": "да",
            "Тошнота": "да",
            "Рвота": "да",
            "Боли_в_правом_подреберье": "да",
            "Метеоризм": "да",
            "Нарушение_стула": "да"
        },
        "conclusion": "гепатит"
    },
    {
        "conditions": {
            "Недомогание": "да",
            "Повышенное_слюноотделение": "да",
            "Потеря_аппетита": "да",
            "Тошнота": "да",
            "Боли_в_животе": "да",
            "Понос": "да"
        },
        "conclusion": "дисбактериоз_кишечника"
    },
    {
        "conditions": {
            "Недомогание": "да",
            "Потеря_аппетита": "да",
            "Головная_боль": "да",
            "Слабость": "да",
            "Частый_стул": "да",
            "Боли_в_животе": "да"
        },
        "conclusion": "дизентерия"
    },
    {
        "conditions": {
            "На_сильно_покрасневшей_слизисто_оболочке_полости_рта_белесовато-желтый_налет": "да",
            "Сосание_и_жевание_болезнены": "да"
        },
        "conclusion": "кандидоз"
    },
    {
        "conditions": {
            "Повышенная_утомляемость": "да",
            "Снижение_работоспособности": "да",
            "Снижение_массы_тела": "да",
            "Ухудшение_сна": "да",
            "Кашель": "да",
            "Отдышка": "да",
            "Кожа_бледная": "да",
            "Потеря_аппетита": "да",
            "Температура": "да"
        },
        "conclusion": "туберкулез"
    },
    {
        "conditions": {
            "Кожный_зуд": "да",
            "Бессонница": "да"
        },
        "conclusion": "чесотка"
    }
]

# Список всех симптомов
symptoms = [
    "Бессонница", "Боли_в_глазах", "Боли_в_животе", "Боли_в_мыщцах,костях,суставах",
    "Боли_в_правом_подреберье", "Головная_боль", "Головокружение", "Жажда",
    "Запоры", "Кашель", "Кожа_бледная", "Кожный_зуд", "Лихорадка",
    "Лицо,шея,верхние_отделы_груди_и_спины_гиперемированы", "Метеоризм",
    "Нарушение_стула", "На_сильно_покрасневшей_слизисто_оболочке_полости_рта_белесовато-желтый_налет",
    "Недомогание", "Обильный_пот", "Ознобы", "Отдышка", "Повышенная_утомляемость",
    "Повышенное_слюноотделение", "Познабливание", "Понос",
    "Постоянные_или_схваткообразные_боли_в_области_желудка", "Потеря_аппетита",
    "Рвота", "Слабость", "Снижение_массы_тела", "Снижение_работоспособности",
    "Сосание_и_жевание_болезнены", "Сухость_во_рту", "Температура", "Тошнота",
    "Увеличение_лимфоузлов", "Ухудшение_сна", "Частый_стул"
]

# Список всех болезней
diseases = [
    "ботулизм", "бруцеллез", "геморрагическая_лихорадка_с_почечным_синдромом(ГЛПС)",
    "гепатит", "дизентерия", "дисбактериоз_кишечника", "кандидоз", "туберкулез", "чесотка"
]


class MedicalExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Экспертная система диагностики заболеваний")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        # Стиль
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('TCheckbutton', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'), padding=[10, 5])

        # Основной контейнер
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создаем вкладки
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка прямой диагностики
        self.forward_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.forward_frame, text="Прямая диагностика")
        self.create_forward_widgets()

        # Вкладка обратной диагностики
        self.backward_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.backward_frame, text="Обратная диагностика")
        self.create_backward_widgets()

        # Вкладка информации о болезнях
        self.info_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.info_frame, text="Информация о болезнях")
        self.create_info_widgets()

    def create_forward_widgets(self):
        # Фрейм для симптомов
        symptoms_frame = ttk.LabelFrame(self.forward_frame, text="Симптомы", padding=10)
        symptoms_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(symptoms_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Холст для симптомов
        self.canvas = tk.Canvas(symptoms_frame, yscrollcommand=scrollbar.set, bg='#f0f0f0')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        # Фрейм внутри холста
        self.symptoms_inner_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.symptoms_inner_frame, anchor=tk.NW)

        # Чекбоксы для симптомов
        self.symptom_vars = {}
        for symptom in symptoms:
            self.symptom_vars[symptom] = tk.StringVar(value="нет")
            cb = ttk.Checkbutton(
                self.symptoms_inner_frame,
                text=symptom.replace("_", " "),
                variable=self.symptom_vars[symptom],
                onvalue="да",
                offvalue="нет"
            )
            cb.pack(anchor=tk.W, padx=5, pady=2)

        # Обновление прокрутки после загрузки всех виджетов
        self.symptoms_inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Кнопка диагностики
        diagnose_button = ttk.Button(
            self.forward_frame,
            text="Провести диагностику",
            command=self.forward_chain
        )
        diagnose_button.pack(pady=10)

        # Поле для вывода результатов
        self.result_text = tk.Text(
            self.forward_frame,
            height=10,
            width=80,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопка очистки
        clear_button = ttk.Button(
            self.forward_frame,
            text="Очистить",
            command=self.clear_forward
        )
        clear_button.pack(pady=5)

    def create_backward_widgets(self):
        # Выбор болезни
        disease_frame = ttk.LabelFrame(self.backward_frame, text="Выберите предполагаемую болезнь", padding=10)
        disease_frame.pack(fill=tk.X, padx=5, pady=5)

        self.disease_var = tk.StringVar()
        disease_combo = ttk.Combobox(
            disease_frame,
            textvariable=self.disease_var,
            values=[d.replace("_", " ") for d in diseases],
            state="readonly"
        )
        disease_combo.pack(fill=tk.X, padx=5, pady=5)

        # Фрейм для симптомов
        symptoms_frame = ttk.LabelFrame(self.backward_frame, text="Симптомы", padding=10)
        symptoms_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(symptoms_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Холст для симптомов
        self.backward_canvas = tk.Canvas(symptoms_frame, yscrollcommand=scrollbar.set, bg='#f0f0f0')
        self.backward_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.backward_canvas.yview)

        # Фрейм внутри холста
        self.backward_inner_frame = ttk.Frame(self.backward_canvas)
        self.backward_canvas.create_window((0, 0), window=self.backward_inner_frame, anchor=tk.NW)

        # Чекбоксы для симптомов
        self.backward_symptom_vars = {}
        for symptom in symptoms:
            self.backward_symptom_vars[symptom] = tk.StringVar(value="нет")
            cb = ttk.Checkbutton(
                self.backward_inner_frame,
                text=symptom.replace("_", " "),
                variable=self.backward_symptom_vars[symptom],
                onvalue="да",
                offvalue="нет"
            )
            cb.pack(anchor=tk.W, padx=5, pady=2)

        # Обновление прокрутки после загрузки всех виджетов
        self.backward_inner_frame.update_idletasks()
        self.backward_canvas.config(scrollregion=self.backward_canvas.bbox("all"))

        # Кнопка проверки гипотезы
        check_button = ttk.Button(
            self.backward_frame,
            text="Проверить гипотезу",
            command=self.backward_chain
        )
        check_button.pack(pady=10)

        # Поле для вывода результатов
        self.backward_result_text = tk.Text(
            self.backward_frame,
            height=10,
            width=80,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.backward_result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопка очистки
        clear_button = ttk.Button(
            self.backward_frame,
            text="Очистить",
            command=self.clear_backward
        )
        clear_button.pack(pady=5)

    def create_info_widgets(self):
        # Выбор болезни
        disease_frame = ttk.LabelFrame(self.info_frame, text="Выберите болезнь для получения информации", padding=10)
        disease_frame.pack(fill=tk.X, padx=5, pady=5)

        self.info_disease_var = tk.StringVar()
        disease_combo = ttk.Combobox(
            disease_frame,
            textvariable=self.info_disease_var,
            values=[d.replace("_", " ") for d in diseases],
            state="readonly"
        )
        disease_combo.pack(fill=tk.X, padx=5, pady=5)

        # Кнопка получения информации
        info_button = ttk.Button(
            disease_frame,
            text="Показать информацию",
            command=self.show_disease_info
        )
        info_button.pack(pady=5)

        # Поле для вывода информации
        self.info_text = tk.Text(
            self.info_frame,
            height=20,
            width=80,
            wrap=tk.WORD,
            font=('Arial', 10)
        )
        self.info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Кнопка очистки
        clear_button = ttk.Button(
            self.info_frame,
            text="Очистить",
            command=self.clear_info
        )
        clear_button.pack(pady=5)

    def forward_chain(self):
        # Собираем факты
        facts = {}
        for symptom, var in self.symptom_vars.items():
            facts[symptom] = var.get()

        # Прямая цепочка рассуждений
        diagnosis = None
        explanation = []

        for rule in rules:
            match = True
            for condition, value in rule["conditions"].items():
                if facts.get(condition, "нет") != value:
                    match = False
                    break

            if match:
                diagnosis = rule["conclusion"]
                explanation.append(f"Найдено соответствие с болезнью: {diagnosis}")
                break

        # Вывод результатов
        self.result_text.delete(1.0, tk.END)
        if diagnosis:
            self.result_text.insert(tk.END, f"Диагноз: {diagnosis.replace('_', ' ')}\n\n")
            self.result_text.insert(tk.END, "Обоснование:\n")
            for line in explanation:
                self.result_text.insert(tk.END, f"- {line}\n")
        else:
            self.result_text.insert(tk.END, "Диагноз не определен. Недостаточно данных для точной диагностики.")

    def backward_chain(self):
        # Получаем предполагаемую болезнь
        disease = self.disease_var.get().replace(" ", "_")
        if not disease:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите болезнь для проверки")
            return

        # Собираем факты
        facts = {}
        for symptom, var in self.backward_symptom_vars.items():
            facts[symptom] = var.get()

        # Ищем выбранную болезнь в правилах
        target_rule = None
        for rule in rules:
            if rule["conclusion"] == disease:
                target_rule = rule
                break

        if not target_rule:
            messagebox.showerror("Ошибка", "Выбранная болезнь не найдена в базе знаний")
            return

        # Проверяем соответствие симптомов
        matched_symptoms = []
        missing_symptoms = []

        for condition, value in target_rule["conditions"].items():
            if facts.get(condition, "нет") == value:
                matched_symptoms.append(condition)
            else:
                missing_symptoms.append(condition)

        # Создаем новое окно для отображения результатов
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Результаты диагностики: {disease.replace('_', ' ')}")
        result_window.geometry("1000x700")

        # Создаем панель с вкладками
        notebook = ttk.Notebook(result_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка 1: Анализ соответствия
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Анализ соответствия")

        analysis_text = tk.Text(
            analysis_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            padx=10,
            pady=10
        )
        analysis_text.pack(fill=tk.BOTH, expand=True)

        # Добавляем текст анализа
        analysis_text.insert(tk.END, f"Анализ для болезни: {disease.replace('_', ' ')}\n\n", "header")

        if not missing_symptoms:
            analysis_text.insert(tk.END, "✅ Все необходимые симптомы присутствуют!\n\n", "success")
            analysis_text.insert(tk.END, f"Вероятный диагноз: {disease.replace('_', ' ')}\n", "success")
        else:
            analysis_text.insert(tk.END,
                                 f"Совпадение: {len(matched_symptoms)}/{len(target_rule['conditions'])} симптомов\n\n",
                                 "stats")

            analysis_text.insert(tk.END, "Совпадающие симптомы:\n", "subheader")
            for symptom in matched_symptoms:
                analysis_text.insert(tk.END, f"  ✓ {symptom.replace('_', ' ')}\n", "match")

            analysis_text.insert(tk.END, "\nОтсутствующие симптомы:\n", "subheader")
            for symptom in missing_symptoms:
                analysis_text.insert(tk.END, f"  ✗ {symptom.replace('_', ' ')}\n", "mismatch")

        # Настраиваем теги для форматирования
        analysis_text.tag_config("header", font=('Arial', 12, 'bold'))
        analysis_text.tag_config("success", foreground="green", font=('Arial', 11, 'bold'))
        analysis_text.tag_config("stats", font=('Arial', 11, 'bold'))
        analysis_text.tag_config("subheader", font=('Arial', 11, 'bold', 'underline'))
        analysis_text.tag_config("match", foreground="green")
        analysis_text.tag_config("mismatch", foreground="red")
        analysis_text.config(state=tk.DISABLED)

        # Вкладка 2: Информация о болезни
        info_frame = ttk.Frame(notebook)
        notebook.add(info_frame, text="Информация о болезни")

        info_text = tk.Text(
            info_frame,
            wrap=tk.WORD,
            font=('Arial', 11),
            padx=10,
            pady=10
        )
        info_text.pack(fill=tk.BOTH, expand=True)

        disease_info = self.load_disease_info(disease)
        if disease_info:
            info_text.insert(tk.END, disease_info)
        else:
            info_text.insert(tk.END, "Информация о болезни не найдена", "error")
        info_text.config(state=tk.DISABLED)

        # Вкладка 3: Возможные диагнозы (если есть)
        possible_diagnoses = []
        for rule in rules:
            if rule["conclusion"] == disease:
                continue

            match_count = 0
            required_count = len(rule["conditions"])
            for condition, value in rule["conditions"].items():
                if facts.get(condition, "нет") == value:
                    match_count += 1

            if match_count > 0:
                percentage = int(match_count / required_count * 100)
                possible_diagnoses.append({
                    "disease": rule["conclusion"],
                    "match": match_count,
                    "total": required_count,
                    "percentage": percentage,
                    "matched_symptoms": [
                        cond for cond in rule["conditions"]
                        if facts.get(cond, "нет") == "да"
                    ]
                })

        if possible_diagnoses:
            possible_diagnoses.sort(key=lambda x: x["percentage"], reverse=True)

            alt_frame = ttk.Frame(notebook)
            notebook.add(alt_frame, text="Возможные диагнозы")

            alt_notebook = ttk.Notebook(alt_frame)
            alt_notebook.pack(fill=tk.BOTH, expand=True)

            for idx, diagnosis in enumerate(possible_diagnoses[:3]):
                diag_frame = ttk.Frame(alt_notebook)
                alt_notebook.add(
                    diag_frame,
                    text=f"{diagnosis['disease'].replace('_', ' ')} ({diagnosis['percentage']}%)"
                )

                # Разделяем на две части
                paned = ttk.PanedWindow(diag_frame, orient=tk.HORIZONTAL)
                paned.pack(fill=tk.BOTH, expand=True)

                # Левая часть - симптомы
                symptoms_frame = ttk.Frame(paned)
                paned.add(symptoms_frame)

                ttk.Label(
                    symptoms_frame,
                    text="Совпадающие симптомы:",
                    font=('Arial', 10, 'bold')
                ).pack(pady=5)

                symptoms_text = tk.Text(
                    symptoms_frame,
                    wrap=tk.WORD,
                    height=10,
                    font=('Arial', 10),
                    padx=5,
                    pady=5
                )
                symptoms_text.pack(fill=tk.BOTH, expand=True)

                for symptom in diagnosis['matched_symptoms']:
                    symptoms_text.insert(tk.END, f"✓ {symptom.replace('_', ' ')}\n")
                symptoms_text.config(state=tk.DISABLED)

                # Правая часть - информация
                info_frame = ttk.Frame(paned)
                paned.add(info_frame)

                diag_info = self.load_disease_info(diagnosis['disease'])
                info_text = tk.Text(
                    info_frame,
                    wrap=tk.WORD,
                    font=('Arial', 11),
                    padx=10,
                    pady=10
                )
                info_text.pack(fill=tk.BOTH, expand=True)

                if diag_info:
                    info_text.insert(tk.END, diag_info)
                else:
                    info_text.insert(tk.END, "Информация не найдена", "error")
                info_text.config(state=tk.DISABLED)

        # Настраиваем теги для ошибок
        for text_widget in [info_text, symptoms_text, analysis_text]:
            if 'text_widget' in locals():
                text_widget.tag_config("error", foreground="red")

        # Кнопка закрытия
        ttk.Button(
            result_window,
            text="Закрыть",
            command=result_window.destroy
        ).pack(pady=10)

    def load_disease_info(self, disease):
        """Загружает информацию о болезни из файла в папке 'Исследования и лечение'"""
        try:
            # Приводим название болезни к формату имени файла
            file_mapping = {
                "ботулизм": "ботулизм.txt",
                "бруцеллез": "бруцеллез.txt",
                "геморрагическая лихорадка с почечным синдромом(ГЛПС)": "геморрагическая_лихорадка_с_почечным_синдромом.txt",
                "гепатит": "гепатит.txt",
                "дизентерия": "дизентерия.txt",
                "дисбактериоз_кишечника": "дисбактериоз_кишечника.txt",
                "кандидоз": "кандидоз.txt",
                "туберкулез": "туберкулез.txt",
                "чесотка": "чесотка.txt"
            }

            # Получаем имя файла по названию болезни
            filename = file_mapping.get(disease)
            if not filename:
                return None

            # Формируем полный путь к файлу
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, "Исследования и лечение", filename)

            # Проверяем существование файла
            if not os.path.exists(file_path):
                return None

            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception as e:
            print(f"Ошибка при загрузке информации: {e}")
            return None

    def show_disease_info(self):
        disease = self.info_disease_var.get().replace(" ", "_")
        if not disease:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите болезнь")
            return

        # Очищаем текстовое поле
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(tk.END, f"Информация о болезни: {disease.replace('_', ' ')}\n\n")

        # Загружаем информацию из файла
        disease_info = self.load_disease_info(disease)

        if disease_info:
            self.info_text.insert(tk.END, disease_info)
        else:
            self.info_text.insert(tk.END, "Информация по данной болезни отсутствует.\n")
            self.info_text.insert(tk.END,
                                  f"Файл с информацией о болезни '{disease}' не найден в папке 'Исследования и лечение'")

    def load_disease_info(self, disease):
        """Загружает информацию о болезни из файла в папке 'Исследования и лечение'"""
        try:
            # Приводим название болезни к формату имени файла
            file_mapping = {
                "ботулизм": "ботулизм.txt",
                "бруцеллез": "бруцеллез.txt",
                "геморрагическая_лихорадка_с_почечным_синдромом(ГЛПС)": "геморрагическая_лихорадка_с_почечным_синдромом.txt",
                "гепатит": "гепатит.txt",
                "дизентерия": "дизентерия.txt",
                "дисбактериоз_кишечника": "дисбактериоз_кишечника.txt",
                "кандидоз": "кандидоз.txt",
                "туберкулез": "туберкулез.txt",
                "чесотка": "чесотка.txt"
            }

            # Получаем имя файла по названию болезни
            filename = file_mapping.get(disease)
            if not filename:
                return None

            # Формируем полный путь к файлу
            dir_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(dir_path, "Исследования и лечение", filename)

            # Проверяем существование файла
            if not os.path.exists(file_path):
                return None

            # Читаем содержимое файла
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

        except Exception as e:
            print(f"Ошибка при загрузке информации: {e}")
            return None

    def clear_forward(self):
        for var in self.symptom_vars.values():
            var.set("нет")
        self.result_text.delete(1.0, tk.END)

    def clear_backward(self):
        self.disease_var.set("")
        for var in self.backward_symptom_vars.values():
            var.set("нет")
        self.backward_result_text.delete(1.0, tk.END)

    def clear_info(self):
        self.info_disease_var.set("")
        self.info_text.delete(1.0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalExpertSystem(root)
    root.mainloop()