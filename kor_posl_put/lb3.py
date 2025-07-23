import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import time


class NeuroNet:
    def __init__(self, num_inputs, num_hidden):
        self.num_inputs = num_inputs
        self.num_hidden = num_hidden

        # Инициализация весов с другим распределением
        self.w_input_hidden = np.random.normal(0, 0.1, (num_inputs, num_hidden))
        self.w_hidden_output = np.random.normal(0, 0.1, (num_hidden + 1, 1))

        self.lr = 0.15  # Измененная скорость обучения
        self.max_epochs = 2500
        self.min_error = 0.003
        self.bias_value = 1

    def activate(self, x):
        return 1 / (1 + np.exp(-x))

    def forward_pass(self, inputs):
        inputs = np.array(inputs).reshape(-1, 1)

        # Расчет скрытого слоя
        hidden = self.activate(np.dot(self.w_input_hidden.T, inputs))
        hidden_with_bias = np.vstack(([self.bias_value], hidden))

        # Расчет выходного слоя
        output = self.activate(np.dot(self.w_hidden_output.T, hidden_with_bias))

        return hidden, output

    def learn(self, training_data, targets):
        error_history = []
        for iteration in range(self.max_epochs):
            total_err = 0

            for data, target in zip(training_data, targets):
                # Прямой проход
                h, out = self.forward_pass(data)

                # Ошибка
                err = target - out
                total_err += np.mean(err ** 2)

                # Обратное распространение
                delta_out = err * out * (1 - out)
                delta_h = np.dot(self.w_hidden_output[1:], delta_out) * h * (1 - h)

                # Обновление весов
                h_with_bias = np.vstack(([self.bias_value], h))
                self.w_hidden_output += self.lr * delta_out * h_with_bias
                self.w_input_hidden += self.lr * np.dot(np.array(data).reshape(-1, 1), delta_h.T)

            avg_error = total_err / len(training_data)
            error_history.append(avg_error)

            if avg_error < self.min_error:
                print(f"Обучение завершено на итерации {iteration}")
                break

        return error_history


