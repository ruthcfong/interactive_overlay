import numpy as np


YELLOW = (1., 1., 0.)


def many_cossim(us,v):
    """
    Compute the cosine similarity between a batch of activation vectors
    (:param:`us`) and a single activation vector (:param:`v`, which contains
    an activation tensor at a single spatial location)."""
    us_mags = np.sqrt((us*us).sum(-1)) + 1e-4
    v_mag = np.sqrt((v*v).sum()) + 1e-4
    return (us*v).sum(-1) / us_mags / v_mag


def cossim_grid(acts1, acts2):
    cossims = [[many_cossim(acts2, v)
                for v in row] for row in acts1]
    return np.asarray(cossims)


def add_color_index(arr, stride, color=YELLOW):
    assert isinstance(arr, np.ndarray)
    assert len(arr.shape) == 2
    arr = np.tile(arr[:,:,None], (1, 1, 3))
    for i in range(int(arr.shape[0]/stride)):
        for j in range(int(arr.shape[1]/stride)):
            arr[i*stride+i,j*stride+j] = color
    return arr


def add_color_index_multi(arr, stride, color_each=False, color=YELLOW):
    assert isinstance(arr, list)
    for i in range(len(arr)):
        assert isinstance(arr[i], list)
        for j in range(len(arr[i])):
            assert isinstance(arr[i][j], np.ndarray)
            assert len(arr[i][j].shape) == 2
            if not color_each and i != j:
                arr[i][j] = np.tile(arr[i][j][:,:,None], (1, 1, 3))
                continue
            arr[i][j] = add_color_index(arr[i][j], stride, color=color)
    assert isinstance(arr[0][0], np.ndarray)
    return arr