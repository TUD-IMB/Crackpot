import base64
import json
import math
import os
import pathlib
import sys
import cv2
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QEvent, QPoint, QSettings, QTranslator
from PySide6.QtGui import QAction, QPixmap, QIcon, QImage, QPainter, QColor, QPen, QCursor, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget, QSlider, \
	QMessageBox, QToolTip, QAbstractButton, QProgressDialog, QColorDialog
from skimage.measure import regionprops,label
from crackpot.backend.edgedetection import EdgeDetection, MISSING_BACKEND_HINT, is_detection_available
from crackpot.backend.maskprocessor import MaskProcessor
from crackpot.backend.skeletonprocessor import SkeletonProcessor
from crackpot.frontend.aboutdialog import AboutDialog
from crackpot.frontend.documentationdialog import DocumentationDialog
from crackpot.frontend.progressmanager import ProgressManager
from crackpot.frontend.ui.uimain import Ui_MainWindow
from skimage.morphology import skeletonize

from crackpot.utils.utils import resource_path

# Radius of a manually placed node in image pixels. The overlay draws the node
# with it and get_clicked_node() uses it as the click tolerance, so everything
# that can be seen can also be hit.
NODE_RADIUS = 5
# Radius a calibration point is marked with, in image pixels.
CALIBRATION_POINT_RADIUS = 10
# Color the brush cursor is drawn in until the user picks another one. Red reads
# better on the bright concrete these photographs usually show than yellow does.
DEFAULT_CURSOR_COLOR = '#ff0000'


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


# Result keys written before the units were spelled out. Projects saved with those
# versions still carry the old names, so they are renamed on the way in instead of
# leaving the export and the result labels with missing values.
_RENAMED_CRACK_RESULT_KEYS = {
	"crack_area": "crack_area_mm2",
	"skeleton_length": "skeleton_length_mm",
	"crack_width": "crack_width_mm",
}


def _migrate_crack_result(result):
	r"""
	Bring one stored crack result entry up to the current key names.

	\param result: The entry as it was read from the project file.
	\return: A new dictionary using the current key names.
	"""
	return {_RENAMED_CRACK_RESULT_KEYS.get(key, key): value for key, value in result.items()}


