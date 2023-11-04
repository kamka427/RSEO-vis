
from objects.sensor import Sensor

"""
This function returns the maximum reward and its sensors to a given Storage constraint.
"""


def knapSack(V: set[Sensor], S: int) -> (int, set[Sensor]):
    # Base Case
    if len(V) == 0 or S == 0:
        return 0, []

    # If weight of the nth item is
    # more than Knapsack of capacity W,
    # then this item cannot be included
    # in the optimal solution
    if V[-1].data_size > S:
        result, sensors = knapSack(V[:-1], S)
        return result, sensors

    # Calculate the value if the nth item is included
    with_item, sensors_with_item = knapSack(V[:-1], S - V[-1].data_size)
    with_item += V[-1].reward

    # Calculate the value if the nth item is not included
    without_item, sensors_without_item = knapSack(V[:-1], S)

    # Compare the values and update the sensors accordingly
    if with_item > without_item:
        result = with_item
        sensors = sensors_with_item + [V[-1]]
    else:
        result = without_item
        sensors = sensors_without_item

    return result, sensors
