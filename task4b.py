import pandas as pd
import math
import matplotlib.pyplot as plt
import numpy as np
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal
from dijkstra import dijkstra
from print_path import print_path


def load_data(filepath):
    #Load data from excel sheet
    return pd.read_excel(filepath, sheet_name=0,
                         header=None,
                         names=['Line', 'Station1', 'Station2', 'JourneyTime'])


def build_graph(df):
    #Build a graph from the dataframe and map station names to indices
    unique_sts = set(df['Station1'].dropna()).union(set(df['Station2'].dropna()))
    stn_indices = {station: idx for idx, station in enumerate(sorted(unique_sts))}

    # Initialize graph
    num_stations = len(unique_sts)
    graph = AdjacencyListGraph(num_stations, False, True)

    original_edges = set()
    for _, row in df.iterrows():
        if pd.notna(row['JourneyTime']):
            u = stn_indices[row['Station1']]
            v = stn_indices[row['Station2']]
            weight = row['JourneyTime']

            if not graph.has_edge(u, v):
                graph.insert_edge(u, v, weight)
                original_edges.add((min(u, v), max(u, v)))

    return graph, original_edges, stn_indices


def compute_mst_edges(graph):
    #Compute the Minimum Spanning Tree (MST) edges using Kruskal's algorithm
    mst_graph = kruskal(graph)
    return {(min(edge[0], edge[1]), max(edge[0], edge[1]))
            for edge
            in mst_graph.get_edge_list()}


def find_affected_routes(original_edges, mst_edges, station_indices):
    #Find and print affected routes
    affected_routes = original_edges - mst_edges
    print("Closed routes:")
    for u, v in sorted(affected_routes):
        station1 = [station for station, idx in station_indices.items() if idx == u][0]
        station2 = [station for station, idx in station_indices.items() if idx == v][0]
        print(f"{station1} --> {station2}")
    print(f"\nNumber of affected routes: {len(affected_routes)}")
    return affected_routes


def analyze_longest_journey(graph, station_indices):
    #Analyze and display the longest journey in the reduced network
    journey_times = []
    max_time = 0
    max_start, max_end, max_previous = None, None, None

    for start_index in range(len(station_indices)):
        distances, previous = dijkstra(graph, start_index)
        for end_index in range(len(station_indices)):
            if start_index != end_index and math.isfinite(distances[end_index]):
                journey_times.append(distances[end_index])
                if distances[end_index] > max_time:
                    max_time = distances[end_index]
                    max_start, max_end = start_index, end_index
                    max_previous = previous

    start_station = [station for station, idx in station_indices.items() if idx == max_start][0]
    end_station = [station for station, idx in station_indices.items() if idx == max_end][0]
    route_names = print_path(max_previous, max_start, max_end,
                             lambda i: [station for station, idx in station_indices.items() if idx == i][0])

    print(f"\nLongest journey time in reduced network: {max_time} minutes")
    print(f"Longest journey path from {start_station} to {end_station}: {' -> '.join(route_names)}")

    # Plot histogram of journey times
    plt.figure(figsize=(12, 8))
    plt.hist(journey_times, bins=30, color='blue', alpha=0.85, edgecolor='black')
    plt.title("Journey Times in Reduced Network (min)")
    plt.xlabel("Journey Time (min)")
    plt.ylabel("Number of Journeys")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def main(filepath):
    df = load_data(filepath)
    graph, original_edges, station_indices = build_graph(df)
    mst_edges = compute_mst_edges(graph)
    affected_routes = find_affected_routes(original_edges, mst_edges, station_indices)

    # Remove affected edges from the graph
    for u, v in affected_routes:
        graph.delete_edge(u, v)

    # Analyze longest journey in the reduced network
    analyze_longest_journey(graph, station_indices)


if __name__ == "__main__":
    main("/Users/yasmi/Downloads/London Underground data.xlsx")