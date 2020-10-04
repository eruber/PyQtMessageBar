import sys

from setuptools import setup

if sys.version_info[0] < 3:
	sys.exit('Error: Python 3.x is required.')


long_description='''\
PyQtMessageBar is a PyQT Custom Widget that subclasses QStatusBar
to provide a message buffer plus numerous other features including
keyboard interaction allowing the user to scroll forward and backward 
through all statusbar messages in the message buffer.

For more details, please go to the `project home page <https://github.com/eruber/PyQtMessageBar>`_ or 
to the `project's User Manual <https://eruber.github.io/PyQtMessageBar/build/html/index.html>`_.
'''

setup(name='PyQtMessageBar',
	version = '0.3.0',
	description="Subclass of Qt's QStatusBar that adds a message buffer, wait queue, and user interaction.",
	long_description=long_description,
	long_description_content_type="text/plain",
	author='E.R. Uber',
	author_email='eruber@gmail.com',
	url='https://github.com/eruber/PyQtMessageBar',
	download_url = "https://github.com/eruber/PyQtMessageBar/archive/v0.3.0.tar.gz",
	packages=['pyqtmessagebar'],
	python_requires='>=3.7.1',
	requires=['PyQt5'],
	install_requires=[
	'PyQt5>=5.14.0',
	'pyqtlineeditprogressbar>=0.3.5',
	'colour>=0.1.5',
	],
	license='GPLv3',
	entry_points={
		'gui_scripts': ['PyQtMessageBarTestbed = tests.testbed:main'],
	},
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	)