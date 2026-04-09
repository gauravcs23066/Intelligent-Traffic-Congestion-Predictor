n = int(input("Enter an odd number: "))
magic = [[0]*n for _ in range(n)]
num = 1
i = 0
j = n // 2
while num <= n*n:
    magic[i][j] = num
    num += 1
    new_i = (i - 1) % n
    new_j = (j + 1) % n
    if magic[new_i][new_j] != 0:
        i = (i + 1) % n
    else:
        i = new_i
        j = new_j
print("\nMagic Square:")
for row in magic:
    print(row)
print("\nMagic Sum:", n * (n*n + 1) // 2)