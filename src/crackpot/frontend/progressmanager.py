CURRENT_STAGE_COLOR = "#4CAF50"
COMPLETED_LINE_STYLE = "background-color: #4CAF50;"
DEFAULT_LINE_STYLE = "background-color: #CCCCCC;"


class ProgressManager:
	r"""
	Manage the progress stage indicators in the UI.
	This class marks the stage buttons and the connecting lines between them
	as reached or still pending, following the current stage of the workflow.
	"""
	def __init__(self, buttons, lines, recolor_icon, default_color):
		r"""
		Initialize the ProgressManager with stage buttons and connecting lines.

		\param buttons: A list of QPushButton elements representing each stage.
		\param lines: A list of QFrame elements representing progress lines between stages.
		\param recolor_icon: Callable(icon, size, color) returning the icon drawn in
			that color, used to mark a stage as reached.
		\param default_color: The color an unreached stage icon is drawn in.
		"""
		self.buttons = buttons
		self.lines = lines
		self.recolor_icon = recolor_icon
		self.default_color = default_color
		self.base_icons = []

	def capture_icons(self):
		r"""
		Remember the icon every stage button currently carries, as the starting
		point for recoloring.

		Has to run after the icons have been adapted to the color scheme
		(see MainWindow.apply_icon_color), otherwise the raw icons from the
		resource file are kept instead of the readable ones.
		"""
		self.base_icons = [button.icon() for button in self.buttons]

	def update_progress(self, current_stage):
		r"""
		Mark every stage up to and including the current one as reached, and the
		lines in between as passed.

		Only the icon color changes, never the button style: the buttons carry
		their transparent background and hover feedback from main.ui, and a
		border would resize them and shift the whole row on every stage change.

		\param current_stage: The index of the current stage.
		"""
		for i, button in enumerate(self.buttons):
			if i < len(self.base_icons):
				color = CURRENT_STAGE_COLOR if i <= current_stage else self.default_color
				button.setIcon(self.recolor_icon(self.base_icons[i], button.iconSize(), color))

		# Line i sits between button i and button i+1, so it counts as passed
		# only once the stage behind it has been left. Setting every line on
		# every call is what makes the bar retreat again when going back.
		for i, line in enumerate(self.lines):
			line.setStyleSheet(COMPLETED_LINE_STYLE if i < current_stage else DEFAULT_LINE_STYLE)
