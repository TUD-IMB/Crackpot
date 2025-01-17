import os
import cv2
import numpy as np
import tensorflow as tf
import keras
from keras import backend as K
import matplotlib.pyplot as plt

def dice_coef(y_true, y_pred, smooth=1e-6):
	y_true_f = tf.cast(K.flatten(y_true), tf.float32)
	y_pred_f = tf.cast(K.flatten(y_pred), tf.float32)
	intersection = tf.reduce_sum(y_true_f * y_pred_f)
	return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
	return 1.0 - dice_coef(y_true, y_pred)


def IOU(y_true, y_pred):
	y_true = K.flatten(y_true)
	y_pred = K.flatten(y_pred)

	thresh = 0.5

	y_true = K.cast(K.greater_equal(y_true, thresh), 'float32')
	y_pred = K.cast(K.greater_equal(y_pred, thresh), 'float32')

	union = K.sum(K.maximum(y_true, y_pred)) + K.epsilon()
	intersection = K.sum(K.minimum(y_true, y_pred)) + K.epsilon()

	iou = intersection / union

	return iou


# model_path = '../resources/model/my_model.keras'
# model = keras.models.load_model(
# 	model_path,
# 	custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss, 'IOU': IOU},
# 	compile=False
# )
# # model.summary()
#
# image_path = "../resources/4.png"
# image = cv2.imread(image_path)
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# image = cv2.resize(image, (256, 256))
#
# image = image / 255.0
# image = np.expand_dims(image, axis=0)
#
# prediction = model.predict(image)
# predicted_mask = np.squeeze(prediction, axis=0)
#
# plt.imshow(np.squeeze(predicted_mask, axis=-1), cmap="gray")
# plt.axis("off")
# plt.show()


class EdgeDetection:
	def __init__(self):
		current_file_dir = os.path.dirname(os.path.abspath(__file__))
		model_path = os.path.join(current_file_dir, '../resources/model/my_model.keras')

		self.model = keras.models.load_model(
			model_path,
			custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss, 'IOU': IOU},
			compile=False
		)

	def resize_back(self, image, original_size):
		original_width, original_height = original_size
		restored_image = cv2.resize(image, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
		return restored_image

	def detect_edges(self, image_path):
		image = cv2.imread(image_path)
		original_size = (image.shape[1], image.shape[0])
		print(original_size)

		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)
		image = image / 255.0
		image = np.expand_dims(image, axis=0)

		prediction = self.model.predict(image)
		predicted_mask = np.squeeze(prediction, axis=0)

		resize_back_mask = self.resize_back(predicted_mask, original_size)

		return resize_back_mask