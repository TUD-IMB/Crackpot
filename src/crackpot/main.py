import os
import sys

from crackpot.frontend.mainwindow import main as run_application

WINDOWS_APP_ID = "TUD-IMB-FOS.Crackpot"


def ensure_standard_streams():
	r"""
	Make sure that sys.stdout and sys.stderr can be written to.

	The crackpot entry point starts without a console on Windows, where Python
	sets both streams to None. Libraries writing to them directly then raise an
	AttributeError in the middle of the workflow instead of staying quiet.
	Discarding their output keeps the application usable without a console.
	"""
	for name in ("stdout", "stderr"):
		if getattr(sys, name, None) is None:
			setattr(sys, name, open(os.devnull, "w"))


def set_windows_app_id():
	r"""
	Give the application its own identity in the Windows taskbar.

	Windows groups the taskbar entries by the application user model ID and takes
	the icon from it. Without an explicit ID, the one of the hosting process is
	used and the entry stays without the application icon. This has to happen
	before the first window is created and does nothing on other systems.
	"""
	if sys.platform != "win32":
		return

	try:
		import ctypes

		ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(WINDOWS_APP_ID)
	except Exception:
		# Only affects the taskbar grouping, which must not stop the start.
		pass


def main():
	r"""
	Set up the environment and run the application.
	"""
	ensure_standard_streams()
	set_windows_app_id()
	run_application()


if __name__ == "__main__":
	main()
