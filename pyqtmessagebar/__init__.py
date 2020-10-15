"""
.. py:module:: pyqtmessagebar

.. moduleauthor: E.R. Uber <eruber@gmail.com>

Class PyQtMessageBar
====================
This messagebar subclasses the standard Qt QStatusbar and provides
a drop-in replacement for QStatusBar. 

See the :ref:`intro_label` section for a high-level review of **PyQtMessageBar** features.

LOGGING
-------
This module creates a logging handler named 'PyQtMessageBar' and always
configures a Null handler.

See `Configuring Logging for a Library <https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library>`_.

REFERENCES
----------
The following Qt references proved helpful:
	* `Qt StatusBar <https://doc.qt.io/qt-5/qstatusbar.html>`_
	* `Qt Keyboard Enumerations <https://doc.qt.io/qt-5/qt.html#Key-enum>`_


LICENSE GPL
-----------
This file is part of **PyQtMessageBar**.

PyQtMessageBar is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PyQtMessageBar is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PyQtMessageBar in the file named LICENSE. If not, 
see <https://www.gnu.org/licenses/>.

COPYRIGHT (C) 2020 E.R. Uber (eruber@gmail.com)

.. _pyqtmessagebar_class_label:

USAGE
-----
You use **PyQtMessageBar** in your code just like you would use QStatusBar,
it just can have a bit more going on with its constructor call. But here
we show the simplest usage::

	from PyQt5.Qt import Qt
	from pyqtmessagebar import PyQtMessageBar
	...
	# Note that the root 'self' shown here is typically an earlier
	# instantiated QMainWindow

	# The least complex constructor signature -- every parameter has a default value
	self.statusbar = PyQtMessageBar()
	
	# In order for keyboard input to work with a PyQtMessageBar object, the focus
	# must be properly set
	self.statusbar.setFocusPolicy(Qt.StrongFocus)
	self.setFocusProxy(self.statusbar)

	# This actually attaches the ByQtMessageBar to the QMainWindow
	self.setStatusBar(statusbar)

PyQtMessageBar Details
----------------------
"""
# ----------------------------------------------------------------------------
# ------------------------ Python Standard Library ---------------------------
# ----------------------------------------------------------------------------
import os
import queue  # This is a First-In-First-Out Queue
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

# ----------------------------------------------------------------------------
# -------------------------- Third Party Packages ----------------------------
# ----------------------------------------------------------------------------
from PyQt5.Qt import Qt
from PyQt5.QtCore import QEvent, QSize, QByteArray, QFileInfo, QTimer, QObject, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QIcon, QImage, QPixmap, QFont
from PyQt5.QtWidgets import (
	QStatusBar, QApplication, QLabel, QFrame, QPushButton, QSizePolicy,
	QFileIconProvider, QFileDialog, 
	)

from colour import Color

# ----------------------------------------------------------------------------
# -------------------------- Application Packages ----------------------------
# ----------------------------------------------------------------------------
from pyqtlineeditprogressbar import PyQtLineEditProgressBar
import pyqtlineeditprogressbar as PYQTPROGBAR
from pyqtmessagebar.aboutdialog import AboutDialog
from pyqtmessagebar.vline import VLine
#from pyqtmessagebar.waitqueuesignal import WaitQueueEmptiedSignal

# ----------------------------------------------------------------------------
# ----------------------- Module Global & Constants --------------------------
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# --------------------- Module Classes & Functions ---------------------------
# ----------------------------------------------------------------------------
DEFAULT_BUFFER_SIZE = 100  # Message Queue can never get smaller than this
DEFAULT_PAGE_SIZE   = 10   # As used by Key_PageUp and Key_PageDown

DEFAULT_BG_COLOR_QUEUED_MSGS_WAITING = 'rgba(170,255,255,255)'

#https://doc.qt.io/qt-5/qt.html#Key-enum
KEY_MOVE = [
	Qt.Key_Up,         # -1 Entry
	Qt.Key_Down,       # +1 Entry
	Qt.Key_Home,       # 0th Entry
	Qt.Key_End,        # Max Entry
	Qt.Key_PageUp,     # -pagesize Entries
	Qt.Key_PageDown,   # +pagesize Entries
]

