import sys
import cv2
import numpy as np
from PySide2.QtCore import QFile, Qt, QSize, QEvent, QPoint
from PySide2.QtGui import QPixmap, QIcon, QImage, QPainter, QColor, QPen, qRgb
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget, QSlider, \
	QButtonGroup
from backend.edgedetection import EdgeDetection
from frontend.progressmanager import ProgressManager
from frontend.ui.uimain import Ui_MainWindow


class MainWindow(QMainWindow):
	r"""
	Main User Interface for the application.
	"""

	def __init__(self):
		super().__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.progress_stage = 0
		self.current_image_path = None
		self.prediction_results = {}

		self.ui.listWidget.setViewMode(QListWidget.IconMode)
		self.ui.listWidget.setSpacing(10)
		self.ui.listWidget.setResizeMode(QListWidget.Adjust)

		self.ui.plusButton.clicked.connect(self.upload_figures)
		self.ui.listWidget.itemClicked.connect(self.display_large_image)

		self.resize(2000, 1500)
		self.edge_detector = EdgeDetection()

		self.ui.opacitySlider.setRange(0, 100)
		self.ui.opacitySlider.setValue(50)
		self.ui.opacitySlider.setTickInterval(10)
		self.ui.opacitySlider.valueChanged.connect(self.upload_and_display_image)

		self.progress_manager = ProgressManager(
			buttons=[
				self.ui.uploadProcessButton,
				self.ui.editProcessButton,
				self.ui.selectProcessButton,
				self.ui.fileProcessButton
			],
			lines=[self.ui.line1, self.ui.line2, self.ui.line3]
		)

		self.drawing = False
		self.last_point = QPoint()
		self.brush_color = QColor(255, 255, 255)
		self.brush_size = 2
		self.image = None

		self.init_stacked_widget()
		self.init_image_label()

	def init_stacked_widget(self):
		self.ui.nextButton0.clicked.connect(lambda: self.set_stage(1))
		self.ui.nextButton1.clicked.connect(lambda: self.set_stage(2))
		self.ui.nextButton2.clicked.connect(lambda: self.set_stage(3))
		self.ui.nextButton3.clicked.connect(lambda: self.set_stage(0))
		self.ui.stackedWidget.setCurrentIndex(self.progress_stage)

		self.button_group = QButtonGroup(self)
		self.button_group.setExclusive(True)

		self.button_group.addButton(self.ui.addButton)
		self.button_group.addButton(self.ui.deleteButton)

		self.ui.addButton.clicked.connect(self.activate_add_mode)
		self.ui.deleteButton.clicked.connect(self.activate_delete_mode)

	def init_image_label(self):
		self.ui.imageLabel.setMouseTracking(True)
		self.ui.imageLabel.installEventFilter(self)

# ------------------------ Event Handling ----------------------------------------------------------------------
	def eventFilter(self, source, event):
		if source == self.ui.imageLabel:
			if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
				self.drawing = True
				self.last_point = event.pos()

			elif event.type() == QEvent.MouseMove and self.drawing:
				self.draw_on_image(event.pos())

			elif event.type() == QEvent.MouseButtonRelease and event.button() == Qt.LeftButton:
				self.drawing = False

				if self.image is not None and self.current_image_path is not None:
					updated_array = self.qimage_to_np(self.image)
					updated_array = updated_array.astype(np.float32) / 255.0
					self.prediction_results[self.current_image_path] = updated_array

		return super().eventFilter(source, event)

	def qimage_to_np(self, qimage: QImage) -> np.ndarray:
		qimage = qimage.convertToFormat(QImage.Format_Grayscale8)
		width = qimage.width()
		height = qimage.height()
		ptr = qimage.bits()
		arr = np.array(ptr).reshape(height, width)
		return arr

	def resizeEvent(self, event):
		if self.current_image_path:
			self.upload_and_display_image()
		super().resizeEvent(event)

