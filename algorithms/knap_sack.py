from objects.sensor import Sensor

"""
This function returns the maximum reward and its sensors to a given Storage constraint.
"""


def knapSack(V: list[Sensor], S: int) -> (int, set[Sensor]):
    # Handle edge cases
    if not V or S <= 0:
        return 0, list()

    n = len(V)
    dp = [[0 for _ in range(S + 1)] for _ in range(n + 1)]
    keep = [[False for _ in range(S + 1)] for _ in range(n + 1)]

    # Build the dp and keep tables
    for i in range(1, n + 1):
        for s in range(1, S + 1):
            if V[i - 1].data_size <= s:
                not_taken = dp[i - 1][s]
                taken = dp[i - 1][s - V[i - 1].data_size] + V[i - 1].reward
                if taken > not_taken:
                    dp[i][s] = taken
                    keep[i][s] = True
                else:
                    dp[i][s] = not_taken
            else:
                dp[i][s] = dp[i - 1][s]

    # Reconstruct the set of chosen sensors
    sensors = set()
    s = S
    for i in range(n, 0, -1):
        if keep[i][s]:
            sensors.add(V[i - 1])
            s -= V[i - 1].data_size

    return dp[n][S], list(sensors)