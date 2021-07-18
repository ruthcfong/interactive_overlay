import numpy as np
import PIL


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


def get_cossim_grids(acts):
  grids = [[np.hstack(np.hstack(cossim_grid(acts1, acts2)))
          for acts2 in acts] for acts1 in acts]
  return grids


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


def polar2degrees(x):
  return x*360/(2*math.pi)


def get_rot_coords(x, y, a, N=0):
    off = float((N-1)/2)
    x_ = (y - off) * np.sin(a) + (x - off) * np.cos(a)
    y_ = (y - off) * np.cos(a) - (x - off) * np.sin(a)
    return x_ + off, y_ + off


def get_scale_coords(x, y, N, curr_bbox, target_bbox, endpoint=True):
  offset = -1 if endpoint else 0

  v_global = y / float(N + offset) * (curr_bbox[2] - curr_bbox[0]) + curr_bbox[0]
  u_global = x / float(N + offset) * (curr_bbox[3] - curr_bbox[1]) + curr_bbox[1]

  # y_curr = (v_global - curr_bbox[0]) / (curr_bbox[2] - curr_bbox[0]) * float(N + offset)
  # x_curr =  (u_global - curr_bbox[1]) / (curr_bbox[3] - curr_bbox[1]) * float(N + offset)
  # assert(int(np.round(y_curr)) == y)
  # assert(int(np.round(x_curr)) == x)

  # if u_global < target_bbox[1] or u_global > target_bbox[3] or v_global < target_bbox[0] or v_global > target_bbox[2]:
  #  return np.nan, np.nan
  # else:
  y_target = (v_global - target_bbox[0]) / (target_bbox[2] - target_bbox[0]) * float(N + offset)
  x_target =  (u_global - target_bbox[1]) / (target_bbox[3] - target_bbox[1]) * float(N + offset)

  return x_target, y_target


def get_image_name(path):
  return os.path.splitext(os.path.basename(path))[0]


def create_dir_if_necessary(directory):
  if not os.path.exists(directory):
    os.makedirs(directory)


def save_img(object, url, domain=None, **kwargs):
    if isinstance(object, np.ndarray):
        normalized = _normalize_array(object, domain=domain)
        object = PIL.Image.fromarray(normalized)

    if isinstance(object, PIL.Image.Image):
        object.save(url, **kwargs)  # will infer format from url's url ext.
    else:
        raise ValueError("Can only save_img for numpy arrays or PIL.Images!")