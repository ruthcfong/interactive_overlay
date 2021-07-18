"""
Experimental code - not thoroughly tested.
"""

import numpy as np
import tensorflow.compat.v1 as tf
import tensorflow.contrib as tfc
import tensorflow_probability as tfp


dog_cat_path = "https://raw.githubusercontent.com/ruthcfong/interactive_overlay/master/images/dog_cat.jpeg"


def get_acts_contrast(model, layer, img, contrast_factor):
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [224, 224, 3])
    transformed_input = tf.image.adjust_contrast(t_input, contrast_factor=contrast_factor)
    T = render.import_model(model, transformed_input, transformed_input)
    acts = T(layer).eval({t_input: img})[0]
    transformed_img = transformed_input.eval({t_input: img})
  return acts, transformed_img


def get_acts_brightness(model, layer, img, delta):
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [224, 224, 3])
    transformed_input = tf.image.adjust_brightness(t_input, delta=delta)
    T = render.import_model(model, transformed_input, transformed_input)
    acts = T(layer).eval({t_input: img})[0]
    transformed_img = transformed_input.eval({t_input: img})
  return acts, transformed_img


def gaussian_kernel(size, sigma, mu=0.0):
    """Makes 2D gaussian Kernel for convolution."""
    d = tfp.distributions.Normal(mu, sigma)

    vals = d.prob(tf.range(start = -size, limit = size + 1, dtype = tf.float32))

    gauss_kernel = tf.einsum('i,j->ij',
                                  vals,
                                  vals)

    return gauss_kernel / tf.reduce_sum(gauss_kernel)


def get_acts_blur(model, layer, img, blur_sigma, blur_size):
  img = img[np.newaxis, :, :, :]
  with tf.Graph().as_default(), tf.Session():
    t_input = tf.placeholder(tf.float32, [1, 224, 224, 3])
    if blur_sigma == 0.:
      blur_input = t_input
    else:
      gauss_kernel = gaussian_kernel(blur_size, blur_sigma)
      gauss_kernel = tf.tile(gauss_kernel[:, :, tf.newaxis, tf.newaxis], (1, 1, 3, 1))
      # gauss_kernel = tf.tile(gauss_kernel[:, :, tf.newaxis, tf.newaxis], (1, 1, 3, 3))
      blur_input = tf.nn.depthwise_conv2d(t_input, gauss_kernel, strides=[1, 1, 1, 1], padding="SAME")
    T = render.import_model(model, blur_input, blur_input)
    acts = T(layer).eval({t_input: img})[0]
    blur_img = blur_input.eval({t_input: img})
  return acts, blur_img


def vis_multi_blur(model, img_path=dog_cat_path, num_imgs=8, layer="mixed4d", blur_size=11, max_blur_sigma=None, save_results=False):
    vis_multi_transform(model=model,
                        transform_name="blur",
                        img_path=img_path,
                        num_imgs=num_imgs,
                        layer=layer,
                        max_value=max_blur_sigma,
                        blur_size=blur_size,
                        save_results=save_results)


def vis_multi_brightness(model, img_path=dog_cat_path, num_imgs=8, layer="mixed4d"):
  vis_multi_transform(model=model,
                      transform_name="brightness",
                      img_path=img_path,
                      num_imgs=num_imgs,
                      layer=layer)