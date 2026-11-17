"""Optional Qt5 compatibility runner for environments without Qt6.

The shipped app targets PyQt6. This runner checks the same widgets and painter
code using system PyQt5 when PyQt6 cannot be downloaded. It is not a Qt6 or a
native macOS certification. Run: PYTHONPATH=src python3 tests/qt5_check.py
"""
import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
import sys
import unittest
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
sys.modules['PyQt6'] = PyQt5
sys.modules['PyQt6.QtCore'] = QtCore
sys.modules['PyQt6.QtGui'] = QtGui
sys.modules['PyQt6.QtWidgets'] = QtWidgets
sys.modules['PyQt6.QtTest'] = QtTest

if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'))
    sys.exit(not result.wasSuccessful())
