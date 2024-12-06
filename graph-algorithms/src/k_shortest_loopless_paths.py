# Computing Algorithms - Graph Algorithms - K-Shortest Loopless Paths
# Designed and developed by Kobi Chambers - Griffith University

# Import packages and modules
try:
    # import os
    import sys
    import time
    import heapq
    # import tkinter as tk
    # from tkinter import filedialog
    from collections import defaultdict
except ImportError as e:
    print(f"Error importing module: {e}")
    print(f"Please ensure that required modules are installed...\n")
    sys.exit(1)

##################################
### INPUT PROCESSING FUNCTIONS ###
##################################


def process_input_file(input_file_path):
    """
    Process the input file and extract parameters.

    Parameters:
    input_file_path (str): Directory path to the input file.

    Returns:
    network (defaultdict): A dictionary structure representing the network.
    num_vertices (int): The number of vertices present in the network.
    num_edges (int): The number of edges present in the network.
    source (str): The source vertex.
    destination (str): The destination vertex.
    k_paths (int): The target number of k shortest loopless paths to find.
    """
    # Reading input file not included in algorithm time
    with open(input_file_path, 'r') as f:
        # Get first line parameters
        num_vertices, num_edges = map(int, f.readline().split())

        # Get remaining lines
        lines = f.readlines()

        # Initialise network with defaultdict class from collections module
        network = defaultdict(dict)
        for line in lines[:-1]:
            line_values = line.split()
            ai, bi = line_values[:-1]
            edge_weight = float(line_values[-1])
            network[ai][bi] = edge_weight

        # Get last line parameters
        last_line = lines[-1].split()
        source, destination = last_line[:-1]
        k_paths = int(last_line[-1])

    # Ensure input matches rest of file
    if source not in network:
        sys.exit("Input parameter 'source' not found in the network. Exiting...")

    if destination not in network:
        sys.exit("Input parameter 'destination' not found in the network. Exiting...")

    return network, num_vertices, num_edges, source, destination, k_paths


def get_input_file():
    """
    Get the input file path from the command line arguments.

    Returns:
    str: The input file path.
    """
    if len(sys.argv) != 2:
        sys.exit("Usage: python k_shortest_paths.py [input_file_path]")

    input_file_path = sys.argv[1]

    return input_file_path

####################################
### UTILITY AND HELPER FUNCTIONS ###
####################################


def timer(function_name):
    """
    Decorator function to measure the execution time of another function.

    Parameters:
    function_name (function): The function to time.

    Returns:
    function: A wrapper function that times the execution of the input function and returns the result and the time taken.
    """
    def wrapper(*args, **kwargs):
        # Time and execute function
        start_time = time.perf_counter()
        result = function_name(*args, **kwargs)
        end_time = time.perf_counter()

        # Elapsed time calculation - Convert to milliseconds
        elapsed_time = (end_time - start_time) * 1_000
        return result, elapsed_time

    return wrapper

#####################################
### ALGORITHM EXECUTION FUNCTIONS ###
#####################################


def bidirectional_dijkstra(network, source, destination):
    """
    Helper function implementing bidirectional Dijkstra's algorithm to find the shortest path in a network.

    Parameters:
    network (defaultdict): A dictionary structure representing the network.
    source (str): The source vertex.
    destination (str): The destination vertex.

    Returns:
    path (list): A list of vertices representing the shortest path.
    distance (float): The summed distance of the path.
    """
    # Initialise bidirectional search

    # Cumulative distance dicts from both directions
    frwd_edge_distance = {source: 0}
    bkwd_edge_distance = {destination: 0}
    # Store previously visited vertices in dict
    frwd_last_vertex = {}
    bkwd_last_vertex = {}
    # Prio queues from both directions
    frwd_prio_queue = [(0, source)]
    bkwd_prio_queue = [(0, destination)]
    # Vertex that both paths converge on
    meeting_vertex = None
    # Minimum path distance found
    min_distance = float('inf')

    # Loop until one of the prio queues are empty
    while frwd_prio_queue and bkwd_prio_queue:

        # Forward search
        # Pop and return lowest weight and vertex heap in prio queue based on edge weights
        frwd_edge_weight, frwd_current_vertex = heapq.heappop(frwd_prio_queue)

        # Check if current vertex already visited by backward search
        if frwd_current_vertex in bkwd_edge_distance:
            # Find distance
            total_distance = frwd_edge_distance[frwd_current_vertex] + \
                bkwd_edge_distance[frwd_current_vertex]

            # Check if current path is lower total distance so far
            if total_distance < min_distance:
                # Set new meeting vertex and minimum distance
                meeting_vertex = frwd_current_vertex
                min_distance = total_distance

        # Skip iteration if current distance is shorter than next path
        if frwd_edge_weight > frwd_edge_distance[frwd_current_vertex]:
            continue

        # Loop to find neighbours
        for frwd_neighbour, frwd_weight in network[frwd_current_vertex].items():
            # Calculate edge weight to neighbour
            frwd_neighbour_weight = frwd_edge_distance[frwd_current_vertex] + frwd_weight

            # Check if neighbour is better
            if frwd_neighbour not in frwd_edge_distance or frwd_neighbour_weight < frwd_edge_distance[frwd_neighbour]:
                # Set distance to neighbour and last vertex in search
                frwd_edge_distance[frwd_neighbour] = frwd_neighbour_weight
                frwd_last_vertex[frwd_neighbour] = frwd_current_vertex

                # Add weight and neighbouring vertex heap to forward prio queue
                heapq.heappush(frwd_prio_queue,
                               (frwd_neighbour_weight, frwd_neighbour))

        # Backward search
        # Did not include commenting as would be practically the same as forward search steps
        bkwd_edge_weight, bkwd_current_vertex = heapq.heappop(bkwd_prio_queue)

        if bkwd_current_vertex in frwd_edge_distance:
            total_distance = frwd_edge_distance[bkwd_current_vertex] + \
                bkwd_edge_distance[bkwd_current_vertex]

            if total_distance < min_distance:
                meeting_vertex = bkwd_current_vertex
                min_distance = total_distance

        if bkwd_edge_weight > bkwd_edge_distance[bkwd_current_vertex]:
            continue

        for bkwd_neighbour, bkwd_weight in network[bkwd_current_vertex].items():
            bkwd_neighbour_weight = bkwd_edge_distance[bkwd_current_vertex] + bkwd_weight

            if bkwd_neighbour not in bkwd_edge_distance or bkwd_neighbour_weight < bkwd_edge_distance[bkwd_neighbour]:
                bkwd_edge_distance[bkwd_neighbour] = bkwd_neighbour_weight
                bkwd_last_vertex[bkwd_neighbour] = bkwd_current_vertex

                heapq.heappush(bkwd_prio_queue,
                               (bkwd_neighbour_weight, bkwd_neighbour))

    # Check if no path found
    if meeting_vertex is None:
        return None, float('inf')

    # Initialise path lists and build full path
    frwd_path = []
    bkwd_path = []
    current_vertex = meeting_vertex

    # Traverse vertices from meeting vertex to source
    while current_vertex != source:
        frwd_path.append(current_vertex)
        current_vertex = frwd_last_vertex[current_vertex]

    # Add final vertex to list and reverse
    frwd_path.append(source)
    frwd_path.reverse()

    # Reset current vertex
    current_vertex = meeting_vertex

    # Traverse vertices from meeting vertex to destination
    while current_vertex != destination:
        bkwd_path.append(current_vertex)
        current_vertex = bkwd_last_vertex[current_vertex]

    # Add final vertex to list
    bkwd_path.append(destination)

    # Combine the forward and backward paths
    path = frwd_path + bkwd_path[1:]

    # Return the path built and associated distance found
    return path, min_distance