class NeuroApp:
    def __init__(self, master):
        self.master = master
        master.title("Исследователь нейросетей")

        self.net = NeuroNet(5, 3)  # 5 входов, 3 скрытых нейрона

        # Данные для обучения
        self.train_data = [
            [0, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0], [0, 0, 1, 1],
            [0, 1, 0, 0], [0, 1, 0, 1], [0, 1, 1, 0], [0, 1, 1, 1],
            [1, 0, 0, 0], [1, 0, 0, 1], [1, 0, 1, 0], [1, 0, 1, 1],
            [1, 1, 0, 0], [1, 1, 0, 1], [1, 1, 1, 0], [1, 1, 1, 1]
        ]
        self.targets = [1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0]

        self.setup_ui()
        self.init_weight_table()

    def setup_ui(self):
        main_panel = ttk.Frame(self.master, padding="15")
        main_panel.grid(row=0, column=0)

        # Панель ввода
        input_panel = ttk.LabelFrame(main_panel, text="Параметры входа", padding="10")
        input_panel.grid(row=0, column=0, sticky="n")

        ttk.Label(input_panel, text="Смещение (X0):").grid(row=0, column=0)
        self.bias_select = ttk.Combobox(input_panel, values=[1, -1], state="readonly")
        self.bias_select.current(0)
        self.bias_select.grid(row=0, column=1)

        input_labels = ['X1', 'X2', 'X3', 'X4']
        self.input_fields = []
        for i, label in enumerate(input_labels):
            ttk.Label(input_panel, text=f"{label}:").grid(row=i + 1, column=0)
            entry = ttk.Entry(input_panel)
            entry.grid(row=i + 1, column=1)
            entry.insert(0, "0")
            self.input_fields.append(entry)

        # Панель управления
        control_panel = ttk.Frame(main_panel)
        control_panel.grid(row=1, column=0, pady=10)

        ttk.Button(control_panel, text="Обучение", command=self.start_training).pack(side="left", padx=5)
        ttk.Button(control_panel, text="Предсказание", command=self.make_prediction).pack(side="left", padx=5)

        # Панель вывода
        output_panel = ttk.LabelFrame(main_panel, text="Результаты", padding="10")
        output_panel.grid(row=2, column=0)

        self.result_display = tk.Text(output_panel, height=12, width=55)
        self.result_display.pack()

        # Панель весов
        weight_panel = ttk.LabelFrame(main_panel, text="Параметры сети", padding="10")
        weight_panel.grid(row=0, column=1, rowspan=3, padx=10)

        self.weight_tree = ttk.Treeview(weight_panel, height=18)
        self.weight_tree.pack()

        scrollbar = ttk.Scrollbar(weight_panel, orient="vertical", command=self.weight_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.weight_tree.configure(yscrollcommand=scrollbar.set)

    def init_weight_table(self):
        self.weight_tree["columns"] = ("val")
        self.weight_tree.column("#0", width=150)
        self.weight_tree.column("val", width=100)
        self.weight_tree.heading("#0", text="Вес")
        self.weight_tree.heading("val", text="Значение")

        # Веса входного слоя
        input_weights = self.weight_tree.insert("", "end", text="Входные веса", open=True)
        for i in range(5):
            for j in range(3):
                self.weight_tree.insert(input_weights, "end",
                                        text=f"Вход {i} → Нейрон {j}",
                                        iid=f"in_{i}_{j}",
                                        values=("0.0000",))

        # Веса скрытого слоя
        hidden_weights = self.weight_tree.insert("", "end", text="Выходные веса", open=True)
        for i in range(4):
            self.weight_tree.insert(hidden_weights, "end",
                                    text=f"Нейрон {i} → Выход",
                                    iid=f"out_{i}",
                                    values=("0.0000",))

    def refresh_weights(self):
        # Обновление весов входного слоя
        for i in range(5):
            for j in range(3):
                self.weight_tree.item(f"in_{i}_{j}",
                                      values=(f"{self.net.w_input_hidden[i, j]:.6f}",))

        # Обновление весов скрытого слоя
        for i in range(4):
            self.weight_tree.item(f"out_{i}",
                                  values=(f"{self.net.w_hidden_output[i, 0]:.6f}",))

    def start_training(self):
        try:
            bias = int(self.bias_select.get())
            self.net.bias_value = bias

            # Подготовка данных
            train_set = [[bias] + data for data in self.train_data]

            self.result_display.insert("end", f"Начало обучения со смещением = {bias}...\n")
            self.master.update()

            start = time.time()
            errors = self.net.learn(train_set, self.targets)
            duration = time.time() - start

            self.result_display.insert("end",
                                       f"Обучение завершено за {duration:.2f} сек\n"
                                       f"Итераций: {len(errors)}\n"
                                       f"Финальная ошибка: {errors[-1]:.6f}\n\n")

            self.refresh_weights()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def make_prediction(self):
        try:
            # Получение входных данных
            bias = int(self.bias_select.get())
            inputs = [bias] + [float(field.get()) for field in self.input_fields]

            # Проверка входных значений
            if any(not 0 <= x <= 1 for x in inputs[1:]):
                raise ValueError("Входные значения должны быть от 0 до 1")

            # Выполнение прогноза
            hidden, output = self.net.forward_pass(inputs)
            prediction = 1 if output[0, 0] > 0.5 else 0

            # Вывод результатов
            self.result_display.insert("end",
                                       f"Входные данные: {inputs}\n"
                                       f"Активация скрытого слоя: {hidden.flatten()}\n"
                                       f"Выход: {output[0, 0]:.6f} → Результат: {prediction}\n"
                                       f"------------------------\n")
            self.result_display.see("end")

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = NeuroApp(root)
    root.mainloop()