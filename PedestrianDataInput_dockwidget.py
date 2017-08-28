# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PedestrianDataInputDockWidget
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
import os
import time
from PyQt4 import QtGui, uic
from PyQt4.QtCore import pyqtSignal
import os.path
from qgis.core import *
from qgis.gui import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import qgis


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PedestrianDataInput_dockwidget_base.ui'))


class PedestrianDataInputDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(PedestrianDataInputDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        # signals for layers added?
        # layer.layersAdded.connect(self.updateLayer)
        QgsMapLayerRegistry.instance().layersAdded.connect(self.update_Layer_List)
        QgsMapLayerRegistry.instance().layersRemoved.connect(self.update_Layer_List)



    #def closeEvent(self, event):
        #self.closingPlugin.emit()
        #event.accept()

    #this function creates QgsVector layer to fill in data
    def create_layer(self):
        v2 = QgsVectorLayer("Point?crs=epsg:27700", "Temp_snapshot", "memory")
        pr = v2.dataProvider()
        v2.startEditing()
        pr.addAttributes([QgsField("id", QVariant.Int),
                          QgsField("activity", QVariant.String),
                          QgsField("category", QVariant.String),
                          QgsField("time", QVariant.String),
                          QgsField("day",QVariant.String)])

        # this commits the layer
        v2.commitChanges()
        v2.updateExtents()
        # this loads the layer
        QgsMapLayerRegistry.instance().addMapLayer(v2)
        # this is not needed as it updates the layer twice
        #self.update_Layer_List()


    #update functions

    def update_Layer_List(self):
        print "hello world - layers updated!!"
        layer_objects = self.update_list()
        self.update_layer(layer_objects)

    def update_list(self):
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        layer_objects = []
        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                for i in layer.fields():
                    if i.name()=='activity':
                        layer_objects.append((layer.name(), layer))
                        print "True"

        return layer_objects

    def update_layer(self, layer_objects):
        for layer in layer_objects:
            self.layer_comboBox.addItem(layer[0], layer[1])

    def update_activity(self,activities):
        for i in activities:
            self.layer_comboBox_02.addItem(i)

    def update_category(self,categories):
        for i in categories:
            self.layer_comboBox_03.addItem(i)

    def update_time_period(self,time_periods):
        for i in time_periods:
            self.layer_comboBox_04.addItem(i)


    #get functions
    def get_layer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        return layer

    def get_activity(self):
        activity = self.layer_comboBox_02.currentText()
        return activity

    def get_category(self):
        category = self.layer_comboBox_03.currentText()
        return category

    def get_time_period(self):
        time_period = self.layer_comboBox_04.currentText()
        return time_period

    def get_day(self):
        day="weekday"
        if self.radioButton.isChecked():
            day="weekday"
        elif self.radioButton_2.isChecked():
            day="weekend"
        return day


    #add functions
    def add_Feature(self):

        # this sets style
        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/SnapThematic_test.qml"
        print qml_path

        # this sets data
        layer = self.get_layer()
        layer.loadNamedStyle(qml_path)

        # needs to catch the last added feature signal
        layer.featureAdded.connect(self.logFeatureAdded)

        # this activates the toggle editing
        if not layer.isEditable():
            self.iface.actionToggleEditing().trigger()

        # this updates layer by adding features
        self.iface.actionAddFeature().trigger()

    def update_Feature(self):
        layer = self.get_layer()
        activity = self.get_activity()
        category = self.get_category()
        time_period = self.get_time_period()
        day=self.get_day()
        layer.startEditing()
        selection = layer.selectedFeatures()
        for feature in selection:
            #layer.changeAttributeValue(feature.id(), 0, 100, True)
            layer.changeAttributeValue(feature.id(), 1, str(activity), True)
            layer.changeAttributeValue(feature.id(), 2, str(category), True)
            layer.changeAttributeValue(feature.id(), 3, str(time_period), True)
            layer.changeAttributeValue(feature.id(), 4, str(day),True)
        QApplication.beep()
        layer.commitChanges()

    def disconnect_Layer(self):

        layer = self.get_layer()
        #print layer
        if layer.isEditable():
            self.iface.actionToggleEditing().trigger()
        layer.commitChanges()
        self.closingPlugin.emit()
        #event.accept()
        #layer.stopEditing()



# these functions work in python console but not in plugin

    # Signal Functions to catch
    # http://gis.stackexchange.com/questions/53269/handle-add-new-feature-event-and-or-access-feature-before-commit
    # http://gis.stackexchange.com/questions/102376/how-to-find-the-id-of-the-last-added-feature-using-pyqgis
    # http://gis.stackexchange.com/questions/176686/automatically-updating-user-edited-features-in-qgis-plugin

    def logFeatureAdded(self,fid):
        QgsMessageLog.logMessage("feature added, id = " + str(fid))
        QApplication.beep()

        # this gets layer and activity
        activity = self.get_activity()
        category = self.get_category()
        time_period = self.get_time_period()
        layer = self.get_layer()
        day= self.get_day()

        # this starts editing
        layer.startEditing()
        feature_count=layer.featureCount()

        # this updates the updated features
        features = layer.getFeatures()
        #data = layer.dataProvider()
        layer.changeAttributeValue(fid, 0,feature_count,True)
        layer.changeAttributeValue(fid, 1,str(activity), True)
        layer.changeAttributeValue(fid, 2,str(category), True)
        layer.changeAttributeValue(fid, 3,str(time_period), True)
        layer.changeAttributeValue(fid, 4,str(day), True)
        print activity
        print category
        print time_period
        print day

    # QGIS direct functions
    # layer = iface.activeLayer()
    # layer.featureAdded.connect(logFeatureAdded)
    # layer.editingStarted.connect(logEditingStarted)




