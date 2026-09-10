from PySide6.QtCore import QUrl
from PySide6.QtGui import QTextCursor, QTextDocument
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from utils.utils import resource_path

DOCS_DIR = resource_path('resources/docs')
README_PATH_BY_LANGUAGE = {
	'english': resource_path('resources/docs/README.md'),
	'german': resource_path('resources/docs/README_de.md'),
}

# The screenshots in the README are much wider than the dialog; setMarkdown()
# embeds them at their native pixel size, which pushes the whole document
# past the visible width. Qt has no markdown-side "max-width", so images are
# capped to this many pixels by rewriting their QTextImageFormat after load.
MAX_IMAGE_WIDTH = 700


class DocumentationDialog(QDialog):
	r"""
	Dialog showing the project README offline, so the workflow documentation
	is available without an internet connection or a GitHub account.
	"""
	def __init__(self, language, parent=None):
		r"""
		\param language: The app's current language ('english' or 'german'),
			used to pick between README.md and README_de.md.
		"""
		super().__init__(parent)
		self.setWindowTitle(self.tr("Documentation"))
		self.resize(800, 700)

		readme_path = README_PATH_BY_LANGUAGE.get(language, README_PATH_BY_LANGUAGE['english'])

		browser = QTextBrowser(self)
		browser.setOpenExternalLinks(True)
		# Search path is the README's own directory, not images_en itself: the
		# README references images as "./images_en/x.png", so Qt needs to resolve
		# that path relative to where the README lives, not relative to the
		# images folder (which would look for images_en/images_en/x.png).
		browser.setSearchPaths([DOCS_DIR])
		with open(readme_path, 'r', encoding='utf-8') as readme_file:
			browser.setMarkdown(readme_file.read())
		_shrink_oversized_images(browser.document())

		layout = QVBoxLayout(self)
		layout.addWidget(browser)


def _shrink_oversized_images(document):
	r"""Cap every embedded image's display size to MAX_IMAGE_WIDTH, keeping its aspect ratio."""
	block = document.begin()
	while block.isValid():
		fragment = block.begin()
		while not fragment.atEnd():
			char_format = fragment.fragment().charFormat()
			if char_format.isImageFormat():
				image_format = char_format.toImageFormat()
				pixmap = document.resource(QTextDocument.ResourceType.ImageResource, QUrl(image_format.name()))
				if pixmap and not pixmap.isNull() and pixmap.width() > MAX_IMAGE_WIDTH:
					scale = MAX_IMAGE_WIDTH / pixmap.width()
					image_format.setWidth(pixmap.width() * scale)
					image_format.setHeight(pixmap.height() * scale)
					cursor = QTextCursor(document)
					cursor.setPosition(fragment.fragment().position())
					cursor.setPosition(fragment.fragment().position() + fragment.fragment().length(), QTextCursor.MoveMode.KeepAnchor)
					cursor.setCharFormat(image_format)
			fragment += 1
		block = block.next()