class MainWindow(QMainWindow):
	r"""
	Main User Interface for the application.
	"""

	DETECTION_METHOD_NONE = "None"

	CSV_EXPORT_FILTER = "CSV Files (*.csv)"
	EXCEL_EXPORT_FILTER = "Excel Files (*.xlsx)"
	EXPORT_COLUMN_WIDTH_PX = 150

	def __init__(self):
		super().__init__()

		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)

		self.settings = QSettings()
		self.translator = QTranslator(self)
		self.switch_language(self.settings.value('language', 'english'))
		self.cursor_color = self.stored_cursor_color()

		self.progress_stage = 0
		self.current_image_path = None
		self.prediction_results = {}
		self.skeleton_results = {}
		self.crack_results = {}
		self.skeleton_processor = SkeletonProcessor()
		self.mask_processor = MaskProcessor()

		self.ui.imageListWidget.setViewMode(QListWidget.ViewMode.IconMode)
		self.ui.imageListWidget.setSpacing(10)
		self.ui.imageListWidget.setResizeMode(QListWidget.ResizeMode.Adjust)
		# todo: multi selection
		# self.ui.imageListWidget.setSelectionMode(QAbstractItemView.MultiSelection)

		self.ui.imageListWidget.itemClicked.connect(self.display_large_image)
		self.ui.previousFigButton.clicked.connect(self.show_previous_image)
		self.ui.nextFigButton.clicked.connect(self.show_next_image)

		self.edge_detector = None
		self.configure_detection_availability()

		self.progress_manager = ProgressManager(
			buttons=[
				self.ui.calibrationProcessButton,
				self.ui.uploadProcessButton,
				self.ui.maskingProcessButton,
				self.ui.skeletonProcessButton,
				self.ui.exportProcessButton
			],
			lines=[self.ui.stageSeparator0, self.ui.stageSeparator1, self.ui.stageSeparator2, self.ui.stageSeparator3],
			recolor_icon=self.recolor_icon,
			default_color=self.palette().color(QPalette.ColorRole.ButtonText)
		)
		self.ui.calibrationProcessButton.clicked.connect(lambda: self.set_stage(0))
		self.ui.uploadProcessButton.clicked.connect(lambda: self.set_stage(1))
		self.ui.maskingProcessButton.clicked.connect(lambda: self.set_stage(2))
		self.ui.skeletonProcessButton.clicked.connect(lambda: self.set_stage(3))
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
		# The layer the brush paints on: the mask in the masking stage, the skeleton
		# overlay in the skeleton stage. Kept as a QImage because QPainter writes to
		# it directly, unlike the NumPy masks in prediction_results.
		self.editable_qimage = None
		self.original_pixmap = None
		self.zoom_base_pixmap = None
		self.zoom_factor = 1.0
		self.overlay_scale_in_use = NODE_RADIUS
		self.keep_zoom_on_refresh = False

		self.init_stacked_widget()
		self.init_image_label()
		self.apply_icon_color()

		# Only now do the stage buttons carry the icons the color scheme asks for,
		# and only those are worth remembering as the unmarked state.
		self.progress_manager.capture_icons()
		self.progress_manager.update_progress(self.progress_stage)

		# Which of the two skeleton editing modes a click is handled as. Mutually
		# exclusive: turning one on turns the other off (see toggle_add_node_mode).
		self.add_node_mode = False
		self.delete_node_mode = False
		self.dragged_node = None

		self.resolution = None
		self.calibration_image = None
		self.calibration_path = None
		self.calibration_points = []
		# Where this session was last saved to, so "Finish" can tell an already
		# written project from one that would be lost.
		self.project_path = None

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
		self.ui.stageStack.setCurrentIndex(self.progress_stage)

		# File menu
		self.ui.actionExportProject.triggered.connect(self.export_project)
		self.ui.actionImportProject.triggered.connect(self.import_project)
		self.ui.actionExit.triggered.connect(self.close)

		# Help menu
		self.ui.actionDocumentation.triggered.connect(self.show_documentation_dialog)
		self.ui.actionAbout.triggered.connect(self.show_about_dialog)

		# On macOS, Qt guesses at "About"/"Quit" etc. by their English label text and
		# moves them into the app menu - which then hides them under English, but not
		# under the German translation ("Über"/"Beenden"). Pinning the role keeps every
		# action in the menu main.ui puts it in, regardless of language or platform.
		for action in (self.ui.actionAbout, self.ui.actionDocumentation, self.ui.actionExit):
			action.setMenuRole(QAction.MenuRole.NoRole)

		# Setting menu
		self.ui.actionEnglish.triggered.connect(lambda: self.switch_language('english'))
		self.ui.actionGerman.triggered.connect(lambda: self.switch_language('german'))
		self.ui.actionCursorColor.triggered.connect(self.choose_cursor_color)

		self.ui.nextButton0.clicked.connect(lambda: self.set_stage(1))
		self.ui.nextButton1.clicked.connect(lambda: self.set_stage(2))
		self.ui.nextButton2.clicked.connect(lambda: self.set_stage(3))
		self.ui.nextButton3.clicked.connect(lambda: self.set_stage(4))
		self.ui.nextButton4.clicked.connect(self.finish_session)

		self.ui.previousButton1.clicked.connect(lambda: self.set_stage(0))
		self.ui.previousButton2.clicked.connect(lambda: self.set_stage(1))
		self.ui.previousButton3.clicked.connect(lambda: self.set_stage(2))
		self.ui.previousButton4.clicked.connect(lambda: self.set_stage(3))

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
		# The circle only stands where a click places something, so switching a mode
		# switches it on or off.
		self.ui.clickAddButton.clicked.connect(self.update_cursor)
		self.ui.clickDeleteButton.clicked.connect(self.update_cursor)
		# self.ui.adjustNodeButton.clicked.connect(self.toggle_adjust_node_mode)
		self.ui.hintsButton.setVisible(False)
		self.ui.addNodeHintLabel.setVisible(False)
		self.ui.newSegmentHintLabel.setVisible(False)
		self.ui.deleteNodeHintLabel.setVisible(False)

		# export stage
		self.ui.exportButton.clicked.connect(self.export_to_csv)

	# ------------------------ Calibration ----------------------------------------------------------------------
	def upload_calibration_image(self):
		r"""
		Open a file dialog to select a calibration image, load it, and initialize calibration points list.
		"""
		calibration_file_path, _ = QFileDialog.getOpenFileName(
			self, "Select a Calibration Picture", "", "Images (*.png *.jpg *.jpeg *.bmp)"
		)
		if not calibration_file_path:
			return
		self.calibration_image = cv2.imread(calibration_file_path)
		if self.calibration_image is None:
			QMessageBox.warning(self, self.tr("Error"), self.tr("Failed to load the image."))
			return
		self.calibration_path = calibration_file_path
		self.calibration_points.clear()
		self.display_calibration_image()

	def calculate_pixel_distance(self):
		r"""
		Calculate the pixel distance between two selected calibration points.
		Update the pixel distance value in the UI if exactly two points are selected.
		Clear the pixel distance field if the number of points is incorrect.
		"""
		if len(self.calibration_points) != 2:
			self.ui.pixelLineEdit.clear()
			return
		calibration_point_array = np.array(self.calibration_points)
		pixel_distance = np.linalg.norm(calibration_point_array[1] - calibration_point_array[0])
		self.ui.pixelLineEdit.setText(str(pixel_distance))

	def display_calibration_image(self, keep_zoom=False):
		r"""
		Display the calibration image with marked calibration points.

		\param keep_zoom: Keep the current zoom factor instead of returning to the
			overview. Used when only a point was added or removed, so that marking
			a distance in a zoomed in view does not throw the user back out of it.
		"""
		if self.calibration_image is not None:
			marked_image = cv2.cvtColor(self.calibration_image.copy(), cv2.COLOR_BGR2RGB)
			for point in self.calibration_points:
				cv2.circle(marked_image, point, CALIBRATION_POINT_RADIUS, (255, 0, 0), -1)
			height, width, channels = marked_image.shape
			bytes_per_line = 3 * width
			marked_qimage = QImage(marked_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
			pixmap = QPixmap.fromImage(marked_qimage)
			self.original_pixmap = pixmap
			# Handed over at full resolution, like in every other stage:
			# set_display_pixmap() scales it to the zoom factor itself. Pre-scaling
			# it to the label size here made the two disagree about how large the
			# image is, which is what moved the marks away from the cursor.
			self.set_display_pixmap(pixmap, keep_zoom=keep_zoom)

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
				QMessageBox.information(
					self, self.tr("Success"),
					self.tr("Current resolution: {value} mm/px saved").format(value=f"{self.resolution:.6f}"),
					QMessageBox.StandardButton.Ok
				)
			except ValueError:
				QMessageBox.warning(
					self, self.tr("Invalid resolution"),
					self.tr("The resolution is not a valid number. Calculate it again from two "
							"calibration points and the distance between them.")
				)
		else:
			QMessageBox.warning(
				self, self.tr("No resolution"),
				self.tr("No resolution yet. Mark two calibration points, enter the distance "
						"between them and confirm afterwards.")
			)

	# ------------------------ Skeleton Adjust ----------------------------------------------------------------------

	def toggle_add_node_mode(self):
		r"""
		Toggle the mode for adding skeleton nodes in the skeleton editing process.
		"""
		if self.ui.nodeAddButton.isChecked():
			self.add_node_mode = True
			self.delete_node_mode = False
			self.ui.nodeDeleteButton.setChecked(False)
			self.ui.hintsButton.setVisible(True)
			self.ui.addNodeHintLabel.setVisible(True)
			self.ui.newSegmentHintLabel.setVisible(True)
			self.ui.deleteNodeHintLabel.setVisible(False)
		else:
			self.add_node_mode = False
			self.ui.hintsButton.setVisible(False)
			self.ui.addNodeHintLabel.setVisible(False)
			self.ui.newSegmentHintLabel.setVisible(False)
			self.ui.deleteNodeHintLabel.setVisible(False)
		self.update_cursor()

	def toggle_delete_node_mode(self):
		r"""
		Toggle the mode for deleting skeleton nodes in the skeleton editing process.
		"""
		if self.ui.nodeDeleteButton.isChecked():
			self.delete_node_mode = True
			self.add_node_mode = False
			self.ui.nodeAddButton.setChecked(False)
			self.ui.hintsButton.setVisible(True)
			self.ui.addNodeHintLabel.setVisible(False)
			self.ui.newSegmentHintLabel.setVisible(False)
			self.ui.deleteNodeHintLabel.setVisible(True)
		else:
			self.delete_node_mode = False
			self.ui.hintsButton.setVisible(False)
			self.ui.addNodeHintLabel.setVisible(False)
			self.ui.newSegmentHintLabel.setVisible(False)
			self.ui.deleteNodeHintLabel.setVisible(False)
		self.update_cursor()

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

		if self.ui.imageListWidget.currentItem():
			self.display_large_image(self.ui.imageListWidget.currentItem())

		self.skeleton_processor.skeletons = self.skeleton_results
		self.refresh_display_image()

	def clean_skeleton_branches(self, all_images=False):
		r"""
		Remove short side branches from the skeleton and keep the longest path.

		Only the branches hanging off the line are removed, and only as a whole
		(see SkeletonProcessor.remove_small_branches). The line itself keeps its
		length however often this is run, so the button can be pressed repeatedly
		with a larger threshold until the skeleton looks right.

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
			largest_component = self.get_largest_skeleton_component(clean_skeleton)
			branch_points = self.skeleton_processor.find_branch_points(clean_skeleton)
			end_points = self.skeleton_processor.find_end_points(clean_skeleton)

			# Update in place instead of replacing the entry: the manually drawn nodes
			# and lines belong to the image, not to the automatic skeleton, and must
			# survive a cleaning run.
			skeleton_data["skeleton"] = clean_skeleton
			skeleton_data["branch_points"] = branch_points
			skeleton_data["end_points"] = end_points
			# Key stays "longest_path" so existing .crackpot project files keep loading.
			skeleton_data["longest_path"] = largest_component

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

	def get_largest_skeleton_component(self, skeleton):
		r"""
		Return the coordinates of the largest connected component of the skeleton,
		measured by pixel count.

		Note that this is not the longest *path* through the skeleton: a component
		with many short side branches can outweigh a longer but thinner one. The
		result is currently only stored, never drawn (see refresh_display_image).

		\param skeleton: A binary skeletonized image.
		\return: An array of coordinates of the largest component, empty if none.
		"""
		labeled_skeleton = label(skeleton, connectivity=2)

		largest_component = []
		max_size = 0

		for region in regionprops(labeled_skeleton):
			coords = region.coords
			size = len(coords)

			if size > max_size:
				max_size = size
				largest_component = coords
		return largest_component

	# ------------------------ Event Handling ----------------------------------------------------------------------
	def convert_to_image_coords(self, pos, img_size):
		r"""
		Calculate the position in the image the cursor points at.

		The scale is the zoom factor, the same one render_current_view() draws
		with and overlay_line_scale() measures the markers in. Deriving it from
		the label size instead only holds while the image fills that label: the
		layout stretches it to the viewport (scrollArea is widgetResizable), so
		an image smaller than the viewport - or one zoomed out - sits centred
		(AlignCenter) in a much larger label that says nothing about how large an
		image pixel is on screen. A click was then read as if the image covered
		the whole label, which happens to be exact in the middle and drifts
		further off towards the edges: the offset between cursor and stroke,
		worth up to 90 image pixels on a small image.

		The label size is still read, for the offset. That only holds as long as it
		does not change while the user draws, which is why render_current_view()
		must not call adjustSize().

		\param pos: The QPoint position of the cursor in the UI.
		\param img_size: The size of the original image (height, width).
		\return: The converted image coordinates (x, y). They may lie outside the
			image, see position_is_on_image().
		"""
		if img_size[0] <= 0 or img_size[1] <= 0:
			return -1, -1

		label_size = self.ui.imageLabel.size()
		scale = self.zoom_factor if self.zoom_factor > 0 else 1.0
		display_width = scale * img_size[1]
		display_height = scale * img_size[0]
		# The image is centred in the label, so half of whatever the label has
		# left over is the offset. It can be negative: fit-to-window measures the
		# viewport, while the label is a little smaller than that because of the
		# layout margins, so a fitted image is a few pixels larger than the label
		# showing it and is cropped evenly instead of leaving a margin.
		x_offset = (label_size.width() - display_width) / 2
		y_offset = (label_size.height() - display_height) / 2
		# floor, not int: int() rounds towards zero, which would pull a click just
		# left of or above the image onto its first column or row.
		img_x = math.floor((pos.x() - x_offset) / scale)
		img_y = math.floor((pos.y() - y_offset) / scale)
		return img_x, img_y

	def position_is_on_image(self, position, img_size):
		r"""
		Tell whether converted coordinates point at a pixel of the image.

		A click can land in the empty area of the label beside the image, which
		converts to coordinates outside it. Acting on those would place a point
		or a stroke somewhere the user never clicked.

		\param position: The (x, y) image coordinates from convert_to_image_coords().
		\param img_size: The size of the original image (height, width).
		\return (bool): True if the position lies inside the image.
		"""
		x, y = position
		return 0 <= x < img_size[1] and 0 <= y < img_size[0]

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
				img_size = self.calibration_image.shape if self.calibration_image is not None else (1, 1, 1)
				img_x, img_y = self.convert_to_image_coords(clicked_pos, img_size)
				if not self.position_is_on_image((img_x, img_y), img_size):
					# Beside the image, not on it: the label is larger than the
					# image whenever that does not fill the viewport.
					return True

				if self.ui.clickAddButton.isChecked():
					if len(self.calibration_points) < 2:
						self.calibration_points.append((int(img_x), int(img_y)))
					else:
						self.calibration_points = [(img_x, img_y)]
					# QMessageBox.warning(self, "Warning", "Only two points can be marked!")
				elif self.ui.clickDeleteButton.isChecked():
					for point in self.calibration_points:
						if abs(point[0] - img_x) < 10 and abs(point[1] - img_y) < 10:
							self.calibration_points.remove(point)
							break
				self.calculate_pixel_distance()
				# Marking a point is an edit of the overlay, not a change of image:
				# falling back to the overview here would undo the zoom the user
				# needed to place the point precisely in the first place.
				self.display_calibration_image(keep_zoom=True)
				return True

		if self.progress_stage == 2:
			if event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
				self.drawing = True
				self.last_point = event.pos()
				# Paint right away, so a click without any mouse movement leaves a
				# mark instead of doing nothing.
				self.draw_on_image(event.pos())
			elif event.type() == QEvent.Type.MouseMove and self.drawing:
				self.draw_on_image(event.pos())
			elif event.type() == QEvent.Type.MouseButtonRelease and event.button() == Qt.MouseButton.LeftButton:
				self.drawing = False
				if self.editable_qimage is not None and self.current_image_path is not None:
					updated_array = self.qimage_to_numpy(self.editable_qimage)
					updated_array = updated_array.astype(np.float32) / 255.0
					self.prediction_results[self.current_image_path] = updated_array

		elif self.progress_stage == 3:
			if self.add_node_mode and event.type() == QEvent.Type.MouseButtonPress:
				clicked_pos = event.pos()
				if self.editable_qimage:
					if event.button() == Qt.MouseButton.LeftButton:
						self.create_node(clicked_pos, connect_to_previous=True)
					elif event.button() == Qt.MouseButton.RightButton:
						self.create_node(clicked_pos, connect_to_previous=False)
			elif self.delete_node_mode and event.type() == QEvent.Type.MouseButtonPress and event.button() == Qt.MouseButton.LeftButton:
				clicked_pos = event.pos()
				if self.editable_qimage:
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
		if not self.position_is_on_image((img_x, img_y), img_size):
			return

		new_node = (int(img_x), int(img_y))

		if not connect_to_previous:
			skeleton_data["created_nodes"].append(new_node)
			# Placing a node is an edit of the overlay, not a change of image: falling
			# back to the overview here would undo the zoom before the next click.
			self.refresh_display_image(keep_zoom=True)
			return

		if len(skeleton_data["created_nodes"]) > 0:
			last_node = skeleton_data["created_nodes"][-1]
			skeleton_data.setdefault("created_lines", []).append((last_node, new_node))

		skeleton_data["created_nodes"].append(new_node)
		self.refresh_display_image(keep_zoom=True)

	def delete_node(self, clicked_pos):
		r"""
		Remove the node that was clicked on and close the gap it leaves behind.

		A node in the middle of a drawn chain has a node on either side of it; those
		two are connected directly, so the line stays in one piece instead of falling
		apart at that point. A click that does not hit any node goes to the automatic
		skeleton instead (see delete_skeleton_segment).

		\param clicked_pos: The QPoint position where the user clicked.
		"""
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data:
			return

		closest_node = self.get_clicked_node(clicked_pos)
		if not closest_node or closest_node not in skeleton_data["created_nodes"]:
			self.delete_skeleton_segment(clicked_pos)
			return

		lines = skeleton_data.get("created_lines", [])
		neighbor_nodes = [start if end == closest_node else end
						  for start, end in lines if closest_node in (start, end)]

		skeleton_data["created_nodes"].remove(closest_node)
		skeleton_data["created_lines"] = [line for line in lines if closest_node not in line]

		# Two neighbors mean the node sat between them, so the line continues from one
		# to the other. With one neighbor it was the end of a chain and there is
		# nothing to bridge.
		if len(neighbor_nodes) == 2 and neighbor_nodes[0] != neighbor_nodes[1]:
			skeleton_data["created_lines"].append((neighbor_nodes[0], neighbor_nodes[1]))

		self.refresh_display_image(keep_zoom=True)

	def delete_skeleton_segment(self, clicked_pos):
		r"""
		Remove the piece of the automatic skeleton that was clicked on.

		The piece is the same unit the branch cleanup works with: the line between
		two forks, or between a fork and a loose end. This is the manual counterpart
		to "remove branches shorter than" - a wrong branch that is too long for the
		threshold, or one that has to go although it is long enough, can be taken out
		by hand without touching the rest of the crack.

		\param clicked_pos: The QPoint position where the user clicked.
		"""
		skeleton_data = self.skeleton_results.get(self.current_image_path)
		if not skeleton_data or skeleton_data.get("skeleton") is None:
			return

		skeleton = skeleton_data["skeleton"]
		img_x, img_y = self.convert_to_image_coords(clicked_pos, skeleton.shape)
		segments = self.skeleton_processor.find_branch_segments(skeleton)
		clicked_segment = self.find_clicked_segment(segments, (img_y, img_x))
		if clicked_segment is None:
			return

		junction_zones = self.skeleton_processor.find_junction_zones(skeleton)
		self.skeleton_processor.remove_pixels(skeleton, clicked_segment["pixels"], junction_zones)
		skeleton_data["branch_points"] = self.skeleton_processor.find_branch_points(skeleton)
		skeleton_data["end_points"] = self.skeleton_processor.find_end_points(skeleton)
		self.refresh_display_image(keep_zoom=True)

	def find_clicked_segment(self, segments, position):
		r"""
		Find the skeleton segment a click was meant for.

		\param segments: The segments as returned by find_branch_segments().
		\param position: The clicked position as (row, col) in image coordinates.
		\return: The closest segment, or None if the click was too far away from all
			of them.
		"""
		pixels = [pixel for segment in segments for pixel in segment["pixels"]]
		if not pixels:
			return None
		owners = [index for index, segment in enumerate(segments) for _ in segment["pixels"]]

		coordinates = np.array(pixels)
		distances = np.hypot(coordinates[:, 0] - position[0], coordinates[:, 1] - position[1])
		nearest = int(np.argmin(distances))
		# Same tolerance as for the nodes, so both react to a click the same way.
		if distances[nearest] > self.node_click_tolerance():
			return None
		return segments[owners[nearest]]

	def node_click_tolerance(self):
		r"""
		Return how far a click may miss a node and still count as hitting it, in
		image pixels.

		It follows the radius the node is drawn with, which is measured in screen
		pixels: a fixed number of image pixels would shrink to well under a screen
		pixel in the zoomed out overview, which is what made the nodes so hard to
		hit. Zoomed in the radius gets small in image pixels instead, so it never
		falls below the drawn size at zoom 1 - hitting a node should not turn into
		pixel-precise aiming.

		\return (float): The tolerance in image pixels.
		"""
		return max(NODE_RADIUS * self.overlay_line_scale(), NODE_RADIUS)

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

		threshold = self.node_click_tolerance()

		nodes = np.array(created_nodes)
		distances = np.linalg.norm(nodes - np.array([img_x, img_y]), axis=1)
		min_index = np.argmin(distances)
		min_dist = distances[min_index]

		if min_dist < threshold:
			return tuple(created_nodes[min_index])

		return None

	def qimage_to_numpy(self, qimage: QImage):
		r"""
		Convert a QImage object to a NumPy array.

		\param qimage: The QImage to be converted.
		\return: A NumPy array representing the image.
		"""
		qimage = qimage.convertToFormat(QImage.Format.Format_Grayscale8)
		width = qimage.width()
		height = qimage.height()
		# QImage pads every row out to a four byte boundary, so a row in the buffer is
		# bytesPerLine wide, not width. Reshaping to the width alone raised a
		# ValueError for every width that is not a multiple of four - three widths out
		# of four - which took the program down when the mask was read back after a
		# brush stroke. np.array copies, so the padded view does not outlive the
		# converted image it belongs to.
		padded = np.array(qimage.bits(), dtype=np.uint8).reshape(height, qimage.bytesPerLine())
		return padded[:, :width]

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
		if self.editable_qimage is None:
			return

		image_size = self.editable_qimage.size()
		x1, y1 = self.convert_to_image_coords(self.last_point, (image_size.height(), image_size.width()))
		x2, y2 = self.convert_to_image_coords(current_point, (image_size.height(), image_size.width()))

		# Carried along even when nothing is drawn. Leaving it on the last position
		# inside the image meant that coming back after a trip outside drew a line
		# across everything in between, the reported jumping stroke. There is room for
		# such a trip whenever the image is smaller than the viewport, because the
		# label then keeps empty space around it.
		self.last_point = current_point

		if not self.segment_touches_image((x1, y1), (x2, y2), image_size):
			return

		painter = QPainter(self.editable_qimage)
		pen = QPen(self.brush_color)
		pen.setWidth(self.brush_size)
		pen.setCapStyle(self.pen_cap_style)
		painter.setPen(pen)

		if (int(x1), int(y1)) == (int(x2), int(y2)):
			# A zero length line has no direction, so QPainter draws nothing for a
			# round cap. drawPoint applies the pen shape and covers a plain click.
			painter.drawPoint(int(x1), int(y1))
		else:
			painter.drawLine(int(x1), int(y1), int(x2), int(y2))
		painter.end()

		self.refresh_display_after_draw()

	def segment_touches_image(self, start, end, image_size):
		r"""
		Tell whether a stroke from start to end can put paint on the image at all.

		QPainter clips to the image by itself, so this is not about correctness but
		about cost: refresh_display_after_draw() rereads the file and rebuilds the
		whole overlay, which is not worth doing for a stroke dragged around in the
		empty area beside the image. The bounding box of the segment is widened by
		half the brush width, because a thick pen reaches into the image from just
		outside it. A box test never rejects a segment that does cross the image; a
		diagonal one may pass the test without touching it, which costs one redraw.

		\param start: The (x, y) image coordinates the segment starts at.
		\param end: The (x, y) image coordinates the segment ends at.
		\param image_size: The QSize of the image being drawn on.
		\return (bool): True if the segment may reach the image.
		"""
		reach = self.brush_size / 2
		left = min(start[0], end[0]) - reach
		right = max(start[0], end[0]) + reach
		top = min(start[1], end[1]) - reach
		bottom = max(start[1], end[1]) + reach
		return (right >= 0 and left < image_size.width()
				and bottom >= 0 and top < image_size.height())

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

	def cursor_circle_size(self):
		r"""
		Return the size the cursor circle should have in screen pixels, or 0 where
		no circle belongs.

		The circle shows what a click is about to put on the image, so it follows
		whatever the current stage places there. The two sizes are measured in
		different units, which is why they are converted differently:
		CALIBRATION_POINT_RADIUS and the brush size are image pixels and therefore
		grow with the zoom, while NODE_RADIUS is a screen size already (see
		overlay_size_in_pixels), so a node keeps its size at every zoom level.

		A stage that puts nothing on the image, and a mode that is not switched on,
		get no circle: the plain arrow then says that a click does nothing here.

		\return (int): The diameter in screen pixels, 0 for no circle.
		"""
		if self.progress_stage == 0:
			if not (self.ui.clickAddButton.isChecked() or self.ui.clickDeleteButton.isChecked()):
				return 0
			return max(int(round(2 * CALIBRATION_POINT_RADIUS * self.zoom_factor)), 1)

		if self.progress_stage == 2:
			return max(int(round(self.brush_size * self.zoom_factor)), 1)

		if self.progress_stage == 3:
			if not (self.add_node_mode or self.delete_node_mode):
				return 0
			return max(2 * NODE_RADIUS, 1)

		return 0

	def update_cursor(self):
		r"""
		Draw the cursor circle for the current stage, so that what a click will put
		on the image can be seen before the click happens.

		The size comes from cursor_circle_size(), the color from the setting behind
		the Setting menu. The masking stage additionally follows the shape of the
		pen; a calibration point and a node are round whatever the pen is set to.
		"""
		# No circle where there is nothing to click on. A stage can be entered with
		# an empty window, and the circle then stood in the grey background with no
		# image under it.
		shown = self.ui.imageLabel.pixmap()
		size = self.cursor_circle_size()
		if size <= 0 or shown is None or shown.isNull():
			self.ui.imageLabel.unsetCursor()
			return

		# Add a small margin so the outline stays fully visible even for tiny radii.
		margin = 2
		pixmap_size = size + 2 * margin
		cursor_pixmap = QPixmap(pixmap_size, pixmap_size)
		cursor_pixmap.fill(Qt.GlobalColor.transparent)
		painter = QPainter(cursor_pixmap)
		pen = QPen(self.cursor_color)
		pen.setWidth(2)
		painter.setPen(pen)

		if self.progress_stage == 2 and self.pen_cap_style == Qt.PenCapStyle.SquareCap:
			painter.drawRect(margin, margin, size, size)
		else:
			painter.drawEllipse(margin, margin, size, size)
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

	def stored_cursor_color(self):
		r"""
		Read the brush cursor color from the settings.

		\return: The stored color, or the default one if nothing readable is stored.
			The settings file can be edited by hand, so an unusable entry must not
			leave the cursor without a color.
		"""
		color = QColor(self.settings.value('cursor_color', DEFAULT_CURSOR_COLOR))
		return color if color.isValid() else QColor(DEFAULT_CURSOR_COLOR)

	def choose_cursor_color(self):
		r"""
		Let the user pick the color of the brush cursor and keep the choice for the
		next start.

		The circle is drawn on top of the photograph, so no single color works on
		every image: a light crack surface swallows yellow, a dark one swallows
		blue. Which one is readable is something only the person looking at the
		picture can decide.
		"""
		color = QColorDialog.getColor(self.cursor_color, self, self.tr("Cursor Color"))
		# An invalid color means the dialog was cancelled.
		if not color.isValid():
			return

		self.cursor_color = color
		self.settings.setValue('cursor_color', color.name())
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

		if self.ui.imageListWidget.currentItem():
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
				self.ui.imageListWidget.addItem(item)

		if not self.ui.imageListWidget.currentItem() and self.ui.imageListWidget.count() > 0:
			self.ui.imageListWidget.setCurrentRow(0)
			self.display_large_image(self.ui.imageListWidget.currentItem())

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
				# An unreadable file has no shape to build a mask from; it stays without
				# one instead of taking the masking stage down with it.
				if image is None:
					continue
				self.prediction_results[file_name] = np.zeros(image.shape[:2], dtype=np.float32)

	def configure_detection_availability(self):
		r"""
		Disable the automatic detection methods if their optional backend is missing.

		TensorFlow is an optional dependency. Without it only manual annotation is
		possible, so every detection method except "None" is greyed out and
		preselected. The entries are addressed by index, so the setting survives a
		language switch, which replaces their texts.
		"""
		if is_detection_available():
			return

		combo = self.ui.modelComboBox
		none_index = combo.findText(self.tr(self.DETECTION_METHOD_NONE))
		for index in range(combo.count()):
			if index == none_index:
				continue
			item = combo.model().item(index)
			if item is not None:
				item.setEnabled(False)
			combo.setItemData(index, MISSING_BACKEND_HINT, Qt.ItemDataRole.ToolTipRole)

		if none_index >= 0:
			combo.setCurrentIndex(none_index)
		combo.setToolTip(MISSING_BACKEND_HINT)

	def detection_method_is_none(self):
		r"""
		Check whether the model dropdown is set to "None".

		The entry is translated at runtime ("Keins" in German), so it is compared
		against the translation rather than the literal English text.

		\return (bool): True if no automatic detection is selected.
		"""
		return self.ui.modelComboBox.currentText() == self.tr(self.DETECTION_METHOD_NONE)

	def apply_model_detection(self, all_images=False):
		r"""
		Run crack detection for the selected images, overwriting their current mask.

		Unless the model dropdown is set to "None", in which case the mask is
		instead reset to empty, same as \ref clear_mask.

		Loading the model and predicting take several seconds, in which the window
		would otherwise appear frozen, so the progress is displayed. The model is
		loaded only once and reused for later runs.

		\param all_images: Process every image if True (right button), only the
			currently displayed one if False (left button).
		"""
		if not self.prediction_results:
			return

		if self.detection_method_is_none():
			self.clear_mask(all_images)
			return

		if not is_detection_available():
			QMessageBox.warning(self, self.tr("Automatic detection unavailable"), MISSING_BACKEND_HINT)
			return

		image_paths = list(self._skeleton_target_paths(all_images, self.prediction_results))
		if not image_paths:
			return

		progress = QProgressDialog(self.tr("Loading the detection model..."), None, 0, len(image_paths), self)
		progress.setWindowTitle(self.tr("Crack detection"))
		progress.setWindowModality(Qt.WindowModality.WindowModal)
		progress.setMinimumDuration(0)
		progress.setValue(0)
		QApplication.processEvents()

		try:
			if self.edge_detector is None:
				self.edge_detector = EdgeDetection()

			for index, image_path in enumerate(image_paths):
				progress.setLabelText(self.tr("Detecting cracks in {file}...").format(file=os.path.basename(image_path)))
				QApplication.processEvents()
				self.prediction_results[image_path] = self.edge_detector.detect_edges(image_path)
				progress.setValue(index + 1)
		except Exception as error:
			progress.cancel()
			QMessageBox.critical(self, self.tr("Crack detection failed"), str(error))
			return

		if self.ui.imageListWidget.currentItem():
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

		if self.ui.imageListWidget.currentItem():
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
			if not self.refresh_display_image():
				# Only here, not in refresh_display_image itself: that one also runs on
				# every slider move and every window resize, which would turn a single
				# unreadable file into a stream of dialogs.
				QMessageBox.warning(
					self, self.tr("Image unreadable"),
					self.tr("{file} could not be read. It may have been moved, deleted or damaged.").format(
						file=os.path.basename(file_path)
					)
				)

	def refresh_display_image(self, keep_zoom=False):
		r"""
		Depending on the stage, display the original image, overlay predictions,
		or skeletonization results. Clear the label if no image is selected.

		\param keep_zoom: Keep the current zoom factor instead of returning to the
			overview. Used when only the overlay is rebuilt, not the image itself.
		\return (bool): False if the image could not be read, True otherwise.
		"""
		self.keep_zoom_on_refresh = keep_zoom
		if not self.current_image_path:
			self.clear_displayed_image()
			return True

		original_image = cv2.imread(self.current_image_path)
		# imread reports an unreadable file by returning None rather than raising,
		# and passing that on to cvtColor aborts the whole application.
		if original_image is None:
			self.clear_displayed_image()
			return False

		original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

		original_qimage = QImage(
			original_image.data, original_image.shape[1], original_image.shape[0],
			original_image.shape[1] * 3, QImage.Format.Format_RGB888
		)
		original_pixmap = QPixmap.fromImage(original_qimage)
		if original_pixmap.isNull():
			self.clear_displayed_image()
			return False

		if self.progress_stage == 1:
			self.display_original_image(original_pixmap)
		elif self.progress_stage == 2:
			self.display_prediction_overlay(original_pixmap)
		elif self.progress_stage == 3:
			self.display_skeleton_overlay(original_image)
		elif self.progress_stage == 4:
			self.display_original_image(original_pixmap)
			self.display_calculation_results()

		return True

	def clear_displayed_image(self):
		r"""
		Empty the image area, so that nothing is left standing that suggests the
		file is still being shown.
		"""
		self.ui.imageLabel.clear()
		self.original_pixmap = None
		self.zoom_base_pixmap = None

	def display_original_image(self, original_pixmap):
		r"""
		Display the original image scaled to fit the QLabel.

		\param original_pixmap: The QPixmap representation of the original image.
		"""
		self.original_pixmap = original_pixmap
		# Hand over the full resolution: render_current_view scales it to the
		# current zoom level, so no detail is thrown away up front.
		self.set_display_pixmap(original_pixmap)
		self.editable_qimage = None

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
		self.set_display_pixmap(combined_pixmap)

		self.editable_qimage = prediction_qimage.copy()

	def overlay_line_scale(self):
		r"""
		Return how many image pixels make up one screen pixel at the current zoom
		level.

		Markers are drawn into the full resolution image and scaled along with it,
		so their size on screen only stays put if it is measured in this unit.
		Multiplying a wanted screen size by this factor gives the size to draw with.

		\return (float): The image pixels per screen pixel, at least a small
			positive number.
		"""
		if self.zoom_factor <= 0:
			return 1.0
		return 1.0 / self.zoom_factor

	def overlay_size_in_pixels(self, screen_size):
		r"""
		Convert a size meant to be seen on screen into the size to draw with in the
		full resolution image.

		\param screen_size: The wanted size in screen pixels.
		\return (int): The size in image pixels, at least 1.
		"""
		return max(int(round(screen_size * self.overlay_line_scale())), 1)

	def overlay_dilation_width(self):
		r"""
		Return the width to thicken the skeleton line by, so that it survives being
		scaled down.

		\return (int): An odd width in image pixels, at least 1. Odd widths keep the
			line centred on the original skeleton pixel.
		"""
		width = self.overlay_size_in_pixels(1)
		return width + 1 - width % 2

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

		# The overlay is drawn at full resolution and scaled down for display, so every
		# marker is sized in image pixels for the screen size it should end up with.
		# That keeps it the same size to look at at every zoom level, instead of
		# growing and shrinking along with the image.
		node_radius = self.overlay_size_in_pixels(NODE_RADIUS)
		line_width = self.overlay_size_in_pixels(1)
		dilation_width = self.overlay_dilation_width()
		self.overlay_scale_in_use = node_radius

		overlay_image = original_image.copy()
		skeleton_coords = np.where(skeleton == 1)
		overlay_image[skeleton_coords[0], skeleton_coords[1]] = [255, 0, 0]
		if dilation_width > 1:
			skeleton_mask = cv2.dilate(
				(skeleton == 1).astype(np.uint8),
				cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dilation_width, dilation_width))
			)
			overlay_image[skeleton_mask > 0] = [255, 0, 0]

		created_nodes = skeleton_data.get("created_nodes", [])
		for node in created_nodes:
			cv2.circle(overlay_image, (node[0], node[1]), radius=node_radius,
					   color=(255, 251, 13), thickness=-1)

		lines = skeleton_data.get("created_lines", [])
		for line in lines:
			start, end = line
			cv2.line(overlay_image, (start[0], start[1]), (end[0], end[1]), color=(255, 251, 13), thickness=line_width)

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
				cv2.circle(overlay_image, point_tuple, radius=self.overlay_size_in_pixels(5),
						   color=color, thickness=self.overlay_size_in_pixels(2))

		overlay_qimage = QImage(
			overlay_image.data,
			overlay_image.shape[1],
			overlay_image.shape[0],
			overlay_image.shape[1] * 3,
			QImage.Format.Format_RGB888
		)
		overlay_pixmap = QPixmap.fromImage(overlay_qimage)

		self.original_pixmap = overlay_pixmap
		self.set_display_pixmap(overlay_pixmap)
		self.editable_qimage = overlay_qimage.copy()

	def display_calculation_results(self):
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
		# Show the last two directories along with the file name, so images with the
		# same name from different measurement folders can still be told apart.
		parent_directory = os.path.basename(os.path.dirname(full_path))
		grandparent_directory = os.path.basename(os.path.dirname(os.path.dirname(full_path)))

		if grandparent_directory:
			display_name = f"/{grandparent_directory}/{parent_directory}/{os.path.basename(full_path)}"
		else:
			display_name = f"/{parent_directory}/{os.path.basename(full_path)}"

		self.ui.fileNameLabel.setText(display_name)

		crack_width_mm = self.crack_results[self.current_image_path]["crack_width_mm"]
		crack_area_mm = self.crack_results[self.current_image_path]["crack_area_mm2"]
		skeleton_length_mm = self.crack_results[self.current_image_path]["skeleton_length_mm"]

		self.ui.crackWidthLabel.setText(f"{crack_width_mm:.6f} mm")
		self.ui.crackAreaLabel.setText(f"{crack_area_mm:.6f} mm²")
		self.ui.skeletonLengthLabel.setText(f"{skeleton_length_mm:.6f} mm")

	def refresh_display_after_draw(self):
		r"""
		Refresh the QLabel display after a drawing operation.
		Overlay the manually drawn mask onto the original image and update the UI.
		"""
		if not self.current_image_path or self.editable_qimage is None:
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

		prediction_pixmap = QPixmap.fromImage(self.editable_qimage)

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
		# Same image, only redrawn: keep the zoom instead of jumping back to the
		# overview after every single brush stroke.
		self.set_display_pixmap(combined_pixmap, keep_zoom=True)
	# ------------------------ Progress Management ----------------------------------------------------------------------

	def set_stage(self, stage):
		r"""
		Change the application workflow to the specified stage and switch the stacked widget index to the corresponding tool page.

		\param stage: The target stage index (0 to 4).
		"""

		if stage < 0 or stage > 4:
			return
		self.progress_stage = stage
		self.ui.stageStack.setCurrentIndex(stage)
		self.progress_manager.update_progress(self.progress_stage)

		if self.progress_stage == 2:
			self.ensure_masks_initialized()
		# update_cursor() knows which stages show a circle and which do not.
		self.update_cursor()

		if self.progress_stage == 0:
			self.display_calibration_image()
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
			self.crack_results = self.calculate_crack_properties()
			print("File export stage")

		if self.ui.imageListWidget.currentItem():
			self.display_large_image(self.ui.imageListWidget.currentItem())

	def finish_session(self):
		r"""
		End the session behind the "Finish" button, asking what should happen to the
		work first.

		Finishing throws away every image, mask and skeleton of this session, and the
		button sits right next to the ones used to page through the stages, so it is
		easily hit by accident. Saving first is offered rather than assumed: a session
		that was only looked at is legitimately discarded, and forcing a file dialog on
		it would be in the way.
		"""
		if not self.session_has_data():
			# Nothing to lose, so the question would only be noise.
			self.reset_all_data()
			return

		question = QMessageBox(self)
		question.setIcon(QMessageBox.Icon.Question)
		question.setWindowTitle(self.tr("Finish session"))
		question.setText(self.tr("Finishing clears all images and results of this session.\n\n"
								 "Do you want to save the project first?"))
		question.setStandardButtons(
			QMessageBox.StandardButton.Save | QMessageBox.StandardButton.Discard
			| QMessageBox.StandardButton.Cancel
		)
		question.setDefaultButton(QMessageBox.StandardButton.Save)
		# Qt translates its standard buttons from its own catalog, which this program
		# does not ship, so they would stay English inside a German dialog.
		question.button(QMessageBox.StandardButton.Save).setText(self.tr("Save project"))
		question.button(QMessageBox.StandardButton.Discard).setText(self.tr("Discard"))
		question.button(QMessageBox.StandardButton.Cancel).setText(self.tr("Cancel"))

		answer = question.exec()

		if answer == QMessageBox.StandardButton.Cancel:
			return
		if answer == QMessageBox.StandardButton.Save:
			# export_project asks for the file name and reports whether it got one.
			# A cancelled file dialog must not go on to clear the session.
			if not self.export_project():
				return

		self.reset_all_data()

	def session_has_data(self):
		r"""
		Check whether this session holds anything a reset would throw away.

		\return (bool): True if images, calibration or results are present.
		"""
		return bool(
			self.ui.imageListWidget.count()
			or self.calibration_points
			or self.resolution
			or self.calibration_path
		)

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

		self.ui.imageListWidget.clear()
		self.ui.imageLabel.clear()
		self.zoom_base_pixmap = None
		self.ui.imageLabel.repaint()
		self.ui.imageListWidget.repaint()

		self.ui.fileNameLabel.setText("")
		self.ui.crackWidthLabel.setText("")
		self.ui.skeletonLengthLabel.setText("")
		self.ui.crackAreaLabel.setText("")

		self.ui.distanceLineEdit.clear()
		self.ui.pixelLineEdit.clear()
		self.ui.resolutionLineEdit.clear()

		self.drawing = False
		self.editable_qimage = None
		self.original_pixmap = None
		self.resolution = None
		self.calibration_image = None
		self.calibration_path = None
		self.calibration_points = []
		self.add_node_mode = False
		self.delete_node_mode = False
		self.dragged_node = None
		self.project_path = None

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

		\return (bool): True if the project was written, False if the user cancelled
			or the export failed.
		"""
		if self.ui.imageListWidget.count() == 0:
			QMessageBox.warning(self, self.tr("Export Error"),
								self.tr("No images to export. Please upload images first."))
			return False

		file_path, _ = QFileDialog.getSaveFileName(
			self, "Save Project", "", "Crackpot Project (*.crackpot)"
		)
		if not file_path:
			return False
		if not file_path.lower().endswith(".crackpot"):
			file_path += ".crackpot"

		project_dir = pathlib.Path(file_path).resolve().parent
		images = []
		prediction_results = {}
		skeleton_results = {}
		crack_results = {}
		skipped = []
		for i in range(self.ui.imageListWidget.count()):
			stored_path = self.ui.imageListWidget.item(i).data(Qt.ItemDataRole.UserRole)
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

		calibration_image_path = None
		if self.calibration_path is not None:
			calibration_image_path = self._project_to_relative(self.calibration_path, project_dir)
			if calibration_image_path is None:
				skipped.append(self.calibration_path)

		project_data = {
			"format_version": 4,
			"images": images,
			# The "cali_" keys keep their abbreviated names on purpose: they are part
			# of the stored file format, and renaming them would silently drop the
			# calibration when an older project file is opened.
			"cali_image_path": calibration_image_path,
			"cali_points": self.calibration_points,
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
			message = self.tr("Project exported successfully:\n{path}").format(path=file_path)
			if skipped:
				message += "\n\n" + self.tr(
					"Skipped (on a different drive than the project file, so they "
					"couldn't be referenced by a relative path):"
				) + "\n" + "\n".join(skipped)
			QMessageBox.information(self, self.tr("Success"), message, QMessageBox.StandardButton.Ok)
			self.project_path = file_path
			return True
		except Exception as e:
			QMessageBox.critical(self, self.tr("Export Failed"),
								 self.tr("Error:\n{message}").format(message=str(e)))
			return False

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
			QMessageBox.critical(self, self.tr("Import Failed"),
								 self.tr("Error:\n{message}").format(message=str(e)))
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
		self.calibration_points = project_data.get("cali_points", [])

		stored_calibration_path = project_data.get("cali_image_path")
		calibration_image_path = resolve(stored_calibration_path)
		if calibration_image_path is not None:
			self.calibration_image = cv2.imread(calibration_image_path)
			if self.calibration_image is None:
				missing_paths.append(stored_calibration_path)
			else:
				self.calibration_path = calibration_image_path
		elif stored_calibration_path:
			missing_paths.append(stored_calibration_path)

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
			self.ui.imageListWidget.addItem(item)

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
				self.crack_results[current_path] = _migrate_crack_result(crack_data[rel_path])

		self.skeleton_processor.skeletons = self.skeleton_results

		if self.resolution is not None:
			self.ui.resolutionLineEdit.setText(f"{self.resolution:.6f}")

		if self.ui.imageListWidget.count() > 0:
			self.ui.imageListWidget.setCurrentRow(0)
			self.display_large_image(self.ui.imageListWidget.currentItem())

		restored_stage = project_data.get("progress_stage", 0)
		if self.ui.imageListWidget.count() == 0:
			restored_stage = min(restored_stage, 1)
		self.set_stage(restored_stage)

		if missing_paths:
			QMessageBox.warning(
				self, self.tr("Some images missing"),
				self.tr("Project loaded, but the following images could not be found or loaded "
						"and were skipped:") + "\n\n" + "\n".join(missing_paths)
			)
		else:
			QMessageBox.information(self, self.tr("Success"),
									self.tr("Project loaded successfully."),
									QMessageBox.StandardButton.Ok)

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
			reasons.append(self.tr("No crack masks yet. Run the crack detection or draw a mask "
								   "in the Masking Stage."))
		if self.resolution is None or self.resolution <= 0:
			reasons.append(self.tr("No calibration yet. Set the resolution in the Calibration Stage."))
		return reasons

	def calculate_crack_properties(self):
		r"""
		Calculate crack properties including area, skeleton length, and average crack width.

		Images without a skeleton are still included, with a skeleton length of zero,
		so that a partly processed session yields results for the images that are ready
		instead of failing as a whole.

		\return: A dictionary containing calculated crack properties for each image.
		Always a dictionary, never None: it is empty if the requirements are not met
		yet, so that callers can assign the result without a fallback.
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
			# Measured along the lines instead of counted: a skeleton draws a slanted
			# crack as a staircase, and counting its pixels reads a diagonal step as
			# one pixel although it covers sqrt(2). A crack running at 45 degrees came
			# out almost 30 % too short that way, and it was the only value here that
			# was not measured geometrically - the manually drawn lines below always
			# were, and both end up in the same sum.
			skeleton_length = self.skeleton_processor.measure_skeleton_length(clean_skeleton)

			manual_line_length = 0
			created_lines = skeleton_data.get("created_lines", [])

			for line in created_lines:
				start, end = line
				line_length = np.linalg.norm(np.array(start) - np.array(end))
				manual_line_length += line_length

			total_skeleton_length = skeleton_length + manual_line_length
			skeleton_length_mm = total_skeleton_length * self.resolution

			avg_crack_width_pixels = (crack_region_pixels / total_skeleton_length) if total_skeleton_length > 0 else 0

			# Every key carries its unit: the same quantity appears twice here, once
			# in pixels and once converted with the calibration, and without the
			# suffix the two were only told apart by which one had one.
			crack_results[image_path] = {
				"crack_pixels": crack_region_pixels,
				"skeleton_length_px": total_skeleton_length,
				"crack_area_mm2": crack_area_mm2,
				"skeleton_length_mm": skeleton_length_mm,
				"crack_width_mm": avg_crack_width_pixels * self.resolution
			}

		return crack_results

	def build_export_table(self, export_dir):
		r"""
		Build the export table, holding one row per image and one column per value.

		\param export_dir: Directory of the export file, used as base for the relative image paths.
		\return: A pandas DataFrame with the rows to export.
		"""

		export_rows = []

		for image_path, result in self.crack_results.items():
			try:
				relative_path = os.path.relpath(image_path, export_dir)
			except ValueError:
				# Image and export file on different drives (Windows): there is no
				# relative path between them, so fall back to the absolute one.
				relative_path = os.path.abspath(image_path)

			prediction = self.prediction_results.get(image_path)
			if prediction is not None:
				height, width = prediction.shape[:2]
				image_size = f"{width} x {height}"
			else:
				image_size = ""

			export_rows.append({
				"File Name": os.path.basename(image_path),
				"File Path": relative_path,
				"Image Size (px)": image_size,
				"Crack Pixel (px)": int(result["crack_pixels"]),
				# Column header kept as-is so existing exports and the evaluations built
				# on them keep working, even though the value is a measured length now.
				"Skeleton Pixel (px)": round(float(result["skeleton_length_px"]), 2),
				"Crack Area (mm\u00b2)": round(result["crack_area_mm2"], 4),
				"Skeleton Length (mm)": round(result["skeleton_length_mm"], 4),
				"Mean Crack Width (mm)": round(result["crack_width_mm"], 4),
				"Resolution (mm/px)": self.resolution
			})

		return pd.DataFrame(export_rows)

	def write_excel_file(self, dataframe, file_path):
		r"""
		Write the export table to an Excel file with all columns widened to EXPORT_COLUMN_WIDTH_PX.

		\param dataframe: The DataFrame holding the rows to export.
		\param file_path: Target path of the .xlsx file.
		"""

		sheet_name = "Crack Results"

		with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
			dataframe.to_excel(writer, sheet_name=sheet_name, index=False)

			# Excel stores column widths in characters, which the default font maps to
			# roughly width * 7 + 5 pixels, so the pixel target is converted accordingly.
			column_width = (self.EXPORT_COLUMN_WIDTH_PX - 5) / 7
			worksheet = writer.sheets[sheet_name]

			for column_cells in worksheet.columns:
				worksheet.column_dimensions[column_cells[0].column_letter].width = column_width

	def default_export_path(self):
		r"""
		Build the file name proposed in the save dialog: the first uploaded image
		decides the directory, so the results are offered next to the images they
		belong to.

		\return: A suggested path, or just the file name if no image is available.
		"""
		file_name = "crack_results.csv"
		if self.ui.imageListWidget.count() > 0:
			first_image = self.ui.imageListWidget.item(0).data(Qt.ItemDataRole.UserRole)
			if first_image:
				return os.path.join(os.path.dirname(os.path.abspath(first_image)), file_name)
		return file_name

	def export_to_csv(self):
		r"""
		Ask for the target file and export the crack analysis results into it, written
		as an Excel sheet for a .xlsx path and as a comma separated CSV otherwise.
		"""
		if not self.crack_results:
			# Name the missing step instead of only stating that there is no data,
			# so the user knows which stage to go back to.
			reasons = self.missing_export_requirements()
			message = self.tr("No valid data to export!")
			if reasons:
				message += "\n\n" + "\n".join(reasons)
			QMessageBox.warning(self, self.tr("Export Error"), message)
			return

		file_path, selected_filter = QFileDialog.getSaveFileName(
			self, "Export Results", self.default_export_path(),
			f"{self.CSV_EXPORT_FILTER};;{self.EXCEL_EXPORT_FILTER}", options=QFileDialog.Option(0)
		)
		if not file_path:
			return

		# The extension decides the format below, so append the one matching the
		# chosen filter if the user typed a name without any.
		if not file_path.lower().endswith((".csv", ".xlsx")):
			file_path += ".xlsx" if selected_filter == self.EXCEL_EXPORT_FILTER else ".csv"

		# Absolute, so a bare file name resolves to the current directory rather than
		# to an empty string, which os.makedirs() and os.path.relpath() both reject.
		export_dir = os.path.dirname(os.path.abspath(file_path))
		dataframe = self.build_export_table(export_dir)

		try:
			os.makedirs(export_dir, exist_ok=True)
			if file_path.lower().endswith(".xlsx"):
				self.write_excel_file(dataframe, file_path)
			else:
				# US number formatting
				dataframe.to_csv(file_path, index=False, sep=",", decimal=".", encoding="utf-8-sig")
			QMessageBox.information(
				self, self.tr("Success"),
				self.tr("File exported successfully:\n{path}").format(path=file_path),
				QMessageBox.StandardButton.Ok
			)
		except Exception as e:
			QMessageBox.critical(self, self.tr("Export Failed"),
								 self.tr("Error:\n{message}").format(message=str(e)))
	# ------------------------ Menu Actions ----------------------------------------------------------------------

	def show_documentation_dialog(self):
		r"""Open the offline README as a modal dialog, in the currently active language."""
		DocumentationDialog(self.settings.value('language', 'english'), self).exec()

	def show_about_dialog(self):
		r"""Open a dialog displaying version, authors, copyright and license."""
		AboutDialog(self).exec()

	def switch_language(self, language):
		r"""
		Switch the UI language, retranslate every widget in place, and
		remember the choice for the next start.

		\param language: The target language, either 'english' or 'german'.
		"""
		if language == 'german':
			translation_path = resource_path('resources/translations/crackpot_de.qm')
			self.translator.load(translation_path)
			QApplication.instance().installTranslator(self.translator)
		else:
			QApplication.instance().removeTranslator(self.translator)
		self.ui.retranslateUi(self)
		self.settings.setValue('language', language)
	# ------------------------ Global UI Functions ----------------------------------------------------------------------

	def apply_icon_color(self):
		r"""
		Repaint the interface icons in the color of the active color scheme.

		The icons are monochrome drawings in a fixed color, which is barely
		visible if it does not match the color scheme. The button text color of
		the palette keeps them readable in both the light and the dark scheme.
		"""
		color = self.palette().color(QPalette.ColorRole.ButtonText)

		for button in self.findChildren(QAbstractButton):
			icon = button.icon()
			if icon.isNull():
				continue
			button.setIcon(self.recolor_icon(icon, button.iconSize(), color))

	def recolor_icon(self, icon, size, color):
		r"""
		Draw a monochrome icon in a different color.

		The icon is rendered at the pixel ratio of the display, so that it stays
		sharp on high resolution screens.

		\param icon: The icon to recolor.
		\param size: The size to render the icon at.
		\param color: The color to draw the icon in.
		\return: A new icon showing the same shape in the given color.
		"""
		ratio = self.devicePixelRatio()
		pixmap = icon.pixmap(size * ratio)
		if pixmap.isNull():
			return icon
		pixmap.setDevicePixelRatio(ratio)

		painter = QPainter(pixmap)
		painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
		painter.fillRect(pixmap.rect(), color)
		painter.end()

		return QIcon(pixmap)

	def set_display_pixmap(self, pixmap, keep_zoom=False):
		r"""
		Show a freshly built pixmap in the image label and remember it as the
		base for zooming.

		Every zoom step is recomputed from this untouched base pixmap (see
		render_current_view) instead of rescaling the already scaled pixmap that
		is currently shown. This prevents the image from being resampled over and
		over again, which otherwise makes it progressively blurrier with each
		zoom cycle.

		\param pixmap: The QPixmap to display and store as the zoom base.
		\param keep_zoom: Keep the current zoom factor instead of resetting it.
			Used when the same image is only redrawn, e.g. after a brush stroke.
		"""
		self.zoom_base_pixmap = pixmap
		if not (keep_zoom or self.keep_zoom_on_refresh):
			self.zoom_factor = self.fit_to_window_factor()
		self.render_current_view()
		self.refresh_overlay_if_line_width_changed()

	def fit_to_window_factor(self):
		r"""
		Return the zoom factor at which the image fits completely into the visible
		area, keeping its aspect ratio. Images smaller than the viewport are shown
		at their native size rather than blown up.

		\return: The factor to pass to render_current_view, 1.0 if no image is shown.
		"""
		if self.original_pixmap is None or self.original_pixmap.isNull():
			return 1.0
		if self.original_pixmap.width() == 0 or self.original_pixmap.height() == 0:
			return 1.0

		viewport = self.ui.imageScrollArea.viewport().size()
		factor = min(viewport.width() / self.original_pixmap.width(),
					 viewport.height() / self.original_pixmap.height())
		return min(factor, 1.0) if factor > 0 else 1.0

	def render_current_view(self):
		r"""
		Draw the image at the current zoom factor, always scaled from the full
		resolution pixmap.

		Rendering from the full resolution matters for the thin structures this
		program works with: scaling the image down to the window first destroys the
		one pixel wide skeleton lines, and scaling that result back up cannot bring
		them back. The brush cursor is refreshed alongside, so it keeps matching the
		stroke that will actually be drawn.
		"""
		if self.zoom_base_pixmap is None or self.zoom_base_pixmap.isNull():
			return

		width = max(int(self.zoom_base_pixmap.width() * self.zoom_factor), 1)
		height = max(int(self.zoom_base_pixmap.height() * self.zoom_factor), 1)

		# Smooth scaling below the native size, nearest neighbour above it: shrinking
		# needs the averaging to keep thin lines visible at all, while magnifying
		# should show honest pixel blocks instead of an interpolated blur.
		mode = (Qt.TransformationMode.SmoothTransformation if self.zoom_factor < 1.0
				else Qt.TransformationMode.FastTransformation)
		scaled_pixmap = self.zoom_base_pixmap.scaled(
			width, height, Qt.AspectRatioMode.KeepAspectRatio, mode
		)

		self.ui.imageLabel.setPixmap(scaled_pixmap)
		# No adjustSize() here. It shrank the label to the pixmap even when that was
		# smaller than the viewport, and the layout stretched it back on its next run
		# (the label is Expanding inside a widgetResizable scroll area). So the label
		# jumped between both sizes on every redraw, and with it the offset a click is
		# read with - a constant shift of half the leftover space, which showed up as a
		# mark sitting away from the stroke it belonged to. Scrolling large images does
		# not need it: setPixmap already updates the size hint the layout grows to.
		self.refresh_cursor_for_view()

	def refresh_overlay_if_line_width_changed(self):
		r"""
		Rebuild the skeleton overlay when the zoom level needs a different line width.

		The markers are baked into the full resolution overlay, so their width only
		fits the zoom level they were drawn for. Rebuilding on every zoom step would
		be wasteful on large images, hence the check for an actual change: the
		rounded marker size, not the zoom factor behind it, is what a redraw would
		change.
		"""
		if self.progress_stage != 3:
			return
		if self.overlay_size_in_pixels(NODE_RADIUS) == self.overlay_scale_in_use:
			return

		# The overlay is drawn for whatever zoom factor is set at that moment, so the
		# current one has to survive the rebuild instead of falling back to the
		# overview.
		self.refresh_display_image(keep_zoom=True)

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
		self.render_current_view()
		self.refresh_overlay_if_line_width_changed()

	def refresh_cursor_for_view(self):
		r"""
		Refresh the cursor circle after the view was redrawn, so that its size keeps
		matching the zoom factor and it disappears with the image.
		"""
		self.update_cursor()

	def zoom_fit_to_window(self):
		r"""
		Scale the displayed image to fit entirely within the visible viewport, keeping the aspect ratio.
		"""
		if self.zoom_base_pixmap is None:
			return

		self.zoom_factor = self.fit_to_window_factor()
		self.render_current_view()
		self.refresh_overlay_if_line_width_changed()

	def zoom_one_to_one(self):
		r"""
		Display the image at its native resolution, so one image pixel corresponds to one screen pixel.
		"""
		if self.zoom_base_pixmap is None:
			return

		self.zoom_factor = 1.0
		self.render_current_view()
		self.refresh_overlay_if_line_width_changed()

	def delete_current_image(self):
		r"""
		Delete the currently selected image from the list and clear associated data (prediction results,
		skeleton results, and crack results). It will prompt the user for confirmation before delete it.
		"""
		selected_item = self.ui.imageListWidget.currentItem()
		if not selected_item:
			QMessageBox.warning(self, self.tr("Error"), self.tr("No image selected!"))
			return

		image_path = selected_item.data(Qt.ItemDataRole.UserRole)

		reply = QMessageBox.question(
			self, self.tr("Confirm delete"),
			self.tr("Are you sure you want to delete {file}?").format(file=os.path.basename(image_path)),
			QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
		)

		if reply == QMessageBox.StandardButton.No:
			return

		row = self.ui.imageListWidget.row(selected_item)
		self.ui.imageListWidget.takeItem(row)

		self.prediction_results.pop(image_path, None)
		self.skeleton_results.pop(image_path, None)
		self.crack_results.pop(image_path, None)

		self.ui.imageListWidget.repaint()

		if self.ui.imageListWidget.count() > 0:
			new_index = min(row, self.ui.imageListWidget.count() - 1)
			self.ui.imageListWidget.setCurrentRow(new_index)
			self.display_large_image(self.ui.imageListWidget.currentItem())
		else:
			self.current_image_path = None
			self.editable_qimage = None
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
		current_row = self.ui.imageListWidget.currentRow()
		if current_row > 0:
			self.ui.imageListWidget.setCurrentRow(current_row - 1)
			self.display_large_image(self.ui.imageListWidget.currentItem())

	def show_next_image(self):
		r"""
		Navigate to and display the next image in the list.
		"""
		current_row = self.ui.imageListWidget.currentRow()
		if current_row < self.ui.imageListWidget.count() - 1:
			self.ui.imageListWidget.setCurrentRow(current_row + 1)
			self.display_large_image(self.ui.imageListWidget.currentItem())

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
	QApplication.setOrganizationName("Institut für Massivbau, TU Dresden")
	QApplication.setApplicationName("Crackpot")
	app = QApplication(sys.argv)
	# Set on the application instead of the main window, so that dialogs and the
	# taskbar entry show the icon as well.
	app.setWindowIcon(QIcon(resource_path('resources/crackpot.ico')))
	window = MainWindow()
	window.show_and_check_config()
	sys.exit(app.exec())
