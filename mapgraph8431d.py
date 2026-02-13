import re
from collections import defaultdict
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch, ArrowStyle
import matplotlib.patches as mpatches

def parse_mapinfo(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Находим все определения уровней
    map_pattern = re.compile(
        r'map\s+(\w+)\s+"[^"]*"(?:\s+cluster\s+\d+)?\s*'
        r'(?:next\s+(\w+))?\s*'
        r'(?:secretnext\s+(\w+))?',
        re.IGNORECASE
    )
    
    maps = {}
    nodes = set()
    
    # Сначала собираем все существующие уровни
    for match in map_pattern.finditer(content):
        map_id = match.group(1).lower()
        next_map = match.group(2).lower() if match.group(2) else None
        secret_next = match.group(3).lower() if match.group(3) else None
        
        maps[map_id] = {
            'next': next_map,
            'secretnext': secret_next
        }
        nodes.add(map_id)
    
    # Функция для получения следующего числового идентификатора
    def get_next_map_id(map_id):
        match = re.search(r'(\d+)$', map_id)
        if match:
            num = int(match.group(1))
            next_num = num + 1
            old_num_str = match.group(1)
            new_num_str = str(next_num).zfill(len(old_num_str))
            return map_id[:match.start(1)] + new_num_str + map_id[match.end(1):]            
        else:
            return f"{map_id}1"
    
    # Функция для рекурсивного создания цепочки недостающих уровней
    def ensure_map_exists(map_id, visited=None):
        if visited is None:
            visited = set()
        
        # Если уже посещали этот ID в текущей цепочке (предотвращаем бесконечную рекурсию)
        if map_id in visited:
            return
        
        # Если карта уже существует, ничего не делаем
        if map_id in maps:
            return
        
        visited.add(map_id)
        
        # Создаём недостающую карту
        next_id = get_next_map_id(map_id)
        print(f"Создаём недостающий уровень: {map_id} -> {next_id}")
        
        # Рекурсивно создаём следующую карту, если она не существует
        ensure_map_exists(next_id, visited)
        
        # Добавляем новую карту в словарь
        maps[map_id] = {'next': next_id, 'secretnext': None}
        nodes.add(map_id)
    
    # Проверяем каждый выход и создаём цепочки недостающих уровней
    # Создаём копию списка ключей, чтобы не изменять словарь во время итерации
    map_items = list(maps.items())
    
    for map_id, data in map_items:
        # Проверяем обычный выход
        if data['next'] and data['next'] not in maps:
            ensure_map_exists(data['next'])
        
        # Проверяем секретный выход
        if data['secretnext'] and data['secretnext'] not in maps:
            ensure_map_exists(data['secretnext'])
    
    # Строим списки рёбер
    normal_edges = []
    secret_edges = []
    
    for map_id, data in maps.items():
        if data['next']:
            normal_edges.append((map_id, data['next']))
        if data['secretnext']:
            secret_edges.append((map_id, data['secretnext']))
    
    return nodes, normal_edges, secret_edges, maps

def visualize_graph(nodes, normal_edges, secret_edges, maps):
    """Визуализирует граф с помощью networkx и matplotlib"""
    
    # Создаём граф
    G = nx.DiGraph()
    
    # Добавляем узлы
    for node in nodes:
        G.add_node(node)
    
    # Добавляем рёбра
    G.add_edges_from(normal_edges)
    G.add_edges_from(secret_edges)
    
    # Создаём фигуру
    plt.figure(figsize=(20, 16))
    
    # Выбираем layout для графа
    # Можно попробовать разные: spring_layout, circular_layout, kamada_kawai_layout, spectral_layout
    pos = nx.spring_layout(G, k=3, iterations=50, seed=42)
    
    # Рисуем узлы
    nx.draw_networkx_nodes(G, pos, node_size=800, node_color='lightblue', 
                          node_shape='s', edgecolors='black', linewidths=1)
    
    # Рисуем обычные рёбра (чёрные сплошные)
    nx.draw_networkx_edges(G, pos, edgelist=normal_edges, 
                          edge_color='black', width=1.5, 
                          arrows=True, arrowsize=20, 
                          arrowstyle='->', connectionstyle='arc3,rad=0.1')
    
    # Рисуем секретные рёбра (красные пунктирные)
    nx.draw_networkx_edges(G, pos, edgelist=secret_edges, 
                          edge_color='red', width=1.5, 
                          style='dashed', arrows=True, arrowsize=20,
                          arrowstyle='->', connectionstyle='arc3,rad=0.1')
    
    # Рисуем подписи узлов
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight='bold')
    
    # Добавляем легенду
    normal_patch = mpatches.Patch(color='black', label='Normal exit')
    secret_patch = mpatches.Patch(color='red', label='Secret exit', linestyle='dashed')
    plt.legend(handles=[normal_patch, secret_patch], loc='upper right', fontsize=12)
    
    # Настраиваем отображение
    plt.title("Map Graph Visualization", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    
    # Сохраняем в файл
    #plt.savefig('map_graph.png', dpi=150, bbox_inches='tight')
    #print(f"\nГраф сохранён в файл: map_graph.png")
    
    # Показываем
    plt.show()

def print_graph(nodes, normal_edges, secret_edges):
    print("\nГраф уровней:")
    print("=" * 50)
    print("Обычные выходы:")
    for src, tgt in sorted(normal_edges):
        print(f"{src} -> {tgt}")
    print("\nСекретные выходы:")
    for src, tgt in sorted(secret_edges):
        print(f"{src} -> {tgt} [secret]")

def save_dot_file(nodes, normal_edges, secret_edges, filename="map_graph.dot"):
    """Сохраняет граф в формате DOT для визуализации"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("digraph MapGraph {\n")
        f.write("  rankdir=LR;\n")
        f.write("  node [shape=box];\n")
        
        # Узлы
        for node in sorted(nodes):
            clean_node = node.replace('"', '\\"')
            f.write(f'  "{clean_node}";\n')
        
        # Обычные рёбра
        for src, tgt in normal_edges:
            clean_src = src.replace('"', '\\"')
            clean_tgt = tgt.replace('"', '\\"')
            f.write(f'  "{clean_src}" -> "{clean_tgt}" [color=black, style=solid];\n')
        
        # Секретные рёбра
        for src, tgt in secret_edges:
            clean_src = src.replace('"', '\\"')
            clean_tgt = tgt.replace('"', '\\"')
            f.write(f'  "{clean_src}" -> "{clean_tgt}" [color=red, style=dashed, label="secret"];\n')
        
        f.write("}\n")
    print(f"\nDOT файл сохранён: {filename}")

def save_graph_text(nodes, normal_edges, secret_edges, filename="map_graph.txt"):
    """Сохраняет граф в текстовом формате"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Граф уровней:\n")
        f.write("=" * 50 + "\n")
        f.write("Обычные выходы:\n")
        for src, tgt in sorted(normal_edges):
            f.write(f"{src} -> {tgt}\n")
        f.write("\nСекретные выходы:\n")
        for src, tgt in sorted(secret_edges):
            f.write(f"{src} -> {tgt} [secret]\n")
    print(f"Текстовый граф сохранён: {filename}")

