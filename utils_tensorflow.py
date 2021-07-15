import numpy as np
import tensorflow as tf

import lucid.optvis.render as render


def get_acts(model, x, layer_name):
  """
  Returns activations at :param:`layer_name` in :param:`model` for
  input :param:`x`.

  Args:
    model (:class:`lucid.modelzoo.vision_base.Model`): Lucid model.
    x (:class:`numpy.ndarray`): numpy array representing input image for model.
    layer_name (str): name of TensorFlow layer from whic to collect activations.
  
  Returns:
    (:class:`numpy.ndarray`): intermediate activations .
  """
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [224, 224, 3])
    T = render.import_model(model, t_input, t_input)
    acts = T(layer_name).eval({t_input: x})[0]
  return acts