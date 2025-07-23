import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Пример базы данных операций сборки
assembly_data = [
    {"операция": "Сборка узла 1", "трудоёмкость": 5, "время": 10, "стоимость": 50},
    {"операция": "Сборка узла 2", "трудоёмкость": 3, "время": 8, "стоимость": 30},
    {"операция": "Установка детали", "трудоёмкость": 4, "время": 6, "стоимость": 40},
    {"операция": "Финальная сборка", "трудоёмкость": 6, "время": 12, "стоимость": 60},
]

# Ограничения на последовательность операций
constraints = {
    "Сборка узла 1": ["Сборка узла 2"],
    "Сборка узла 2": ["Установка детали"],
    "Установка детали": ["Финальная сборка"],
}


# Функция для выбора оптимальной схемы с учетом ограничений
def calculate_optimal_scheme():
    try:
        criterion = combo_criterion.get()
        if not criterion:
            messagebox.showerror("Ошибка", "Выберите критерий оптимизации.")
            return

        # Сортировка операций по критерию
        sorted_data = sorted(assembly_data, key=lambda x: x[criterion])

        # Учет ограничений
        sorted_operations = [item["операция"] for item in sorted_data]
        ordered_operations = []
        visited = set()

        def dfs(operation):
            if operation in visited:
                return
            for dependency in constraints.get(operation, []):
                dfs(dependency)
            if operation not in ordered_operations:
                ordered_operations.append(operation)
            visited.add(operation)

        for operation in sorted_operations:
            dfs(operation)

        # Формирование результата
        result_text = "Оптимальная последовательность:\n"
        for i, operation in enumerate(ordered_operations, start=1):
            op_data = next(item for item in assembly_data if item["операция"] == operation)
            result_text += f"{i}. {operation} (Трудоёмкость: {op_data['трудоёмкость']}, Время: {op_data['время']}, Стоимость: {op_data['стоимость']})\n"

        text_result.delete("1.0", tk.END)
        text_result.insert(tk.END, result_text)

        # Обновление визуализации
        update_graph(ordered_operations)

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")


# Функция для визуализации графа сборки
def update_graph(operations):
    graph.clear()
    edges = []
    for operation in operations:
        for dependency in constraints.get(operation, []):
            edges.append((dependency, operation))

    graph.add_edges_from(edges)
    ax.clear()
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=2000, edge_color="black", font_size=10, ax=ax)
    canvas.draw()


# Создание основного окна
root = tk.Tk()
root.title("Подсистема автоматизированного проектирования сборки")

# Поля ввода
frame_inputs = tk.Frame(root)
frame_inputs.pack(pady=10)

label_criterion = tk.Label(frame_inputs, text="Критерий оптимизации:")
label_criterion.grid(row=0, column=0, padx=5)

# Выбор критерия оптимизации
combo_criterion = ttk.Combobox(frame_inputs, values=["трудоёмкость", "время", "стоимость"])
combo_criterion.grid(row=0, column=1, padx=5)

button_calculate = ttk.Button(frame_inputs, text="Рассчитать", command=calculate_optimal_scheme)
button_calculate.grid(row=1, column=0, columnspan=2, pady=10)

# Отображение результата
label_result = tk.Label(root, text="Результат:")
label_result.pack(pady=5)

text_result = tk.Text(root, width=60, height=10)
text_result.pack(pady=5)

# Визуализация графа
frame_plot = tk.Frame(root)
frame_plot.pack(pady=10)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=frame_plot)
canvas.get_tk_widget().pack()

graph = nx.DiGraph()

# Запуск приложения
root.mainloop()
