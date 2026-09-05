import base64
import json
import os
import pathlib
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
from backend.maskprocessor import MaskProcessor
from backend.skeletonprocessor import SkeletonProcessor
from frontend.progressmanager import ProgressManager
from frontend.ui.uimain import Ui_MainWindow
from skimage.morphology import skeletonize

from utils.utils import resource_path


class _NumpyJSONEncoder(json.JSONEncoder):
	r"""
	JSON encoder that additionally accepts numpy scalars and arrays, which show up
	throughout the project data (e.g. skeleton coordinates, crack measurements).
	"""
	def default(self, obj):
		if isinstance(obj, np.generic):
			return obj.item()
		if isinstance(obj, np.ndarray):
			return obj.tolist()
		return super().default(obj)


def _encode_mask_png(mask):
	r"""Encode a 2D uint8 mask as a base64 string, for compact storage in a JSON project file."""
	ok, encoded = cv2.imencode(".png", mask)
	if not ok:
		raise ValueError("Failed to encode mask as PNG.")
	return base64.b64encode(encoded.tobytes()).decode("ascii")


def _decode_mask_png(data):
	r"""Decode a base64 string produced by _encode_mask_png back into a 2D uint8 mask."""
	encoded = np.frombuffer(base64.b64decode(data), dtype=np.uint8)
	return cv2.imdecode(encoded, cv2.IMREAD_UNCHANGED)


