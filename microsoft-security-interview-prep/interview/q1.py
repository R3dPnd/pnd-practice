import heapq

def social_distance(building):
    # p - person
    # l - locked
    # b - empty open office
    
    # Traverse the building creatign a mapping from each office pace representing the current minmum discace from a person
    # If we find a locked room or an enp,ty room, fill it with inf
    # if we fid a person we fill it with 0 and add it our queue
    # Ocnce we have our queue, we traverse from each person keeping track of the distance traveled and update only the empty rooms with this minimum distance
    INF = float("inf")
    directions = [(0,1),(1,0),(-1,0),(0,-1)]
    
    person_distace = [[INF]*len(building)] * len(building[0])
    queue = []
    
    for i in range(len(building)):
        for j in range(len(building[0])):
            curr = building[i][j]
            if curr == "P":
                person_distace[i][j] = 0
                queue.append((i,j))
            else:
                person_distace[i][j] = INF
    while queue:
        person = queue.pop()
        heap = []
        heapq.heappush(heap, (0, person))
        while heap:
            d,loc = heapq.heappop(heap)
            x,y = loc
            if 0 <= x < len(building) and 0<= y < len(building[0])  and building[x][y] != "L":
                new_d = d+1
                if person_distace[x][y] > new_d:
                    person_distace[x][y] = new_d
                    for dx,dy in directions:
                        heapq.heappush(heap, (new_d, (x+dx, y+dy)))
    return person_distace
        

res = social_distance([
    ["P","B","B"],
    ["B","P","L"],
    ["B","B","L"]
    ])
print(res)