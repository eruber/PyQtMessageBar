"""
aboutdialog

Implements PyQtMessageBar's About Dialog

GPL LICENSE
This file is part of PyQtMessageBar.

PyQtMessageBar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyQtMessageBar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyQtMessageBar in the file named COPYING. If not, 
see <https://www.gnu.org/licenses/>.

COPYRIGHT (C) 2020 E.R. Uber (eruber@gmail.com.com)

"""

# ----------------------------------------------------------------------------
# ------------------------ Python Standard Library ---------------------------
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# -------------------------- Third Party Packages ----------------------------
# ----------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets

# ----------------------------------------------------------------------------
# -------------------------- Application Packages ----------------------------
# ----------------------------------------------------------------------------
import pyqtmessagebar.qtresources

# ----------------------------------------------------------------------------
# ----------------------- Module Global & Constants --------------------------
# ----------------------------------------------------------------------------
usage = """PyQtMessageBar buffers StatusBar messages and increments the Message
Index as it buffers. The message buffer is currently configured to hold the last {} messages.
Once the buffer fills, the oldest message is deleted.

A message may have an associated display timeout; if it does, the Countdown
Timer in the background of the Message Index display area will count down the timeout. 
If mutiple messages with timeouts are buffered, they are placed in a wait queue 
and the Wait Queue Depth is incremented.

Keyboard input can be used to move back and forth through the message buffer.

If the PyQtMessageBar has input focus, the following keyboard inputs are recognized:

     Up Arrow - display the message before the current message
   Down Arrow - display the message after the current message
      Page Up - display the page before the current message
    Page Down - display the page after the current message
         Home - display the oldest message (top of the message buffer)
          End - display the newest message (bottom of the message buffer)

                Note: Page Size is currently configured to be {} messages.

      CTRL-ALT-X - Delete currently displayed messsage 
CTRL-ALT-SHIFT-X - Delete all messages

      CTRL-ALT-S - Saves the entire message buffer to a timestamped file 
                   at: '{}'
CTRL-ALT-SHIFT-S - Opens a File Save As Dialog to save the entire message buffer
                   to a timestamped file per user input.

"""

# ----------------------------------------------------------------------------
# --------------------- Module Classes & Functions ---------------------------
# ----------------------------------------------------------------------------
class AboutDialog(QtWidgets.QDialog):

	def __init__(self, parent=None):

		super(AboutDialog, self).__init__(parent)

		self.parent = parent

		self.setWindowTitle('About PyQtMessageBar')

		icon = QtGui.QIcon()
		self.setWindowIcon(self.parent._icon)

		# Width, Height
		#self.resize(790, 590)
		self.setFixedSize(790, 590)

		self.components = QtWidgets.QLabel(self)
		self.components.setPixmap(QtGui.QPixmap(':/gfx/PyQtMessageBar_Components_feathered.png'))

		self.textEdit = QtWidgets.QTextEdit(self)
		self.textEdit.setGeometry(QtCore.QRect(15, 265, 750, 270))
		self.textEdit.setReadOnly(True)
		font = QtGui.QFont("Courier New", 10, QtGui.QFont.Bold)
		if font:
			self.textEdit.setFont(font)

		self.textEdit.setText(usage.format(self.parent._buffer_size, 
			self.parent._buf_page_size,
			self.parent._save_msg_buffer_dir))

		self.close = QtWidgets.QPushButton('Close', self)
		self.close.setGeometry(QtCore.QRect(350, 550, 75, 23))
		self.close.setToolTip("Close this dialog...")
		self.close.clicked.connect(self.close_clicked)

	def close_clicked(self):
		self.accept()