class MainWindow(QMainWindow):
	r"""
	Main User Interface for the application.
	"""

	DETECTION_METHOD_NONE = "None"

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
		self.mask_processor = MaskProcessor()

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
				self.ui.selectProcessButton,
				self.ui.exportProcessButton
			],
			lines=[self.ui.line0, self.ui.line1, self.ui.line2, self.ui.line4]
		)
		self.ui.calibrationProcessButton.clicked.connect(lambda: self.set_stage(0))
		self.ui.uploadProcessButton.clicked.connect(lambda: self.set_stage(1))
		self.ui.detectProcessButton.clicked.connect(lambda: self.set_stage(2))
		self.ui.selectProcessButton.clicked.connect(lambda: self.set_stage(3))
		self.ui.exportProcessButton.clicked.connect(lambda: self.set_stage(4))

		self.ui.zoomInButton.clicked.connect(lambda: self.zoom_image(zoom_in=True))
		self.ui.zoomOutButton.clicked.connect(lambda: self.zoom_image(zoom_in=False))
		self.ui.zoomFitButton.clicked.connect(self.zoom_fit_to_window)
		self.ui.zoomOneToOneButton.clicked.connect(self.zoom_one_to_one)
		self.ui.zoomFitButton.setShortcut("Ctrl+0")
		self.ui.zoomOneToOneButton.setShortcut("Ctrl+1")
		self.ui.deleteImageButton.clicked.connect(self.delete_current_image)

		self.drawing = False
		self.last_point = QPoint()
		self.brush_color = QColor(255, 255, 255)
		self.brush_size = 10
		self.pen_cap_style = Qt.PenCapStyle.RoundCap
		self.image = None
		self.original_pixmap = None
		self.zoom_base_pixmap = None
		self.zoom_factor = 1.0

		self.init_stacked_widget()
		self.init_image_label()

		self.deleting_node = None
		self.creating_node = None
		self.dragged_node = None

		self.resolution = None
		self.cali_image = None
		self.cali_path = None
		self.cali_points = []

		self.setWindowIcon(QIcon(resource_path('resources/crackpot.ico')))
		self.adjust_window_size()

	def adjust_window_size(self):
		r"""
		Adjust the main window size based on the available screen geometry.
		"""
		screen = self.screen()
		screen_size = screen.availableGeometry()

		width = int(screen_size.width() * 0.7)
		height = int(screen_size.height() * 0.9)

		self.resize(width, height)

	def init_image_label(self):
		r"""
		Initialize the image label, enabling mouse tracking and event filtering.
		"""
		self.ui.imageLabel.setMouseTracking(True)
		self.ui.imageLabel.installEventFilter(self)

	def init_stacked_widget(self):
		r"""
		Initialize the stacked widget and connect tool components to their respective functions.
		"""
		self.ui.stackedWidget.setCurrentIndex(self.progress_stage)

		# File menu
		self.ui.actionExportProject.triggered.connect(self.export_project)
		self.ui.actionImportProject.triggered.connect(self.import_project)

		self.ui.nextButton0.clicked.connect(lambda: self.set_stage(1))
		self.ui.nextButton1.clicked.connect(lambda: self.set_stage(2))
		self.ui.nextButton3.clicked.connect(lambda: self.set_stage(3))
		self.ui.nextButton4.clicked.connect(lambda: self.set_stage(4))
		self.ui.nextButton5.clicked.connect(self.reset_all_data)

		# masking stage
		self.ui.applyModelButton.clicked.connect(lambda: self.apply_model_detection(all_images=False))
		self.ui.applyModelAllButton.clicked.connect(lambda: self.apply_model_detection(all_images=True))
		self.ui.clearMaskButton.clicked.connect(lambda: self.clear_mask(all_images=False))
		self.ui.clearMaskAllButton.clicked.connect(lambda: self.clear_mask(all_images=True))

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
		# Left buttons act on the currently displayed image, right buttons on all images.
		self.ui.skeletonButton.clicked.connect(lambda: self.apply_skeletonization(all_images=False))
		self.ui.skeletonAllButton.clicked.connect(lambda: self.apply_skeletonization(all_images=True))
		self.ui.cleanBranchButton.clicked.connect(lambda: self.clean_skeleton_branches(all_images=False))
		self.ui.cleanBranchAllButton.clicked.connect(lambda: self.clean_skeleton_branches(all_images=True))
		self.ui.clearSkeletonButton.clicked.connect(lambda: self.clear_skeleton(all_images=False))
		self.ui.clearSkeletonAllButton.clicked.connect(lambda: self.clear_skeleton(all_images=True))

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

		self.ui.removePatchesButton.clicked.connect(lambda: self.clean_mask_patches(all_images=False))
		self.ui.removePatchesAllButton.clicked.connect(lambda: self.clean_mask_patches(all_images=True))

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
		r"""
		Open a file dialog to select a calibration image, load it, and initialize calibration points list.
		"""
		cali_path, _ = QFileDialog.getOpenFileName(
			self, "Select a Calibration Picture", "", "Images (*.png *.jpg *.jpeg *.bmp)"
		)
		if not cali_path:
			return
		self.cali_image = cv2.imread(cali_path)
		if self.cali_image is None:
			QMessageBox.warning(self, "Error", "Failed to load the image.")
			return
		self.cali_path = cali_path
		self.cali_points.clear()
		self.display_cali_image()

	def calculate_pixel_distance(self):
		r"""
		Calculate the pixel distance between two selected calibration points.
		Update the pixel distance value in the UI if exactly two points are selected.
		Clear the pixel distance field if the number of points is incorrect.
		"""
		if len(self.cali_points) != 2:
			self.ui.pixelLineEdit.clear()
			return
		cali_points = np.array(self.cali_points)
		pixel_distance = np.linalg.norm(cali_points[1] - cali_points[0])
		self.ui.pixelLineEdit.setText(str(pixel_distance))

	def display_cali_image(self):
		r"""
		Display the calibration image with marked calibration points.
		"""
		if self.cali_image is not None:
			img = self.cali_image.copy()
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			for point in self.cali_points:
				cv2.circle(img, point, 10, (255, 0, 0), -1)
			height, width, channel = img.shape
			bytes_per_line = 3 * width
			q_img = QImage(img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
			pixmap = QPixmap.fromImage(q_img)
			self.original_pixmap = pixmap
			label_size = self.ui.imageLabel.size()
			scaled_pixmap = pixmap.scaled(
				label_size.width(), label_size.height(),
				Qt.AspectRatioMode.KeepAspectRatio,
				Qt.TransformationMode.SmoothTransformation
			)
			self.set_display_pixmap(scaled_pixmap)

	def update_resolution(self):
		r"""
		Retrieve the real-world distance and pixel distance from the UI,
		calculate resolution (mm per pixel), and update the resolution field.
		"""
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
		r"""
		Confirm and save the calculated resolution.
		"""
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
		r"""
		Toggle the mode for adding skeleton nodes in the skeleton editing process.
		"""
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
		r"""
		Toggle the mode for deleting skeleton nodes in the skeleton editing process.
		"""
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

	def _skeleton_target_paths(self, all_images, source):
		r"""
		Resolve which images a skeleton action applies to.

		The three skeleton actions (create, remove small branches, clear) share the
		same rule: the left button acts on the currently displayed image, the right
		button on every uploaded image. Centralising this here keeps them consistent.

		\param all_images: If True, act on all images (right button); if False, only
			on the currently displayed one (left button).
		\param source: The dictionary whose keys define the available images
			(prediction results when creating skeletons, skeleton results otherwise).
		\return: A list of image paths to process.
		"""
		if all_images:
			return list(source.keys())
		if self.current_image_path and self.current_image_path in source:
			return [self.current_image_path]
		return []

	def apply_skeletonization(self, all_images=False):
		r"""
		Create the crack skeleton from the prediction mask.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.prediction_results:
			return

		for image_path in self._skeleton_target_paths(all_images, self.prediction_results):
			prediction = self.prediction_results.get(image_path)
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
		self.refresh_display_image()

	def clean_skeleton_branches(self, all_images=False):
		r"""
		Remove short branches from the skeleton and keep the longest path.
		Identify main endpoints, clean unnecessary branches, and extract the longest path.
		Branches shorter than the length threshold set in the UI are removed.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.skeleton_results:
			return

		for image_path in self._skeleton_target_paths(all_images, self.skeleton_results):
			skeleton_data = self.skeleton_results.get(image_path)
			if not skeleton_data:
				continue
			skeleton = skeleton_data.get("skeleton")
			if skeleton is None:
				continue

			main_endpoints = self.skeleton_processor.find_main_endpoints(skeleton)
			clean_skeleton = self.skeleton_processor.remove_small_branches(
				skeleton, max_branch_length=self.ui.branchLengthSpinBox.value(), main_endpoints=main_endpoints
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

		self.skeleton_processor.skeletons = self.skeleton_results
		self.refresh_display_image()

	def clear_skeleton(self, all_images=False):
		r"""
		Discard the skeleton and any manually added nodes/lines, resetting it to an
		empty but valid state so it can be regenerated or edited from scratch.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.skeleton_results:
			return

		for image_path in self._skeleton_target_paths(all_images, self.skeleton_results):
			skeleton_data = self.skeleton_results.get(image_path)
			if not skeleton_data or skeleton_data.get("skeleton") is None:
				continue

			self.skeleton_results[image_path] = {
				"skeleton": np.zeros_like(skeleton_data["skeleton"]),
				"branch_points": None,
				"end_points": None,
				"longest_path": None,
				"selected_points": [],
				"created_nodes": [],
				"created_lines": []
			}

		self.skeleton_processor.skeletons = self.skeleton_results
		self.refresh_display_image()

	def get_longest_skeleton(self, skeleton):
		r"""
		Find and return the longest connected path in the skeletonized results.
		Label connected components in the skeleton and determine the longest one
		based on the number of pixels in each region.

		\param skeleton: A binary skeletonized image.
		\return: A list of coordinates representing the longest skeleton path.
		"""
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
		r"""
		Calculate the corresponding position in the image based on the
		displayed image's scale and offsets within the QLabel.

		\param pos: The QPoint position of the cursor in the UI.
		\param img_size: The size of the original image (height, width).
		\return: The converted image coordinates (x, y).
		"""
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
		r"""
		Handle various mouse interactions based on the progressing stage.
		e.g. calibration clicks, crack drawing actions, and skeleton node creation/deletion.

		\param source: The object generating the event.
		\param event: The event being processed.
		\return: A boolean indicating whether the event was handled.
		"""
		if source != self.ui.imageLabel:
			return super().eventFilter(source, event)

		if event.type() == QEvent.Type.Wheel and event.modifiers() & Qt.KeyboardModifier.ControlModifier:
			self.zoom_image(zoom_in=event.angleDelta().y() > 0)
			return True

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

		if self.progress_stage == 2:
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

		elif self.progress_stage == 3:
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

	def empty_skeleton_result(self, shape):
		r"""
		Build an empty but valid skeleton entry for an image of the given shape.
		Used when the user edits the skeleton manually without running the automatic
		skeletonization first, so the rest of the code can rely on a proper "skeleton"
		array being present.

		\param shape: The (height, width) of the image the skeleton belongs to.
		\return: A skeleton result dictionary with an empty (all-zero) skeleton.
		"""
		return {
			"skeleton": np.zeros(shape, dtype=np.uint8),
			"branch_points": None,
			"end_points": None,
			"longest_path": None,
			"selected_points": [],
			"created_nodes": [],
			"created_lines": []
		}

	def create_node(self, clicked_pos, connect_to_previous=True):
		r"""
		Create a skeleton node at the clicked position and optionally connect it to the previous node.

		\param clicked_pos: The QPoint position where the user clicked.
		\param connect_to_previous: Boolean indicating whether to connect to the last node.
		"""
		if self.current_image_path not in self.skeleton_results:
			original_image = cv2.imread(self.current_image_path)
			if original_image is None:
				return
			self.skeleton_results[self.current_image_path] = self.empty_skeleton_result(original_image.shape[:2])

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
		r"""
		Identify the closest node, remove it from the created skeleton nodes, and
		clean up any isolated nodes.

		\param clicked_pos: The QPoint position where the user clicked.
		"""
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
		r"""
		Find the closest node to the given position within a threshold.

		\param position: The QPoint position where the user clicked.
		\return: The nearest node's coordinates or None if no node is close enough.
		"""
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
		r"""
		Convert a QImage object to a NumPy array.

		\param qimage: The QImage to be converted.
		\return: A NumPy array representing the image.
		"""
		qimage = qimage.convertToFormat(QImage.Format.Format_Grayscale8)
		width = qimage.width()
		height = qimage.height()
		ptr = qimage.bits()
		arr = np.array(ptr).reshape(height, width)
		return arr

	def resizeEvent(self, event):
		r"""
		Handle the resize event and refresh the displayed image.

		\param event: The QResizeEvent triggered by the resize action.
		"""
		if self.current_image_path:
			self.refresh_display_image()
		super().resizeEvent(event)

# ------------------------ Drawing Functions ----------------------------------------------------------------------
	def draw_on_image(self, current_point):
		r"""
		Draw a line using the selected brush properties and update the display after drawing.

		\param current_point: The QPoint representing the current mouse position.
		"""
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
		r"""
		Activate the add mode for drawing by setting the brush color to white.
		"""
		self.brush_color = QColor(255, 255, 255)
		self.update_cursor()

	def activate_delete_mode(self):
		r"""
		Activate the delete mode by setting the brush color to black.
		"""
		self.brush_color = QColor(0, 0, 0)
		self.update_cursor()

	def update_brush_size(self, value):
		r"""
		Update the brush size based on the slider value, display a tooltip showing the selected size,
		and update the brush cursor accordingly.

		\param value: The new brush size value from the slider.
		"""
		self.brush_size = value
		self.show_brush_size_tooltip(value)
		self.update_cursor()

	def show_brush_size_tooltip(self, value):
		r"""
		Display a tooltip near the slider to show the selected brush size.

		\param value: The current brush size value.
		"""
		slider = self.ui.penSizeSlider
		slider_pos = slider.mapToGlobal(QPoint(0, 0))

		handle_x = slider_pos.x() + int(
			slider.width() * ((value - slider.minimum()) / (slider.maximum() - slider.minimum()))
		) + 15
		handle_y = slider_pos.y() - 50

		QToolTip.showText(QPoint(handle_x, handle_y), f"{value} px", slider)

	def display_scale(self):
		r"""
		Return the current scale factor between image pixels and screen pixels,
		based on the displayed image size within the QLabel. Uses the same
		scaling logic as convert_to_image_coords, so the cursor matches the
		stroke that will actually be drawn. Returns 1.0 when no image is shown.
		"""
		if self.image is None:
			return 1.0
		image_size = self.image.size()
		if image_size.width() == 0 or image_size.height() == 0:
			return 1.0
		label_size = self.ui.imageLabel.size()
		return min(label_size.width() / image_size.width(), label_size.height() / image_size.height())

	def update_cursor(self):
		r"""
		Update a custom transparent cursor to visually represent the current brush size and shape.
		The radius is scaled by the current zoom factor, so the cursor always matches the
		stroke in image pixels regardless of the zoom level.
		"""
		size = max(int(round(self.brush_size * self.display_scale())), 1)

		# Add a small margin so the outline stays fully visible even for tiny radii.
		margin = 2
		pixmap_size = size + 2 * margin
		cursor_pixmap = QPixmap(pixmap_size, pixmap_size)
		cursor_pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(cursor_pixmap)
		pen = QPen(Qt.GlobalColor.yellow)
		pen.setWidth(2)
		painter.setPen(pen)

		if self.pen_cap_style == Qt.PenCapStyle.RoundCap:
			painter.drawEllipse(margin, margin, size, size)
		else:
			painter.drawRect(margin, margin, size, size)
		painter.end()

		custom_cursor = QCursor(cursor_pixmap, pixmap_size // 2, pixmap_size // 2)
		self.ui.imageLabel.setCursor(custom_cursor)

	def update_pen_shape(self, shape):
		r"""
		Update the pen shape based on the selected option in the UI and refresh the cursor appearance accordingly.

		\param shape: A string indicating the selected pen shape ("Round" or "Square").
		"""
		if shape == "Round":
			self.pen_cap_style = Qt.PenCapStyle.RoundCap
		elif shape == "Square":
			self.pen_cap_style = Qt.PenCapStyle.SquareCap
		self.update_cursor()

	def clean_mask_patches(self, all_images=False):
		r"""
		Remove small disconnected patches from the crack mask.
		Patches smaller than the area threshold set in the UI are removed.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.prediction_results:
			return

		for image_path in self._skeleton_target_paths(all_images, self.prediction_results):
			mask = self.prediction_results.get(image_path)
			if mask is None:
				continue

			self.prediction_results[image_path] = self.mask_processor.remove_small_patches(
				mask, min_patch_area=self.ui.patchAreaSpinBox.value()
			)

		if self.ui.listWidget.currentItem():
			self.refresh_display_image()

	# ------------------------ Image Display ----------------------------------------------------------------------
	def upload_figures(self):
		r"""
		Open a file dialog to select and upload multiple images and display their thumbnails in the QListWidget.
		"""
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

	def ensure_masks_initialized(self):
		r"""
		Give every uploaded image without a mask yet an empty, editable one.

		Entering the masking stage always shows the mask overlay so it can be
		edited with the brush tools, even before a model has been applied. An
		empty (all-zero) mask keeps that overlay and the brush tools usable from
		the start, exactly like selecting "None" as the detection method used to.
		"""
		for file_name, prediction in self.prediction_results.items():
			if prediction is None:
				image = cv2.imread(file_name)
				self.prediction_results[file_name] = np.zeros(image.shape[:2], dtype=np.float32)

	def apply_model_detection(self, all_images=False):
		r"""
		Run crack detection for the selected images, overwriting their current mask.

		Unless the model dropdown is set to "None", in which case the mask is
		instead reset to empty, same as \ref clear_mask.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.prediction_results:
			return

		if self.ui.modelComboBox.currentText() == self.DETECTION_METHOD_NONE:
			self.clear_mask(all_images)
			return

		self.edge_detector = EdgeDetection()
		for image_path in self._skeleton_target_paths(all_images, self.prediction_results):
			self.prediction_results[image_path] = self.edge_detector.detect_edges(image_path)

		if self.ui.listWidget.currentItem():
			self.refresh_display_image()

	def clear_mask(self, all_images=False):
		r"""
		Reset the crack mask to empty for the selected images, so it can be rebuilt manually.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.prediction_results:
			return

		for image_path in self._skeleton_target_paths(all_images, self.prediction_results):
			image = cv2.imread(image_path)
			if image is not None:
				self.prediction_results[image_path] = np.zeros(image.shape[:2], dtype=np.float32)

		if self.ui.listWidget.currentItem():
			self.refresh_display_image()

	def display_large_image(self, item):
		r"""
		Retrieve the file path from the clicked item in the QListWidget and
		update the current image path before refreshing the display.

		\param item: The selected QListWidgetItem.
		"""
		file_path = item.data(Qt.ItemDataRole.UserRole)
		if file_path:
			self.current_image_path = file_path
			self.refresh_display_image()

	def refresh_display_image(self):
		r"""
		Depending on the stage, display the original image, overlay predictions,
		or skeletonization results. Clear the label if no image is selected.
		"""
		if not self.current_image_path:
			self.ui.imageLabel.clear()
			self.original_pixmap = None
			self.zoom_base_pixmap = None
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

		if self.progress_stage == 1:
			self.display_original_image(original_pixmap)
		elif self.progress_stage == 2:
			self.display_prediction_overlay(original_pixmap)
		elif self.progress_stage == 3:
			self.display_skeleton_overlay(original_image)
		elif self.progress_stage == 4:
			self.display_original_image(original_pixmap)
			self.display_calcu_results()

	def display_original_image(self, original_pixmap):
		r"""
		Display the original image scaled to fit the QLabel.

		\param original_pixmap: The QPixmap representation of the original image.
		"""
		self.original_pixmap = original_pixmap
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = original_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.set_display_pixmap(scaled_pixmap)
		self.image = None

	def display_prediction_overlay(self, original_pixmap):
		r"""
		Overlay the predicted mask on the original image.

		\param original_pixmap: The QPixmap representation of the original image.
		"""
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

		self.original_pixmap = combined_pixmap
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()

		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.set_display_pixmap(scaled_pixmap)

		self.image = prediction_qimage.copy()

	def display_skeleton_overlay(self, original_image):
		r"""
		Overlay the skeletonized result onto the original image.

		\param original_image: The original image in NumPy array format.
		"""
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data or skeleton_data.get("skeleton") is None:
			# No skeleton for this image yet: show the plain original image so it can
			# still be viewed (and skeletonized/edited later). An empty, all-zero
			# skeleton means the rest of this method simply draws no overlay.
			skeleton_data = {
				"skeleton": np.zeros(original_image.shape[:2], dtype=np.uint8),
				"branch_points": None,
				"end_points": None,
				"longest_path": [],
				"selected_points": [],
				"created_nodes": [],
				"created_lines": [],
			}

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

		self.original_pixmap = overlay_pixmap
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = overlay_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.set_display_pixmap(scaled_pixmap)
		self.image = overlay_qimage.copy()

	def display_calcu_results(self):
		r"""
		Display calculated crack width, area, and skeleton length in the UI.
		If no results exist for the current image, clear the labels.
		"""
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
		r"""
		Refresh the QLabel display after a drawing operation.
		Overlay the manually drawn mask onto the original image and update the UI.
		"""
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

		self.original_pixmap = combined_pixmap
		label_width = self.ui.imageLabel.width()
		label_height = self.ui.imageLabel.height()
		scaled_pixmap = combined_pixmap.scaled(
			label_width, label_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.set_display_pixmap(scaled_pixmap)
	# ------------------------ Progress Management ----------------------------------------------------------------------

	def set_stage(self, stage):
		r"""
		Change the application workflow to the specified stage and switch the stacked widget index to the corresponding tool page.

		\param stage: The target stage index (0 to 4).
		"""

		if stage < 0 or stage > 4:
			return
		self.progress_stage = stage
		self.ui.stackedWidget.setCurrentIndex(stage)
		self.progress_manager.update_progress(self.progress_stage)

		if self.progress_stage == 2:
			self.ensure_masks_initialized()
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
			print("Masking stage")
		elif self.progress_stage == 3:
			self.refresh_display_image()
			print("Select skeleton stage")
		elif self.progress_stage == 4:
			self.refresh_display_image()
			# Always a dict: every other place treats crack_results as one
			# (.pop, .clear, "in"), so it must never become None here.
			self.crack_results = self.calculate_crack_properties() or {}
			print("File export stage")

		if self.ui.listWidget.currentItem():
			self.display_large_image(self.ui.listWidget.currentItem())

	def reset_all_data(self):
		r"""
		Reset all stored data and UI elements to their initial state.
		Clear image paths, prediction results, skeleton results, and crack results.
		Reset UI components such as labels, input fields, and the list widget.
		"""
		self.set_stage(0)
		self.current_image_path = None
		self.prediction_results.clear()
		self.skeleton_results.clear()
		self.crack_results.clear()

		self.ui.listWidget.clear()
		self.ui.imageLabel.clear()
		self.zoom_base_pixmap = None
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
		self.original_pixmap = None
		self.resolution = None
		self.cali_image = None
		self.cali_path = None
		self.cali_points = []
		self.creating_node = None
		self.deleting_node = None
		self.dragged_node = None

	# ------------------------ Project Save/Load ----------------------------------------------------------------------
	def _project_to_relative(self, path, project_dir):
		r"""
		Express `path` relative to `project_dir`, or None if that isn't possible
		(e.g. on Windows, if they're on different drives).
		"""
		try:
			return os.path.relpath(pathlib.Path(path).resolve(), project_dir)
		except ValueError:
			return None

	def export_project(self):
		r"""
		Save the current session (uploaded images, calibration, crack masks, and skeleton
		data, including manual edits) to a single project file so the work can be resumed
		later via "Import Project". Images (and the calibration image) are not copied;
		only their paths are stored, purely relative to the project file, so the file
		contains no local absolute paths and can be shared or moved to another machine
		alongside the images. The file is JSON; masks are PNG-compressed and
		base64-encoded, since a raw pixel dump per mask would make it huge.
		"""
		if self.ui.listWidget.count() == 0:
			QMessageBox.warning(self, "Export Error", "No images to export. Please upload images first.")
			return

		file_path, _ = QFileDialog.getSaveFileName(
			self, "Save Project", "", "Crackpot Project (*.crackpot)"
		)
		if not file_path:
			return
		if not file_path.lower().endswith(".crackpot"):
			file_path += ".crackpot"

		project_dir = pathlib.Path(file_path).resolve().parent
		images = []
		prediction_results = {}
		skeleton_results = {}
		crack_results = {}
		skipped = []
		for i in range(self.ui.listWidget.count()):
			stored_path = self.ui.listWidget.item(i).data(Qt.ItemDataRole.UserRole)
			rel_path = self._project_to_relative(stored_path, project_dir)
			if rel_path is None:
				# Image and project file on different drives (Windows): there is no
				# relative path between them, and we don't fall back to an absolute
				# one, so this image can't be referenced from the project file at all.
				skipped.append(stored_path)
				continue
			images.append(rel_path)

			prediction = self.prediction_results.get(stored_path)
			if prediction is not None:
				mask_u8 = np.clip(np.round(prediction * 255), 0, 255).astype(np.uint8)
				prediction_results[rel_path] = _encode_mask_png(mask_u8)

			skeleton_data = self.skeleton_results.get(stored_path)
			if skeleton_data is not None:
				# branch_points/end_points aren't stored: they're pure functions of
				# "skeleton" and are recomputed on import instead.
				skeleton_results[rel_path] = {
					"skeleton": _encode_mask_png(skeleton_data["skeleton"]),
					"longest_path": skeleton_data.get("longest_path", []),
					"selected_points": skeleton_data.get("selected_points", []),
					"created_nodes": skeleton_data.get("created_nodes", []),
					"created_lines": skeleton_data.get("created_lines", []),
				}

			if stored_path in self.crack_results:
				crack_results[rel_path] = self.crack_results[stored_path]

		cali_image_path = None
		if self.cali_path is not None:
			cali_image_path = self._project_to_relative(self.cali_path, project_dir)
			if cali_image_path is None:
				skipped.append(self.cali_path)

		project_data = {
			"format_version": 4,
			"images": images,
			"cali_image_path": cali_image_path,
			"cali_points": self.cali_points,
			"resolution": self.resolution,
			"prediction_results": prediction_results,
			"skeleton_results": skeleton_results,
			"crack_results": crack_results,
			"progress_stage": self.progress_stage,
		}

		try:
			# A bare file name has no directory part, and os.makedirs("") raises.
			project_dir_to_create = os.path.dirname(file_path)
			if project_dir_to_create:
				os.makedirs(project_dir_to_create, exist_ok=True)
			with open(file_path, "w", encoding="utf-8") as f:
				json.dump(project_data, f, cls=_NumpyJSONEncoder)
			message = f"Project exported successfully:\n{file_path}"
			if skipped:
				message += (
					"\n\nSkipped (on a different drive than the project file, so they "
					"couldn't be referenced by a relative path):\n" + "\n".join(skipped)
				)
			QMessageBox.information(self, "Success", message, QMessageBox.StandardButton.Ok)
		except Exception as e:
			QMessageBox.critical(self, "Export Failed", f"Error:\n{str(e)}")

	def import_project(self):
		r"""
		Load a previously exported project file and restore the full working state
		(images, calibration, crack masks, and skeleton data) to continue where it left
		off. Images that can no longer be found at their path relative to the project
		file are skipped and reported, without failing the rest of the import.
		"""
		file_path, _ = QFileDialog.getOpenFileName(
			self, "Open Project", "", "Crackpot Project (*.crackpot)"
		)
		if not file_path:
			return

		try:
			with open(file_path, "r", encoding="utf-8") as f:
				project_data = json.load(f)
		except Exception as e:
			QMessageBox.critical(self, "Import Failed", f"Error:\n{str(e)}")
			return

		project_dir = pathlib.Path(file_path).resolve().parent

		def resolve(rel_path):
			if not rel_path:
				return None
			candidate = project_dir / rel_path
			return str(candidate) if candidate.exists() else None

		entries = project_data.get("images", [])
		resolved = [(rel_path, resolve(rel_path)) for rel_path in entries]
		found = [(rel_path, current) for rel_path, current in resolved if current is not None]
		missing_paths = [rel_path for rel_path, current in resolved if current is None]

		self.reset_all_data()

		self.resolution = project_data.get("resolution")
		self.cali_points = project_data.get("cali_points", [])

		raw_cali_path = project_data.get("cali_image_path")
		cali_image_path = resolve(raw_cali_path)
		if cali_image_path is not None:
			self.cali_image = cv2.imread(cali_image_path)
			self.cali_path = cali_image_path
		elif raw_cali_path:
			missing_paths.append(raw_cali_path)

		prediction_data = project_data.get("prediction_results", {})
		skeleton_data_raw = project_data.get("skeleton_results", {})
		crack_data = project_data.get("crack_results", {})

		for rel_path, current_path in found:
			pixmap = QPixmap(current_path)
			if pixmap.isNull():
				missing_paths.append(rel_path)
				continue
			item = QListWidgetItem()
			item.setIcon(QIcon(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)))
			item.setData(Qt.ItemDataRole.UserRole, current_path)
			self.ui.listWidget.addItem(item)

			# Every uploaded image gets a prediction_results entry, even if it's just
			# None (not yet detected): run_model_detection() iterates this dict's keys
			# to find images still awaiting detection.
			if rel_path in prediction_data:
				mask_u8 = _decode_mask_png(prediction_data[rel_path])
				self.prediction_results[current_path] = mask_u8.astype(np.float32) / 255.0
			else:
				self.prediction_results[current_path] = None

			if rel_path in skeleton_data_raw:
				entry = skeleton_data_raw[rel_path]
				skeleton = _decode_mask_png(entry["skeleton"])
				self.skeleton_results[current_path] = {
					"skeleton": skeleton,
					"branch_points": self.skeleton_processor.find_branch_points(skeleton),
					"end_points": self.skeleton_processor.find_end_points(skeleton),
					"longest_path": entry.get("longest_path", []),
					"selected_points": entry.get("selected_points", []),
					"created_nodes": [tuple(node) for node in entry.get("created_nodes", [])],
					"created_lines": [
						(tuple(start), tuple(end)) for start, end in entry.get("created_lines", [])
					],
				}

			if rel_path in crack_data:
				self.crack_results[current_path] = crack_data[rel_path]

		self.skeleton_processor.skeletons = self.skeleton_results

		if self.resolution is not None:
			self.ui.resolutionLineEdit.setText(f"{self.resolution:.6f}")

		if self.ui.listWidget.count() > 0:
			self.ui.listWidget.setCurrentRow(0)
			self.display_large_image(self.ui.listWidget.currentItem())

		restored_stage = project_data.get("progress_stage", 0)
		if self.ui.listWidget.count() == 0:
			restored_stage = min(restored_stage, 1)
		self.set_stage(restored_stage)

		if missing_paths:
			QMessageBox.warning(
				self, "Some Images Missing",
				"Project loaded, but the following images could not be found or loaded and "
				"were skipped:\n\n" + "\n".join(missing_paths)
			)
		else:
			QMessageBox.information(self, "Success", "Project loaded successfully.", QMessageBox.StandardButton.Ok)

	# ------------------------ Results Export ----------------------------------------------------------------------
	def missing_export_requirements(self):
		r"""
		Collect the reasons why no results can be calculated yet, in the order the
		user is expected to work through the stages.

		Used to tell the user what is still missing instead of leaving the export
		stage silently empty.

		\return: A list of human-readable reasons. Empty if everything is available.
		"""
		reasons = []
		if not self.prediction_results:
			reasons.append("No crack masks yet. Run the crack detection or draw a mask in the Masking Stage.")
		if self.resolution is None or self.resolution <= 0:
			reasons.append("No calibration yet. Set the resolution in the Calibration Stage.")
		return reasons

	def calculate_crack_properties(self):
		r"""
		Calculate crack properties including area, skeleton length, and average crack width.

		Images without a skeleton are still included, with a skeleton length of zero,
		so that a partly processed session yields results for the images that are ready
		instead of failing as a whole.

		\return: A dictionary containing calculated crack properties for each image.
		It is empty if the requirements are not met yet.
		"""
		if self.missing_export_requirements():
			return {}

		crack_results = {}

		for image_path, prediction in self.prediction_results.items():
			if prediction is None:
				# Imported projects can carry images whose mask was never stored.
				continue

			crack_region_pixels = np.sum(prediction == 1)
			crack_area_mm2 = crack_region_pixels * (self.resolution ** 2)

			# Images that were never skeletonized have no entry here. They are treated
			# as an empty skeleton, just like in the Skeleton Extraction Stage, instead
			# of failing the whole calculation.
			skeleton_data = self.skeleton_results.get(image_path) or self.empty_skeleton_result(prediction.shape[:2])
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
		r"""
		Open a file dialog to select the export file path, ensure it has a .csv extension and update the export path field.
		"""

		options = QFileDialog.Option(0)
		file_path, _ = QFileDialog.getSaveFileName(
			self, "Select Export File", "", "CSV Files (*.csv);;All Files (*)", options=options
		)

		if file_path:
			if not file_path.lower().endswith(".csv"):
				file_path += ".csv"

			self.ui.exportPathLineEdit.setText(file_path)

	def export_to_csv(self):
		r"""
		Export crack analysis results to a CSV file.
		"""
		file_path = self.ui.exportPathLineEdit.text().strip()

		if not file_path:
			QMessageBox.warning(self, "Export Error", "Please select a file path!")
			return

		if not self.crack_results:
			# Name the missing step instead of only stating that there is no data,
			# so the user knows which stage to go back to.
			reasons = self.missing_export_requirements()
			message = "No valid data to export!"
			if reasons:
				message += "\n\n" + "\n".join(reasons)
			QMessageBox.warning(self, "Export Error", message)
			return

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
				"Crack Pixel (px)": crack_pixels,
				"Skeleton Pixel (px)": skeleton_pixels,
				"Crack Area (mm²)": crack_area,
				"Skeleton length (mm)": skeleton_length,
				"Mean Crack Width (mm)": crack_width,
				"Resolution (mm/px)": self.resolution
			})

		df = pd.DataFrame(data_list)

		try:
			# Only create a directory if one was given: a bare file name has no
			# directory part, and os.makedirs("") raises instead of doing nothing.
			export_dir = os.path.dirname(file_path)
			if export_dir:
				os.makedirs(export_dir, exist_ok=True)
			df.to_csv(file_path, index=False, encoding="utf-8-sig")
			QMessageBox.information(self, "Success", f"File exported successfully:\n{file_path}", QMessageBox.StandardButton.Ok)
		except Exception as e:
			QMessageBox.critical(self, "Export Failed", f"Error:\n{str(e)}")
	# ------------------------ Global UI Functions ----------------------------------------------------------------------

	def set_display_pixmap(self, pixmap):
		r"""
		Show a freshly built pixmap in the image label and remember it as the
		base for zooming.

		Every zoom step is recomputed from this untouched base pixmap (see
		zoom_image) instead of rescaling the already scaled pixmap that is
		currently shown. This prevents the image from being resampled over and
		over again, which otherwise makes it progressively blurrier with each
		zoom cycle.

		\param pixmap: The QPixmap to display and store as the zoom base.
		"""
		self.zoom_base_pixmap = pixmap
		self.zoom_factor = 1.0
		self.ui.imageLabel.setPixmap(pixmap)

	def zoom_image(self, zoom_in=True):
		r"""
		Zoom in or out on the displayed image.

		The zoomed view is always derived from the unscaled base pixmap and the
		accumulated zoom factor, using nearest-neighbor scaling
		(FastTransformation). Pixels are therefore shown as discrete blocks
		without interpolation, keeping the image and the skeleton lines crisp
		and free of progressive degradation.

		\param zoom_in: Boolean flag to determine zoom direction (True for in, False for out).
		"""
		if self.zoom_base_pixmap is None:
			return

		scale_factor = 1.1 if zoom_in else 1 / 1.1
		new_factor = self.zoom_factor * scale_factor

		new_width = int(self.zoom_base_pixmap.width() * new_factor)
		new_height = int(self.zoom_base_pixmap.height() * new_factor)

		if new_width < 50 or new_height < 50:
			return
		if new_width > 5000 or new_height > 5000:
			return

		self.zoom_factor = new_factor
		scaled_pixmap = self.zoom_base_pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation)

		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.ui.imageLabel.adjustSize()
		self.refresh_cursor_if_drawing()

	def refresh_cursor_if_drawing(self):
		r"""
		Refresh the brush cursor after a zoom change, but only while the drawing stage
		is active, so its size keeps matching the current zoom factor.
		"""
		if self.progress_stage == 2:
			self.update_cursor()

	def zoom_fit_to_window(self):
		r"""
		Scale the displayed image to fit entirely within the visible viewport, keeping the aspect ratio.
		"""
		if self.original_pixmap is None:
			return

		viewport_size = self.ui.scrollArea.viewport().size()
		scaled_pixmap = self.original_pixmap.scaled(
			viewport_size.width(), viewport_size.height(),
			Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
		)
		self.ui.imageLabel.setPixmap(scaled_pixmap)
		self.ui.imageLabel.adjustSize()

	def zoom_one_to_one(self):
		r"""
		Display the image at its native resolution, so one image pixel corresponds to one screen pixel.
		"""
		if self.original_pixmap is None:
			return

		self.ui.imageLabel.setPixmap(self.original_pixmap)
		self.ui.imageLabel.adjustSize()

	def delete_current_image(self):
		r"""
		Delete the currently selected image from the list and clear associated data (prediction results,
		skeleton results, and crack results). It will prompt the user for confirmation before delete it.
		"""
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
			self.original_pixmap = None
			self.ui.imageLabel.clear()
			self.zoom_base_pixmap = None
			if self.progress_stage == 3:
				self.ui.fileNameLabel.clear()
				self.ui.crackWidthLabel.clear()

	def show_previous_image(self):
		r"""
		Navigate to and display the previous image in the list.
		"""
		current_row = self.ui.listWidget.currentRow()
		if current_row > 0:
			self.ui.listWidget.setCurrentRow(current_row - 1)
			self.display_large_image(self.ui.listWidget.currentItem())

	def show_next_image(self):
		r"""
		Navigate to and display the next image in the list.
		"""
		current_row = self.ui.listWidget.currentRow()
		if current_row < self.ui.listWidget.count() - 1:
			self.ui.listWidget.setCurrentRow(current_row + 1)
			self.display_large_image(self.ui.listWidget.currentItem())

	def show_and_check_config(self):
		r"""
		Display the main window and verify configuration settings.
		"""
		self.show()
		# todo: config file


def main():
	r"""
	Initialize and run the application.
	"""
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show_and_check_config()
	sys.exit(app.exec_())
