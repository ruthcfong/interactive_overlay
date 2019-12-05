import requests
from io import BytesIO
from PIL import Image

import torch
import torch.nn as nn
import numpy as np
from torchray.attribution.common import Probe, get_module


def load_image(url):
    """Return :class:`PIL.Image` loaded from url."""
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def get_device(gpu=None):
    """Return :class:`torch.device`; if :param:`gpu` is None; return CPU."""
    if gpu is None:
        return torch.device("cpu")
    assert isinstance(gpu, int)
    return torch.device(f"cuda:{gpu}")


def torch_to_numpy(x):
    """
    Convert :class:`torch.Tensor` in NCHW format to :class:`numpy.ndarray`
    in (N)HWC format (remove batch dimension if N = 1).
    """
    assert isinstance(x, torch.Tensor)
    if len(x.shape) == 3:
        x = x.unsqueeze(0)
    assert len(x.shape) == 4
    return np.transpose(x.cpu().data.numpy(), (0, 2, 3, 1)).squeeze()


def get_acts(model, x, layer_name, convert=False):
    """
    Return activations at :param:`layer_name` if :param:`model` for input
    :param:`x`.

    Args:
        model (:class:`nn.Module`): PyTorch model.
        x (:class:`torch.Tensor`): input tensor for model.
        layer_name (str): name of PyTorch module from which to collect
            activations.
        convert (bool, optional): If True, convert intermediate activations
            to numpy array using :func:`torch_to_numpy`. Default: `False`.

    Returns:
        (:class:`torch.Tensor` or :class:`np.ndarray`): intermediate
            activations.
    """
    assert isinstance(x, torch.Tensor)
    assert isinstance(model, nn.Module)

    # Get layer.
    layer = get_module(model, layer_name)
    assert layer is not None

    # Attach probe to layer to collect activations.
    probe = Probe(layer, "output")
    _ = model(x)

    # Return tensor.
    if not convert:
        return probe.data[0]

    # Return numpy array.
    return torch_to_numpy(probe.data[0])


def remove_transform(transform, text):
    """
    Remove a transform from a composition of transforms from
    :func:`torchvision.transforms.Compose` if the transform name includes
    :param:`text`.

    Args:
        transform (object): data transformation from
            :func:`torchvision.transforms.Compose`.
        text (str): substring search text used to identify transform(s)
            to remove.

        transform (object): data transformation with transform(s) whose name(s)
            include :param:`text` are removed.
    """
    assert hasattr(transform, "transforms")
    transform.transforms = [t for t in transform.transforms
                            if text not in str(t)]
    return transform


def remove_resize_transform(transform):
    """Remove transform(s) that include 'Resize' in their name(s)."""
    return remove_transform(transform, text="Resize")