@timer
def execute_ksp_yen(network, source, destination, k_paths):
    """
    Execute Yen's algorithm to find the k shortest paths between the source and destination in a network.

    Parameters:
    network (defaultdict): A dictionary structure representing the network.
    source (str): The source vertex.
    destination (str): The destination vertex.
    k_paths (int): The number of shortest paths to find.

    Returns:
    distances (list): A list of distances of the k shortests paths in the network.
    """
    # Initialise our path lists and track removed edges
    paths = []
    possible_paths = []
    rmd_edges = defaultdict(list)

    # We use a bi-directional dijkstra's algorithmn to find the actual shortest path first
    first_path, first_distance = bidirectional_dijkstra(
        network, source, destination)
    # Check if we found a valid path from source to dest
    if first_path is None:
        return paths

    # Append path and associated distance, as we need to sort by the path distance later and this makes it easier
    paths.append((first_path, first_distance))

    # Loop through k - 1 times to find rest of paths
    for _ in range(k_paths - 1):
        # Loop 1 less time than the length of the shortest path found earlier
        for i in range(len(paths[-1][0]) - 1):
            # Create a temporary vertex and root path leading to the temp vertex
            temp_vertex = paths[-1][0][i]
            root_path = paths[-1][0][:i + 1]

            # Check if root path has less than 2 vertices, skip if so
            if len(root_path) < 2:
                continue

            # Loop through current paths to remove edges from paths
            for path, _ in paths:
                if root_path == path[:i + 1]:
                    rmd_edges[root_path[-2]].append(path[-2])

            # Update network, removing edges
            for path, _ in paths[:-1]:
                if temp_vertex in path:
                    # Store original weight and set temp edge weight to inf
                    og_edge_weight = network[path[-2]][path[-1]]
                    network[path[-2]][path[-1]] = float('inf')

            # Find path from temp vertex to destinations
            temp_path, temp_distance = bidirectional_dijkstra(
                network, temp_vertex, destination)

            # Add to possible paths if we reached the destination
            if temp_path and temp_path[-1] == destination:
                possible_paths.append(
                    (root_path[:-1] + temp_path, paths[-1][1] + temp_distance))

            # Rebuild network
            for path, _ in paths[:-1]:
                if temp_vertex in path:
                    network[path[-2]][path[-1]] = og_edge_weight

            # Replace removed edges
            for vertex in rmd_edges[root_path[-2]]:
                network[root_path[-2]][vertex] = float('inf')

        # Exit loop if we have no more possible paths to traverse in the network
        if not possible_paths:
            break

        # Since we kept paths and distances as a tuple, we can easily sort our possible paths based on distances
        possible_paths.sort(key=lambda p: p[1])
        # Add the shortest path & distance to our paths list
        paths.append(possible_paths.pop(0))

    # Clearer to the reader if we utilise list comprehension before returning the result
    distances = [distance for _, distance in paths]
    return distances

##############
### DRIVER ###
##############


if __name__ == '__main__':
    # Get the input file path from command line arguments
    input_file_path = get_input_file()

    # Get the input lines from text file
    network, num_vertices, num_edges, source, destination, k_paths = process_input_file(
        input_file_path)

    # Execute algorithm function with timer decorator
    distances, elapsed_time = execute_ksp_yen(
        network, source, destination, k_paths)
    print("\nResults")

    if not distances:
        print("No path was found from source to destination.\n")

    else:
        # Print distances of k shortests paths, separated by commas
        for distance in distances[:-1]:
            sys.stdout.write(f"{distance:.4f}, ")
        sys.stdout.write(f"{distances[-1]:.4f}\n")

    # Display execution time
    print(f"Execution time - {elapsed_time:.2f} milliseconds\n")
