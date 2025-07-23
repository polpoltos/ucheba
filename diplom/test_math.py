import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Генерация тестовых данных
tambov_area_points = {
    'Start': (52.7211, 41.4526),
    'Point1': (52.735, 41.438),
    'Point2': (52.712, 41.467),
    'Point3': (52.726, 41.443),
    'Point4': (52.718, 41.461)
}


class AntColonyTSP:
    def __init__(self, points, n_ants=10, n_iter=50, alpha=1, beta=2, rho=0.1):
        self.points = list(points.keys())  # Список имен точек
        self.coords = points  # Словарь с координатами
        self.n_ants = n_ants
        self.n_iter = n_iter
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        # Создаем граф и матрицу расстояний
        self.G = self._create_graph()
        self.dist_matrix = self._compute_distance_matrix()
        self.node_indices = {node: idx for idx, node in enumerate(self.points)}  # Сопоставление имен и индексов

    def _create_graph(self):
        """Создание графа с индексами"""
        G = nx.Graph()

        # Добавляем узлы с индексами
        for idx, node in enumerate(self.points):
            G.add_node(node, index=idx)

        # Добавляем ребра
        for i in self.points:
            for j in self.points:
                if i != j:
                    distance = np.linalg.norm(
                        np.array(self.coords[i]) - np.array(self.coords[j])
                    )
                    G.add_edge(i, j, weight=distance)
        return G

    def _compute_distance_matrix(self):
        """Матрица расстояний через Floyd-Warshall"""
        return nx.floyd_warshall_numpy(self.G, weight='weight')

    def run(self):
        n = len(self.points)
        pheromone = np.ones((n, n))
        best_path = None
        best_length = np.inf

        for _ in range(self.n_iter):
            paths = []

            for _ in range(self.n_ants):
                path = ['Start']
                visited = set(path)

                while len(visited) < len(self.points):
                    current = path[-1]
                    available = [node for node in self.points if node not in visited]

                    # Вычисляем вероятности
                    probs = []
                    total = 0
                    for node in available:
                        i = self.node_indices[current]
                        j = self.node_indices[node]
                        p = (pheromone[i, j] ** self.alpha) * ((1 / self.dist_matrix[i, j]) ** self.beta)
                        probs.append(p)
                        total += p

                    # Нормализация
                    probs = [p / total for p in probs]
                    next_node = np.random.choice(available, p=probs)
                    path.append(next_node)
                    visited.add(next_node)

                # Вычисляем длину пути
                length = 0
                for i in range(len(path) - 1):
                    length += self.G.edges[path[i], path[i + 1]]['weight']

                if length < best_length:
                    best_length = length
                    best_path = path

            # Обновление феромонов
            pheromone *= (1 - self.rho)
            for i in range(len(path) - 1):
                u_idx = self.node_indices[path[i]]
                v_idx = self.node_indices[path[i + 1]]
                pheromone[u_idx, v_idx] += 1 / self.dist_matrix[u_idx, v_idx]

        return best_path, best_length

    def plot_route(self, path):
        """Визуализация маршрута"""
        fig, ax = plt.subplots(figsize=(10, 8))

        # Отображение точек
        for name, (lat, lon) in self.coords.items():
            ax.scatter(lon, lat, s=100, zorder=2)
            ax.text(lon + 0.0005, lat + 0.0005, name, fontsize=9)

        # Отображение маршрута
        for i in range(len(path) - 1):
            start = self.coords[path[i]]
            end = self.coords[path[i + 1]]
            ax.plot([start[1], end[1]], [start[0], end[0]],
                    color='red', linewidth=2, zorder=1)

        ax.set_title('Оптимальный маршрут')
        plt.show()


# Запуск
aco = AntColonyTSP(tambov_area_points)
best_path, best_length = aco.run()
print(f"Лучший маршрут: {best_path}")
print(f"Длина: {best_length:.2f}")
aco.plot_route(best_path)