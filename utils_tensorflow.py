import numpy as np
# import tensorflow as tf
import tensorflow.compat.v1 as tf
import tensorflow.contrib as tfc

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


def get_acts_rotate(model, layer, img, rot_angle=0.0, interpolation='NEAREST'):
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [224, 224, 3])
    rot_input = tfc.image.rotate(t_input, rot_angle,
                                        interpolation=interpolation)
    T = render.import_model(model, rot_input, rot_input)
    acts = T(layer).eval({t_input: img})[0]
    rot_img = rot_input.eval({t_input: img})
  return acts, rot_img


def get_acts_scale(model, layer, img, box, crop_size=[224, 224], interpolation='bilinear'):
  img = img[np.newaxis, :, :, :]
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [1, 224, 224, 3])
    t_boxes = tf.placeholder(tf.float32, [1, 4])
    t_box_ind = tf.placeholder(tf.int32, [1,])
    t_crop_size = tf.placeholder(tf.int32, [2,])

    box_ind = tf.constant([0], tf.int32)
    transformed_input = tf.image.crop_and_resize(t_input,
                                                 boxes=t_boxes,
                                                 box_ind=box_ind,
                                                 crop_size=crop_size,
                                                 method=interpolation)
    T = render.import_model(model, transformed_input, transformed_input)
    feed_dict = {
        t_input: img,
        t_boxes: box,
        t_crop_size: crop_size}
    acts = T(layer).eval(feed_dict)[0]
    transformed_img = transformed_input.eval(feed_dict)[0]
  return acts, transformed_img

