import pandas as pd
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra


file_path = '/Users/yasmi/Downloads/London Underground data.xlsx'
df = pd.read_excel(file_path)


cleaned_df = df.iloc[:, [0, 1, 2, 3]].dropna().reset_index(drop=True)


cleaned_df.columns = ['Line', 'From Station', 'To Station', 'Minutes Between Stations']


stations = cleaned_df['From Station'].unique()
station_indices = {station: idx for idx, station in enumerate(stations)}
n = len(stations)


connections = {}
for line in cleaned_df['Line'].unique():
    line_stations = cleaned_df[cleaned_df['Line'] == line]['From Station'].tolist()
    for i in range(len(line_stations) - 1):
        station1, station2 = line_stations[i], line_stations[i + 1]
        if station1 != station2:
            edge = tuple(sorted((station1, station2)))
            if edge not in connections:
                connections[edge] = 1

# Create the graph and add edges
graph = AdjacencyListGraph(n, False, True)
for (station1, station2), stop in connections.items():
    u_index, v_index = station_indices[station1], station_indices[station2]
    graph.insert_edge(u_index, v_index, stop)


max_comparisons = 272 * 271 / 2
comparisons_made = 0

longest_stops = 0
longest_path = []


journey_durations = []


def get_path(start, end, predecessors):
    path = []
    node = end
    while node is not None:
        path.append(stations[node])
        node = predecessors[node]
    return path[::-1]


for i in range(n):
    if comparisons_made >= max_comparisons:
        break
    distances, predecessors = dijkstra(graph, i)
    for j in range(i + 1, n):
        if comparisons_made >= max_comparisons:
            break

        if distances[j] < float('inf'):
            journey_durations.append(distances[j])

            if distances[j] > longest_stops:
                longest_stops = distances[j]
                longest_path = get_path(i, j, predecessors)
        comparisons_made += 1


print(f"The longest journey between any two pairs of stations are: {longest_stops} stops")
print(" The stations between are :", " - ".join(longest_path))
print(f"Total comparisons made: {comparisons_made}")


plt.figure(figsize=(12, 8))
plt.hist(journey_durations, bins=range(1, max(journey_durations) + 2), edgecolor='black', alpha=0.85)
plt.title('Histogram of Journey Durations By Number of Stops')
plt.xlabel('Number of Stops')
plt.ylabel('Frequency')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()