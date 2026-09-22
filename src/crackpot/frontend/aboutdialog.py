from PySide6.QtCore import Qt
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout

from crackpot.version import __version__, RELEASE_DATE
from crackpot.utils.utils import resource_path

LICENSE_TEXT = (
	"This software is licensed under the GNU General Public License (GPL) Version 3, 29 June 2007."
)


class AboutDialog(QDialog):
	r"""
	Dialog showing version, authors, copyright and license, in the style of
	the institute's other tools (fosKeyMan).
	"""
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle(self.tr("About"))
		# The window flags are left alone on purpose: Qt 6 no longer puts the context
		# help button on dialogs, and masking it out with ~ takes WindowCloseButtonHint
		# with it under Python 3.11, which leaves the title bar X without effect.

		layout = QVBoxLayout(self)
		logo = QSvgWidget(resource_path('resources/crackpot.svg'))
		logo.setFixedSize(120, 120)
		layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

		for text in (
			self.tr("Version: {version}\nRelease Date: {date}").format(version=__version__, date=RELEASE_DATE),
			self.tr("Authors:\nBertram Richter\nCarl Stock\nXiaoli Song"),
			self.tr("Copyright:\nInstitut für Massivbau\nTechnische Universität Dresden"),
			self.tr("License:\n{license_text}").format(license_text=self.tr(LICENSE_TEXT)),
		):
			label = QLabel(text)
			label.setAlignment(Qt.AlignmentFlag.AlignCenter)
			label.setWordWrap(True)
			layout.addWidget(label)
