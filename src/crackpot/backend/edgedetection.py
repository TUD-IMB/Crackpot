import importlib.util
import os
import cv2
import numpy as np

from crackpot.utils.utils import resource_path

MISSING_BACKEND_HINT = (
	"Automatic crack detection is unavailable because TensorFlow is not "
	"installed. Install it with 'pip install \"crackpot[tensorflow]\"', or keep "
	"working without automatic detection by selecting 'None' as the detection "
	"method."
)

BROKEN_BACKEND_HINT = (
	"TensorFlow is installed, but the detection backend could not be loaded. On "
	"Windows this usually means the Microsoft Visual C++ Redistributable that "
	"TensorFlow needs is missing. Reinstall the backend with 'pip install "
	"--force-reinstall \"crackpot[tensorflow]\"', or select 'None' as the "
	"detection method to continue without automatic detection."
)


def model_path():
	r"""
	Locate the pre-trained detection model shipped with the package.

	\return (str): The path to the model file, or None if it is not present.
	"""
	path = resource_path('resources/model/my_model.keras')
	return path if os.path.exists(path) else None


def is_detection_available():
	r"""
	Check whether automatic crack detection can be used.

	TensorFlow is only looked up, not imported, so that starting the application
	does not pay for loading it. The model file ships with the package, but is
	checked as well, because a standalone build may leave it out.

	\return (bool): True if detection is possible.
	"""
	for name in ("tensorflow", "keras"):
		try:
			if importlib.util.find_spec(name) is None:
				return False
		except (ImportError, ValueError):
			# A stubbed or half-initialized module has no usable __spec__.
			return False
	return model_path() is not None


def dice_coef(y_true, y_pred, smooth=1e-6):
	import tensorflow as tf
	from keras import backend as K

	y_true_f = tf.cast(K.flatten(y_true), tf.float32)
	y_pred_f = tf.cast(K.flatten(y_pred), tf.float32)
	intersection = tf.reduce_sum(y_true_f * y_pred_f)
	return (2. * intersection + smooth) / (tf.reduce_sum(y_true_f) + tf.reduce_sum(y_pred_f) + smooth)


def dice_coef_loss(y_true, y_pred):
	return 1.0 - dice_coef(y_true, y_pred)


def IOU(y_true, y_pred):
	from keras import backend as K

	y_true = K.flatten(y_true)
	y_pred = K.flatten(y_pred)

	binarization_threshold = 0.5

	y_true = K.cast(K.greater_equal(y_true, binarization_threshold), 'float32')
	y_pred = K.cast(K.greater_equal(y_pred, binarization_threshold), 'float32')

	union = K.sum(K.maximum(y_true, y_pred)) + K.epsilon()
	intersection = K.sum(K.minimum(y_true, y_pred)) + K.epsilon()

	iou = intersection / union

	return iou


class EdgeDetection:
	r"""
	Load a pre-trained edge detection model to detect crack edges in images
	and resize the results back to the original image size.
	"""
	def __init__(self):
		r"""
		Initialize the EdgeDetection class and load the pre-trained model.

		Raises a RuntimeError if TensorFlow is missing, or if the installed
		backend cannot be loaded. Use is_detection_available() to check for the
		former beforehand.
		"""
		if not is_detection_available():
			raise RuntimeError(MISSING_BACKEND_HINT)

		# So far only the presence of the packages was checked. Importing them can
		# still fail on an incomplete installation.
		try:
			import keras

			self.model = keras.models.load_model(
				model_path(),
				custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss, 'IOU': IOU},
				compile=False
			)
		except Exception as error:
			raise RuntimeError("%s\n\n%s" % (BROKEN_BACKEND_HINT, error)) from error

	def resize_back(self, image, original_size):
		r"""
		Resize the predicted mask back to the original image size.

		\param image: The predicted mask.
		\param original_size: Tuple (width, height) of the original image.
		\return: Resized mask matching the original image dimensions.
		"""
		original_width, original_height = original_size
		restored_image = cv2.resize(image, (original_width, original_height), interpolation=cv2.INTER_NEAREST)
		return restored_image

	def detect_edges(self, image_path):
		r"""
		Preprocess the image by resizing and normalizing, apply the model for prediction,
		and resize the predicted mask back to the original size.

		\param image_path: Path to the input image file.
		\return: Resized predicted edge mask.
		"""
		image = cv2.imread(image_path)
		original_size = (image.shape[1], image.shape[0])

		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_AREA)
		image = image / 255.0
		image = np.expand_dims(image, axis=0)

		# The progress bar of the default verbosity writes to sys.stdout, which is
		# unavailable when the application is started without a console.
		prediction = self.model.predict(image, verbose=0)
		predicted_mask = np.squeeze(prediction, axis=0)

		return self.resize_back(predicted_mask, original_size)
