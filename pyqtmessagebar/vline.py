"""
.. module:: vline

See `How to Add Separator to StatusBar <https://www.geeksforgeeks.org/pyqt5-how-to-add-separator-in-status-bar/>`_.
"""

from PyQt5.QtWidgets import QFrame

# ----------------------------------------------------------------------------
class VLine(QFrame):
	"""A simple VLine (Vertical Line), like the one you get from Qt Designer.

	This class is used when the **PyQtMessageBar** constructor parameter **enable_separators** is set True.
	"""
	def __init__(self):
		"""Intializes a simple Vertical Line object that subclasses QFrame."""
		super(VLine, self).__init__()
		self.setFrameShape(self.VLine|self.Sunken)
