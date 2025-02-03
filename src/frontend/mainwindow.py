import sys
import cv2
import numpy as np
from PySide2.QtCore import Qt, QSize, QEvent, QPoint
from PySide2.QtGui import QPixmap, QIcon, QImage, QPainter, QColor, QPen
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget, QSlider
from skimage.measure import regionprops,label

from backend.edgedetection import EdgeDetection
from backend.skeletonprocessor import SkeletonProcessor
from frontend.progressmanager import ProgressManager
from frontend.ui.uimain import Ui_MainWindow
from skimage.morphology import skeletonize


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
		self.skeleton_results = {}
		self.skeleton_processor = SkeletonProcessor()

		self.ui.listWidget.setViewMode(QListWidget.IconMode)
		self.ui.listWidget.setSpacing(10)
		self.ui.listWidget.setResizeMode(QListWidget.Adjust)

		self.ui.listWidget.itemClicked.connect(self.display_large_image)
		self.ui.previousFigButton.clicked.connect(self.show_previous_image)
		self.ui.nextFigButton.clicked.connect(self.show_next_image)

		self.resize(2000, 1600)
		self.edge_detector = None

		self.progress_manager = ProgressManager(
			buttons=[
				self.ui.uploadProcessButton,
				self.ui.detectProcessButton,
				self.ui.editProcessButton,
				self.ui.selectProcessButton,
				self.ui.exportProcessButton
			],
			lines=[self.ui.line1, self.ui.line2, self.ui.line3, self.ui.line4]
		)
		self.ui.uploadProcessButton.clicked.connect(lambda: self.set_stage(0))
		self.ui.detectProcessButton.clicked.connect(lambda: self.set_stage(1))
		self.ui.editProcessButton.clicked.connect(lambda: self.set_stage(2))
		self.ui.selectProcessButton.clicked.connect(lambda: self.set_stage(3))
		self.ui.exportProcessButton.clicked.connect(lambda: self.set_stage(4))

		self.ui.zoomInButton.clicked.connect(lambda: self.zoom_image(zoom_in=True))
		self.ui.zoomOutButton.clicked.connect(lambda: self.zoom_image(zoom_in=False))

		self.drawing = False
		self.last_point = QPoint()
		self.brush_color = QColor(255, 255, 255)
		self.brush_size = 5
		self.pen_cap_style = Qt.RoundCap
		self.image = None

		self.init_stacked_widget()
		self.init_image_label()

		self.adjusting_node = None
		self.creating_node = None
		self.dragged_node = None

	def init_stacked_widget(self):
		self.ui.stackedWidget.setCurrentIndex(self.progress_stage)
		self.ui.nextButton0.clicked.connect(lambda: self.set_stage(1))
		# self.ui.nextButton1.clicked.connect(lambda: self.set_stage(2))
		self.ui.nextButton2.clicked.connect(lambda: self.set_stage(3))
		self.ui.nextButton3.clicked.connect(lambda: self.set_stage(4))
		self.ui.nextButton4.clicked.connect(lambda: self.set_stage(0))

		# upload image stage
		self.ui.plusButton.clicked.connect(self.upload_figures)

		# model detection stage
		self.ui.runModelButton.clicked.connect(self.run_model_detection)

		# skeleton select stage
		self.ui.skeletonButton.clicked.connect(self.apply_skeletonization)
		self.ui.cleanBranchButton.clicked.connect(self.clean_skeleton_branches)

		# edit stage
		self.ui.addButton.clicked.connect(self.activate_add_mode)
		self.ui.deleteButton.clicked.connect(self.activate_delete_mode)
		self.ui.penSizeSlider.setRange(1, 50)
		self.ui.penSizeSlider.setValue(10)
		self.ui.penSizeSlider.setTickInterval(10)
		self.ui.penSizeSlider.setTickPosition(QSlider.TicksBelow)
		self.ui.penSizeSlider.valueChanged.connect(self.update_brush_size)

		self.ui.penShapeComboBox.currentTextChanged.connect(self.update_pen_shape)

		self.ui.opacitySlider.setRange(0, 100)
		self.ui.opacitySlider.setValue(50)
		self.ui.opacitySlider.setTickInterval(10)
		self.ui.opacitySlider.valueChanged.connect(self.refresh_display_image)

		self.ui.addNodeButton.clicked.connect(self.toggle_add_node_mode)
		self.ui.adjustNodeButton.clicked.connect(self.toggle_adjust_node_mode)

	def toggle_add_node_mode(self):
		if self.ui.addNodeButton.isChecked():
			self.creating_node = True
			self.adjusting_node = False
			self.ui.adjustNodeButton.setChecked(False)
		else:
			self.creating_node = False

	def toggle_adjust_node_mode(self):
		if self.ui.adjustNodeButton.isChecked():
			self.adjusting_node = True
			self.creating_node = False
			self.ui.addNodeButton.setChecked(False)
		else:
			self.adjusting_node = False

	def init_image_label(self):
		self.ui.imageLabel.setMouseTracking(True)
		self.ui.imageLabel.installEventFilter(self)

	def apply_skeletonization(self):
		if not self.prediction_results or len(self.prediction_results) == 0:
			return

		if not hasattr(self, "skeleton_results"):
			self.skeleton_results = {}
		else:
			self.skeleton_results.clear()

		for image_path, prediction in self.prediction_results.items():
			if prediction is None:
				continue
			skeleton = skeletonize(prediction).astype(np.uint8)

			branch_points = self.skeleton_processor.find_branch_points(skeleton)
			end_points = self.skeleton_processor.find_end_points(skeleton)

			self.skeleton_results[image_path] = {
				"skeleton": skeleton,
				"branch_points": branch_points,
				"end_points": end_points,
				"longest_path": None,
				"selected_points": []
			}

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

		self.skeleton_processor.skeletons = self.skeleton_results

	def clean_skeleton_branches(self):
		if not hasattr(self, "skeleton_results") or not self.skeleton_results:
			return

		for image_path, skeleton_data in self.skeleton_results.items():
			skeleton = skeleton_data.get("skeleton")
			if skeleton is None:
				continue

			main_endpoints = self.skeleton_processor.find_main_endpoints(skeleton)
			clean_skeleton = self.skeleton_processor.remove_small_branches(
				skeleton, max_branch_length=50, main_endpoints=main_endpoints
			)
			# clean_skeleton = self.skeleton_processor.extract_main_skeleton(skeleton)

			longest_path = self.get_longest_skeleton(clean_skeleton)
			branch_points = self.skeleton_processor.find_branch_points(clean_skeleton)
			end_points = self.skeleton_processor.find_end_points(clean_skeleton)

			self.skeleton_results[image_path] = {
				"skeleton": clean_skeleton,
				"branch_points": branch_poinats,
				"end_points": end_points,
				"longest_path": longest_path,
				"selected_points": []
			}

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

		self.skeleton_processor.skeletons = self.skeleton_results

	def get_longest_skeleton(self, skeleton):

		labeled_skeleton = label(skeleton, connectivity=2)

		longest_path = []
		max_length = 0

		for region in regionprops(labeled_skeleton):
			coords = region.coords
			length = len(coords)

			if length > max_length:
				max_length = length
				longest_path = coords
		return longest_path

	# ------------------------ Event Handling ----------------------------------------------------------------------
	def eventFilter(self, source, event):
		if source != self.ui.imageLabel:
			return super().eventFilter(source, event)

		if self.progress_stage == 2:
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

		elif self.progress_stage == 3:
			if self.creating_node and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
				clicked_pos = event.pos()
				if self.image:
					selected_node = self.create_node(clicked_pos)
					if selected_node:
						self.dragged_node = selected_node

			elif self.adjusting_node and event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
				clicked_pos = event.pos()
				skeleton_data = self.skeleton_results.get(self.current_image_path)

				if skeleton_data:
					selected_node = self.get_clicked_node(clicked_pos)
					if selected_node:
						skeleton_data["selected_points"] = [selected_node]
						self.refresh_display_image()
						self.dragged_node = selected_node

			elif self.adjusting_node and event.type() == QEvent.MouseMove and self.dragged_node:
				new_pos = event.pos()
				skeleton_data = self.skeleton_results.get(self.current_image_path)
				# todo: drag node to new pos and refresh skeleton path

		return super().eventFilter(source, event)

	def move_node(self, old_pos, new_pos):
		return

	def create_node(self, clicked_pos):
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			return None

		skeleton = skeleton_data["skeleton"]
		branch_points = skeleton_data["branch_points"]

		if branch_points is None:
			branch_points = np.zeros_like(skeleton)

		label_size = self.ui.imageLabel.size()
		skeleton_shape = skeleton.shape

		scale = min(label_size.width() / skeleton_shape[1], label_size.height() / skeleton_shape[0])
		display_width = scale * skeleton_shape[1]
		display_height = scale * skeleton_shape[0]

		x_offset = (label_size.width() - display_width) / 2
		y_offset = (label_size.height() - display_height) / 2

		img_x = (clicked_pos.x() - x_offset) / scale
		img_y = (clicked_pos.y() - y_offset) / scale

		skeleton_coords = np.argwhere(skeleton > 0)
		min_dist = float('inf')
		closest_point = None

		for node in skeleton_coords:
			node_x, node_y = node[1], node[0]
			dist = np.sqrt((img_x - node_x) ** 2 + (img_y - node_y) ** 2)
			if dist < 5 and dist < min_dist:
				min_dist = dist
				closest_point = (node_x, node_y)

		if closest_point is None:
			return None

		branch_points[closest_point[1], closest_point[0]] = 1
		skeleton_data["branch_points"] = branch_points

		self.refresh_display_image()

		return closest_point

	def get_clicked_node(self, position):
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			return None

		branch_points = np.argwhere(skeleton_data["branch_points"] > 0)
		end_points = np.argwhere(skeleton_data["end_points"] > 0)
		all_nodes = np.vstack((branch_points, end_points))

		label_size = self.ui.imageLabel.size()
		skeleton_shape = skeleton_data["skeleton"].shape

		scale = min(label_size.width() / skeleton_shape[1], label_size.height() / skeleton_shape[0])
		display_width = scale * skeleton_shape[1]
		display_height = scale * skeleton_shape[0]

		x_offset = (label_size.width() - display_width) / 2
		y_offset = (label_size.height() - display_height) / 2

		img_x = (position.x() - x_offset) / scale
		img_y = (position.y() - y_offset) / scale

		for node in all_nodes:
			node_x, node_y = node[1], node[0]
			if abs(img_x - node_x) < 5 and abs(img_y - node_y) < 5:
				return (node_x, node_y)
		return None

	def qimage_to_np(self, qimage: QImage):
		qimage = qimage.convertToFormat(QImage.Format_Grayscale8)
		width = qimage.width()
		height = qimage.height()
		ptr = qimage.bits()
		arr = np.array(ptr).reshape(height, width)
		return arr

	def resizeEvent(self, event):
		if self.current_image_path:
			self.refresh_display_image()
		super().resizeEvent(event)