def main():
    filename = "MAPINFO8341.txt"
    try:
        nodes, normal_edges, secret_edges, maps = parse_mapinfo(filename)
        
        print(f"Найдено уровней: {len(nodes)}")
        print(f"Обычных выходов: {len(normal_edges)}")
        print(f"Секретных выходов: {len(secret_edges)}")
        
        # Выводим граф в консоль
        print_graph(nodes, normal_edges, secret_edges)
        
        # Сохраняем в разные форматы
        #save_dot_file(nodes, normal_edges, secret_edges)
        #save_graph_text(nodes, normal_edges, secret_edges)
        
        # Визуализируем граф
        try:
            visualize_graph(nodes, normal_edges, secret_edges, maps)
        except Exception as e:
            print(f"\nОшибка при визуализации графа: {e}")
            print("Убедитесь, что установлены библиотеки: matplotlib и networkx")
            print("Установка: pip install matplotlib networkx")
        
        # Дополнительная информация
        print("\nДетальная информация (первые 20 уровней):")
        count = 0
        for map_id, data in sorted(maps.items()):
            if count >= 20:
                print(f"... и ещё {len(maps) - 20} уровней")
                break
            next_str = data['next'] if data['next'] else "нет"
            secret_str = data['secretnext'] if data['secretnext'] else "нет"
            print(f"{map_id}: next={next_str}, secret={secret_str}")
            count += 1
            
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден!")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
