# PyQtMessageBar README #

**PyQtMessageBar** is a full featured drop-in replacement for Qt's QStatusBar.

Most notable amoung its numerous features are statusbar message buffering and 
keyboard activated scrolling through the message buffer.

For more information about its features, read the [PyQtMessageBar User Manual](https://eruber.github.io/PyQtMessageBar/build/html/index.html).

![](https://eruber.github.io/PyQtMessageBar/build/html/_static/components_readme.png)

# Dependencies #
The following packages are installed with **PyQtMessageBar**:

- 	[PyQt5](https://riverbankcomputing.com/software/pyqt/intro) (5.14.0 or later)
- 	[colour](https://pypi.org/project/colour/) (0.1.5 or later)
- 	[pyqtlineeditorprogressbar](https://github.com/eruber/pyqtlineeditprogressbar) (0.3.5 or later)

# Installation #
**PyQtMessageBar** can be installed via pip:

	pip install pyqtmessagebar

# Test the Installation #
A test bed utility is available in the **PyQtMessageBar** source distribution that exposes most of the package features via a GUI that drives the **PyQtMessageBar** at the bottom of the tools' user interface..

After installing **PyQtMessageBar** and changing directory package *tests* directory, run the testbed tool like this:

	python testbed.py

![](https://eruber.github.io/PyQtMessageBar/build/html/_static/testbed.png)

# License #
**PyQtMessageBar** is licensed GPLv3. See the LICENSE file in the package root to satisfy all your legalese cravings. 

# Attributions #
The help icons built-in to **PyQtMessageBar** are from [Google's Material Design project](https://material.io/resources/icons/?style=baseline) and are free to use (but not to sell) under the terms of the [Apache license version 2.0](https://www.apache.org/licenses/LICENSE-2.0.html).

The built-in Help Icons look like this (LIGHT, DARK, TWO-TONE):

![](https://eruber.github.io/PyQtMessageBar/build/html/_static/help_icons.png)

# API #
For more information on the inner workings of **PyQtMessageBar** read the [API documentation](https://eruber.github.io/PyQtMessageBar/build/html/api.html).