# ------------------------ Drawing Functions ----------------------------------------------------------------------
	def draw_on_image(self, current_point):
		if self.image is None:
			return

		label_size = self.ui.imageLabel.size()
		image_size = self.image.size()

		scale = min(label_size.width() / image_size.width(), label_size.height() / image_size.height())

		display_width = scale * image_size.width()
		display_height = scale * image_size.height()

		x_offset = (label_size.width() - display_width) / 2
		y_offset = (label_size.height() - display_height) / 2

		x1 = (self.last_point.x() - x_offset) / scale
		y1 = (self.last_point.y() - y_offset) / scale
		x2 = (current_point.x() - x_offset) / scale
		y2 = (current_point.y() - y_offset) / scale

		if not (0 <= x1 < image_size.width() and 0 <= y1 < image_size.height()):
			return
		if not (0 <= x2 < image_size.width() and 0 <= y2 < image_size.height()):
			return

		painter = QPainter(self.image)
		pen = QPen(self.brush_color)
		pen.setWidth(self.brush_size)
		pen.setCapStyle(self.pen_cap_style)
		painter.setPen(pen)

		painter.drawLine(int(x1), int(y1), int(x2), int(y2))
		painter.end()

		self.last_point = current_point

		self.refresh_display_after_draw()

	def activate_add_mode(self):
		self.brush_color = QColor(255, 255, 255)

	def activate_delete_mode(self):
		self.brush_color = QColor(0, 0, 0)

	def update_brush_size(self, value):
		self.brush_size = value

	def zoom_image(self, zoom_in=True):
		if not self.ui.imageLabel.pixmap():
			return

		scale_factor = 1.1 if zoom_in else 1 / 1.1

		original_pixmap = self.ui.imageLabel.pixmap()
		current_width = original_pixmap.width()
		current_height = original_pixmap.height()
		new_width = int(current_width * scale_factor)
		new_height = int(current_height * scale_factor)

		if new_width < 50 or new_height < 50:
			return
		if new_width > 5000 or new_height > 5000:
			return

		scaled_pixmap = original_pixmap.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.ui.imageLabel.adjustSize()

	def update_pen_shape(self, shape):
		if shape == "Round":
			self.pen_cap_style = Qt.RoundCap
		elif shape == "Square":
			self.pen_cap_style = Qt.SquareCap

	# ------------------------ Image Display ----------------------------------------------------------------------
	def upload_figures(self):
		image_paths, _ = QFileDialog.getOpenFileNames(
			self, "Select Images", "", "Images (*.png *.jpg *.jpeg *.bmp)"
		)

		if not image_paths:
			return

		for image_path in image_paths:
			pixmap = QPixmap(image_path)
			if not pixmap.isNull():
				# predicted_mask = self.edge_detector.detect_edges(image_path)
				# self.prediction_results[image_path] = predicted_mask
				self.prediction_results[image_path] = None

				item = QListWidgetItem()
				item.setIcon(QIcon(pixmap.scaled(100, 100, aspectRatioMode=Qt.KeepAspectRatio)))
				item.setData(Qt.UserRole, image_path)
				self.ui.listWidget.addItem(item)

		if not self.ui.listWidget.currentItem() and self.ui.listWidget.count() > 0:
			self.ui.listWidget.setCurrentRow(0)
			self.display_large_image(self.ui.listWidget.currentItem())

	def run_model_detection(self):
		self.edge_detector = EdgeDetection()
		for file_name, prediction in self.prediction_results.items():
			if prediction is None:
				predicted_mask = self.edge_detector.detect_edges(file_name)
				self.prediction_results[file_name] = predicted_mask

		next_stage = self.progress_stage + 1
		self.set_stage(next_stage)

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

	def display_large_image(self, item):
		# Retrieve the file path from the clicked item's UserRole
		file_path = item.data(Qt.UserRole)
		if file_path:
			self.current_image_path = file_path
			self.refresh_display_image()

	def refresh_display_image(self):
		"""
		Update the QLabel display with the combined original image and prediction.
		"""
		if not self.current_image_path:
			return

		original_image = cv2.imread(self.current_image_path)
		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
		if original_image is None:
			return

		original_qimage = QImage(
			original_image.data, original_image.shape[1], original_image.shape[0],
			original_image.shape[1] * 3, QImage.Format_RGB888
		)
		original_pixmap = QPixmap.fromImage(original_qimage)
		if original_pixmap.isNull():
			return

		if self.progress_stage in [0, 1]:
			self.display_original_image(original_pixmap)
		elif self.progress_stage == 2:
			self.display_prediction_overlay(original_pixmap)
		elif self.progress_stage == 3:
			self.display_skeleton_overlay(original_image)

	def display_original_image(self, original_pixmap):
		"""Display the original image scaled to fit the label."""
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = original_pixmap.scaled(
			label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.image = None

	def display_prediction_overlay(self, original_pixmap):
		"""Display the original image with the prediction overlay."""
		prediction = self.prediction_results.get(self.current_image_path)
		if prediction is None:
			return

		if len(prediction.shape) == 3 and prediction.shape[-1] == 1:
			prediction = np.squeeze(prediction, axis=-1)
		elif len(prediction.shape) != 2:
			raise ValueError(f"Unexpected prediction shape: {prediction.shape}")

		prediction = (prediction * 255).astype(np.uint8)
		prediction_qimage = QImage(
			prediction, prediction.shape[1], prediction.shape[0],
			prediction.shape[1], QImage.Format_Grayscale8
		)

		prediction_pixmap = QPixmap.fromImage(prediction_qimage)
		if prediction_pixmap.isNull():
			return

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

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)

		self.image = prediction_qimage.copy()

	def display_skeleton_overlay(self, original_image):
		"""Display the original image with skeleton overlay."""
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			print("No skeletonization result found.")
			return

		skeleton = skeleton_data["skeleton"]
		branch_points = skeleton_data.get("branch_points", None)
		end_points = skeleton_data.get("end_points", None)
		longest_path = skeleton_data.get("longest_path", [])
		selected_points = skeleton_data.get("selected_points", [])

		overlay_image = original_image.copy()
		skeleton_coords = np.where(skeleton == 1)
		overlay_image[skeleton_coords[0], skeleton_coords[1]] = [255, 255, 0]

		if longest_path is not None and len(longest_path) > 0:
			for point in longest_path:
				overlay_image[point[0], point[1]] = [255, 0, 0]

		# if branch_points is not None and np.any(branch_points):
		# 	branch_coords = np.argwhere(branch_points > 0)
		# 	for coord in branch_coords:
		# 		point_tuple = (coord[1], coord[0])  # (x, y)
		# 		color = (0, 255, 0) if point_tuple in selected_points else (255, 255, 255)
		# 		cv2.circle(overlay_image, point_tuple, radius=5, color=color, thickness=2)

		if end_points is not None and np.any(end_points):
			end_coords = np.argwhere(end_points > 0)
			for coord in end_coords:
				point_tuple = (coord[1], coord[0])  # (x, y)
				color = (0, 255, 0) if point_tuple in selected_points else (255, 255, 255)
				cv2.circle(overlay_image, point_tuple, radius=5, color=color, thickness=2)

		overlay_qimage = QImage(
			overlay_image.data,
			overlay_image.shape[1],
			overlay_image.shape[0],
			overlay_image.shape[1] * 3,
			QImage.Format_RGB888
		)
		overlay_pixmap = QPixmap.fromImage(overlay_qimage)

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = overlay_pixmap.scaled(
			label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)

	def refresh_display_after_draw(self):
		if not self.current_image_path or self.image is None:
			return

		original_image = cv2.imread(self.current_image_path)
		if original_image is None:
			return

		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
		original_qimage = QImage(
			original_image.data, original_image.shape[1], original_image.shape[0],
			original_image.shape[1] * 3, QImage.Format_RGB888
		)
		original_pixmap = QPixmap.fromImage(original_qimage)
		if original_pixmap.isNull():
			return

		prediction_pixmap = QPixmap.fromImage(self.image)

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

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)
	# ------------------------ Progress Management ----------------------------------------------------------------------

	def set_stage(self, stage):

		if stage < 0 or stage > 4:
			return
		self.progress_stage = stage
		self.ui.stackedWidget.setCurrentIndex(stage)
		self.progress_manager.update_progress(self.progress_stage)

		# Perform actions based on the stage
		if self.progress_stage == 0:
			print("Upload stage")
		elif self.progress_stage == 1:
			print("Model detection stage")
		elif self.progress_stage == 2:
			print("Edit stage")
		elif self.progress_stage == 3:
			print("Select skeleton stage")
		elif self.progress_stage == 4:
			print("File export stage")

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

	# ------------------------ Others ----------------------------------------------------------------------

	def show_previous_image(self):
		current_row = self.ui.listWidget.currentRow()
		if current_row > 0:
			self.ui.listWidget.setCurrentRow(current_row - 1)
			self.display_large_image(self.ui.listWidget.currentItem())

	def show_next_image(self):
		current_row = self.ui.listWidget.currentRow()
		if current_row < self.ui.listWidget.count() - 1:
			self.ui.listWidget.setCurrentRow(current_row + 1)
			self.display_large_image(self.ui.listWidget.currentItem())

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