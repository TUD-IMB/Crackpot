import os
import cv2
import numpy as np
import keras
from keras import backend as K
from openpyxl import Workbook
from openpyxl.drawing.image import Image


def dice_coef(y_true, y_pred, smooth=1e-6):
	y_true_f = K.flatten(y_true)
	y_pred_f = K.flatten(y_pred)
	intersection = K.sum(y_true_f * y_pred_f)
	return (2. * intersection + smooth) / (K.sum(y_true_f) + K.sum(y_pred_f) + smooth)


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
	return intersection / union


class EdgeDetection:
	def __init__(self, model_path):
		self.model = keras.models.load_model(
			model_path,
			custom_objects={'dice_coef': dice_coef, 'dice_coef_loss': dice_coef_loss, 'IOU': IOU},
			compile=False
		)

	def resize_image(self, image, target_size=(256, 256)):
		return cv2.resize(image, target_size, interpolation=cv2.INTER_AREA)

	def detect_edges(self, image_path):
		image = cv2.imread(image_path)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = self.resize_image(image)
		image = image / 255.0
		image = np.expand_dims(image, axis=0)
		prediction = self.model.predict(image)
		return np.squeeze(prediction, axis=0)


def process_images_to_excel(input_dir, model_path, output_excel):

	edge_detector = EdgeDetection(model_path)

	wb = Workbook()
	ws = wb.active
	ws.title = "Image Results"

	ws.append(["Original Path", "Original Image", "Predicted Image"])

	ws.column_dimensions["A"].width = 30
	ws.column_dimensions["B"].width = 20
	ws.column_dimensions["C"].width = 20

	current_row = 2

	for root, dirs, files in os.walk(input_dir):
		for file in files:
			if file.endswith('.bmp'):
				file_path = os.path.join(root, file)
				relative_path = os.path.relpath(file_path, input_dir)

				prediction = edge_detector.detect_edges(file_path)

				pred_folder = os.path.join(root, 'pred')
				os.makedirs(pred_folder, exist_ok=True)

				predicted_image_path = f"{os.path.splitext(file)[0]}_predicted.png"
				predicted_image_full_path = os.path.join(pred_folder, predicted_image_path)

				cv2.imwrite(predicted_image_full_path, (prediction * 255).astype(np.uint8))

				ws.append([relative_path])

				original_image_obj = Image(file_path)
				original_image_obj.width, original_image_obj.height = 100, 100
				ws.add_image(original_image_obj, f"B{current_row}")

				predicted_image_obj = Image(predicted_image_full_path)
				predicted_image_obj.width, predicted_image_obj.height = 100, 100
				ws.add_image(predicted_image_obj, f"C{current_row}")

				ws.row_dimensions[current_row].height = 80

				current_row += 1

	wb.save(output_excel)
	print(f"Excel generated：{output_excel}")


if __name__ == '__main__':
	input_dir = "D:/IMB/Early_age_crack_development/original_images_sorted"
	model_path = "../resources/model/my_model.keras"
	output_excel = "D:/IMB/Early_age_crack_development/results_with_images.xlsx"

	process_images_to_excel(input_dir, model_path, output_excel)
