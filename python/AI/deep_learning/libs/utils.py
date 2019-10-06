def mean_squared_error(x, t):
    return 0.5 * np.sum((y-t)**2)

def cross_entropy_error(x, t):
    delta = 1e-7
    return -np.sum(t * np.log(x+delta))

#one hot
def cross_entropy_error_batch(x, t):
    if x.ndim == 1:
        t = t.reshape(1, t.size)
        x = x.reshape(1, x.size)
    batch_size = t.shape[0]
    return -np.sum(t * np.log(x)) / batch_size
