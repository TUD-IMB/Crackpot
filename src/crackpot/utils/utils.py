import os
import sys


def resource_path(relative_path):
	r"""
	Generate the absolute path to a resource.
	If the application is frozen (e.g., packaged with PyInstaller), it uses the _MEIPASS directory.
	\param relative_path (str): The relative path to the resource.
	\return (str): The absolute path to the resource.
	"""
	if getattr(sys, 'frozen', False):
		base_dir = sys._MEIPASS
	else:
		base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	return os.path.join(base_dir, relative_path)
