# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PedestrianDataInput
                                 A QGIS plugin
 PedestrianDataInput
                             -------------------
        begin                : 2016-10-03
        copyright            : (C) 2016 by Stephen Law
        email                : s.law@spacesyntax.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PedestrianDataInput class from file PedestrianDataInput.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PedestrianDataInput import PedestrianDataInput
    return PedestrianDataInput(iface)
