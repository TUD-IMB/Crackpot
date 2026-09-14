r"""
Compiled Qt interface and resource modules.

The toolbar and stage icons are SVGs embedded in icon_rc. Rendering them relies
on the qsvgicon image plugin, which in turn links against the Qt SVG library. On
Windows that library sits in a different directory than the plugin, and the
loader does not resolve the dependency when the plugin is picked up lazily on
first use. The icons then come out blank, without any error message. Importing
the module here loads the library before any icon is requested.

The import looks unused - it is not, and removing it silently breaks all icons
on Windows.
"""

import PySide6.QtSvg  # noqa: F401
