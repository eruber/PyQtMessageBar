import sys

from setuptools import setup

if sys.version_info[0] < 3:
	sys.exit('Error: Python 3.x is required.')


# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='PyQtMessageBar',
	version = '0.3.2',
	description="Subclass of Qt's QStatusBar that adds a message buffer, wait queue, and user interaction.",
	long_description=long_description,
	long_description_content_type='text/markdown',
	author='E.R. Uber',
	author_email='eruber@gmail.com',
	url='https://github.com/eruber/PyQtMessageBar',
	download_url = "https://github.com/eruber/PyQtMessageBar/archive/v0.3.2.tar.gz",
	packages=['pyqtmessagebar'],
	python_requires='>=3.7.1',
	requires=['PyQt5'],
	install_requires=[
	'PyQt5>=5.14.0',
	'pyqtlineeditprogressbar>=0.3.5',
	'colour>=0.1.5',
	],
	license='GPLv3',
	# entry_points={
	# 	'gui_scripts': ['PyQtMessageBarTestbed = tests.testbed:main'],
	# },
	classifiers = [
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
	],
	)