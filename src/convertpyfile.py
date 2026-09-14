import os
import subprocess
import re

# The application lives in the crackpot package one level below this script,
# which is deliberately not part of it: it is a development tool, not shipped.
base_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'crackpot')
ui_source_dir = os.path.join(base_dir, 'resources/ui')
qrc_source_dir = os.path.join(base_dir, 'resources')
py_target_dir = os.path.join(base_dir, 'frontend/ui')
translations_dir = os.path.join(base_dir, 'resources/translations')
frontend_dir = os.path.join(base_dir, 'frontend')

if not os.path.exists(py_target_dir):
	os.makedirs(py_target_dir)


def convert_ui_files():
	for file_name in os.listdir(ui_source_dir):
		if file_name.endswith('.ui'):
			ui_file_path = os.path.join(ui_source_dir, file_name).replace("\\", "/")
			py_file_name = f"ui{os.path.splitext(file_name)[0]}.py"
			py_file_path = os.path.join(py_target_dir, py_file_name).replace("\\", "/")

			if os.path.exists(ui_file_path):
				command = f'pyside6-uic "{ui_file_path}" -o "{py_file_path}"'
				try:
					result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					print(f"Successfully converted {ui_file_path} to {py_file_path}.")
					modify_import_statement(py_file_path)
				except subprocess.CalledProcessError as e:
					print(f"Converting {ui_file_path} failed: {e}")
			else:
				print(f"File does not exist: {ui_file_path}")


def modify_import_statement(py_file_path):
	with open(py_file_path, 'r', encoding='utf-8') as file:
		content = file.read()

	content = re.sub(r'^import (\w+_rc)', r'from crackpot.frontend.ui import \1', content, flags=re.M)

	with open(py_file_path, 'w', encoding='utf-8') as file:
		file.write(content)


def convert_qrc_files():
	for file_name in os.listdir(qrc_source_dir):
		if file_name.endswith('.qrc'):
			qrc_file_path = os.path.join(qrc_source_dir, file_name)
			py_file_name = f"{os.path.splitext(file_name)[0]}_rc.py"
			py_file_path = os.path.join(py_target_dir, py_file_name).replace("\\", "/")

			if os.path.exists(qrc_file_path):
				command = f'pyside6-rcc "{qrc_file_path}" -o "{py_file_path}"'
				try:
					result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					print(f"Successfully converted {qrc_file_path} to {py_file_path}")
				except subprocess.CalledProcessError as e:
					print(f"Converting {qrc_file_path} failed: {e}")
			else:
				print(f"The file does not exist:{qrc_file_path}")


def update_translation_source():
	r"""
	Rescan the Python sources and .ui files for self.tr()/tr() calls and merge
	newly found or changed strings into crackpot_de.ts. Run this after adding
	or changing translatable text, then translate the new entries in Qt
	Linguist before releasing.
	"""
	ts_file_path = os.path.join(translations_dir, 'crackpot_de.ts')
	py_files = [os.path.join(root, name) for root, _, names in os.walk(frontend_dir) for name in names if name.endswith('.py')]
	ui_files = [os.path.join(ui_source_dir, name) for name in os.listdir(ui_source_dir) if name.endswith('.ui')]
	command = ['pyside6-lupdate', *py_files, *ui_files, '-ts', ts_file_path]
	try:
		subprocess.run(command, check=True)
		print(f"Successfully updated {ts_file_path}.")
	except subprocess.CalledProcessError as e:
		print(f"Updating {ts_file_path} failed: {e}")


def compile_translations():
	r"""Compile every .ts translation source into the .qm binary QTranslator loads at runtime."""
	for file_name in os.listdir(translations_dir):
		if file_name.endswith('.ts'):
			ts_file_path = os.path.join(translations_dir, file_name)
			qm_file_path = os.path.splitext(ts_file_path)[0] + '.qm'
			command = f'pyside6-lrelease "{ts_file_path}" -qm "{qm_file_path}"'
			try:
				subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				print(f"Successfully compiled {ts_file_path} to {qm_file_path}.")
			except subprocess.CalledProcessError as e:
				print(f"Compiling {ts_file_path} failed: {e}")


if __name__ == '__main__':
	print("Start converting .ui files...")
	convert_ui_files()

	print("\nStart converting .qrc files...")
	convert_qrc_files()

	print("\nStart updating translation sources...")
	update_translation_source()

	print("\nStart compiling translations...")
	compile_translations()

	print("Done.")
