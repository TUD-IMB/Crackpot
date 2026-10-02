from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QTextCursor, QTextDocument
from PySide6.QtWidgets import QDialog, QTextBrowser, QVBoxLayout

from crackpot.utils.utils import resource_path

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
		\param parent: The parent window, usually the main window.
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
		_shrink_oversized_images(browser.document(), browser.devicePixelRatioF())

		layout = QVBoxLayout(self)
		layout.addWidget(browser)


def _shrink_oversized_images(document, device_pixel_ratio):
	r"""
	Cap every embedded image's display size to MAX_IMAGE_WIDTH, keeping its aspect ratio.

	\param document: The QTextDocument the README was rendered into.
	\param device_pixel_ratio: Screen pixels per logical pixel (2.0 on a Retina display),
		so the shrunk images stay sharp on high-DPI screens.
	"""
	block = document.begin()
	while block.isValid():
		fragment = block.begin()
		while not fragment.atEnd():
			char_format = fragment.fragment().charFormat()
			if char_format.isImageFormat():
				image_format = char_format.toImageFormat()
				url = QUrl(image_format.name())
				pixmap = document.resource(QTextDocument.ResourceType.ImageResource, url)
				if pixmap and not pixmap.isNull() and pixmap.width() > MAX_IMAGE_WIDTH:
					# Only setting the smaller size in the format leaves the shrinking to
					# Qt's painter, which does it without smoothing and tears the small UI
					# text in the screenshots apart. So the image is shrunk here, smoothly
					# and in screen pixels, and replaces the original resource; Qt then
					# draws it 1:1. Never scaled up beyond its native size.
					target_width = min(pixmap.width(), round(MAX_IMAGE_WIDTH * device_pixel_ratio))
					scaled = pixmap.scaledToWidth(target_width, Qt.TransformationMode.SmoothTransformation)
					scaled.setDevicePixelRatio(device_pixel_ratio)
					document.addResource(QTextDocument.ResourceType.ImageResource, url, scaled)
					image_format.setWidth(scaled.width() / device_pixel_ratio)
					image_format.setHeight(scaled.height() / device_pixel_ratio)
					cursor = QTextCursor(document)
					cursor.setPosition(fragment.fragment().position())
					cursor.setPosition(fragment.fragment().position() + fragment.fragment().length(), QTextCursor.MoveMode.KeepAnchor)
					cursor.setCharFormat(image_format)
			fragment += 1
		block = block.next()
