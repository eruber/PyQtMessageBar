"""
testbed

Test Bed for Py Qt Smart StatusBar

GPL LICENSE
This file is part of AutoFoE.

AutoFoE is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

AutoFoE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with AutoFoE in the file named COPYING. If not, 
see <https://www.gnu.org/licenses/>.

COPYRIGHT (C) 2019-2020 Exil Risedo (ExilRisedo@protonmail.com)

"""
# ----------------------------------------------------------------------------
# ------------------------ Python Standard Library ---------------------------
# ----------------------------------------------------------------------------
import os
import sys 
import logging
import time
import inspect
import random

# ----------------------------------------------------------------------------
# -------------------------- Third Party Packages ----------------------------
# ----------------------------------------------------------------------------
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt, QSize, QTimer, QSettings, QEvent
from PyQt5.QtGui import QIcon, QPainter, QColor, QKeySequence
from PyQt5.QtWidgets import (
	QAction, 
	QApplication, 
	QButtonGroup,
	QCheckBox,
	QComboBox,
	QDesktopWidget,
	QFileDialog,
	QGridLayout,
	QHBoxLayout,
	QLabel,
	QLineEdit,
	QMainWindow,
	QVBoxLayout,
	QWidget,
	QMainWindow, 
	QPushButton,
	QRadioButton,
	QSizePolicy,
	QShortcut,
	QSpinBox,
	QStatusBar,
	QToolBar,
	QTextEdit,
	)

from colour import Color

# ----------------------------------------------------------------------------
# -------------------------- Application Packages ----------------------------
# ----------------------------------------------------------------------------
#from pyqtmessagebar.pyqtmessagebar import PyQtMessageBar
from pyqtmessagebar import PyQtMessageBar
import pyqtlineeditprogressbar as progressbar
import pyqtmessagebar

# ----------------------------------------------------------------------------
# ----------------------- Module Global & Constants --------------------------
# ----------------------------------------------------------------------------
PROGRESS_BAR_COLOR_SET = [
	progressbar.DEFAULT_COLOR_GREEN, 
	progressbar.DEFAULT_COLOR_BLUE, 
	progressbar.DEFAULT_COLOR_RED, 
	progressbar.DEFAULT_COLOR_ORANGE, 
	progressbar.DEFAULT_COLOR_YELLOW, 
	progressbar.DEFAULT_COLOR_PURPLE,
	None, None, None, None, None, None,      # NONE means generate a random "light" color 
	]

TIMEOUT_SELECTION_SET = [
	None, None, None, None, None, None, 1, 1, 1,1 
]

# This could break in future versions of Python should they change the logging
# level integer values
LEVEL_MAP = {
	10 : 'DEBUG',
	20 : 'INFO',
	30 : 'WARNING',
	40 : 'ERROR',
	50 : 'CRITICAL',
}

