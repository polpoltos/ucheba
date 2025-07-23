import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
from matplotlib.figure import Figure


class FuzzyApparatusSelector:
    def __init__(self, master):
        self.master = master
        master.title("Нечёткий выбор аппарата")
        master.geometry("1200x800")

        self.create_widgets()
        self.create_graphs()
        self.create_truth_labels()  # Добавляем метки для степеней истинности

    def create_truth_labels(self):
        # Создаем метки для отображения степеней истинности
        truth_frame = ttk.Frame(self.master)
        truth_frame.pack(fill=tk.X, padx=10, pady=5)

        self.truth_labels = []
        for i in range(4):
            label = ttk.Label(truth_frame, text=f"Аппарат {chr(65 + i)}: 0.000")
            label.pack(side=tk.LEFT, padx=10)
            self.truth_labels.append(label)

    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(main_frame, text="Параметры процесса")
        input_frame.pack(fill=tk.X, padx=5, pady=5)

        # Поле для ввода температуры
        ttk.Label(input_frame, text="Температура (100-150 °C):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.temp_entry = ttk.Entry(input_frame)
        self.temp_entry.grid(row=0, column=1, padx=5, pady=5)
        self.temp_entry.insert(0, "100")

        # Поле для ввода расхода
        ttk.Label(input_frame, text="Расход сырья (70-110 ед.):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.flow_entry = ttk.Entry(input_frame)
        self.flow_entry.grid(row=1, column=1, padx=5, pady=5)
        self.flow_entry.insert(0, "70")

        # Кнопка расчета
        calc_btn = ttk.Button(input_frame, text="Определить аппарат", command=self.calculate)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=10)

        # Фрейм для вывода результатов
        result_frame = ttk.LabelFrame(main_frame, text="Результаты")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Графики принадлежности
        self.graph_frame = ttk.Frame(result_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Текстовый вывод
        self.output_text = tk.Text(result_frame, height=15, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(self.output_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)

    def create_graphs(self):
        # Создаем графики с расширенными диапазонами
        fig = Figure(figsize=(8, 4), dpi=100)

        # График для температуры (диапазон 50-200)
        temp_plot = fig.add_subplot(211)
        x_temp = np.linspace(100, 150, 500)

        # Ограничиваем значения функций диапазоном [0, 1]
        y_low = [max(0, min(1, self.temp_low(t))) for t in x_temp]
        y_medium = [max(0, min(1, self.temp_medium(t))) for t in x_temp]
        y_high = [max(0, min(1, self.temp_high(t))) for t in x_temp]

        temp_plot.plot(x_temp, y_low, 'b', label='Малая')
        temp_plot.plot(x_temp, y_medium, 'g', label='Средняя')
        temp_plot.plot(x_temp, y_high, 'r', label='Большая')

        temp_plot.set_title("Функции принадлежности для температуры")
        temp_plot.set_xlabel("Температура (°C)")
        temp_plot.set_ylabel("Степень принадлежности [0,1]")
        temp_plot.set_ylim(0, 1.1)  # Фиксируем ось Y от 0 до 1.1
        temp_plot.legend()
        temp_plot.grid()

        # Добавляем вертикальные линии для рабочего диапазона (100-150)
        temp_plot.axvline(x=100, color='gray', linestyle='--')
        temp_plot.axvline(x=150, color='gray', linestyle='--')
        temp_plot.text(125, -0.1, "Рабочий диапазон", ha='center', color='gray')

        # График для расхода (диапазон 60-120)
        flow_plot = fig.add_subplot(212)
        x_flow = np.linspace(70, 110, 500)

        y_low_f = [max(0, min(1, self.flow_low(f))) for f in x_flow]
        y_medium_f = [max(0, min(1, self.flow_medium(f))) for f in x_flow]
        y_high_f = [max(0, min(1, self.flow_high(f))) for f in x_flow]
        y_not_high_f = [max(0, min(1, self.no_very_high(f))) for f in x_flow]
        print(y_not_high_f)

        flow_plot.plot(x_flow, y_low_f, 'b', label='Малый')
        flow_plot.plot(x_flow, y_medium_f, 'g', label='Средний')
        flow_plot.plot(x_flow, y_high_f, 'r', label='Большой')
        flow_plot.plot(x_flow, y_not_high_f, 'm', label='Не очень большой')

        flow_plot.set_title("Функции принадлежности для расхода")
        flow_plot.set_xlabel("Расход сырья")
        flow_plot.set_ylabel("Степень принадлежности [0,1]")
        flow_plot.set_ylim(0, 1.1)  # Фиксируем ось Y от 0 до 1.1
        flow_plot.legend()
        flow_plot.grid()

        # Добавляем вертикальные линии для рабочего диапазона (70-110)
        flow_plot.axvline(x=70, color='gray', linestyle='--')
        flow_plot.axvline(x=110, color='gray', linestyle='--')
        flow_plot.text(90, -0.1, "Рабочий диапазон", ha='center', color='gray')

        # Встраиваем графики в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # Функции принадлежности для температуры
    def temp_low(self, T):
        return (1 / 10000) * (T - 200) ** 2

    def temp_medium(self, T):
        return 1 - (1 / 1000) * (125 - T) ** 2

    def temp_high(self, T):
        return (1 / 10000) * (T - 50) ** 2

    # Функции принадлежности для расхода
    def flow_low(self, G):
        return math.exp(-0.2 * math.log(10 * abs(G - 75.1))) ** 2

    def flow_medium(self, G):
        return math.exp(-0.2 * math.log(10 * abs(G - 85.1))) ** 2

    def flow_high(self, G):
        return math.exp(-0.2 * math.log(10 * abs(G - 100.1))) ** 2

    def no_very_high(self, G):
        return min(1, 1-self.flow_high(G)) ** 2

    def validate_input(self, value, min_val, max_val, name):
        try:
            num = float(value)
            if not (min_val <= num <= max_val):
                raise ValueError
            return num
        except ValueError:
            messagebox.showerror("Ошибка",
                                 f"Некорректное значение {name}. Введите число от {min_val} до {max_val}")
            return None

    def calculate(self):
        # Получаем и проверяем входные данные
        temp = self.validate_input(self.temp_entry.get(), 100, 150, "температуры")
        flow = self.validate_input(self.flow_entry.get(), 70, 110, "расхода")

        if temp is None or flow is None:
            return

        # Вычисляем степени принадлежности
        temp_low = self.temp_low(temp)
        temp_medium = self.temp_medium(temp)
        temp_high = self.temp_high(temp)

        flow_low = self.flow_low(flow)
        flow_medium = self.flow_medium(flow)
        flow_high = self.flow_high(flow)
        flow_not_very_high = self.no_very_high(flow)

        # Очищаем вывод
        self.output_text.delete(1.0, tk.END)

        # Выводим значения функций принадлежности
        self.output_text.insert(tk.END, "Значения функций принадлежности:\n")
        self.output_text.insert(tk.END, f"Температура малая: {temp_low:.3f}\n")
        self.output_text.insert(tk.END, f"Температура средняя: {temp_medium:.3f}\n")
        self.output_text.insert(tk.END, f"Температура большая: {temp_high:.3f}\n")
        self.output_text.insert(tk.END, f"Расход малый: {flow_low:.3f}\n")
        self.output_text.insert(tk.END, f"Расход средний: {flow_medium:.3f}\n")
        self.output_text.insert(tk.END, f"Расход большой: {flow_high:.3f}\n")
        self.output_text.insert(tk.END, f"Расход не очень большой: {flow_not_very_high:.3f}\n\n")

        # Применяем правила
        # Правило 1: Аппарат A
        rule1 = min(flow_low, temp_low)
        rule2 = min(flow_low, temp_medium)
        rule3 = min(flow_medium, temp_low)
        rule_a = max(rule1, rule2, rule3)

        # Правило 2: Аппарат B
        rule1 = min(flow_low, temp_high)
        rule2 = min(flow_high, temp_low)
        rule3 = min(flow_medium, temp_medium)
        rule_b = max(rule1, rule2, rule3)

        # Правило 3: Аппарат C
        rule1 = min(flow_medium, temp_high)
        rule2 = min(flow_high, temp_medium)
        rule3 = min(flow_high, temp_high)
        rule_c = max(rule1, rule2, rule3)

        # Правило 4: Аппарат D
        rule_d = min(flow_not_very_high, max(temp_low, temp_medium, temp_high))

        # Вычисляем степени истинности по новому методу
        q1 = min(1, 1 - rule_a + 1, 1 - rule_b + 0, 1 - rule_c + 0, 1 - rule_d + 0)
        q2 = min(1, 1 - rule_a + 0, 1 - rule_b + 1, 1 - rule_c + 0, 1 - rule_d + 0)
        q3 = min(1, 1 - rule_a + 0, 1 - rule_b + 0, 1 - rule_c + 1, 1 - rule_d + 0)
        q4 = min(1, 1 - rule_a + 0, 1 - rule_b + 0, 1 - rule_c + 0, 1 - rule_d + 1)

        self.truth_degrees = [q1, q2, q3, q4]

        # Обновляем метки с степенями истинности
        for i in range(4):
            self.truth_labels[i].config(text=f"Аппарат {chr(65+i)}: {self.truth_degrees[i]:.3f}")

        # Выводим правила
        self.output_text.insert(tk.END, "Степени истинности правил (Первоначальные коэф):\n")
        self.output_text.insert(tk.END, f"Аппарат A: {rule_a:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат B: {rule_b:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат C: {rule_c:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат D: {rule_d:.3f}\n\n")

        # Выводим новые степени истинности
        self.output_text.insert(tk.END, "Степени истинности (Преобразованные коэф):\n")
        self.output_text.insert(tk.END, f"Аппарат A: {q1:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат B: {q2:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат C: {q3:.3f}\n")
        self.output_text.insert(tk.END, f"Аппарат D: {q4:.3f}\n\n")

        # Определяем результат по максимальной степени истинности (новый метод)
        max_degree = max(self.truth_degrees)
        best_results = [chr(65+i) for i, degree in enumerate(self.truth_degrees) if degree == max_degree]

        if len(best_results) == 1:
            self.output_text.insert(tk.END,
                                  f"Рекомендуемый аппарат (Преобразованные коэф): {best_results[0]}\n"
                                  f"Степень истинности: {max_degree:.3f}\n")
        else:
            self.output_text.insert(tk.END,
                                  f"Рекомендуемые аппараты (Преобразованные коэф): {', '.join(best_results)}\n"
                                  f"Степень истинности: {max_degree:.3f}\n")

        # Старый метод определения результата (для сравнения)
        old_rules = {'A': rule_a, 'B': rule_b, 'C': rule_c, 'D': rule_d}
        old_best = max(old_rules, key=old_rules.get)
        self.output_text.insert(tk.END,
                             f"\nДля сравнения (Первоначальные коэф):\n"
                             f"Рекомендуемый аппарат: {old_best}\n"
                             f"Степень истинности: {old_rules[old_best]:.3f}\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApparatusSelector(root)
    root.mainloop()