# ------------------------ Drawing Functions ----------------------------------------------------------------------

	def draw_on_image(self, current_point):
		"""
		在 self.image（灰度 QImage，即当前 prediction）上用画笔(白/黑)画线。
		"""
		if self.image is None:
			return

		painter = QPainter(self.image)
		pen = QPen(self.brush_color)  # 白笔 => (255,255,255)，黑笔 => (0,0,0)
		pen.setWidth(self.brush_size)
		painter.setPen(pen)

		label_size = self.ui.imageLabel.size()
		image_size = self.image.size()
		sx = image_size.width() / label_size.width()
		sy = image_size.height() / label_size.height()
		x1, y1 = int(self.last_point.x() * sx), int(self.last_point.y() * sy)
		x2, y2 = int(current_point.x() * sx), int(current_point.y() * sy)

		painter.drawLine(x1, y1, x2, y2)
		painter.end()

		self.last_point = current_point

		self.update_label()

	def activate_add_mode(self):
		self.brush_color = QColor(255, 255, 255)

	def activate_delete_mode(self):
		self.brush_color = QColor(0, 0, 0)

	def update_label(self):
		if self.image is not None:
			pixmap = QPixmap.fromImage(self.image)
			self.ui.imageLabel.setPixmap(pixmap.scaled(
				self.ui.imageLabel.size(),
				Qt.KeepAspectRatio,
				Qt.SmoothTransformation,
			))

	# ------------------------ Image Display ----------------------------------------------------------------------
	def upload_figures(self):
		file_names, _ = QFileDialog.getOpenFileNames(
			self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp)"
		)

		if not file_names:
			return

		for file_name in file_names:
			pixmap = QPixmap(file_name)
			if not pixmap.isNull():
				predicted_mask = self.edge_detector.detect_edges(file_name)
				self.prediction_results[file_name] = predicted_mask

				item = QListWidgetItem()
				item.setIcon(QIcon(pixmap.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)))
				item.setData(Qt.UserRole, file_name)
				self.ui.listWidget.addItem(item)

	def display_large_image(self, item):
		# Retrieve the file path from the clicked item's UserRole
		file_path = item.data(Qt.UserRole)
		if file_path:
			self.current_image_path = file_path
			self.upload_and_display_image()

	def upload_and_display_image(self):
		"""
		Update the QLabel display with the combined original image and prediction.
		"""
		if not self.current_image_path:
			return

		# Load the original image
		original_image = cv2.imread(self.current_image_path)
		if original_image is None:
			return

		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
		resized_image = cv2.resize(original_image, (256, 256), interpolation=cv2.INTER_AREA)

		# Convert to QPixmap
		resized_image_bgr = cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR)
		resized_image_qimage = QImage(
			resized_image_bgr.data, resized_image_bgr.shape[1], resized_image_bgr.shape[0],
			resized_image_bgr.shape[1] * 3, QImage.Format_BGR888
		)
		original_pixmap = QPixmap.fromImage(resized_image_qimage)

		if original_pixmap.isNull():
			return

		# Get the prediction result
		prediction = self.prediction_results.get(self.current_image_path)
		if prediction is None:
			return

		# Ensure the prediction is 2D
		if len(prediction.shape) == 3 and prediction.shape[-1] == 1:
			prediction = np.squeeze(prediction, axis=-1)  # Remove the last dimension
		elif len(prediction.shape) != 2:
			raise ValueError(f"Unexpected prediction shape: {prediction.shape}")

		# Convert prediction to QImage
		prediction = (prediction * 255).astype(np.uint8)  # 将数据从 [0, 1] 转为 [0, 255]
		prediction_qimage = QImage(prediction, prediction.shape[1], prediction.shape[0],
								   prediction.shape[1], QImage.Format_Grayscale8)

		# Convert the prediction to QPixmap
		prediction_pixmap = QPixmap.fromImage(prediction_qimage)
		if prediction_pixmap.isNull():
			return

		# Combine the original image and the prediction
		combined_pixmap = QPixmap(original_pixmap.size())
		combined_pixmap.fill(Qt.transparent)
		painter = QPainter(combined_pixmap)
		painter.setOpacity(1.0)
		painter.drawPixmap(0, 0, original_pixmap)
		opacity = self.ui.opacitySlider.value() / 100.0
		painter.setOpacity(opacity)
		painter.drawPixmap(0, 0, prediction_pixmap.scaled(
			original_pixmap.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
		))
		painter.end()

		# Display the combined image
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)

		# Initialize the drawing layer with prediction
		self.image = prediction_qimage.copy()

	# ------------------------ Progress Management ----------------------------------------------------------------------

	def set_stage(self, stage):

		if stage < 0 or stage > 3:
			return
		self.progress_stage = stage
		self.ui.stackedWidget.setCurrentIndex(stage)
		self.progress_manager.update_progress(self.progress_stage)

		# Perform actions based on the stage
		if self.progress_stage == 0:
			print("Upload stage")
		elif self.progress_stage == 1:
			print("Edit stage")
		elif self.progress_stage == 2:
			print("Select stage")
		elif self.progress_stage == 3:
			print("File export stage")

