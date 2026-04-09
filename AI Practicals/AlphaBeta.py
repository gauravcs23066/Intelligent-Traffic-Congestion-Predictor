import math
def alpha_beta(depth, node_index, maximizing_player, values, alpha, beta, max_depth):
    
    if depth == max_depth:
        return values[node_index]

    if maximizing_player:
        max_eval = -math.inf

        for i in range(2):
            eval = alpha_beta(depth + 1, node_index * 2 + i, False, values, alpha, beta, max_depth)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = math.inf

        for i in range(2):
            eval = alpha_beta(depth + 1, node_index * 2 + i, True, values, alpha, beta, max_depth)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break

        return min_eval


depth = int(input("Enter depth of game tree: "))
leaf_nodes = 2 ** depth

print(f"Enter {leaf_nodes} leaf node values:")
values = []

for i in range(leaf_nodes):
    val = int(input(f"Value {i+1}: "))
    values.append(val)

result = alpha_beta(0, 0, True, values, -math.inf, math.inf, depth)

print("\nOptimal value using Alpha-Beta Pruning:", result)