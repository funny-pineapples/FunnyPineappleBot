n = int(input())
lt = []

for i in range(n - 1):
    lt += [list(map(str, input().split()))]

lts = [lt[0]]
l = lt[0][0]
r = lt[0][1]
lt.pop(0)

for i in range(n - 2):
    for j in range(len(lt)):
        if lt[j][0] == r:
            lts += [lt[j]]
            lt.pop(j)
            r = lts[-1][-1]
            break
        elif lt[j][1] == l:
            lts = [lt[j]] + lts
            lt.pop(j)
            l = lts[0][0]
            break

for i in range(n - 2, -1, -1):
    print(lts[i][1])

print(lts[0][0])
