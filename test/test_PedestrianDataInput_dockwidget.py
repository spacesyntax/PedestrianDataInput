# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 's.law@spacesyntax.com'
__date__ = '2016-10-03'
__copyright__ = 'Copyright 2016, Stephen Law'

import unittest

from PyQt4.QtGui import QDockWidget

from PedestrianDataInput_dockwidget import PedestrianDataInputDockWidget

from utilities import get_qgis_app

QGIS_APP = get_qgis_app()


class PedestrianDataInputDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = PedestrianDataInputDockWidget(None)

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_dockwidget_ok(self):
        """Test we can click OK."""
        pass

if __name__ == "__main__":
    suite = unittest.makeSuite(PedestrianDataInputDialogTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

