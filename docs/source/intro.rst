.. ############################################################################
   This file contains reStructuredText, please do not edit it unless you are
   familar with reStructuredText markup as well as Sphinx specific markup.

   For information regarding reStructuredText markup see
      http://sphinx.pocoo.org/rest.html

   For information regarding Sphinx specific markup see
      http://sphinx.pocoo.org/markup/index.html

   ############################################################################

.. ############################################################################
   Copyright 2020 E.R. Uber (eruber@gmail.com)
   ############################################################################

.. ########################### SECTION HEADING REMINDER #######################
   # with overline, for parts
   * with overline, for chapters
   =, for sections
   -, for subsections
   ^, for subsubsections
   ", for paragraphs

.. -----------------------------------------------------------------------------

.. _intro_label: 

Introduction
============
**PyQtMessageBar** subclasses the QStatusBar widget to add the following features:

   * StatusBar message buffering
   * StatusBar messages can specify a foreground color, a background color, enable bold text, and set a display timeout
   * Display of a PyQtMessageBar Help Icon which provides access to a PyQtMessageBar Help Dialog
   * Keyboard activated recall of buffered message via keys Up Arrow, Down Arrow, Page Up, Page Down, Home, and End
   * Wait queueing of messages that have explicit display timeouts specified (the Timer Wait Queue)
   * An indicator showing the currently displayed Message Index and Wait Queued Message Count Depth (how many messages
     or waiting to be displayed)
   * Countdown timer progressbar display of wait queued messages in the background of the above mentioned indicator
   * Delete the currently displayed message
   * Deletion of ENTIRE message buffer
   * Save ENTIRE message buffer to a file under a directory specified at PyQtMessageBar object intialization
   * Save ENTIRE message buffer to a file under a user chosen directory (using a File Save As Dialog)
   * Custom signal that the application can connect a slot method to in order to be informed when the Timer Wait Queue empties

   .. image:: _static/components.png
      :align: center

**PyQtMessageBar** supports the following configurable features:

   * Color of the countdown timer progressbar
   * Choice of PyQtMessageBar Help Icon Style -- Light Color, Dark Color, or Two-Tone Color
   * Support of user specified Help Icon
   * Ability to enable a vertical separator between StatusBar's permanent widgets that might be added by the user

   The Built-in Help Icons: Light, Dark, Two-Tone

   .. image:: _static/help_icons.png
      :align: center

Keyboard Input
--------------
The following key sequences are recognized by an in focus **PyQtMessageBar** object. See the first note below.

* **Up Arrow** - Display the buffered message before the currently displayed message.
* **Down Arrow** - Display the buffered message after the currently displayed message.
* **Home** - Display the oldest buffered message.
* **End** - Display the most recent buffered message.
* **PageUp** - Page the buffered message displayed up by page size entries.
* **PageDown** - Page the buffered message displayed down by page size entries.
* **control-alt-X** - Delete the currently displayed buffered message.
* **control-alt-shift-X** - Delete all of the buffered messages.
* **control-alt-S** - Save the message buffer to a file in the **save_msg_buffer_dir** directory.
* **control-alt-shift-S** - Save the message buffer to a file location determined by the user's use of the displayed File Save As Dialog.


.. note:: In order for a **PyQtMessageBar** object to interact with the keyboard it must have its focus properly
   set. See :ref:`pyqtmessagebar_class_label` in the API section for a code example of how to setup the keyboard
   focus for a statusbar.

.. note:: The page size for **PageUp/PageDown** is 10 messages.

Testbed
-------
The source distribution of **PyQtMessageBar** contains a **testbed.py** file in the *tests* directory that
facilitates composing custom message colors and demonstrates how to exercise the **PyQtMessageBar** API.

The testbed GUI looks like this when first invoked:

.. image:: _static/testbed_at_startup.png
   :align: center

The **Configure StatusBar** group of widgets will instantiate a new statusbar when a widget in that
group is used. So these widgets are disabled during any generation of random messages by the **Generate Random
Messages** widget group. After random message generation is complete, the **Configure StatusBar** group of widgets
should be enabled again.

.. note:: While the random generation of statusbar messages highlights the display of the message index and the 
   timer wait queue countdown progressbar; it does not always generate foreground and background colors that
   have high enough contrast to be easily readable -- eventhough a minimal amount of effort was expended to
   try and generate constrasting colors. |ohwell| 

Further Reading
---------------
For more internal details see the :ref:`api_label` section.

For more information on Qt's QStatusBar `read the Qt QStatusBar Docs <https://doc.qt.io/qt-5/qstatusbar.html>`_.

**PyQtMessageBar** manifestations on-line are:
   * `PyQtMessageBar at GitHub`_
   * `PyQtMessageBar at PyPi`_
   * `PyQtMessageBar GitHub Pages`_


.. _PyQtMessageBar at GitHub: https://github.com/eruber/PyQtMessageBar
.. _PyQtMessageBar at PyPi: https://pypi.org/project/pyqtmessagebar
.. _PyQtMessageBar GitHub Pages: https://eruber.github.io/PyQtMessageBar/build/html/index.html
.. |ohwell| image:: _static/inverted_smiley_18.png