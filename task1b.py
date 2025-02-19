import time
import matplotlib.pyplot as plt
from generate_random_graph import generate_random_graph
from random_sample import random_sample
from task1a import Get_path


def generate_and_time_path(num):
    """Generate a graph, select random stations, and compute the path while timing execution."""
    print(f'#{num} stations generation')
    graph = generate_random_graph(num, 0.25, True, False, True, 1, 15)

    selected_stations = list(random_sample(2, num - 1))
    start_time = time.time()
    Get_path(graph, [str(i) for i in range(num)], str(selected_stations[0]), str(selected_stations[1]))
    exec_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    print(f'Execution time : {exec_time} milliseconds\n')
    return exec_time


def calculate_theoretical_times(stations, max_empirical_time):
    """Calculate normalized theoretical O(n^2) times based on the empirical max time."""
    theoretical_times = [n ** 2 for n in stations]
    max_theoretical_time = max(theoretical_times)
    return [t / max_theoretical_time * max_empirical_time for t in theoretical_times]


def plot_results(stations, empirical_times, theoretical_times):
    """Plot the empirical and theoretical execution times."""
    plt.figure(figsize=(10, 6))
    plt.plot(stations, empirical_times, 'o-', label='Empirical Time (measured)', color='blue')
    plt.plot(stations, theoretical_times, 's--', label='Theoretical Time O(n^2)', color='red')

    plt.xlabel('Network Size (n)')
    plt.ylabel('Average Execution Time (ms)')  # ms for consistency
    plt.title('Empirical vs Theoretical Time Complexity')
    plt.legend()
    plt.grid(True)
    plt.show()


def num_of_stations():
    stations = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]

    empirical_times = [generate_and_time_path(num) for num in stations]

    normalized_theoretical_times = calculate_theoretical_times(stations, max(empirical_times))

    plot_results(stations, empirical_times, normalized_theoretical_times)


# Testing
if __name__ == "__main__":
    num_of_stations()
