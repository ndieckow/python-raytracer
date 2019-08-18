# Nothing important.

# the numpy way
mat = np.zeros((width, height))
for k in range(mat.shape[0]):
    for i in range(mat.shape[1]):
        mat[i, k] = (20*(k+i)) % 255

mlist = map(lambda x : map(int, x), mat.tolist())

# the non-numpy way
lst = [[(20*(k+i)) % 255 for i in range(16)] for k in range(16)]
###########
