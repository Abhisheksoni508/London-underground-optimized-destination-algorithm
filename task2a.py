from adjacency_list_graph import AdjacencyListGraph
from dijkstra import dijkstra
def Get_path(graph, pi, starting_index, ending_index):
    if (starting_index and ending_index) in pi:
        distances, predecessors = dijkstra(graph, pi.index(ending_index))
        shortest_path = (f'Travel Duration from Station {starting_index} to {ending_index} is '
                         f'{str(distances[pi.index(starting_index)])} Stations \nShortest path: {starting_index}')
        transit_node = pi.index(starting_index)

        while predecessors[transit_node] is not None:
            shortest_path += f" --> {pi[predecessors[transit_node]]}"
            transit_node = predecessors[transit_node]
        print(shortest_path)
    else:
        print('Invalid station')
def Stations(starting_station, ending_station):
    stations = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    connections = [('A', 'B', 1), ('B', 'C', 1), ('C', 'E', 1), ('A', 'D', 1),
             ('D', 'E', 1), ('A', 'E', 1), ('E', 'F', 1), ('E', 'G', 1)]

    graph = AdjacencyListGraph(len(stations), False, True)
    for edge in connections:
        graph.insert_edge(stations.index(edge[0]), stations.index(edge[1]), edge[2])

    Get_path(graph, stations, starting_station, ending_station)

if __name__ == "__main__": # Testing the code, we can change the stations accordingly
    Stations('A', 'G')