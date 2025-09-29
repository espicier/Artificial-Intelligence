import time

def best_path(city_map, start=0):
    start_exec = time.perf_counter()
    visited = set([start])
    path = [start]
    total_cost = 0
    current = start

    while len(visited) < len(city_map):
        # On cherche la ville la plus proche non encore visitée
        next_city = min(
            (city for city in city_map[current] if city not in visited),
            key=lambda city: city_map[current][city]
        )
        path.append(next_city)
        total_cost += city_map[current][next_city]
        visited.add(next_city)
        current = next_city

    # Retour à la ville de départ
    total_cost += city_map[current][start]
    path.append(start)

    end_exec = time.perf_counter()
    time_exec = end_exec - start_exec

    return path, total_cost, time_exec

