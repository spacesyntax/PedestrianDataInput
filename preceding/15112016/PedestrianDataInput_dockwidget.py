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



    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    #update layer - fill combo with layer lists
    def update_layer(self, layer_objects):
        for layer in layer_objects:
            self.layer_comboBox.addItem(layer[0], layer[1])

    # get layer - retrieve layer
    def get_layer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        return layer

    # NEW FUNCTIONS
    def add_Feature(self):



        # this sets style
        #plugin_path = os.path.dirname(__file__)
        #qml_path = plugin_path + "/frontagesThematic.qml"
        #input.loadNamedStyle(qml_path)

        # this sets layer
        layer = self.get_layer()
        print layer


        # this activates the toggle editing
        if not layer.isEditable():
            self.iface.actionToggleEditing().trigger()

        # this updates layer by adding features
        self.iface.actionAddFeature().trigger()

        # needs to catch the last added feature signal
        #http://gis.stackexchange.com/questions/53269/handle-add-new-feature-event-and-or-access-feature-before-commit
        #http://gis.stackexchange.com/questions/102376/how-to-find-the-id-of-the-last-added-feature-using-pyqgis
        #http://gis.stackexchange.com/questions/176686/automatically-updating-user-edited-features-in-qgis-plugin



        # this updates the contents of the feature
        #feature = QgsFeature()
        #feature.setAttributes([count, str(x1), str(x0), time, mode, origin, destination])

        # this sets layer
        #index = self.layer_comboBox.currentIndex()
        #layer = self.layer_comboBox.itemData(index)
        #layer = self.iface.activeLayer()
        #self.iface.setActiveLayer(layer)

        # this commit layers
        #layer.startEditing()
        #layer.commitChanges()
        #layer.updateExtents()
        #print layer

    def update_selected_Feature(self):

        layer = self.get_layer()
        selection = layer.selectedFeatures()
        for feature in selection:
            feature.setAttributes(["0"])

    def disconnect_Layer(self):

        layer = self.get_layer()
        print layer
        if layer.isEditable():
            self.iface.actionToggleEditing().trigger()
        #layer.stopEditing()


# these functions work in python console but not in plugin

    # Signal Functions to catch
    def logFeatureAdded(fid):
        QgsMessageLog.logMessage("feature added, id = " + str(fid))
        QApplication.beep()

    def logEditingStarted():
        QgsMessageLog.logMessage("editing started")
        QApplication.beep()

    # layer = self.iface.activeLayer()
    # layer.featureAdded.connect(logFeatureAdded)
    # layer.editingStarted.connect(logEditingStarted)



# these are abhi's function that needs translation

    # Abhis functions
    def Abhi_loadFrontageLayer(self):
        if self.useExistingcomboBox.count() > 0:
            input = self.setFrontageLayer()

            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontagesThematic.qml"
            input.loadNamedStyle(qml_path)

            input.startEditing()

            input.featureAdded.connect(self.logFeatureAdded)
            input.selectionChanged.connect(self.addDataFields)

            # Draw/Update Feature

    def Abhi_setFrontageLayer(self):
        index = self.useExistingcomboBox.currentIndex()
        self.frontage_layer = self.useExistingcomboBox.itemData(index)
        return self.frontage_layer

    def Abhi_isFrontageLayer(self, layer):
        if layer.type() == QgsMapLayer.VectorLayer \
                and layer.geometryType() == QGis.Line:
            fieldlist = uf.getFieldNames(layer)
            if 'F_Group' in fieldlist and 'F_Type' in fieldlist:
                return True

        return False

    def Abhi_updateFrontageLayer(self):
        self.useExistingcomboBox.clear()
        self.useExistingcomboBox.setEnabled(False)
        layers = self.iface.legendInterface().layers()
        for lyr in layers:
            if self.isFrontageLayer(lyr):
                self.useExistingcomboBox.addItem(lyr.name(), lyr)

        if self.useExistingcomboBox.count() > 0:
            self.useExistingcomboBox.setEnabled(True)
            self.setFrontageLayer()
            print self.frontage_layer

    def Abhi_logFeatureAdded(self, fid):

        #QgsMessageLog.logMessage("feature added, id = " + str(fid))

        mc = self.canvas
        v_layer = self.setFrontageLayer()
        feature_Count = v_layer.featureCount()
        features = v_layer.getFeatures()
        inputid = 0

        if feature_Count == 1:
            for feat in features:
                inputid = 1

        elif feature_Count > 1:
            for feat in features:
                inputid = feature_Count

        data = v_layer.dataProvider()
        update1 = data.fieldNameIndex("F_Group")
        update2 = data.fieldNameIndex("F_Type")
        update3 = data.fieldNameIndex("F_ID")

        if self.frontageslistWidget.currentRow() == 0:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Transparent", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

        if self.frontageslistWidget.currentRow() == 1:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Semi Transparent", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

        if self.frontageslistWidget.currentRow() == 2:
            v_layer.changeAttributeValue(fid, update1, "Building", True)
            v_layer.changeAttributeValue(fid, update2, "Blank", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

        if self.frontageslistWidget.currentRow() == 3:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High Opaque Fence", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

        if self.frontageslistWidget.currentRow() == 4:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "High See Through Fence", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

        if self.frontageslistWidget.currentRow() == 5:
            v_layer.changeAttributeValue(fid, update1, "Fence", True)
            v_layer.changeAttributeValue(fid, update2, "Low Fence", True)
            v_layer.changeAttributeValue(fid, update3, inputid, True)
            v_layer.updateFields()

    #def logFeatureAdded(self, fid):
            # message = str(fid)
            # QgsMessageLog.logMessage("feature added, id = " + str(fid))
            # print fid
            # mc = self.canvas
            # layer = self.get_layer()
            # feature_Count = layer.featureCount()
            # features = layer.getFeatures()
            # inputid = 0
            # print layer