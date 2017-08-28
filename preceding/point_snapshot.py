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


class point_snapshot(QgsMapTool):
    #http://gis.stackexchange.com/questions/45094/how-to-programatically-check-for-a-mouse-click-in-qgis
    #http://www.lutraconsulting.co.uk/blog/2014/10/17/getting-started-writing-qgis-python-plugins/

    def __init__(self, canvas):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.cursor = QCursor(Qt.CrossCursor)
        self.dockwidget = PedestrianDataInputDockWidget()



    def canvasReleaseEvent(self, event):

        # put current layers into comboBox
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_objects = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                layer_objects.append((layer.name(), layer))
        self.dockwidget.update_layer(layer_objects)

        # get current layers
        layer = self.dockwidget.get_layer()

        # if current layer is empty
        if layer == None:
            layer = QgsVectorLayer("Point?crs=epsg:4326", "temporary_output", "memory")
            pr = layer.dataProvider()
            layer.startEditing()
            pr.addAttributes([QgsField("id", QVariant.Int),
                              QgsField("x", QVariant.Double),
                              QgsField("y", QVariant.Double),
                              QgsField("time", QVariant.String),
                              QgsField("eating", QVariant.String)])






        #Get the click
        x = event.pos().x()
        y = event.pos().y()
        point = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
        print point
        print point[0]
        print point[1]
        print layer

        # add points to existing layer
        pr = layer.dataProvider()
        layer.startEditing()
        fet = QgsFeature()
        fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(point[0], point[1])))
        fet.setAttributes([1, x, y, "10:00", "eating"])
        pr.addFeatures([fet])
        layer.commitChanges()
        layer.updateExtents()
        QgsMapLayerRegistry.instance().addMapLayer(layer)


    def create_temp_layer():
        # create new temporary layer to add points on click
        v2 = QgsVectorLayer("Point?crs=epsg:4326", "temporary_output", "memory")
        pr = v2.dataProvider()
        v2.startEditing()
        pr.addAttributes([QgsField("id", QVariant.Int),
                          QgsField("x", QVariant.Double),
                          QgsField("y", QVariant.Double),
                          QgsField("time", QVariant.String),
                          QgsField("eating", QVariant.String)])

        #fet = QgsFeature()
        #fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(point[0], point[1])))
        #fet.setAttributes([1, x, y, "10:00", "eating"])
        #pr.addFeatures([fet])
        #v2.commitChanges()
        #v2.updateExtents()
        #QgsMapLayerRegistry.instance().addMapLayer(v2)




        #







