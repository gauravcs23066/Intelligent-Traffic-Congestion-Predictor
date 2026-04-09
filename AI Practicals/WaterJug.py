def water_jug_dfs(capacity1, capacity2, target):
    visited = set()  
    path = []  

    def dfs(jug1, jug2):
        if (jug1, jug2) in visited:
            return False
        
        visited.add((jug1, jug2))

        path.append((jug1, jug2))

        if jug1 == target or jug2 == target:
            return True


        if dfs(3, jug2):
            return True
        if dfs(jug1, 5):
            return True
        if dfs(0, jug2):
            return True
        if dfs(jug1, 0):
            return True
        if dfs(max(0, jug1 - (5 - jug2)), min(5, jug1 + jug2)):
            return True
        if dfs(min(3, jug1 + jug2), max(0, jug2 - (3 - jug1))):
            return True

        path.pop()
        return False

    dfs(0, 0)

    return path

capacity1 = int(input("Enter the capacity of jug 1: "))  
capacity2 = int(input("Enter the capacity of jug 2: "))  
target = int(input("Enter capacity: "))     

solution = water_jug_dfs(capacity1, capacity2, target)

if solution:
    print("Solution steps:")
    for step in solution:
        print(step)
else:
    print("No solution found.")