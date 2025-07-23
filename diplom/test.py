import osmnx as ox
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from tqdm import tqdm

ox.settings.log_console = True
ox.settings.use_cache = True
ox.settings.timeout = 600

points = {
    "Start": (52.7211, 41.4526),
    "Point1": (52.6415, 41.4458),
    "Point2": (52.8979, 41.4333),
    "Point3": (52.8997, 41.3057),
    "Point4": (52.6584, 41.5826)
}


class RouteOptimizer:
    def __init__(self, points, num_ants=30, iterations=200, alpha=1, beta=4, rho=0.1):
        self.points = points
        self.num_ants = num_ants
        self.iterations = iterations
        self.alpha = alpha
        self.beta = beta
        self.rho = rho

        self.original_graph = self._load_osm_graph()
        self.node_mapping = self._map_points_to_nodes()
        self._validate_and_reassign_nodes()
        self._validate_all_points_mapped()

        self.distance_matrix = self._build_distance_matrix()
        self.node_ids = list(self.node_mapping.values())
        self.node_indices = {node: idx for idx, node in enumerate(self.node_ids)}
        self.pheromone = np.ones((len(self.node_ids), len(self.node_ids)))

    def _load_osm_graph(self):
        print("🔄 Загрузка дорожной сети...")
        try:
            return ox.graph_from_point(
                (52.7211, 41.4526),
                dist=20000,
                network_type='drive',
                simplify=True
            )
        except Exception as e:
            print(f"🚨 Ошибка загрузки графа: {str(e)}")
            raise

    def _map_points_to_nodes(self):
        print("📍 Привязка точек к графу:")
        mapping = {}
        for name, (lat, lon) in self.points.items():
            try:
                node = ox.distance.nearest_nodes(self.original_graph, lon, lat)
                mapping[name] = node
                print(f"  {name.ljust(8)} → Узел {node}")
            except Exception as e:
                print(f"🚨 Ошибка привязки {name}: {str(e)}")
        return mapping

    def _validate_all_points_mapped(self):
        missing = [name for name in self.points if name not in self.node_mapping]
        if missing:
            raise ValueError(f"Отсутствуют привязки для точек: {', '.join(missing)}")

    def _validate_and_reassign_nodes(self):
        print("🔍 Проверка узлов в графе...")
        missing = [n for n in self.node_mapping.values()
                   if not self.original_graph.has_node(n)]

        if missing:
            print(f"⚠️ Найдены отсутствующие узлы: {missing}")
            self._reassign_nodes(missing)

    def _reassign_nodes(self, missing_nodes):
        print("🔄 Переназначение узлов...")
        for name, node in list(self.node_mapping.items()):
            if node in missing_nodes:
                try:
                    new_node = ox.distance.nearest_nodes(
                        self.original_graph,
                        self.original_graph.nodes[node]['x'],
                        self.original_graph.nodes[node]['y']
                    )
                    self.node_mapping[name] = new_node
                    print(f"  {name} переназначен → {new_node}")
                except Exception as e:
                    print(f"🚨 Ошибка переназначения {name}: {str(e)}")

    def _build_distance_matrix(self):
        print("📊 Построение матрицы расстояний...")
        matrix = {}
        nodes = list(self.node_mapping.values())

        for u in nodes:
            matrix[u] = {}
            for v in nodes:
                if u == v:
                    matrix[u][v] = 0.0
                    continue

                try:
                    path = nx.shortest_path(self.original_graph, u, v, weight='length')
                    length = sum(self.original_graph[u][v][0]['length'] for u, v in zip(path[:-1], path[1:]))
                    matrix[u][v] = length
                except (nx.NetworkXNoPath, KeyError):
                    matrix[u][v] = float('inf')
                except Exception as e:
                    print(f"⚠️ Ошибка расчета {u}→{v}: {str(e)}")
                    matrix[u][v] = float('inf')
        return matrix

    def optimize(self):
        print("\n🐜 Запуск оптимизации муравьиным алгоритмом...")
        best_path = None
        best_length = float('inf')

        try:
            with tqdm(total=self.iterations, desc="Прогресс") as pbar:
                for _ in range(self.iterations):
                    ant_paths = []
                    for _ in range(self.num_ants):
                        path = self._generate_ant_path()
                        if path['length'] < best_length:
                            best_length = path['length']
                            best_path = path['nodes']
                        ant_paths.append(path)

                    self._update_pheromones(ant_paths, best_length)
                    pbar.update(1)

            return self._convert_node_ids(best_path), best_length
        except Exception as e:
            print(f"🚨 Ошибка оптимизации: {str(e)}")
            return [], float('inf')

    def _generate_ant_path(self):
        current_node = self.node_mapping['Start']
        path = [current_node]
        visited = {current_node}

        while len(visited) < len(self.node_ids):
            possible = [n for n in self.node_ids if n not in visited]
            if not possible:
                break

            probs = []
            total = 0.0
            for node in possible:
                try:
                    pheromone = self.pheromone[self.node_indices[current_node]][self.node_indices[node]]
                    distance = self.distance_matrix[current_node][node]
                    if distance == 0 or np.isinf(distance):
                        continue

                    prob = (pheromone ** self.alpha) * ((1 / distance) ** self.beta)
                    probs.append(prob)
                    total += prob
                except KeyError:
                    continue

            if not probs or total == 0:
                next_node = np.random.choice(possible)
            else:
                probs = [p / total for p in probs]
                next_node = np.random.choice(possible, p=probs)

            path.append(next_node)
            visited.add(next_node)
            current_node = next_node

        try:
            length = sum(self.distance_matrix[path[i]][path[i + 1]] for i in range(len(path) - 1))
        except KeyError:
            length = float('inf')

        return {'nodes': path, 'length': length}

    def _update_pheromones(self, ant_paths, best_length):
        self.pheromone *= (1 - self.rho)

        for path in ant_paths:
            if path['length'] == best_length and best_length > 0:
                delta = 1 / path['length']
                for i in range(len(path['nodes']) - 1):
                    u = self.node_indices[path['nodes'][i]]
                    v = self.node_indices[path['nodes'][i + 1]]
                    self.pheromone[u][v] += delta

    def _convert_node_ids(self, node_ids):
        reverse_map = {v: k for k, v in self.node_mapping.items()}
        return [reverse_map.get(n, 'UNKNOWN') for n in node_ids]

    def visualize(self, path_names, length):
        if not path_names or length == float('inf'):
            print("⚠️ Невозможно визуализировать: недопустимый маршрут")
            return

        print("\n🎨 Начало визуализации...")
        try:
            full_route = []
            valid_segments = 0

            for i in range(len(path_names) - 1):
                start_name = path_names[i]
                end_name = path_names[i + 1]

                start_node = self.node_mapping.get(start_name)
                end_node = self.node_mapping.get(end_name)

                if not start_node or not end_node:
                    print(f"⚠️ Пропущен сегмент {start_name}-{end_name}: узел не найден")
                    continue

                try:
                    if not self.original_graph.has_node(start_node):
                        print(f"⚠️ Узел {start_node} ({start_name}) отсутствует в графе")
                        continue
                    if not self.original_graph.has_node(end_node):
                        print(f"⚠️ Узел {end_node} ({end_name}) отсутствует в графе")
                        continue

                    segment = ox.shortest_path(self.original_graph, start_node, end_node, weight='length')
                    if not segment:
                        print(f"⚠️ Нет пути между {start_name} и {end_name}")
                        continue

                    # Проверка наличия всех ребер в сегменте
                    valid = True
                    for u, v in zip(segment[:-1], segment[1:]):
                        if not self.original_graph.has_edge(u, v):
                            print(f"⚠️ Отсутствует ребро между {u} и {v} в сегменте {start_name}-{end_name}")
                            valid = False
                            break

                    if valid:
                        full_route.extend(segment)
                        valid_segments += 1
                        print(f"✅ Сегмент {start_name}-{end_name}: {len(segment)} узлов")
                    else:
                        print(f"⚠️ Сегмент {start_name}-{end_name} содержит несуществующие ребра")

                except Exception as e:
                    print(f"🚨 Ошибка построения сегмента {start_name}-{end_name}: {str(e)}")

            if valid_segments == 0:
                print("🚨 Все сегменты маршрута недействительны")
                return

            # Фильтрация валидных узлов маршрута
            route_nodes = [n for n in full_route if self.original_graph.has_node(n)]

            # Проверка последовательности узлов
            for i in range(len(route_nodes) - 1):
                u = route_nodes[i]
                v = route_nodes[i + 1]
                if not self.original_graph.has_edge(u, v):
                    print(f"⚠️ Добавлено недостающее ребро между {u} и {v}")
                    self.original_graph.add_edge(u, v, length=0)

            fig, ax = ox.plot_graph_routes(
                self.original_graph,
                [route_nodes],
                route_colors='#FF4500',
                route_linewidth=8,
                node_size=0,
                show=False,
                close=False
            )

            # Добавление меток точек
            for name, (lat, lon) in self.points.items():
                ax.scatter(
                    lon, lat,
                    c='#32CD32' if name == 'Start' else '#1E90FF',
                    s=200,
                    edgecolor='black',
                    zorder=5
                )
                ax.text(
                    lon + 0.001,
                    lat + 0.001,
                    name,
                    fontsize=10,
                    weight='bold',
                    bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
                )

            ax.set_title(f"Оптимальный маршрут: {length / 1000:.2f} км", fontsize=14)
            plt.tight_layout()
            plt.show()

        except Exception as e:
            print(f"🚨 Критическая ошибка визуализации: {str(e)}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    try:
        optimizer = RouteOptimizer(
            points,
            num_ants=20,
            iterations=100,
            alpha=1,
            beta=3,
            rho=0.15
        )

        best_route, best_length = optimizer.optimize()

        if best_route:
            print("\n✅ Результаты оптимизации:")
            print(f"Маршрут: {best_route}")
            print(f"Протяженность: {best_length / 1000:.2f} км")
            optimizer.visualize(best_route, best_length)
        else:
            print("⚠️ Оптимальный маршрут не найден")

    except Exception as e:
        print(f"🚨 Критическая ошибка: {str(e)}")