# ------------------------ Others ----------------------------------------------------------------------



	# def update_image_label(self):
	# 	if not self.current_image_path:
	# 		return
	#
	# 	original_image = cv2.imread(self.current_image_path)
	# 	if original_image is None:
	# 		return
	#
	# 	original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
	#
	# 	resized_image = cv2.resize(original_image, (256, 256), interpolation=cv2.INTER_AREA)
	#
	# 	resized_image_bgr = cv2.cvtColor(resized_image, cv2.COLOR_RGB2BGR)
	# 	height, width, _ = resized_image_bgr.shape
	# 	resized_image_qimage = QImage(
	# 		resized_image_bgr.data, width, height, width * 3, QImage.Format_BGR888
	# 	)
	# 	original_pixmap = QPixmap.fromImage(resized_image_qimage)
	#
	# 	if original_pixmap.isNull():
	# 		return
	#
	# 	# Get the prediction result
	# 	prediction = self.prediction_results.get(self.current_image_path)
	# 	if prediction is None:
	# 		return
	#
	# 	# Handle prediction dimensions (ensure it is 2D)
	# 	if len(prediction.shape) == 3 and prediction.shape[-1] == 1:
	# 		prediction = np.squeeze(prediction, axis=-1)  # Remove the last dimension
	# 	elif len(prediction.shape) != 2:
	# 		raise ValueError(f"Unexpected prediction shape: {prediction.shape}")
	#
	# 	# Convert prediction to QImage
	# 	prediction = (prediction * 255).astype(np.uint8)
	# 	height, width = prediction.shape
	# 	prediction_qimage = QImage(prediction, width, height, width, QImage.Format_Grayscale8)
	#
	# 	# Convert the prediction to QPixmap
	# 	prediction_pixmap = QPixmap.fromImage(prediction_qimage)
	# 	if prediction_pixmap.isNull():
	# 		return
	#
	# 	# Combine the original image and the prediction
	# 	combined_pixmap = QPixmap(original_pixmap.size())
	# 	combined_pixmap.fill(Qt.transparent)
	#
	# 	painter = QPainter(combined_pixmap)
	# 	painter.setOpacity(1.0)
	# 	painter.drawPixmap(0, 0, original_pixmap)
	#
	# 	opacity = self.ui.opacitySlider.value() / 100.0
	# 	painter.setOpacity(opacity)  # 设置预测结果的透明度
	# 	painter.drawPixmap(0, 0, prediction_pixmap.scaled(
	# 		original_pixmap.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
	# 	))
	# 	painter.end()
	#
	# 	# Display the combined image
	# 	label_width = self.ui.imageLabel.width()
	# 	label_height = self.ui.imageLabel.height()
	#
	# 	scaled_pixmap = combined_pixmap.scaled(
	# 		label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
	# 	)
	# 	self.ui.imageLabel.setPixmap(scaled_pixmap)
	# 	self.ui.imageLabel.set_image(prediction)

	def show_and_check_config(self):
		self.show()


def main():
	r"""
	Initialize and run the application.
	"""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show_and_check_config()
	sys.exit(app.exec_())

#
# if __name__ == "__main__":
# 	main()