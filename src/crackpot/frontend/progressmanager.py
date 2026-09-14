COMPLETED_STAGE_STYLE = "background-color: #4CAF50; color: white;"
CURRENT_STAGE_STYLE = "border: 2px solid #4CAF50; color: #4CAF50;"
DEFAULT_STAGE_STYLE = ""
COMPLETED_LINE_STYLE = "background-color: #4CAF50;"
DEFAULT_LINE_STYLE = "background-color: #CCCCCC;"


class ProgressManager:
	r"""
	Manage the progress stage indicators in the UI.
	This class updates the styles of stage buttons and connecting lines
	based on the current stage of the application workflow.
	"""
	def __init__(self, buttons, lines):
		r"""
		Initialize the ProgressManager with stage buttons and connecting lines.

		\param buttons: A list of QPushButton elements representing each stage.
		\param lines: A list of QFrame elements representing progress lines between stages.
		"""
		self.buttons = buttons
		self.lines = lines

	def update_progress(self, current_stage):
		r"""
		Change the styles of buttons and lines to indicate completed,
		current, and pending stages.

		\param current_stage: The index of the current stage.
		"""
		for i, button in enumerate(self.buttons):
			if i < current_stage:
				button.setStyleSheet(COMPLETED_STAGE_STYLE)
				if i < len(self.lines):
					self.lines[i].setStyleSheet(COMPLETED_LINE_STYLE)
			elif i == current_stage:
				button.setStyleSheet(CURRENT_STAGE_STYLE)
				if i > 0:
					self.lines[i - 1].setStyleSheet(COMPLETED_LINE_STYLE)
			else:
				button.setStyleSheet(DEFAULT_STAGE_STYLE)
				if i < len(self.lines):
					self.lines[i].setStyleSheet(DEFAULT_LINE_STYLE)

