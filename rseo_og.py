from sys import maxsize
from itertools import permutations

"""
This function returns the maximum reward and its sensors to a given Storage constraint.
"""
def knapSack(W, wt, val, n):
    # Base Case
    if n == 0 or W == 0:
        return 0, []

    # If weight of the nth item is
    # more than Knapsack of capacity W,
    # then this item cannot be included
    # in the optimal solution
    if wt[n - 1] > W:
        result, indices = knapSack(W, wt, val, n - 1)
        return result, indices

    # Calculate the value if the nth item is included
    with_item, indices_with_item = knapSack(W - wt[n - 1], wt, val, n - 1)
    with_item += val[n - 1]

    # Calculate the value if the nth item is not included
    without_item, indices_without_item = knapSack(W, wt, val, n - 1)

    # Compare the values and update the indices accordingly
    if with_item > without_item:
        result = with_item
        indices = indices_with_item + [n - 1]
    else:
        result = without_item
        indices = indices_without_item

    return result, indices

"""
This function returns the minimum waypoints, that can reach the desired sensors given from the Knapsack function.
"""

def GreedySetCover(X: set, *sets: set) -> set:
    I = set()  # Initialize the set cover as an empty set
    print(X)
    print(sets)

    while X:  # Repeat until every element in X is covered
        max_intersection = 0
        selected_set = None

        for j, Sj in enumerate(sets, start=1):
            print(j, Sj)
            intersection = len(X & Sj)  # Calculate the size of the intersection
            print("intersection: ", intersection)
            if intersection > max_intersection:
                max_intersection = intersection
                selected_set = j
                print("selected set: ", selected_set)
          

        if selected_set is not None:
            I.add(selected_set)  # Include the set with the maximum intersection into the set cover
            X -= sets[selected_set - 1]  # Remove elements in the selected set from X

    return I


"""
This function returns the less energy consuming path for the given waypoints from greedy set cover function.
"""
def travellingSalesmanProblem(graph: list[list],
                              selected_waypoints: list[int]) -> (list[int], int):
    new_graph = [graph[i] for i in selected_waypoints]  # to update the graph with the selected waypoints
    new_graph.insert(0, graph[0])  # add the depo
    vertex = []
    s = 0  # starts from the depo
    for i in range(len(new_graph)):
        if i != s:
            vertex.append(i)

    min_path_weight = maxsize
    min_path = None  # Initialize the min_path as None

    next_permutation = permutations(vertex)
    for i in next_permutation:
        current_path_weight = 0
        path = [s]  # Initialize the path with the source vertex
        k = s
        for j in i:
            current_path_weight += new_graph[k][j]
            path.append(j)
            k = j
        current_path_weight += new_graph[k][s]

        if current_path_weight < min_path_weight:
            min_path_weight = current_path_weight
            min_path = path  # Update min_path if a shorter path is found

    min_path.append(s)  # mission ends in the depo as well

    return min_path, min_path_weight

"""
Calculates the cost for the mission.
"""
def cost(flying_path: list[int],
         flying_cost_of_mission: int,
         hovering_cost: list[int]) -> int:
    hovering_cost_of_mission = sum(
        hovering_cost[i] for i in flying_path if i < len(hovering_cost))  # not sure if we need the if

    return flying_cost_of_mission + hovering_cost_of_mission

"""
RSEO algorithm
"""
def RSEO():
    V_prime = knapSack(STORAGE, DATA_SIZES, REWARDS, len(REWARDS))[1]
    P_prime = GreedySetCover(set(V_prime), S1, S2, S3)
    M, flying_cost = travellingSalesmanProblem(GRAPH, P_prime)

    reward_at_selected_waypoints = {}
    for selected_sensors in V_prime:
        reward_at_selected_waypoints[selected_sensors] = REWARD_AT_WAYPOINTS[selected_sensors]

    while cost(M, flying_cost, HOVERING_COST) > ENERGY:
        p = min(reward_at_selected_waypoints)
        M.remove(p)

    return M


if __name__ == "__main__":
    ENERGY = 100
    HOVERING_COST = [5, 10, 7, 4]
    GRAPH = [[0, 10, 15, 20], [10, 0, 35, 25],
             [15, 35, 0, 30], [20, 25, 30, 0]]  # represents the flying costs to each vertex
    STORAGE = 50
    S1 = set([1, 2, 3, 4, 5])  # from s1 waypoint which sensors can be seen
    S2 = set([4, 5, 6, 7])
    S3 = set([6, 7, 8, 9, 10])
    REWARD_AT_WAYPOINTS = {
        1: 20,
        2: 10,
        3: 5
    }
    SENSORS = ['depo', 's1', 's2', 's3']  # sensor names
    REWARDS = [0, 60, 100, 120]  # reward
    DATA_SIZES = [0, 10, 20, 30]  # how many data stored

    print("The path for the drone:")
    print(RSEO())