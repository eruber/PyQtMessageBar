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
   * Display of a PyQtMessageBar Help Icon which provides access to a Help Dialog
   * Keyboard activated recall of buffered message via keys Up Arrow, Down Arrow, Page Up, Page Down, Home, and End
   * Wait queueing of messages that have explicit display timeouts specified
   * Display of a Message Index and Wait Queued Message Count Indicator
   * Countdown timer progressbar display of wait queued messages
   * Delete the currently displayed message via CTRL-ALT-X
   * Deletion of ENTIRE message buffer via CTRL-ALT-SHIFT-X
   * Save ENTIRE message buffer to a file under a directory specified at PyQtMessageBar object intialization time via CTRL-ALT-S
   * Save ENTIRE message buffer to a file under a user chosen directory (using a File Save As Dialog) via CTRL-ALT-SHIFT-S 

**PyQtMessageBar** supports the following configurable features:

   * Color of the countdown timer progressbar
   * Choice of PyQtMessageBar Help Icon Style -- Light Color, Dark Color, or Two-Tone Color
   * Support of user specified Help Icon
   * Ability to enable a vertical separator between StatusBar's permanent widgets that might be added by the user


Further Reading
---------------
For more internal details see the :ref:`api_label` section.

For more information on Qt's QStatusBar `read the Qt QStatusBar Docs <https://doc.qt.io/qt-5/qstatusbar.html>`_.


