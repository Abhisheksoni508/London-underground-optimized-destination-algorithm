import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra

# Load the Excel data
file_path = '/Users/yasmi/Downloads/London Underground data.xlsx'
df = pd.read_excel(file_path)

# Extract relevant columns and drop any rows with missing values
cleaned_df = df.iloc[:, [0, 1]].dropna().reset_index(drop=True)
cleaned_df.columns = ['Line', 'Station']

# Get unique station names and assign each a unique index
stations = cleaned_df['Station'].unique()
station_indices = {station: idx for idx, station in enumerate(stations)}
n = len(stations)

# Build a dictionary of connections between stations with realistic travel times
connections = {}
for line in cleaned_df['Line'].unique():
    line_stations = cleaned_df[cleaned_df['Line'] == line]['Station'].tolist()
    for i in range(len(line_stations) - 1):
        station1, station2 = line_stations[i], line_stations[i + 1]
        if station1 != station2:
            edge = tuple(sorted((station1, station2)))
            if edge not in connections:
                journey_duration = np.random.randint(1, 7)
                connections[edge] = journey_duration

# Create the graph and add edges
graph = AdjacencyListGraph(n, False, True)
for (station1, station2), duration in connections.items():
    u_index, v_index = station_indices[station1], station_indices[station2]
    graph.insert_edge(u_index, v_index, duration)


# Function to reconstruct path from 'previous' array
def get_path(previous, start, end):
    path = []
    while end is not None:
        path.append(end)
        end = previous[end]
    path.reverse()  # Reverse to get the path from start to end
    return path


# Collect journey durations and paths for all unique pairs of stations
all_journey_durations = []
longest_journey_duration = 0
longest_path = []

for i in range(n):
    distances, previous = dijkstra(graph, i)  # Use the provided dijkstra function
    for j in range(i + 1, n):
        if distances[j] < float('inf'):  # Include only reachable stations
            all_journey_durations.append(distances[j])

            # Check if this is the longest path so far
            if distances[j] > longest_journey_duration:
                longest_journey_duration = distances[j]
                longest_path_indices = get_path(previous, i, j)
                longest_path = [stations[index] for index in longest_path_indices]

# Print the longest journey duration and path
print(f"The longest journey duration is: {longest_journey_duration} minutes")
print("The path with the longest journey is:")
print(" --> ".join(longest_path))

# Plot the histogram of journey durations
plt.figure(figsize=(12, 8))
plt.hist(all_journey_durations, bins=30, color='blue', alpha=0.85, edgecolor='black')
plt.title('Histogram of Journey Durations', fontsize=16)
plt.xlabel('Journey Duration (minutes)', fontsize=14)
plt.ylabel('Frequency', fontsize=14)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.xticks(np.arange(0, max(all_journey_durations) + 10, step=10))
plt.show()