# ----------------------------------------------------------------------------
# --------------------- Module Classes & Functions ---------------------------
# ----------------------------------------------------------------------------
class StatusBarControlPanel(QWidget):
	def __init__(self, parent):
		super(StatusBarControlPanel, self).__init__(parent=parent)

		self.parent = parent

		self.groupBox_cfg_sbar = QtWidgets.QGroupBox(self.parent)
		self.groupBox_cfg_sbar.setGeometry(QtCore.QRect(10, 10, 700, 50))
		#self.groupBox_cfg_sbar.setObjectName("groupBox_cfg_sbar")
		self.groupBox_cfg_sbar.setTitle("Configure StatusBar")

		self.checkBox_enable_seps = QtWidgets.QCheckBox(self.groupBox_cfg_sbar)
		self.checkBox_enable_seps.setGeometry(QtCore.QRect(110, 18, 120, 20))
		#self.checkBox_enable_seps.setObjectName("checkBox_enable_seps")
		self.checkBox_enable_seps.setText("Enable Separators")
		self.checkBox_enable_seps.toggled.connect(self.parent.enable_separators)




		self.comboBox_help_icon_style  = QtWidgets.QComboBox(self.groupBox_cfg_sbar)
		self.comboBox_help_icon_style.addItems(['Light Help Icon', 'Dark Help Icon', 'Two Tone Help Icon'])
		self.comboBox_help_icon_style.setGeometry(QtCore.QRect(240, 18, 130, 20))
		self.comboBox_help_icon_style.currentIndexChanged.connect(self.parent.help_icon_changed)

		# self.checkBox_enable_dark_help_icon = QtWidgets.QCheckBox(self.groupBox_cfg_sbar)
		# self.checkBox_enable_dark_help_icon.setGeometry(QtCore.QRect(240, 18, 130, 20))
		# self.checkBox_enable_dark_help_icon.setObjectName("checkBox_enable_dark_help_icon")
		# self.checkBox_enable_dark_help_icon.setText("Enable Dark Help Icon")
		# self.checkBox_enable_dark_help_icon.toggled.connect(self.parent.enable_dark_help)





		self.pushButton_custom_help_icon = QtWidgets.QPushButton(self.groupBox_cfg_sbar)
		self.pushButton_custom_help_icon.setGeometry(QtCore.QRect(390, 18, 125, 20))
		self.pushButton_custom_help_icon.setObjectName("pushButton_custom_help_icon")
		self.pushButton_custom_help_icon.setText("Load Custom Help Icon 1")
		self.pushButton_custom_help_icon.clicked.connect(self.parent.load_custom_help_icon_1)

		self.pushButton_custom_help_icon = QtWidgets.QPushButton(self.groupBox_cfg_sbar)
		self.pushButton_custom_help_icon.setGeometry(QtCore.QRect(530, 18, 125, 20))
		self.pushButton_custom_help_icon.setObjectName("pushButton_custom_help_icon")
		self.pushButton_custom_help_icon.setText("Load Custom Help Icon 2")
		self.pushButton_custom_help_icon.clicked.connect(self.parent.load_custom_help_icon_2)


		self.groupBox_custom_msg = QtWidgets.QGroupBox(self.parent)
		self.groupBox_custom_msg.setGeometry(QtCore.QRect(10, 60, 700, 211))
		self.groupBox_custom_msg.setObjectName("groupBox_custom_msg")
		self.groupBox_custom_msg.setTitle("Submit a Custom Message to the StatusBar")

		self.lineEdit_msg = QtWidgets.QLineEdit(self.groupBox_custom_msg)
		self.lineEdit_msg.setGeometry(QtCore.QRect(10, 30, 551, 20))
		self.lineEdit_msg.setObjectName("lineEdit_msg")
		self.lineEdit_msg.setText("This is the message text")

		self.groupBox_timeout_CD_color = QtWidgets.QGroupBox(self.groupBox_custom_msg)
		self.groupBox_timeout_CD_color.setGeometry(QtCore.QRect(190, 60, 451, 111))
		self.groupBox_timeout_CD_color.setAlignment(int(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter))
		self.groupBox_timeout_CD_color.setObjectName("groupBox_timeout_CD_color")
		self.groupBox_timeout_CD_color.setTitle("Timeout")

		self.groupBox_timeout = QtWidgets.QGroupBox(self.groupBox_timeout_CD_color)
		self.groupBox_timeout.setGeometry(QtCore.QRect(20, 30, 71, 51))
		self.groupBox_timeout.setObjectName("groupBox_timeout")
		self.groupBox_timeout.setTitle("Seconds")

		self.spinBox_timeout = QtWidgets.QSpinBox(self.groupBox_timeout)
		self.spinBox_timeout.setGeometry(QtCore.QRect(10, 20, 42, 20))
		self.spinBox_timeout.setMaximum(20)
		self.spinBox_timeout.setProperty("value", 0)
		self.spinBox_timeout.setObjectName("spinBox_timeout")

		self.groupBox = QtWidgets.QGroupBox(self.groupBox_timeout_CD_color)
		self.groupBox.setGeometry(QtCore.QRect(100, 20, 341, 81))
		self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
		self.groupBox.setObjectName("groupBox")
		self.groupBox.setTitle("Countdown Background Color")

		self.radioButton_TO_CD_green = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_green.setGeometry(QtCore.QRect(10, 20, 51, 17))
		self.radioButton_TO_CD_green.setObjectName("radioButton_TO_CD_green")
		self.radioButton_TO_CD_green.toggled.connect(self.parent.picked_TO_CD_green)
		self.radioButton_TO_CD_green.setText("Green")

		self.radioButton_TO_CD_red = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_red.setGeometry(QtCore.QRect(10, 40, 51, 17))
		self.radioButton_TO_CD_red.setObjectName("radioButton_TO_CD_red")
		self.radioButton_TO_CD_red.toggled.connect(self.parent.picked_TO_CD_red)
		self.radioButton_TO_CD_red.setText("Red")

		self.radioButton_TO_CD_blue = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_blue.setGeometry(QtCore.QRect(80, 20, 51, 17))
		self.radioButton_TO_CD_blue.setObjectName("radioButton_TO_CD_blue")
		self.radioButton_TO_CD_blue.toggled.connect(self.parent.picked_TO_CD_blue)
		self.radioButton_TO_CD_blue.setText("Blue")

		self.radioButton_TO_CD_orange = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_orange.setGeometry(QtCore.QRect(80, 40, 61, 17))
		self.radioButton_TO_CD_orange.setObjectName("radioButton_TO_CD_orange")
		self.radioButton_TO_CD_orange.toggled.connect(self.parent.picked_TO_CD_orange)
		self.radioButton_TO_CD_orange.setText("Orange")

		self.radioButton_TO_CD_yellow = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_yellow.setGeometry(QtCore.QRect(150, 20, 61, 17))
		self.radioButton_TO_CD_yellow.setObjectName("radioButton_TO_CD_yellow")
		self.radioButton_TO_CD_yellow.toggled.connect(self.parent.picked_TO_CD_yellow)
		self.radioButton_TO_CD_yellow.setText("Yellow")

		self.radioButton_TO_CD_purple = QtWidgets.QRadioButton(self.groupBox)
		self.radioButton_TO_CD_purple.setGeometry(QtCore.QRect(150, 40, 61, 17))
		self.radioButton_TO_CD_purple.setObjectName("radioButton_TO_CD_purple")
		self.radioButton_TO_CD_purple.setChecked(True)
		self.radioButton_TO_CD_purple.toggled.connect(self.parent.picked_TO_CD_purple)
		self.radioButton_TO_CD_purple.setText("Purple")

		self.pushButton_TO_CD_color_custom = QtWidgets.QPushButton(self.groupBox)
		self.pushButton_TO_CD_color_custom.setGeometry(QtCore.QRect(240, 30, 75, 20))
		self.pushButton_TO_CD_color_custom.setObjectName("pushButton_TO_CD_color_custom")
		self.pushButton_TO_CD_color_custom.clicked.connect(self.parent._pick_TO_CD_color)
		self.pushButton_TO_CD_color_custom.setText("Custom")

		self.checkBox_bold = QtWidgets.QCheckBox(self.groupBox_custom_msg)
		self.checkBox_bold.setGeometry(QtCore.QRect(570, 30, 70, 20))
		self.checkBox_bold.setObjectName("checkBox_bold")
		self.checkBox_bold.setText("Bold Text")

		self.groupBox_BG = QtWidgets.QGroupBox(self.groupBox_custom_msg)
		self.groupBox_BG.setGeometry(QtCore.QRect(10, 120, 171, 51))
		self.groupBox_BG.setObjectName("groupBox_BG")
		self.groupBox_BG.setTitle("Message Background Color")

		self.pushButton_BG_color = QtWidgets.QPushButton(self.groupBox_BG)
		self.pushButton_BG_color.setGeometry(QtCore.QRect(15, 20, 75, 20))
		self.pushButton_BG_color.setObjectName("pushButton_BG_color")
		self.pushButton_BG_color.clicked.connect(self.parent.pick_BG_color)
		self.pushButton_BG_color.setText("Custom BG")

		self.checkBox_default_BG = QtWidgets.QCheckBox(self.groupBox_BG)
		self.checkBox_default_BG.setGeometry(QtCore.QRect(103, 20, 70, 20))
		self.checkBox_default_BG.setObjectName("checkBox_default_BG")
		self.checkBox_default_BG.setText("Default")
		self.checkBox_default_BG.setChecked(True)
		self.checkBox_default_BG.stateChanged.connect(self.parent.bg_default_changed)

		self.groupBox_FG = QtWidgets.QGroupBox(self.groupBox_custom_msg)
		self.groupBox_FG.setGeometry(QtCore.QRect(10, 60, 171, 51))
		self.groupBox_FG.setObjectName("groupBox_FG")
		self.groupBox_FG.setTitle("Message Text Color")

		self.pushButton_FG_color = QtWidgets.QPushButton(self.groupBox_FG)
		self.pushButton_FG_color.setGeometry(QtCore.QRect(15, 20, 75, 20))
		self.pushButton_FG_color.setObjectName("pushButton_FG_color")
		self.pushButton_FG_color.clicked.connect(self.parent.pick_FG_color)
		self.pushButton_FG_color.setText("Custom FG")

		self.checkBox_default_FG = QtWidgets.QCheckBox(self.groupBox_FG)
		self.checkBox_default_FG.setGeometry(QtCore.QRect(103, 20, 70, 20))
		self.checkBox_default_FG.setObjectName("checkBox_default_FG")
		self.checkBox_default_FG.setText("Default")
		self.checkBox_default_FG.setChecked(True)
		self.checkBox_default_FG.stateChanged.connect(self.parent.fg_default_changed)


		self.pushButton_AFFIRM = QtWidgets.QPushButton(self.groupBox_custom_msg)
		self.pushButton_AFFIRM.setGeometry(QtCore.QRect(647, 75, 45, 20))
		self.pushButton_AFFIRM.setObjectName("pushButton_AFFIRM")
		self.pushButton_AFFIRM.clicked.connect(lambda: self.parent.helper_msg('AFFIRM'))
		self.pushButton_AFFIRM.setText("AFFIRM")

		self.pushButton_WARN = QtWidgets.QPushButton(self.groupBox_custom_msg)
		self.pushButton_WARN.setGeometry(QtCore.QRect(647, 105, 45, 20))
		self.pushButton_WARN.setObjectName("pushButton_WARN")
		self.pushButton_WARN.clicked.connect(lambda: self.parent.helper_msg('WARN'))
		self.pushButton_WARN.setText("WARN")

		self.pushButton_ERROR = QtWidgets.QPushButton(self.groupBox_custom_msg)
		self.pushButton_ERROR.setGeometry(QtCore.QRect(647, 135, 45, 20))
		self.pushButton_ERROR.setObjectName("pushButton_ERROR")
		self.pushButton_ERROR.clicked.connect(lambda: self.parent.helper_msg('ERROR'))
		self.pushButton_ERROR.setText("ERROR")

		self.pushButton_submit = QtWidgets.QPushButton(self.groupBox_custom_msg)
		self.pushButton_submit.setGeometry(QtCore.QRect(290, 175, 75, 20))
		self.pushButton_submit.setObjectName("pushButton_submit")
		self.pushButton_submit.clicked.connect(self.parent.submit_msg)
		self.pushButton_submit.setText("Submit")

		self.groupBox_random = QtWidgets.QGroupBox(self.parent)
		self.groupBox_random.setGeometry(QtCore.QRect(10, 270, 700, 75))
		self.groupBox_random.setObjectName("groupBox_random")
		self.groupBox_random.setTitle("Generate Random Messages")
		
		self.pushButton_random = QtWidgets.QPushButton(self.groupBox_random)
		self.pushButton_random.setGeometry(QtCore.QRect(10, 27, 60, 20))
		self.pushButton_random.setObjectName("pushButton_random")
		self.pushButton_random.clicked.connect(self.parent.do_random)
		self.pushButton_random.setText("Generate")

		init_value = 3

		self.lineEdit_slider_value = QtWidgets.QLineEdit(self.groupBox_random)
		self.lineEdit_slider_value.setReadOnly(True)
		self.lineEdit_slider_value.setGeometry(80, 27, 25, 20)
		self.lineEdit_slider_value.setMaxLength(3)
		self.lineEdit_slider_value.setText(str(init_value))
		self.lineEdit_slider_value.setAlignment(QtCore.Qt.AlignCenter)

		self.checkBox_double = QtWidgets.QCheckBox(self.groupBox_random)
		self.checkBox_double.setGeometry(QtCore.QRect(115, 27, 35, 20))
		self.checkBox_double.setObjectName("checkBox_double")
		self.checkBox_double.setText("x2")

		self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.groupBox_random, )
		self.slider.setGeometry(155, 25, 535, 30)
		self.slider.setTickInterval(1)
		self.slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
		self.slider.setMinimum(init_value)
		self.slider.setMaximum(105)
		self.slider.setSingleStep(1)
		self.slider.setValue(init_value)
		self.slider.valueChanged.connect(self.parent.slider_changed)


		self.groupBox_logging_level = QtWidgets.QGroupBox(self.parent)
		self.groupBox_logging_level.setGeometry(QtCore.QRect(10, 345, 700, 60))
		self.groupBox_logging_level.setObjectName("groupBox_logging_level")
		self.groupBox_logging_level.setTitle("Logging Level")


		self.radioButton_LogLevel_DEBUG = QtWidgets.QRadioButton(self.groupBox_logging_level)
		self.radioButton_LogLevel_DEBUG.setGeometry(QtCore.QRect(110, 23, 60, 20))
		self.radioButton_LogLevel_DEBUG.setObjectName("radioButton_LogLevel_DEBUG")
		self.radioButton_LogLevel_DEBUG.setChecked(True)
		self.radioButton_LogLevel_DEBUG.clicked.connect(lambda: self.parent.set_logging_level(logging.DEBUG))
		self.radioButton_LogLevel_DEBUG.setText("DEBUG")

		self.radioButton_LogLevel_INFO = QtWidgets.QRadioButton(self.groupBox_logging_level)
		self.radioButton_LogLevel_INFO.setGeometry(QtCore.QRect(200, 23, 60, 20))
		self.radioButton_LogLevel_INFO.setObjectName("radioButton_LogLevel_INFO")
		self.radioButton_LogLevel_INFO.clicked.connect(lambda: self.parent.set_logging_level(logging.INFO))
		self.radioButton_LogLevel_INFO.setText("INFO")

		self.radioButton_LogLevel_WARNING = QtWidgets.QRadioButton(self.groupBox_logging_level)
		self.radioButton_LogLevel_WARNING.setGeometry(QtCore.QRect(290, 23, 85, 20))
		self.radioButton_LogLevel_WARNING.setObjectName("radioButton_LogLevel_WARNING")
		self.radioButton_LogLevel_WARNING.clicked.connect(lambda: self.parent.set_logging_level(logging.WARNING))
		self.radioButton_LogLevel_WARNING.setText("WARNING")

		self.radioButton_LogLevel_ERROR = QtWidgets.QRadioButton(self.groupBox_logging_level)
		self.radioButton_LogLevel_ERROR.setGeometry(QtCore.QRect(405, 23, 65, 20))
		self.radioButton_LogLevel_ERROR.setObjectName("radioButton_LogLevel_ERROR")
		self.radioButton_LogLevel_ERROR.clicked.connect(lambda: self.parent.set_logging_level(logging.ERROR))
		self.radioButton_LogLevel_ERROR.setText("ERROR")

		self.radioButton_LogLevel_CRITICAL = QtWidgets.QRadioButton(self.groupBox_logging_level)
		self.radioButton_LogLevel_CRITICAL.setGeometry(QtCore.QRect(500, 23, 105, 20))
		self.radioButton_LogLevel_CRITICAL.setObjectName("radioButton_LogLevel_CRITICAL")
		self.radioButton_LogLevel_CRITICAL.clicked.connect(lambda: self.parent.set_logging_level(logging.CRITICAL))
		self.radioButton_LogLevel_CRITICAL.setText("CRITICAL")

		groupbox_style = "QGroupBox { font-weight: bold; border: 1px solid rgb(0, 0, 0); border-radius: 5px; margin-top: 7px; margin-bottom: 7px; padding: 2p;}"
		self.groupBox_cfg_sbar.setStyleSheet(groupbox_style)

		self.groupBox_custom_msg.setStyleSheet(groupbox_style)

		self.groupBox_random.setStyleSheet(groupbox_style)

		self.groupBox_logging_level.setStyleSheet(groupbox_style)

