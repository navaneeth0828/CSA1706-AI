from queue import PriorityQueue

graph = {
    'A':[('B',1),('C',4)],
    'B':[('D',2),('E',5)],
    'C':[('F',3)],
    'D':[('G',5)],
    'E':[('G',1)],
    'F':[('G',2)],
    'G':[]
}

heuristic = {
    'A':7,
    'B':6,
    'C':4,
    'D':4,
    'E':2,
    'F':2,
    'G':0
}

def astar(start, goal):

    pq = PriorityQueue()
    pq.put((0,start))

    cost = {start:0}
    parent = {start:None}

    while not pq.empty():

        _, current = pq.get()

        if current == goal:
            break

        for neighbour, weight in graph[current]:

            new_cost = cost[current] + weight

            if neighbour not in cost or new_cost < cost[neighbour]:

                cost[neighbour] = new_cost
                priority = new_cost + heuristic[neighbour]

                pq.put((priority, neighbour))
                parent[neighbour] = current

    path = []

    node = goal

    while node:
        path.append(node)
        node = parent[node]

    print("Path:", path[::-1])
    print("Cost:", cost[goal])

astar('A','G')
