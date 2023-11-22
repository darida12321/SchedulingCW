import numpy as np

# Problem definition
def getDependencies():
    G = np.zeros((31, 31))
    G[0, 30] = 1
    G[1, 0] = 1
    G[2, 7] = 1
    G[3, 2] = 1
    G[4, 1] = 1
    G[5, 15] = 1
    G[6, 5] = 1
    G[7, 6] = 1
    G[8, 7] = 1
    G[9, 8] = 1
    G[10, 0] = 1
    G[11, 4] = 1
    G[12, 11] = 1
    G[13, 12] = 1
    G[16, 14] = 1
    G[14, 10] = 1
    G[15, 4] = 1
    G[16, 15] = 1
    G[17, 16] = 1
    G[18, 17] = 1
    G[19, 18] = 1
    G[20, 17] = 1
    G[21, 20] = 1
    G[22, 21] = 1
    G[23, 4] = 1
    G[24, 23] = 1
    G[25, 24] = 1
    G[26, 25] = 1
    G[27, 25] = 1
    G[28, 27] = 1
    G[29, 3] = 1
    G[29, 9] = 1
    G[29, 13] = 1
    G[29, 19] = 1
    G[29, 22] = 1
    G[28, 26] = 1
    G[29, 28] = 1
    return G
def getDueDates():
    return np.array([172, 82, 18, 61, 93, 71, 217, 295, 290, 287, 253, 307, 279, 73, 355, 34, 233, 77, 88, 122, 71, 181, 340, 141, 209, 217, 256, 144, 307, 329, 269])
def getProcessingTimes(vii=14, blur=5, night=18, onnx=3, emboss=2, muse=10, wave=6):
    return np.array([onnx, muse, emboss, emboss, blur, emboss, vii, blur, wave, blur, blur, emboss, onnx, onnx, blur, wave, wave, wave, emboss, onnx, emboss, onnx, vii, blur, night, muse, emboss, onnx, wave, emboss, muse])


def transitiveClosure(G):
    n = len(G)
    reach = np.copy(G)
    for k in range(n):
        # Pick all vertices as source
        for i in range(n):
            # Pick all vertices as destination
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])
    return reach

# Alternative version of vns, with multiple neighbor selections
# # VNS function
# def vns(x0, I, K, getG, getNeigborhood):
#     x = x0
#     g = getG(x)
#     for k in range(K):
#         print(f'Iteration {k}, Tardiness: {getG(x)}, Job order: {x}')
#         for i in range(1, I+1):
#             maxSwaps = 0
#             y = x
#             for _ in range(3):
#                 swaps, schedule = getNeigborhood(np.copy(x), i)
#                 if swaps >= maxSwaps:
#                     swaps = maxSwaps
#                     y = schedule
#             delta = g-getG(y)
#             if delta > 0:
#                 x = y
#                 g = getG(x)
#                 break
#     return x

# # Produce a function for TABU that check if a neighbor is valid
# def getRandomNeighborTC(G):
#     def getRandomNeighbor(x, i):
#         swaps = np.random.randint(1, i+1)
#         for swap in range(swaps):
#             indices = np.arange(len(x)-2)
#             while True:
#                 index = np.random.choice(indices)
#                 indices = np.delete(indices, np.where(indices == index))
#                 if G[x[index]-1, x[index+1]-1] == 1:
#                     continue
#                 x[index], x[index+1] = x[index+1], x[index]
#                 break
#         return swaps, x
#     return getRandomNeighbor    

# VNS function
def vns(x0, I, K, getG, getNeigborhood):
    x = x0
    g = getG(x)
    for k in range(K):
        print(f'Iteration {k}, Tardiness: {getG(x)}, Job order: {x}')
        for i in range(1, I+1):
            y = getNeigborhood(np.copy(x), i)
            delta = g-getG(y)
            if delta > 0:
                x = y
                g = getG(x)
                break
    return x

# Produce a function for TABU that check if a neighbor is valid
def getRandomNeighborTC(G):
    def getRandomNeighbor(x, i):
        swaps = np.random.randint(1, i+1)
        for swap in range(swaps):
            indices = np.arange(len(x)-2)
            while True:
                index = np.random.choice(indices)
                indices = np.delete(indices, np.where(indices == index))
                if G[x[index]-1, x[index+1]-1] == 1:
                    continue
                x[index], x[index+1] = x[index+1], x[index]
                break
        return x
    return getRandomNeighbor    


# Produce a function for TABU that gets the tardiness
def getTardiness(P, D):
    def getG(x):
        t = 0
        tardiness = 0
        for i in x:
            t += P[i-1]
            tardiness += max(t-D[i-1], 0)
        return tardiness
    return getG


D = getDueDates()
P = getProcessingTimes()
G = getDependencies()
x0 = np.array([30, 29, 23, 10, 9, 14, 13, 12, 4, 20, 22, 3, 27, 28,
              8, 7, 19, 21, 26, 18, 25, 17, 15, 6, 24, 16, 5, 11, 2, 1, 31])

K = 3000

x = vns(x0, 30, K, getTardiness(P, D),
         getRandomNeighborTC(transitiveClosure(G)))
print('-----')
print('Initial job order:', x0)
print('Initial tardiness:', getTardiness(P, D)(x0))
print('-----')
print('Final job order:', x)
print('Final tardiness:', getTardiness(P, D)(x))


# for gamma in [1, 5, 10, 20]:
#     for L in [5, 10, 20, 30]:
#         x = tabu(x0, L, gamma, K, getTardiness(P,D), checkNeighborCorrectnessTC(transitiveClosure(G)))
#         print("Gamma: ", gamma, ", L: ", L, ", Tardiness: ", getTardiness(P,D)(x))