class MessageBarTestBed(QMainWindow):

	def __init__(self, app, parent=None,):
		super(MessageBarTestBed, self).__init__(parent)

		self._enable_separators = False
		#self._enable_dark_help = False
		self._built_in_help_icon = 'Light'
		self._icon_filename = None
		self._bg_color = None
		self._fg_color = None
		self._to_cd_color = None
		self._to_cd_green = progressbar.DEFAULT_COLOR_GREEN
		self._to_cd_red = progressbar.DEFAULT_COLOR_RED
		self._to_cd_blue = progressbar.DEFAULT_COLOR_BLUE
		self._to_cd_orange = progressbar.DEFAULT_COLOR_ORANGE
		self._to_cd_yellow = progressbar.DEFAULT_COLOR_YELLOW
		self._to_cd_purple = progressbar.DEFAULT_COLOR_PURPLE

		self.app = app
		self.app.setStyle('Fusion')
		self.resize(715,430)

		self.setuplogging()

		self.centralwidget = QWidget()
		self.setCentralWidget(self.centralwidget)

		self.setWindowTitle("PyQtMessageBar Test Bed")
		self.vLayout = QVBoxLayout(self.centralwidget)
		self.hLayout = QHBoxLayout()

		self.gridLayout = QGridLayout()
		self.gridLayout.setSpacing(0)

		# center the grid with stretch on both sides
		self.hLayout.addStretch(1)
		self.hLayout.addLayout(self.gridLayout)
		self.hLayout.addStretch(1)

		self.vLayout.addLayout(self.hLayout)
		# push grid to the top of the window
		self.vLayout.addStretch(1)

		self.sb_cp = StatusBarControlPanel(self)
		self.vLayout.addWidget(self.sb_cp)

		self.setDefaultStatusBar()

		# ssb == smart status bar
		self.ssb = self.statusBar()

		self.setCentralWidget(self.centralwidget)

	def setDefaultStatusBar(self):
		self.smartstatusbar_0 = PyQtMessageBar(self, parent_logger_name='TestBed')

		self.smartstatusbar_0.setFocusPolicy(Qt.StrongFocus)
		self.setFocusProxy(self.smartstatusbar_0)
		self.setStatusBar(self.smartstatusbar_0)

	def enable_separators(self):
		# print("ENABLE_SEPARATORS")
		self.configure_statusbar()

	# def enable_dark_help(self):
	# 	# print("ENABLE DARK HELP")
	# 	self._icon_filename = None
	# 	self.configure_statusbar()

	def help_icon_changed(self):
		self._icon_filename = None
		self.configure_statusbar()		

	def load_custom_help_icon_1(self):
		# print("LOAD CUSTOM HELP ICON 1")
		self._icon_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "white-on-red-cross.png")
		# print("Help Icon File Name: {}".format(self._icon_filename))
		self.configure_statusbar()

	def load_custom_help_icon_2(self):
		# print("LOAD CUSTOM HELP ICON 2")
		self._icon_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "red-on-white-cross.png")
		# print("Help Icon File Name: {}".format(self._icon_filename))
		self.configure_statusbar()

	def configure_statusbar(self):
		# print("CONFIGURE STATUSBAR")

		# if self.sb_cp.checkBox_enable_dark_help_icon.isChecked():
		# 	self._enable_dark_help = True
		# else:
		# 	self._enable_dark_help = False

		self._built_in_help_icon = self.sb_cp.comboBox_help_icon_style.currentText().split(' ')[0]

		if self.sb_cp.checkBox_enable_seps.isChecked():
			self._enable_separators = True
		else:
			self._enable_separators = False

		# print("Enable Seps: {}".format(self._enable_separators))
		# print("Enable Dark Help Icon: {}".format(self._enable_dark_help))
		# print("Help Icon File Name: {}".format(self._icon_filename))


		self.smartstatusbar = PyQtMessageBar(self, enable_separators=self._enable_separators,
												#enable_dark_help_icon=self._enable_dark_help,
												built_in_help_icon = self._built_in_help_icon ,
												help_icon_file=self._icon_filename,
												parent_logger_name='TestBed')
		self.setStatusBar(self.smartstatusbar)
		self.smartstatusbar.setFocusPolicy(Qt.StrongFocus)
		self.setFocusProxy(self.smartstatusbar)

		self.ssb = self.statusBar()

	def fg_default_changed(self, state):
		if state == QtCore.Qt.Checked:
			self._fg_color = None
			self.sb_cp.pushButton_FG_color.setStyleSheet("")
		else:
			pass
			# using _fg_color as set

	def bg_default_changed(self, state):
		if state == QtCore.Qt.Checked:
			self._bg_color = None
			self.sb_cp.pushButton_BG_color.setStyleSheet("")
		else:
			pass
			# using _bg_color as set

	def helper_msg(self, name):
		# msg = self.sb_cp.lineEdit_msg.text()
		if name == 'AFFIRM':
			self.ssb.showMessageAskForInput('This is a showMessage() helper for Affirmation of Input')
		elif name == 'WARN':
			self.ssb.showMessageWarning('This is a showMessage() helper for Warning messages')
		elif name == 'ERROR':
			self.ssb.showMessageError('This is a showMessage() helper for Error messages')

	def pick_FG_color(self):
		self._fg_color = QtWidgets.QColorDialog.getColor()
		if self._fg_color.isValid():
			self.logger.info("FG Color: {}".format(self._fg_color.name()))
			self.sb_cp.pushButton_FG_color.setStyleSheet("background-color: {};".format(self._fg_color.name()))
			self._fg_color = self._fg_color.name()
			self.sb_cp.checkBox_default_FG.setChecked(False)
		else:
			self._fg_color = None
			self.sb_cp.checkBox_default_FG.setChecked(True)

	def pick_BG_color(self):
		self._bg_color = QtWidgets.QColorDialog.getColor()
		if self._bg_color.isValid():
			self.logger.info("FG Color: {}".format(self._bg_color.name()))
			self.sb_cp.pushButton_BG_color.setStyleSheet("background-color: {};".format(self._bg_color.name()))
			self._bg_color = self._bg_color.name()
			self.sb_cp.checkBox_default_BG.setChecked(False)
		else:
			self._bg_color = None
			self.sb_cp.checkBox_default_BG.setChecked(True)

	def picked_TO_CD_green(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_green
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")

	def picked_TO_CD_red(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_red
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")

	def picked_TO_CD_blue(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_blue
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")

	def picked_TO_CD_orange(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_orange
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")
	
	def picked_TO_CD_yellow(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_yellow
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")

	def picked_TO_CD_purple(self, selected):
		if selected:
			self._to_cd_color = self._to_cd_purple
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("")

	def _pick_TO_CD_color(self):
		self._to_cd_color = QtWidgets.QColorDialog.getColor()
		if self._to_cd_color.isValid():
			self.logger.info("Timeout Countdown Color: {}".format(self._to_cd_color.name()))
			self.sb_cp.pushButton_TO_CD_color_custom.setStyleSheet("background-color: {};".format(self._to_cd_color.name()))
			self._to_cd_color = self._to_cd_color.name()
		else:
			self._to_cd_color = None

	def	submit_msg(self):
		msg = self.sb_cp.lineEdit_msg.text()
		bold = self.sb_cp.checkBox_bold.isChecked()
		timeout = self.sb_cp.spinBox_timeout.value() * 1000
		progressbar_color = self._to_cd_color
		fg = self._fg_color
		bg = self._bg_color

		if len(msg) == 0:
			# If caller sends an empty message, we create on based on inputs
			msg = "This message has timeout: {} bold: {} fgc: {} bgc: {} pbc: {}".format(timeout, bold, fg, bg, progressbar_color)

		logmsg = "Showing StatusBar Message:\n   msg     : '{}'\n   timeout : {}\n   bold    : {}\n   Fg Color: {}\n   Bg Color: {}\n   PB Color: {}\n"
		logmsg = logmsg.format(msg, timeout, bold, fg, bg, progressbar_color)
		self.logger.info(logmsg)
		if progressbar_color:
			self.ssb.setProgressBarColor(progressbar_color)
		self.ssb.showMessage(msg, timeout, fg, bg, bold)

	def slider_changed(self):
		self.sb_cp.lineEdit_slider_value.setText(str(self.sb_cp.slider.value()))

	def _gen_a_light_random_color(self):
		hue = random.randint(0,359)
		sat = random.randint(0,100)
		val = random.randint(170,200)
		c = Color(hsl=(hue/359, sat/255, val/255))
		return(c.hex_l)

	def _gen_a_progressbar_color(self):
		color = random.choice(PROGRESS_BAR_COLOR_SET)
		if not color:
			color = self._gen_a_light_random_color()
		return(color)

	def _random_color(self):
		c = random.randint(0x111111, 0xeeeeee)
		c_str = f'#{c:06X}'
		return(c_str)

	def _constrasting_color(self, color):
		# https://codereview.stackexchange.com/questions/182202/randomly-generate-a-hex-colour-code-and-its-contrasting-colour-using-python
		rgb = int(color.lstrip('#'), 16)
		complementary_color = 0xffffff - rgb
		complementary_color_str = f'#{complementary_color:06X}'
		return(complementary_color_str)

	def do_random(self):
		n = self.sb_cp.slider.value()
		self.logger.info("Generate {} random messages".format(n))

		if self.sb_cp.checkBox_double.isChecked():
			n = 2 * n

		for i in range(n):
			do_timeout = random.choice(TIMEOUT_SELECTION_SET)
			if do_timeout:
				timeout = random.randint(4,10) * 1000
			else:
				timeout = 0
			bold = random.choice([True, True, False, False, False])
			bg = self._random_color()
			fg = self._constrasting_color(bg)
			pb = self._gen_a_progressbar_color()
			self.logger.info("FG: {}".format(fg))
			self.logger.info("BG: {}".format(bg))
			self.logger.info("PB: {}".format(pb))
			self.logger.info("TO: {}".format(timeout))
			self.logger.info("BOLD: {}".format(bold))
			msg = "{:03d}: Random Message Bold:{} FG:{} BG:{} Timeout:{} PB:{} ".format(i, bold, fg, bg, timeout, pb)
			self.logger.info(msg)

			self.ssb.setProgressBarColor(pb)
			self.ssb.showMessage(msg, timeout, fg, bg, bold)

	def set_logging_level(self, level):
		print("Setting Log Level to {} [{}]".format(LEVEL_MAP[level], level))
		self.logger.setLevel(level)

	def setuplogging(self):
		self.logger = logging.getLogger('TestBed')
		self.logger.setLevel(logging.DEBUG)
		self.ch = logging.StreamHandler()
		self.ch.setLevel(logging.DEBUG)
		self.formatter = logging.Formatter('%(name)s: %(levelname)s: %(filename)s:%(funcName)s @ line %(lineno)d: %(message)s')
		self.ch.setFormatter(self.formatter)
		self.logger.addHandler(self.ch)


# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
def main():
	app = QApplication(sys.argv)
	ws = MessageBarTestBed(app=app)
	ws.show()
	sys.exit(app.exec_())


	# Form = QtWidgets.QWidget()
	# ui = Ui_Form()
	# ui.setupUi(Form)
	# Form.show()

# ----------------------------------------------------------------------------
# ----------------------------- main -----------------------------------------
# ----------------------------------------------------------------------------
if __name__ == "__main__":
	main()