KEY_CMDS = [
	Qt.Key_X,          # Delete current message, +ALT delete all messages
	Qt.Key_S,          # +ALT Save queue to file
	Qt.Key_L,          # +ALT Load queue from file	
]

KEY_MAP = KEY_MOVE + KEY_CMDS

BUILT_IN_HELP_ICON_LIGHT = 'Light'
BUILT_IN_HELP_ICON_DARK = 'Dark'
BUILT_IN_HELP_ICON_TWO_TONE = 'Two'

HELP_ICON_INDICATORS = [BUILT_IN_HELP_ICON_LIGHT, BUILT_IN_HELP_ICON_DARK, BUILT_IN_HELP_ICON_TWO_TONE]

# ----------------------------------------------------------------------------
class PyQtMessageBar(QStatusBar):
	
	def __init__(self, parent=None, 
					msg_buffer_size=DEFAULT_BUFFER_SIZE, 
					enable_separators=False, 
					help_icon_file=None, 
					built_in_help_icon=BUILT_IN_HELP_ICON_LIGHT,
					parent_logger_name=None,
					save_msg_buffer_dir=None,
					timer_wait_q_emptied_signal=None,
					 ):
		"""Constructor for the **PyQtMessageBar** class which subclasses QStatusBar.
	
		See `Qt's QStatusBar Documentation <https://doc.qt.io/qt-5/qstatusbar.html>`_.

		It adds a buffered message index which includes a wait queue depth and it
		adds a messagebar help icon.

		Parameters
		----------
		parent : qtwidget, optional
			Reference to this widget's parent widget
		msg_buffer_size : int, optional
			The number of messages to buffer before removing the oldest
		enable_separators : bool, optional
			If True, any addPermanentWidget() calls will include a 
			vertical separator to the left of the widget added.
		help_icon_file : str, optional
			If specified, this file should be a 24x24 pixel image file
			to be used to replace the built-in help icon image. If specified,
			this icon will have prescedence over any built-in icon.
		built_in_help_icon : str, optional
			This is a string constant that can be one of three values 'Light', 'Dark', 'Two'.
			Use the module constants BUILT_IN_HELP_ICON_LIGHT, BUILT_IN_HELP_ICON_DARK, or
			BUILT_IN_HELP_ICON_TWO_TONE.
		save_msg_buffer_dir : str, optional
			A directory where any saved message buffers will be written to.
			If specified as None, then saving the message buffer will be
			disabled.
		timer_wait_q_emptied_signal : WaitQueueEmptiedSignal object, optional
			Provides a custom signal and allows user to connect their
			own slot method to the timer wait queue becoming empty.
			See WaitQueueEmptiedSignal :ref:`waitqueuesignal_usage_label` for
			a code example of how to set this signal up.

		"""
		super(PyQtMessageBar, self).__init__(parent=parent)

		# Constructor Parameters
		self._parent              = parent
		self._buffer_size         = msg_buffer_size
		self._enable_separators   = enable_separators
		self._help_icon_file      = help_icon_file
		self._built_in_help_icon  = built_in_help_icon
		self._save_msg_buffer_dir = save_msg_buffer_dir
		
		self._timer_wait_q_emptied_signal = timer_wait_q_emptied_signal

		# Initializing internal data
		self._progressbar_delta = None
		self._timer_progressbar_update = None

		self._field_width = len(str(self._buffer_size))
		format_1 = "{" + "0:0{}d".format(self._field_width) + "}"
		format_2 = "{" + "1:0{}d".format(self._field_width) + "}"
		format_3 = " [{2:1d}]" 
		self._displayed_msg_idx_format = format_1 + "/" + format_2 + format_3	
		logger.debug("Msg Index Format Spec: '{}'".format(self._displayed_msg_idx_format))

		self._displayed_msg_idx = -1     # _bufferd_msgs is empty
		self._buf_page_size     = DEFAULT_PAGE_SIZE

		# A _bufferd_msgs entry consists of: (msg, timeout, fg, bg, bold, enqueue_time)
		self._bufferd_msgs    = list()
		
		# We use a single timer, so messages that would generate overlapping timers are put on a wait queue
		# until this currently displayed message timer fires.
		self._timer = None
		self._timer_wait_q = queue.Queue()  # FIFO (First In First Out)
		self._process_zero_timeout_timer = None

		# This is the widget that is currently being displayed, if this is None, then 
		# nothing is being displayed
		self._widget = None

		# Intialize our user interface StatusBar and widgets a few...
		self._initUI()

	# -------------------------------------------------------------------------
	# Private Pythonic Interface ----------------------------------------------
	# -------------------------------------------------------------------------

	def _initUI(self):

		# This will be the default color for the countdown timer progressbar
		self._progressbar_color = PYQTPROGBAR.DEFAULT_COLOR_PURPLE

		# Add permanent QLabel for displayed message index
		self._msg_idx_label = PyQtLineEditProgressBar(
			behavior=PYQTPROGBAR.STARTS_FULL_EMPTIES_RIGHT_TO_LEFT,
			progressbar_color=self._progressbar_color,
			text_for_bounding_rect=" 88888/888 [88] ",
			)
		self._msg_idx_label.setMaxLength((2*self._field_width) + 1 + 6)
		self._msg_idx_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		
		self._clear_msg_idx_label() # rather than: self._update_msg_idx_label()
		
		self._msg_idx_label_tt_msg = "..out of {}".format(self._buffer_size)
		self._msg_idx_label.setToolTip(self._msg_idx_label_tt_msg)
		self.addPermanentWidget(self._msg_idx_label)

		# Add permanent Help Icon
		self._help_button = QPushButton('', self)
		if self._help_icon_file:
			# Load Help Icon from user file
			self._icon = QIcon(self._help_icon_file)
		else:
			# Load Help Icon from binary data
			if self._built_in_help_icon == BUILT_IN_HELP_ICON_DARK:
				self._icon = QIcon(':/gfx/baseline_help_black_24dp.png')
			elif self._built_in_help_icon == BUILT_IN_HELP_ICON_LIGHT:
				self._icon = QIcon(':/gfx/baseline_help_outline_24dp.png')
			elif self._built_in_help_icon == BUILT_IN_HELP_ICON_TWO_TONE:
				self._icon = QIcon(':/gfx/baseline_help_twotone_24dp.png')
			else:
				self._icon = QIcon(':/gfx/baseline_help_outline_24dp.png')
		self._help_button.setIcon(self._icon)
		self._help_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self._help_button.clicked.connect(self._statusbar_help_dialog)
		self._help_button.setToolTip("Statusbar Help...")
		self.addPermanentWidget(self._help_button)

		self._msg_idx_label.removeProgressBar()

	def _buffer_entry(self, entry_tuple):
		"""The entry_tuple looks like: (msg, timeout, fg, bg, bold)"""

		# Before we can update the msg index, we need to insure
		# that we have not reached the limit of the buffer size
		if self._displayed_msg_idx >= self._buffer_size - 1:
			# Reached limit of buffer, so we delete the oldest entry
			entry_to_throw_away = self._bufferd_msgs.pop(0)
			logger.warning("Reached limit of buffer throwing away top entry at idx 0: {}".format(entry_to_throw_away))

		# unpack the tuple
		msg, timeout, fg, bg, bold = entry_tuple

		# Let's add a timestamp to this entry
		now = datetime.now()
		timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

		# enqueue the message
		self._bufferd_msgs.append((msg, timeout, fg, bg, bold, timestamp))

		self._displayed_msg_idx = self._displayed_msg_idx + 1

		logger.warning("At idx: {} Buffered: {}, to:{}, fg:{}, bg:{}, bold:{}, ts:{}".format(self._displayed_msg_idx, msg, timeout, fg, bg, bold, timestamp))

	def _update_msg_idx_label(self):
		"""Use the _displayed_msg_idx to update the _msg_idx_label widget"""
		if self._displayed_msg_idx < 0:
			# If there are no message yet displayed, the label is all dashes
			#label_text = '-' * (len(str(self._buffer_size)) + 1)
			self._clear_msg_idx_label()
			return()
		
		label_text = self._displayed_msg_idx_format.format(self._displayed_msg_idx, len(self._bufferd_msgs)-1,self._timer_wait_q.qsize())
		#logger.debug("Updating msg index label text: {}".format(label_text))
		self._msg_idx_label.setText(label_text)
		#self._msg_idx_label.setAlignment(Qt.AlignCenter)

	def _clear_msg_idx_label(self):
		label_text = '-' * (len(str(self._buffer_size)) + 1) + '/' + '-' * (len(str(self._buffer_size)) + 1) + ' [-]'
		#logger.debug("label text: {}".format(label_text))
		self._msg_idx_label.setText(label_text)	
		self._msg_idx_label.setAlignment(Qt.AlignCenter)

	def _move_viewport(self, delta):
		# Enforce displayed msg idx wrapping
		if len(self._bufferd_msgs) == 0:
			# The queue is empty
			self._displayed_msg_idx = -1
		else:
			# There are messages in the queue

			# These are special cases for the page size commands (PAGE_UP, PAGE_DOWN)
			if (self._displayed_msg_idx == 0) and (delta == -1 * self._buf_page_size):
				# if we are displaying the top of the buffer and we get a PAGE_UP, go to the end of the buffer
				self._displayed_msg_idx = len(self._bufferd_msgs) - 1
			
			elif (self._displayed_msg_idx == len(self._bufferd_msgs) - 1) and (delta == self._buf_page_size):
				# if we are displaying the bottom of the buffer and we get a PAGE_DOWN, go to the top of the buffer
				self._displayed_msg_idx = 0

			elif (self._displayed_msg_idx < self._buf_page_size) and (delta == -1 * self._buf_page_size):
				# if we are displaying a location that is less than the page size away from the top of the buffer,
				# and we get a PAGE_UP, go to the top of the buffer
				self._displayed_msg_idx = 0

			elif (self._displayed_msg_idx > len(self._bufferd_msgs) - 1 - self._buf_page_size) and \
					delta == self._buf_page_size:
				# if we are displaying a location that is within a page size of the end of the bugger, 
				# and we get a PAGE_DOWN, go to the bottom of the buffer
				self._displayed_msg_idx = len(self._bufferd_msgs) - 1

			else:
				# Normal cases, we are moving by just one location up or down
				self._displayed_msg_idx += delta

				if self._displayed_msg_idx < 0:
					# we are beyond the top of the buffer, wrap to end
					self._displayed_msg_idx = len(self._bufferd_msgs) - 1

				if self._displayed_msg_idx > len(self._bufferd_msgs) - 1:
					# we are beyond the end of the buffer, wrap to beginning (home)
					self._displayed_msg_idx = 0

			self._display_viewport()

	def _format_text(self, fg, bg, bold):
		if self._widget:
			if bg and fg:
				self._widget.setStyleSheet("color: {}; background-color: {};".format(fg, bg))
			elif bg:
				self._widget.setStyleSheet("background-color: {};".format(bg))
			elif fg:
				self._widget.setStyleSheet("color: {};".format(fg))
			
			if bold:
				font = QFont()
				font.setBold(True)
				self._widget.setFont(font)

	def _display_viewport(self):

		self.clearMessage()

		# We ignore the timeout when we are moving through the buffer
		msg, timeout, fg, bg, bold, time_not_used = self._bufferd_msgs[self._displayed_msg_idx]
		
		self._widget = QLabel(msg)

		self._format_text(fg, bg, bold)

		self.addWidget(self._widget, stretch=10)
		self._update_msg_idx_label()

	def _add_key_modifiers(self, key=None):
		# https://stackoverflow.com/questions/8772595/how-to-check-if-a-keyboard-modifier-is-pressed-shift-ctrl-alt
		if key:
			QModifiers = QApplication.keyboardModifiers()
			self._key_modifiers = []
			if (QModifiers & Qt.ControlModifier) == Qt.ControlModifier:
				self._key_modifiers.append('control')
			if (QModifiers & Qt.AltModifier) == Qt.AltModifier:
				self._key_modifiers.append('alt')
			if (QModifiers & Qt.ShiftModifier) == Qt.ShiftModifier:
				self._key_modifiers.append('shift')
			new_key = ''
			for modifier in self._key_modifiers:
				new_key += modifier + '-'
			new_key += key
			return(new_key)

	@pyqtSlot()
	def _timer_wait_q_emptied(self):
		print("WAIT QUEUE EMPTIED")

	def _msg_timeout_fired(self, timed_msg=False):
		"""Remove the widget whose timer fired"""
		logger.debug("SingleShot Timer Fired")

		if self._timer_progressbar_update:
			self._timer_progressbar_update.stop()
			# If the progressbar starts filled rather than empty,
			# it will end filled, so clear it with this call.
			# If the progressbar starts empty rather than filled,
			# this call is superfluous.
			self._msg_idx_label.removeProgressBar()

		self._timer = None
		if not self._timer_wait_q.empty():
			msg_entry = self._timer_wait_q.get()
			logger.debug("Dequeued waiting message: {}".format(msg_entry[0]))
			self._buffer_this_entry(msg_entry)

			if self._timer_wait_q.empty():
				if self._timer_wait_q_emptied_signal:
					self._timer_wait_q_emptied_signal.empty()
		else:
			if timed_msg:
				# This was a msg with a non-zero timeout, so clear it
				self.clearMessage()

	def _update_progressbar(self):
		self._msg_idx_label.updateProgress(self._progressbar_delta)
		self._timer_progressbar_update.start(1000)

	def _buffer_this_entry(self, msg_entry):
		msg, timeout, fg, bg, bold = msg_entry
		self.clearMessage()
		self._widget = QLabel(msg)
		logger.debug("Displaying & Buffering Msg: {}".format(msg))

		self._format_text(fg, bg, bold)

		if timeout > 0:
			logger.debug("... timeout > 0...")
			if self._timer is None:
				logger.debug("... no timer running...")
				# No currently active timer, so we set one up...
				# but first lets setup the countdown progressbar if timer is long enough
				if timeout > 2000: # 2 seconds
					logger.debug("... timer greater than 2 seconds...")
					self._progressbar_delta = 1 / (timeout/1000)
					logger.info("Setting up ProgressBar Timer: {}".format(self._progressbar_delta))
					self._msg_idx_label.updateProgress(self._progressbar_delta)
					self._timer_progressbar_update = QTimer()
					self._timer_progressbar_update.timeout.connect(self._update_progressbar)
					self._timer_progressbar_update.start(1000)

				self._timer = QTimer()
				self._timer.singleShot(timeout, lambda: self._msg_timeout_fired(timed_msg=True))
			else:
				logger.debug("... there is a pending timer, so wait queue this msg")
				# There is a pending timer, so put this message on the wait queue
				self._timer_wait_q.put((msg, timeout, fg, bg, bold))
		else:
			logger.debug("... timer = 0, setting up a 1.5 second single shot timer...")
			# timeout == 0
			self._process_zero_timeout_timer = QTimer()
			self._process_zero_timeout_timer.singleShot(1500, lambda: self._msg_timeout_fired(timed_msg=False))

		self._buffer_entry((msg, timeout, fg, bg, bold))
		logger.debug("...adding message widget to statusbar...")
		self.addWidget(self._widget, stretch=10)
		self._update_msg_idx_label()

	def _enqueue_to_wait_q(self, msg, timeout, fg, bg, bold):
		# if timeout == 0:
		# 	# We need some small timeout here so the entry gets removed from the
		# 	# wait queue by the firing of the singleShot timer
		# 	timeout = 1000  # 1000 = 1 second
		msg_entry = (msg, timeout, fg, bg, bold)
		self._timer_wait_q.put(msg_entry)
		self._update_msg_idx_label()

	def _save_message_buffer_to_file(self, msg_buffer_file):
		logger.info("Writing message buffer to file '{}'".format(msg_buffer_file))
		width = len(str(len(self._bufferd_msgs))) + 1
		fmt = "{" + "0:0{}d".format(width) + "}"
		idx = 0
		with open(msg_buffer_file, 'w') as mbf:
			for entry in self._bufferd_msgs:
				idx_str = fmt.format(idx)
				msg, timeout, fg, bg, bold, timestamp = entry 
				mbf.writelines("{}: {} {} msecs FG:{} BG:{} BOLD:{} @ {}\n".format(idx_str, msg, timeout, fg, bg, bold, timestamp))
				idx += 1

	def _statusbar_help_dialog(self):
		self.about_dialog = AboutDialog(self)
		self.about_dialog.exec_()

	# -------------------------------------------------------------------------
	# PyQtMessageBar's Public API
	# -------------------------------------------------------------------------

	# Properties --------------------------------------------------------------
	# @property
	# def buffersize(self):
	# 	return(self._buffer_size) 

	# Methods -----------------------------------------------------------------
	def getWaitQueueDepth(self):
		"""Returns the wait queue depth (int)"""
		if self._timer_wait_q.empty():
			return(0)
		else:
			return(self._timer_wait_q.qsize())

	def waitQueueIsEmpty(self):
		"""Returns True if wait queue is empty, false otherwise."""
		return(self._timer_wait_q.empty())

	# def setBufferSize(self, size_int):
	# 	"""Set message buffer size.

	# 	Parameters
	# 	----------
	# 	size_int : int
	# 		This is the number of messages that can be buffered before the oldest
	# 		message is lost

	# 	Returns
	# 	-------
	# 	Nothing
	# 		Nothing

	# 	Note that the buffer size is never allowed to go below the default buffer size.
	# 	Which is the constant **pyqtmessagebar.DEFAULT_BUFFER_SIZE**.
	# 	"""
	# 	if isinstance(size_int, int):
	# 		if size_int < DEFAULT_BUFFER_SIZE:
	# 			size_int = DEFAULT_BUFFER_SIZE
	# 	else:
	# 		size_int = DEFAULT_BUFFER_SIZE
			
	# 	self._buffer_size  = size_int

	def getBufferSize(self):
		"""Returns the current message buffer size."""
		return(self._buffer_size )

	# def setEnableSeparators(self, flag):
	# 	"""Sets the enable separators boolean to flag value.
	# 	The effect of this flag being True is that any
	# 	widgets added to the statusbar via the addPermanentWidget()
	# 	call will have a separator placed to the left of the widget added.
	# 	"""
	# 	if isinstance(flag, bool):
	# 		self._enable_separators = flag
	
	def getEnableSeparators(self):
		"""Returns the value of the enable separators flag."""
		return(self._enable_separators)

	# def setEnableDarkIcon(self, help_icon_indicator):
	# 	"""Sets the built-in help icon to the help_icon_indicator.

	# 	Parameters
	# 	----------
	# 	help_icon_indicator : str constant
	# 		Must be one of the three following values module constants
	# 		BUILT_IN_HELP_ICON_LIGHT, BUILT_IN_HELP_ICON_DARK, or 
	# 		BUILT_IN_HELP_ICON_TWO_TONE. The default is LIGHT.

	# 	Note the built-in help icons can be replaced using specifying the 
	# 	**help_icon_file** parameter to the **PyQtMessageBar** constructor.
	# 	"""
	# 	if isinstance(help_icon_indicator, str):
	# 		if help_icon_indicator in HELP_ICON_INDICATORS:
	# 			self._built_in_help_icon = help_icon_indicator
	# 		else:
	# 			self._built_in_help_icon = BUILT_IN_HELP_ICON_LIGHT
	# 	else:
	# 		self._built_in_help_icon = BUILT_IN_HELP_ICON_LIGHT

	def getBuiltInHelpIcon(self):
		"""Returns the value of the built-in help icon indicator."""
		return(self._built_in_help_icon)

	def setProgressBarColor(self, color_text):
		"""Sets the color of the countdown timer progress bar
		to the color value specified by color_text.

		Note that color_text can be any color representation
		supported by the `colour package <https://pypi.org/project/colour/>`_.
		"""
		self._msg_idx_label.setProgressBarColor(color_text) 

	def getProgressBarColor(self):
		"""Returns the value of the countdown timer progress bar color."""
		self._progressbar_color = self._msg_idx_label.getProgressBarColor()
		return(self._progressbar_color)

	def clearMessage(self):
		"""This method added to distinguish clearing (or removing) the currently
		displayed message and removing some other custom widget that the user 
		may have added."""
		if self._widget:
			self.removeWidget(self._widget)
			self._widget = None
			self._clear_msg_idx_label()	


	# -------------------------------------------------------------------------
	# Here a three helper methods that serve as shorthand for setting up
	# common color schemes for certain types of messages:
	#     showMessage(self, msg, timeout=0, fg=None, bg=None, bold=False)
	# -------------------------------------------------------------------------
	def showMessageError(self, msg):
		"""This is a helper method that serves as a short-hand call to 
		**showMessage()** that configures the message to be an error message
		which looks like:

			Yellow FG, Brick Red BG, Bold Text, No Timeout

		.. image:: _static/error_message.png
		   :align: center

		"""
		self.showMessage(msg, fg='#ffff00', bg='#aa0000', bold=True)

	def showMessageWarning(self, msg):
		"""This is a helper method that serves as a short-hand call to 
		**showMessage()** that configures the message to be an warning
		message which looks like:

			Black FG, Yellow BG, Bold Text, No Timeout

		.. image:: _static/warning_message.png
		   :align: center

		"""
		self.showMessage(msg, fg='#000000', bg='#ffff00', bold=True)

	def showMessageAskForInput(self, msg):
		"""his is a helper method that serves as a short-hand call to 
		**showMessage()** that configures the message to be an affirmation
		message which looks like:

			White FG, Forest Green BG, Bold Text, No Timeout

		.. image:: _static/affirmation_message.png
		   :align: center

		"""
		self.showMessage(msg, fg='#ffffff', bg='#005500', bold=True)

	# -------------------------------------------------------------------------
	# Overriding these Qt QStatusBar methods
	# -------------------------------------------------------------------------

	def keyPressEvent(self, e):
		"""
		**Overrides Qt keyPressEvent()**
		
		This method overrides the Qt keyPressEvent method to add keyboard input
		processing. Any keys NOT processed here are passed on to the base class
		implementation of keyPressEvent().

		See `QWidget keyPressEvent docs <https://doc.qt.io/qt-5/qwidget.html#keyPressEvent>`_.
		
		The following keys are recognized, all other keys are passed to the base
		class implementation of keyPressEvent():

			* Qt.Key_Up
			* Qt.Key_Home.
			* Qt.Key_Down
			* Qt.Key_End
			* Qt.Key_PageUp
			* Qt.Key_PageDown
			* control-alt-X
			* control-alt-shift-X
			* control-alt-S
			* control-alt-shift-S

		.. note:: The two key sequences based on the S key, will be disabled if the 
				  **PyQtMessageBar** constructor is called without specifying the **save_msg_buffer_dir**
				  parameter.
		
		Parameters
		----------
		e : QEvent
			This event returns the key via the **e.key()** method call.
		
		Returns
		-------
		Nothing
			None, but does call the appropriate PyQtMessageBar method to handle
			recognized keys.
		"""
		if e.type() == QEvent.KeyPress:
			#print("SMARTSTATUSBAR: press {}".format(e.key()))
			key = e.key()
			if key in KEY_MAP:
				if key in KEY_MOVE:
					# https://doc.qt.io/qt-5/qt.html#Key-enum
					if key == Qt.Key_Up:
						#print("UP ARROW")
						if self._widget:
							# only if there is a widget being displayed to we decrement
							# if there is no widget being displayed the idx is already
							# pointing to the bottom of the buffer, so no need to decrement.
							delta = -1
						else:
							delta = 0
					if key == Qt.Key_Down:
						#print("DOWN ARROW")
						delta = 1
					if key == Qt.Key_PageUp:
						#print("PAGE UP")
						delta = -1 * self._buf_page_size
					if key == Qt.Key_PageDown:
						#print("PAGE DOWN") 
						delta = self._buf_page_size
					if key == Qt.Key_Home:
						#print("HOME")
						self._displayed_msg_idx = 0
						delta = 0
					if key == Qt.Key_End:
						#print("END")
						self._displayed_msg_idx = len(self._bufferd_msgs) - 1
						delta = 0

					self._move_viewport(delta)

				elif key in KEY_CMDS:
					if key == Qt.Key_X:
						key = self._add_key_modifiers('X')
						if key == 'control-alt-shift-X':
							logger.debug("Deleting entire message buffer...")
							self._displayed_msg_idx = -1
							self._bufferd_msgs.clear()
							self.clearMessage()

						if key == 'control-alt-X':
							entry_to_throw_away = self._bufferd_msgs.pop(self._displayed_msg_idx)
							logger.debug("Deleted message @ idx {}: {}".format(self._displayed_msg_idx, entry_to_throw_away))
							self._move_viewport(0)

					if key == Qt.Key_S:
						if self._save_msg_buffer_dir:
							key = self._add_key_modifiers('S')
							if key == 'control-alt-shift-S':

								msg_buffer_file = datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss%f") + '.msgs'
								start_file_name = os.path.join(self._save_msg_buffer_dir, msg_buffer_file)

								msg_buffer_file, _ = QFileDialog.getSaveFileName(self, 'Save Message Buffer File',
													start_file_name, "Msg Buf Files (*.msgs)")

								self._save_message_buffer_to_file(msg_buffer_file)

							if key == 'control-alt-S':
								msg_buffer_file = os.path.join(self._save_msg_buffer_dir, datetime.now().strftime("%Y-%m-%d-%Hh%Mm%Ss%f") + '.msgs')	

								self._save_message_buffer_to_file(msg_buffer_file)

			else:
				# If we do not act on the key, then we need to call the base class's
				# implementation of keyPressEvent() so some other widget may act on it.
				super(PyQtMessageBar, self).keyPressEvent(e)


	def addPermanentWidget(self, widget, stretch=0):
		"""**Overrides QStatusBar.addPermanentWidget()**

		This method overrides the base class implementation so
		we can add the ability to insert a separator if so enabled.

		Then the base class addPermantWidget() is called."""
		if self._enable_separators:
			super(PyQtMessageBar, self).addPermanentWidget(VLine())

		super(PyQtMessageBar, self).addPermanentWidget(widget, stretch)


	def insertPermanentWidget(self, widget, stretch=0):
		"""**Overrides QStatusBar.insertPermanentWidget()**

		This method overrides the base class implementation so
		we can add the ability to insert a separator if so enabled.

		Then the base class insertPermanentWidget() is called."""
		if self._enable_separators:
			super(PyQtMessageBar, self).insertPermanentWidget(VLine())

		super(PyQtMessageBar, self).insertPermanentWidget(widget, stretch)

	def currentMessage(self):
		"""**Overrides QStatusBar.currentMessage()**

		Returns the currently displayed message or the empty string if
		there is no currently dislayed message."""
		if self._widget:
			msg = self._widget.text()
		else:
			msg = ''
		return(msg)

	def showMessage(self, msg, timeout=0, fg=None, bg=None, bold=False):
		"""**Overrides QStatusBar.showMessage()**

		This method completely replaces Qt's QStatusBar.ShowMessage() 
		because we need inner knowledge of when messages timeout.

		We also add colors for foreground (fg), background (bg), and
		a flag for enabling bold text.
		
		Note, we do not provide the stretch parameter because we control
		the layout, at least we think we do. :)

		Parameters
		----------
		msg : str
			The statusbar message to be displayed and buffered.
		timeout : int
			If non-zero the message will have a timeout and be removed
			from the statusbar display once the timeout expires.
		fg : str (color)
			The foreground color (text color) of the message to be displayed.
			The color value can be any color representation supported by
			the `colour package <https://pypi.org/project/colour/>`_.
			If not specified, the system default color is used.
		bg : str (color)
			The background color of the message to be displayed.
			The color value can be any color representation supported by
			the `colour package <https://pypi.org/project/colour/>`_.
			If not specified, the system default color is used.
		bold: bool
			If True the text of the message will be bold.

		"""
		# pad msg with a leading space...
		msg = ' ' + msg
		logger.debug("showMessage called...")
		if self._widget:
			logger.debug("msg widget already being displayed...")
			# There is a msg being displayed...
			# If there are other pending messages that have not yet been displayed,
			# we enqueue this message to the wait queue.
			# If msg being displayed has no timeout, we clear it and show this msg.

			if self._timer:
				logger.debug("Wait Queueing message: '{}'".format(msg))
				# We are waiting the currently diplayed message to timeout,
				# or we have older pending messages that have not yet been displayed;
				# so put this message on the wait queue
				self._enqueue_to_wait_q(msg, timeout, fg, bg, bold)

				return()
			else:
				logger.debug("No wait Q timer running...")

		# No message being displayed, however, we may have previous message in the wait queue
		# being processed by the singleShot Timer; only if the wait queue is empty do we
		# process the caller's message; otherwise, we put it on the wait queue.
		if self._timer_wait_q.empty():
			logger.debug("Wait Q empty, clear displayed message and buffer new msg.")
			# self.clearMessage() -->> This is called first thing in _buffer_this_entry() below
			self._buffer_this_entry((msg, timeout, fg, bg, bold))
		else:
			logger.debug("Wait Q NOT empty, enqueue current message...")
			self._enqueue_to_wait_q(msg, timeout, fg, bg, bold)
