"""
.. py:module:: waitqueuesignal

Class WaitQueueEmptiedSignal
============================
This module can be utilized to inform the application using **PyQtMessageBar** that
the messagebar's Timer Wait Queue has been emptied.

.. _waitqueuesignal_usage_label:

USAGE
-----
Here is an example of what the application code needs to do in order to be informed
when the **PyQtMessageBar** Timer Wait Queue becomes empty.

1. The application creates a **WaitQueueEmptiedSignal** object and connects their 
slot method to the signal's emptied signal::

	from PyQt5.QtCore import pyqtSlot
	from pyqtmessagebar.waitqueuesignal import WaitQueueEmptiedSignal
	...
	signal = WaitQueueEmptiedSignal()
	signal.emptied.connect(timer_wait_q_emptied)
	...
	@pyqtSlot()
	def timer_wait_q_emptied(self):
		# Now do something since the timer wait queue is now empty

Note that the **@pyqtSlot()** decorator on the slot method is optional. 
See `The pyqtSlot() Decorator <https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html#the-pyqtslot-decorator>`_
for more information.

2. When the PyQtMessageBar object is instantiated, utilize the **timer_wait_q_emptied_signal** parameter
to pass the app's WaitQueueEmptiedSignal object to the PyQtMessageBar::

	from pyqtmessagebar import PyQtMessageBar
	...
	msgbar = PyQtMessageBar(..., timer_wait_q_emptied_signal=signal, ...)

When the **PyQtMessageBar's** Timer Wait Queue empties, the application's slot method **timer_wait_q_emptied()** will be called.

For information about the complete **PyQtMessageBar** constructor signature which
includes **timer_wait_q_emptied_signal** parameter see :py:meth:`pyqtmessagebar.__init__.PyQtMessageBar`.

CREDIT
------
This module is based on the article `Tutorial on Creating Your Own Signals <https://www.pythoncentral.io/pysidepyqt-tutorial-creating-your-own-signals-and-slots/>`_.

WaitQueueEmptiedSignal Details
------------------------------
"""
from PyQt5.QtCore import QObject, pyqtSignal
# ----------------------------------------------------------------------------
class WaitQueueEmptiedSignal(QObject):
	emptied = pyqtSignal()

	def __init__(self):
		"""This class implements a custom Qt signal named **emptied** that will be
		emitted when the QtMessageBar's Timer Wait Queue has zero entries."""
		super(WaitQueueEmptiedSignal, self).__init__()

	def empty(self):
		"""The method that emits the emptied signal when called by **PyQtMessageBar**."""
		self.emptied.emit()
