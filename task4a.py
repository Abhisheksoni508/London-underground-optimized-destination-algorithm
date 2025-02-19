
import pandas as pd
from adjacency_list_graph import AdjacencyListGraph
from mst import kruskal

def load_data(filepath):
    #Load data from excel sheet
    return pd.read_excel(filepath, sheet_name=0, header=None, names=['Line', 'Station1', 'Station2', 'JourneyTime'])


def build_graph(df):
    #Build a graph and ensure consistent output by sorting station indices
    # Get unique station names
    unique_sts = set(df['Station1'].dropna()).union(set(df['Station2'].dropna()))
    # Map station names to sorted indices
    stn_indices = {station: idx for idx, station in enumerate(sorted(unique_sts))}

    # Initialize graph
    num_stations = len(unique_sts)
    graph = AdjacencyListGraph(num_stations, False, True)

    # Add edges to the graph
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


def get_mst_edges(graph):
    #Compute the Minimum Spanning Tree (MST) edges using Kruskal's algorithm
    mst_graph = kruskal(graph)
    return {(min(edge[0], edge[1]), max(edge[0], edge[1])) for edge in mst_graph.get_edge_list()}


def find_affected_routes(original_edges, mst_edges, station_indices):
    #Identify and print affected routes
    affected_routes = original_edges - mst_edges
    print("Closed routes (closed line sections):")
    for u, v in affected_routes:
        station1 = [station for station, idx in station_indices.items() if idx == u][0]
        station2 = [station for station, idx in station_indices.items() if idx == v][0]
        print(f"{station1} <--> {station2}")
    print(f"\nNumber of affected routes: {len(affected_routes)}")


def main(filepath):
    df = load_data(filepath)
    graph, original_edges, station_indices = build_graph(df)
    mst_edges = get_mst_edges(graph)
    find_affected_routes(original_edges, mst_edges, station_indices)


if __name__ == "__main__":
    main('/Users/yasmi/Downloads/London Underground data.xlsx')