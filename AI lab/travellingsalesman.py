from itertools import permutations

graph = [
    [0,10,15,20],
    [10,0,35,25],
    [15,35,0,30],
    [20,25,30,0]
]

n = 4
cities = list(range(1,n))

minimum = float('inf')
best = None

for path in permutations(cities):

    cost = 0
    k = 0

    for city in path:
        cost += graph[k][city]
        k = city

    cost += graph[k][0]

    if cost < minimum:
        minimum = cost
        best = (0,) + path + (0,)

print("Optimal Path:", best)
print("Minimum Cost:", minimum)
