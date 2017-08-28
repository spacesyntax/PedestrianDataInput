# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PedestrianDataInput
                                 A QGIS plugin
 PedestrianDataInput
                              -------------------
        begin                : 2016-10-03
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Stephen Law
        email                : s.law@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt
from PyQt4.QtGui import QAction, QIcon
# Initialize Qt resources from file resources.py
import resources

# Import the code for the DockWidget
from PedestrianDataInput_dockwidget import PedestrianDataInputDockWidget
import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
import os
from qgis.gui import QgsMapTool
import point_snapshot


# http://gis.stackexchange.com/questions/45094/how-to-programatically-check-for-a-mouse-click-in-qgis


class PointTool(QgsMapTool):
     def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas

    def canvasReleaseEvent(self, event):
        #Get the click
        x = event.pos().x()
        y = event.pos().y()
        print x
        print y

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def points(self):

        # create layer
        vl = QgsVectorLayer("Point?crs=epsg:27700", "temporary_points", "memory")
        pr = vl.dataProvider()

        # changes are only possible when editing the layer
        vl.startEditing()

        #add fields
        pr.addAttributes([QgsField("name", QVariant.String), QgsField("age", QVariant.Int), QgsField("size", QVariant.Double)])

        # add a feature
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(10, 10)))
        fet.setAttributes(["Johny", 2, 0.3])
        pr.addFeatures([fet])

        # commit to stop editing the layer
        vl.commitChanges()

        # update layer's extent when new features have been added because change of extent in provider is not propagated to the layer
        vl.updateExtents()

        # add layer to the legend
        QgsMapLayerRegistry.instance().addMapLayer(vl)

    def addLayer(self):
        v2 = QgsVectorLayer("Point?crs=epsg:27700", "temporary_output", "memory")
        pr = v2.dataProvider()
        v2.startEditing()
        pr.addAttributes([QgsField("id", QVariant.Int),
                          QgsField("x", QVariant.Double),
                          QgsField("y", QVariant.Double),
                          QgsField("time", QVariant.String),
                          QgsField("eating", QVariant.String)])
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(x, y)))
        fet.setAttributes([1, x, y, "10:00", "eating"])
        print "hello world"
        pr.addFeatures([fet])
        v2.commitChanges()
        v2.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayer(v2)


    def backup_canvasReleaseEvent(self, event):
        pass
        # Get the click
        # x = event.pos().x()
        # y = event.pos().y()
        # print x
        # print y
        # point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)


        # v2 = QgsVectorLayer("Point?crs=epsg:4326", "temporary_output", "memory")
        # pr = v2.dataProvider()
        # v2.startEditing()
        # pr.addAttributes([QgsField("id", QVariant.Int),
        # QgsField("x", QVariant.Double),
        # QgsField("y", QVariant.Double),
        # QgsField("time", QVariant.String),
        # QgsField("eating", QVariant.String)])
        # fet = QgsFeature()
        # fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(point[0], point[1])))
        # fet.setAttributes([1, x, y, "10:00", "eating"])
        # pr.addFeatures([fet])
        # v2.commitChanges()
        # v2.updateExtents()
        # QgsMapLayerRegistry.instance().addMapLayer(v2)


    def activate(self):
        pass


    def deactivate(self):
        pass

    def canvasPressEvent(self, event):
        pass

    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)