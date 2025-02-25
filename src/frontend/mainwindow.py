import os
import sys
import cv2
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QEvent, QPoint
from PySide6.QtGui import QPixmap, QIcon, QImage, QPainter, QColor, QPen, QCursor
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget, QSlider, \
	QMessageBox, QToolTip
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
		self.crack_results = {}
		self.skeleton_processor = SkeletonProcessor()

		self.ui.listWidget.setViewMode(QListWidget.ViewMode.IconMode)
		self.ui.listWidget.setSpacing(10)
		self.ui.listWidget.setResizeMode(QListWidget.ResizeMode.Adjust)
		# todo: multi selection
		# self.ui.listWidget.setSelectionMode(QAbstractItemView.MultiSelection)

		self.ui.listWidget.itemClicked.connect(self.display_large_image)
		self.ui.previousFigButton.clicked.connect(self.show_previous_image)
		self.ui.nextFigButton.clicked.connect(self.show_next_image)

		self.edge_detector = None

		self.progress_manager = ProgressManager(
			buttons=[
				self.ui.calibrationProcessButton,
				self.ui.uploadProcessButton,
				self.ui.detectProcessButton,
				self.ui.editProcessButton,
				self.ui.selectProcessButton,
				self.ui.exportProcessButton
			],
			lines=[self.ui.line0, self.ui.line1, self.ui.line2, self.ui.line3, self.ui.line4]
		)
		self.ui.calibrationProcessButton.clicked.connect(lambda: self.set_stage(0))
		self.ui.uploadProcessButton.clicked.connect(lambda: self.set_stage(1))
		self.ui.detectProcessButton.clicked.connect(lambda: self.set_stage(2))
		self.ui.editProcessButton.clicked.connect(lambda: self.set_stage(3))
		self.ui.selectProcessButton.clicked.connect(lambda: self.set_stage(4))
		self.ui.exportProcessButton.clicked.connect(lambda: self.set_stage(5))

		self.ui.zoomInButton.clicked.connect(lambda: self.zoom_image(zoom_in=True))
		self.ui.zoomOutButton.clicked.connect(lambda: self.zoom_image(zoom_in=False))
		self.ui.deleteImageButton.clicked.connect(self.delete_current_image)

		self.drawing = False
		self.last_point = QPoint()
		self.brush_color = QColor(255, 255, 255)
		self.brush_size = 10
		self.pen_cap_style = Qt.PenCapStyle.RoundCap
		self.image = None

		self.init_stacked_widget()
		self.init_image_label()

		self.deleting_node = None
		self.creating_node = None
		self.dragged_node = None

		self.resolution = None
		self.cali_image = None
		self.cali_points = []

		self.adjust_window_size()

	def adjust_window_size(self):
		screen = self.screen()
		screen_size = screen.availableGeometry()

		width = int(screen_size.width() * 0.7)
		height = int(screen_size.height() * 0.9)

		self.resize(width, height)

	def init_image_label(self):
		self.ui.imageLabel.setMouseTracking(True)
		self.ui.imageLabel.installEventFilter(self)

	def init_stacked_widget(self):
		self.ui.stackedWidget.setCurrentIndex(self.progress_stage)
		self.ui.nextButton0.clicked.connect(lambda: self.set_stage(1))
		self.ui.nextButton1.clicked.connect(lambda: self.set_stage(2))
		self.ui.nextButton2.clicked.connect(self.run_model_detection)
		self.ui.nextButton3.clicked.connect(lambda: self.set_stage(4))
		self.ui.nextButton4.clicked.connect(lambda: self.set_stage(5))
		self.ui.nextButton5.clicked.connect(self.reset_all_data)

		# calibration stage
		self.ui.caliUploadButton.clicked.connect(self.upload_calibration_image)
		self.ui.confirmButton.clicked.connect(self.confirm_resolution)
		self.ui.distanceLineEdit.textChanged.connect(self.update_resolution)
		self.ui.pixelLineEdit.textChanged.connect(self.update_resolution)

		# upload image stage
		self.ui.plusButton.clicked.connect(self.upload_figures)

		# model detection stage
		# self.ui.runModelButton.clicked.connect(self.run_model_detection)

		# skeleton select stage
		self.ui.skeletonButton.clicked.connect(self.apply_skeletonization)
		self.ui.cleanBranchButton.clicked.connect(self.clean_skeleton_branches)

		# edit stage
		self.ui.addButton.clicked.connect(self.activate_add_mode)
		self.ui.deleteButton.clicked.connect(self.activate_delete_mode)

		self.ui.penSizeSlider.setRange(1, 50)
		self.ui.penSizeSlider.setValue(10)
		self.ui.penSizeSlider.setTickInterval(10)
		self.ui.penSizeSlider.setTickPosition(QSlider.TickPosition.TicksBelow)
		self.ui.penSizeSlider.valueChanged.connect(self.update_brush_size)

		self.ui.penShapeComboBox.currentTextChanged.connect(self.update_pen_shape)

		self.ui.opacitySlider.setRange(0, 100)
		self.ui.opacitySlider.setValue(50)
		self.ui.opacitySlider.setTickInterval(10)
		self.ui.opacitySlider.valueChanged.connect(self.refresh_display_image)

		# skeleton stage
		self.ui.nodeAddButton.clicked.connect(self.toggle_add_node_mode)
		self.ui.nodeDeleteButton.clicked.connect(self.toggle_delete_node_mode)
		# self.ui.adjustNodeButton.clicked.connect(self.toggle_adjust_node_mode)
		self.ui.hintsButton.setVisible(False)
		self.ui.hintsLabel1.setVisible(False)
		self.ui.hintsLabel2.setVisible(False)
		self.ui.hintsLabel3.setVisible(False)

		# export stage
		self.ui.browseButton.clicked.connect(self.browse_export_path)
		self.ui.exportButton.clicked.connect(self.export_to_csv)

	# ------------------------ Calibration ----------------------------------------------------------------------
	def upload_calibration_image(self):
		cali_path, _ = QFileDialog.getOpenFileName(
			self, "Select a Calibration Picture", "", "Images (*.png *.jpg *.jpeg *.bmp)"
		)
		if not cali_path:
			return
		self.cali_image = cv2.imread(cali_path)
		if self.cali_image is None:
			QMessageBox.warning(self, "Error", "Failed to load the image.")
			return
		self.cali_points.clear()
		self.display_cali_image()

	def calculate_pixel_distance(self):
		if len(self.cali_points) != 2:
			self.ui.pixelLineEdit.clear()
			return
		pixel_distance = abs(self.cali_points[0][0] - self.cali_points[1][0])
		self.ui.pixelLineEdit.setText(str(pixel_distance))

	def display_cali_image(self):
		if self.cali_image is not None:
			img = self.cali_image.copy()
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			for point in self.cali_points:
				cv2.circle(img, point, 10, (255, 0, 0), -1)
			height, width, channel = img.shape
			bytes_per_line = 3 * width
			q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
			pixmap = QPixmap.fromImage(q_img)
			label_size = self.ui.imageLabel.size()
			scaled_pixmap = pixmap.scaled(
				label_size.width(), label_size.height(),
				Qt.AspectRatioMode.KeepAspectRatio,
				Qt.TransformationMode.SmoothTransformation
			)
			self.ui.imageLabel.setPixmap(scaled_pixmap)

	def update_resolution(self):
		distance_text = self.ui.distanceLineEdit.text().strip()
		pixel_text = self.ui.pixelLineEdit.text().strip()

		if distance_text and pixel_text:
			try:
				distance = float(distance_text)
				pixel = float(pixel_text)
				if pixel > 0:
					resolution = distance / pixel
					self.ui.resolutionLineEdit.setText(f"{resolution:.6f}")
				else:
					self.ui.resolutionLineEdit.clear()
			except ValueError:
				self.ui.resolutionLineEdit.clear()
		else:
			self.ui.resolutionLineEdit.clear()

	def confirm_resolution(self):
		resolution_text = self.ui.resolutionLineEdit.text().strip()

		if resolution_text:
			try:
				self.resolution = float(resolution_text)
				QMessageBox.information(self, "Success", f"Current resolution: {self.resolution:.6f} mm/px saved", QMessageBox.StandardButton.Ok)
			except ValueError:
				QMessageBox.warning(self, "Error", "....")
		else:
			QMessageBox.warning(self, "Error", "....")

	# ------------------------ Skeleton Adjust ----------------------------------------------------------------------

	def toggle_add_node_mode(self):
		if self.ui.nodeAddButton.isChecked():
			self.creating_node = True
			self.deleting_node = False
			self.ui.nodeDeleteButton.setChecked(False)
			self.ui.hintsButton.setVisible(True)
			self.ui.hintsLabel1.setVisible(True)
			self.ui.hintsLabel2.setVisible(True)
			self.ui.hintsLabel3.setVisible(False)
		else:
			self.creating_node = False
			self.ui.hintsButton.setVisible(False)
			self.ui.hintsLabel1.setVisible(False)
			self.ui.hintsLabel2.setVisible(False)
			self.ui.hintsLabel3.setVisible(False)

	def toggle_delete_node_mode(self):
		if self.ui.nodeDeleteButton.isChecked():
			self.deleting_node = True
			self.creating_node = False
			self.ui.nodeAddButton.setChecked(False)
			self.ui.hintsButton.setVisible(True)
			self.ui.hintsLabel1.setVisible(False)
			self.ui.hintsLabel2.setVisible(False)
			self.ui.hintsLabel3.setVisible(True)
		else:
			self.deleting_node = False
			self.ui.hintsButton.setVisible(False)
			self.ui.hintsLabel1.setVisible(False)
			self.ui.hintsLabel2.setVisible(False)
			self.ui.hintsLabel3.setVisible(False)

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
				"selected_points": [],
				"created_nodes": [],
				"created_lines": []

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

			# todo: longest path define?
			longest_path = self.get_longest_skeleton(clean_skeleton)
			branch_points = self.skeleton_processor.find_branch_points(clean_skeleton)
			end_points = self.skeleton_processor.find_end_points(clean_skeleton)

			self.skeleton_results[image_path] = {
				"skeleton": clean_skeleton,
				"branch_points": branch_points,
				"end_points": end_points,
				"longest_path": longest_path,
				"selected_points": [],
				"created_nodes": [],
				"created_lines": []

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
	def convert_to_image_coords(self, pos, img_size):
		label_size = self.ui.imageLabel.size()
		scale = min(label_size.width() / img_size[1], label_size.height() / img_size[0])
		display_width = scale * img_size[1]
		display_height = scale * img_size[0]
		x_offset = (label_size.width() - display_width) / 2
		y_offset = (label_size.height() - display_height) / 2
		img_x = (pos.x() - x_offset) / scale
		img_y = (pos.y() - y_offset) / scale
		return int(img_x), int(img_y)

	def eventFilter(self, source, event):
		if source != self.ui.imageLabel:
			return super().eventFilter(source, event)

		if self.progress_stage == 0:
			if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
				clicked_pos = event.pos()
				img_size = self.cali_image.shape if self.cali_image is not None else (1, 1, 1)
				img_x, img_y = self.convert_to_image_coords(clicked_pos, img_size)

				if self.ui.clickAddButton.isChecked():
					if len(self.cali_points) < 2:
						self.cali_points.append((int(img_x), int(img_y)))
					else:
						self.cali_points = [(img_x, img_y)]
					# QMessageBox.warning(self, "Warning", "Only two points can be marked!")
				elif self.ui.clickDeleteButton.isChecked():
					for point in self.cali_points:
						if abs(point[0] - img_x) < 10 and abs(point[1] - img_y) < 10:
							self.cali_points.remove(point)
							break
				self.calculate_pixel_distance()
				self.display_cali_image()
				return True

		if self.progress_stage == 3:
			if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
				self.drawing = True
				self.last_point = event.pos()
			elif event.type() == QEvent.Type.MouseMove and self.drawing:
				self.draw_on_image(event.pos())
			elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
				self.drawing = False
				if self.image is not None and self.current_image_path is not None:
					updated_array = self.qimage_to_np(self.image)
					updated_array = updated_array.astype(np.float32) / 255.0
					self.prediction_results[self.current_image_path] = updated_array

		elif self.progress_stage == 4:
			if self.creating_node and event.type() == QEvent.Type.MouseButtonPress:
				clicked_pos = event.pos()
				if self.image:
					if event.button() == Qt.MouseButton.LeftButton:
						self.create_node(clicked_pos, connect_to_previous=True)
					elif event.button() == Qt.MouseButton.RightButton:
						self.create_node(clicked_pos, connect_to_previous=False)
			elif self.deleting_node and event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
				clicked_pos = event.pos()
				if self.image:
					self.delete_node(clicked_pos)

		return super().eventFilter(source, event)

	def create_node(self, clicked_pos, connect_to_previous=True):
		if self.current_image_path not in self.skeleton_results:
			self.skeleton_results[self.current_image_path] = {
				"created_nodes": [],
				"created_lines": []
			}

		skeleton_data = self.skeleton_results[self.current_image_path]

		img_size = skeleton_data["skeleton"].shape
		img_x, img_y = self.convert_to_image_coords(clicked_pos, img_size)

		new_node = (int(img_x), int(img_y))

		if not connect_to_previous:
			skeleton_data["created_nodes"].append(new_node)
			self.refresh_display_image()
			return

		if len(skeleton_data["created_nodes"]) > 0:
			last_node = skeleton_data["created_nodes"][-1]
			skeleton_data.setdefault("created_lines", []).append((last_node, new_node))

		skeleton_data["created_nodes"].append(new_node)
		self.refresh_display_image()

	def delete_node(self, clicked_pos):
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			return

		closest_node = self.get_clicked_node(clicked_pos)

		if not closest_node or closest_node not in skeleton_data["created_nodes"]:
			return

		connected_lines = [line for line in skeleton_data["created_lines"] if closest_node in line]

		connected_nodes = set()
		for line in connected_lines:
			start, end = line
			connected_nodes.add(start if end == closest_node else end)

		skeleton_data["created_nodes"].remove(closest_node)
		skeleton_data["created_lines"] = [line for line in skeleton_data["created_lines"] if closest_node not in line]

		for node in connected_nodes:
			is_isolated = not any(node in line for line in skeleton_data["created_lines"])
			if is_isolated and node in skeleton_data["created_nodes"]:
				skeleton_data["created_nodes"].remove(node)

		self.refresh_display_image()

	def get_clicked_node(self, position):
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			return None

		created_nodes = skeleton_data.get("created_nodes", [])
		if not created_nodes:
			return None

		img_size = skeleton_data["skeleton"].shape if "skeleton" in skeleton_data else (1, 1)
		img_x, img_y = self.convert_to_image_coords(position, img_size)

		threshold = 5

		nodes = np.array(created_nodes)
		distances = np.linalg.norm(nodes - np.array([img_x, img_y]), axis=1)
		min_index = np.argmin(distances)
		min_dist = distances[min_index]

		if min_dist < threshold:
			return tuple(created_nodes[min_index])

		return None

	def qimage_to_np(self, qimage: QImage):
		qimage = qimage.convertToFormat(QImage.Format.Format_Grayscale8)
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

		image_size = self.image.size()
		x1, y1 = self.convert_to_image_coords(self.last_point, (image_size.height(), image_size.width()))
		x2, y2 = self.convert_to_image_coords(current_point, (image_size.height(), image_size.width()))

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
		self.update_cursor()

	def activate_delete_mode(self):
		self.brush_color = QColor(0, 0, 0)
		self.update_cursor()

	def update_brush_size(self, value):
		self.brush_size = value
		self.show_brush_size_tooltip(value)
		self.update_cursor()

	def show_brush_size_tooltip(self, value):
		slider = self.ui.penSizeSlider
		slider_pos = slider.mapToGlobal(QPoint(0, 0))

		handle_x = slider_pos.x() + int(
			slider.width() * ((value - slider.minimum()) / (slider.maximum() - slider.minimum()))
		) + 15
		handle_y = slider_pos.y() - 50

		QToolTip.showText(QPoint(handle_x, handle_y), f"{value} px", slider)

	def update_cursor(self):
		size = self.brush_size

		cursor_pixmap = QPixmap(size, size)
		cursor_pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(cursor_pixmap)
		pen = QPen(Qt.GlobalColor.yellow)
		pen.setWidth(3)
		painter.setPen(pen)

		if self.pen_cap_style == Qt.PenCapStyle.RoundCap:
			painter.drawEllipse(1, 1, size - 2, size - 2)
		else:
			painter.drawRect(1, 1, size - 2, size - 2)
		painter.end()

		custom_cursor = QCursor(cursor_pixmap)
		self.ui.imageLabel.setCursor(custom_cursor)

	def update_pen_shape(self, shape):
		if shape == "Round":
			self.pen_cap_style = Qt.PenCapStyle.RoundCap
		elif shape == "Square":
			self.pen_cap_style = Qt.PenCapStyle.SquareCap
		self.update_cursor()

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
				self.prediction_results[image_path] = None

				item = QListWidgetItem()
				item.setIcon(QIcon(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)))
				item.setData(Qt.ItemDataRole.UserRole, image_path)
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
		file_path = item.data(Qt.ItemDataRole.UserRole)
		if file_path:
			self.current_image_path = file_path
			self.refresh_display_image()

	def refresh_display_image(self):
		"""
		Update the QLabel display with the combined original image and prediction.
		"""
		if not self.current_image_path:
			self.ui.imageLabel.clear()
			return

		original_image = cv2.imread(self.current_image_path)
		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
		if original_image is None:
			return

		original_qimage = QImage(
			original_image.data, original_image.shape[1], original_image.shape[0],
			original_image.shape[1] * 3, QImage.Format.Format_RGB888
		)
		original_pixmap = QPixmap.fromImage(original_qimage)
		if original_pixmap.isNull():
			return

		if self.progress_stage in [1, 2]:
			self.display_original_image(original_pixmap)
		elif self.progress_stage == 3:
			self.display_prediction_overlay(original_pixmap)
		elif self.progress_stage == 4:
			self.display_skeleton_overlay(original_image)
		elif self.progress_stage == 5:
			self.display_original_image(original_pixmap)
			self.display_calcu_results()

	def display_original_image(self, original_pixmap):
		"""Display the original image scaled to fit the label."""
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = original_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
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
			prediction.shape[1], QImage.Format.Format_Grayscale8
		)

		prediction_pixmap = QPixmap.fromImage(prediction_qimage)
		if prediction_pixmap.isNull():
			return

		combined_pixmap = QPixmap(original_pixmap.size())
		combined_pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(combined_pixmap)
		painter.setOpacity(1.0)
		painter.drawPixmap(0, 0, original_pixmap)
		opacity = self.ui.opacitySlider.value() / 100.0
		painter.setOpacity(opacity)
		painter.drawPixmap(0, 0, prediction_pixmap.scaled(
			original_pixmap.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		))
		painter.end()

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
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
		overlay_image[skeleton_coords[0], skeleton_coords[1]] = [255, 0, 0]

		created_nodes = skeleton_data.get("created_nodes", [])
		for node in created_nodes:
			cv2.circle(overlay_image, (node[0], node[1]), radius=5, color=(255, 251, 13), thickness=-1)

		lines = skeleton_data.get("created_lines", [])
		for line in lines:
			start, end = line
			cv2.line(overlay_image, (start[0], start[1]), (end[0], end[1]), color=(255, 251, 13), thickness=1)

		# if longest_path is not None and len(longest_path) > 0:
		# 	for point in longest_path:
		# 		overlay_image[point[0], point[1]] = [255, 0, 0]

		# if branch_points is not None and np.any(branch_points):
		# 	branch_coords = np.argwhere(branch_points > 0)
		# 	for coord in branch_coords:
		# 		point_tuple = (coord[1], coord[0])
		# 		color = (0, 255, 0) if point_tuple in selected_points else (255, 255, 255)
		# 		cv2.circle(overlay_image, point_tuple, radius=5, color=color, thickness=2)

		if end_points is not None and np.any(end_points):
			end_coords = np.argwhere(end_points > 0)
			for coord in end_coords:
				point_tuple = (coord[1], coord[0])
				color = (0, 255, 0) if point_tuple in selected_points else (255, 255, 255)
				cv2.circle(overlay_image, point_tuple, radius=5, color=color, thickness=2)

		overlay_qimage = QImage(
			overlay_image.data,
			overlay_image.shape[1],
			overlay_image.shape[0],
			overlay_image.shape[1] * 3,
			QImage.Format.Format_RGB888
		)
		overlay_pixmap = QPixmap.fromImage(overlay_qimage)

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = overlay_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.image = overlay_qimage.copy()

	def display_calcu_results(self):
		if not self.crack_results or self.current_image_path not in self.crack_results:
			self.ui.fileNameLabel.setText("")
			self.ui.crackWidthLabel.setText("")
			self.ui.skeletonLengthLabel.setText("")
			self.ui.crackAreaLabel.setText("")
			return

		full_path = self.current_image_path
		parent_1 = os.path.basename(os.path.dirname(full_path))
		parent_2 = os.path.basename(os.path.dirname(os.path.dirname(full_path)))

		if parent_2:
			display_name = f"/{parent_2}/{parent_1}/{os.path.basename(full_path)}"
		else:
			display_name = f"/{parent_1}/{os.path.basename(full_path)}"

		display_name = f"{display_name}"
		self.ui.fileNameLabel.setText(display_name)

		crack_width_mm = self.crack_results[self.current_image_path]["crack_width"]
		crack_area_mm = self.crack_results[self.current_image_path]["crack_area"]
		skeleton_length_mm = self.crack_results[self.current_image_path]["skeleton_length"]

		self.ui.crackWidthLabel.setText(f"{crack_width_mm:.6f} mm")
		self.ui.crackAreaLabel.setText(f"{crack_area_mm:.6f} mm²")
		self.ui.skeletonLengthLabel.setText(f"{skeleton_length_mm:.6f} mm")

	def refresh_display_after_draw(self):
		if not self.current_image_path or self.image is None:
			return

		original_image = cv2.imread(self.current_image_path)
		if original_image is None:
			return

		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
		original_qimage = QImage(
			original_image.data, original_image.shape[1], original_image.shape[0],
			original_image.shape[1] * 3, QImage. Format.Format_RGB888
		)
		original_pixmap = QPixmap.fromImage(original_qimage)
		if original_pixmap.isNull():
			return

		prediction_pixmap = QPixmap.fromImage(self.image)

		combined_pixmap = QPixmap(original_pixmap.size())
		combined_pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(combined_pixmap)
		painter.setOpacity(1.0)
		painter.drawPixmap(0, 0, original_pixmap)

		opacity = self.ui.opacitySlider.value() / 100.0
		painter.setOpacity(opacity)
		painter.drawPixmap(0, 0, prediction_pixmap.scaled(
			original_pixmap.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		))
		painter.end()

		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)
	# ------------------------ Progress Management ----------------------------------------------------------------------

	def set_stage(self, stage):

		if stage < 0 or stage > 5:
			return
		self.progress_stage = stage
		self.ui.stackedWidget.setCurrentIndex(stage)
		self.progress_manager.update_progress(self.progress_stage)

		if self.progress_stage == 3:
			self.update_cursor()
		else:
			self.ui.imageLabel.unsetCursor()

		if self.progress_stage == 0:
			self.display_cali_image()
			print("Calibration stage")
		elif self.progress_stage == 1:
			self.refresh_display_image()
			print("Upload stage")
		elif self.progress_stage == 2:
			self.refresh_display_image()
			print("Model detection stage")
		elif self.progress_stage == 3:
			self.refresh_display_image()
			print("Edit stage")
		elif self.progress_stage == 4:
			self.refresh_display_image()
			print("Select skeleton stage")
		elif self.progress_stage == 5:
			self.refresh_display_image()
			self.crack_results = self.calculate_crack_properties()
			print("File export stage")

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

	def reset_all_data(self):
		self.set_stage(0)
		self.current_image_path = None
		self.prediction_results.clear()
		self.skeleton_results.clear()
		self.crack_results.clear()

		self.ui.listWidget.clear()
		self.ui.imageLabel.clear()
		self.ui.imageLabel.repaint()
		self.ui.listWidget.repaint()

		self.ui.fileNameLabel.setText("")
		self.ui.crackWidthLabel.setText("")
		self.ui.skeletonLengthLabel.setText("")
		self.ui.crackAreaLabel.setText("")

		self.ui.distanceLineEdit.clear()
		self.ui.pixelLineEdit.clear()
		self.ui.resolutionLineEdit.clear()

		self.drawing = False
		self.image = None
		self.resolution = None
		self.cali_image = None
		self.cali_points = []
		self.creating_node = None
		self.deleting_node = None
		self.dragged_node = None

	# ------------------------ Results Export ----------------------------------------------------------------------
	def calculate_crack_properties(self):
		if not self.prediction_results or not self.skeleton_results:
			return {}

		if self.resolution is None or self.resolution <= 0:
			print("No valid resolution.")
			return

		crack_results = {}

		for image_path, prediction in self.prediction_results.items():

			crack_region_pixels = np.sum(prediction == 1)
			crack_area_mm2 = crack_region_pixels * (self.resolution ** 2)

			skeleton_data = self.skeleton_results.get(image_path)
			clean_skeleton = skeleton_data.get("skeleton")
			skeleton_length = np.sum(clean_skeleton == 1)

			manual_line_length = 0
			created_lines = skeleton_data.get("created_lines", [])

			for line in created_lines:
				start, end = line
				line_length = np.linalg.norm(np.array(start) - np.array(end))
				manual_line_length += line_length

			total_skeleton_length = skeleton_length + manual_line_length
			skeleton_length_mm = total_skeleton_length * self.resolution

			avg_crack_width_pixels = (crack_region_pixels / total_skeleton_length) if total_skeleton_length > 0 else 0

			crack_results[image_path] = {
				"crack_pixels": crack_region_pixels,
				"skeleton_pixels": total_skeleton_length,
				"crack_area": crack_area_mm2,
				"skeleton_length": skeleton_length_mm,
				"crack_width": avg_crack_width_pixels * self.resolution
			}

		return crack_results

	def browse_export_path(self):
		options = QFileDialog.Option(0)
		file_path, _ = QFileDialog.getSaveFileName(
			self, "Select Export File", "", "CSV Files (*.csv);;All Files (*)", options=options
		)

		if file_path:
			if not file_path.lower().endswith(".csv"):
				file_path += ".csv"

			self.ui.exportPathLineEdit.setText(file_path)

	def export_to_csv(self):
		file_path = self.ui.exportPathLineEdit.text().strip()

		if not file_path:
			QMessageBox.warning(self, "Export Error", "Please select a file path!")
			return

		if not self.crack_results:
			QMessageBox.warning(self, "Export Error", "No valid data to export!")
			return

		os.makedirs(os.path.dirname(file_path), exist_ok=True)

		data_list = []
		for image_path, result in self.crack_results.items():
			file_name = os.path.basename(image_path)
			full_path = os.path.abspath(image_path)

			crack_pixels = result["crack_pixels"]
			skeleton_pixels = result["skeleton_pixels"]
			crack_area = result["crack_area"]
			skeleton_length = result["skeleton_length"]
			crack_width = result["crack_width"]

			data_list.append({
				"File Path": full_path,
				"File Name": file_name,
				"Crack Pixel (px²)": crack_pixels,
				"Skeleton Pixel (px)": skeleton_pixels,
				"Crack Area (mm²)": crack_area,
				"Skeleton length (mm)": skeleton_length,
				"Crack Width (mm)": crack_width,
				"Resolution (mm/px)": self.resolution
			})

		df = pd.DataFrame(data_list)

		try:
			df.to_csv(file_path, index=False, encoding="utf-8-sig")
			QMessageBox.information(self, "Success", f"File exported successfully:\n{file_path}", QMessageBox.StandardButton.Ok)
		except Exception as e:
			QMessageBox.critical(self, "Export Failed", f"Error:\n{str(e)}")
	# ------------------------ Global UI Functions ----------------------------------------------------------------------

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

		scaled_pixmap = original_pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.ui.imageLabel.adjustSize()

	def delete_current_image(self):

		selected_item = self.ui.listWidget.currentItem()
		if not selected_item:
			QMessageBox.warning(self, "Error", "No image selected!")
			return

		image_path = selected_item.data(Qt.ItemDataRole.UserRole)

		reply = QMessageBox.question(self, "Confirm Delete",
									 f"Are you sure you want to delete {os.path.basename(image_path)}?",
									 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

		if reply == QMessageBox.StandardButton.No:
			return

		row = self.ui.listWidget.row(selected_item)
		self.ui.listWidget.takeItem(row)

		self.prediction_results.pop(image_path, None)
		self.skeleton_results.pop(image_path, None)
		self.crack_results.pop(image_path, None)

		self.ui.listWidget.repaint()

		if self.ui.listWidget.count() > 0:
			new_index = min(row, self.ui.listWidget.count() - 1)
			self.ui.listWidget.setCurrentRow(new_index)
			self.display_large_image(self.ui.listWidget.currentItem())
		else:
			self.current_image_path = None
			self.image = None
			self.ui.imageLabel.clear()
			if self.progress_stage == 4:
				self.ui.fileNameLabel.clear()
				self.ui.crackWidthLabel.clear()

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