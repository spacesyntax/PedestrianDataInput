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

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'PedestrianDataInput_dockwidget_base.ui'))


class PedestrianDataInputDockWidget(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, parent=None):
        """Constructor."""
        super(PedestrianDataInputDockWidget, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()

    #update layer - fill combo with layer lists
    def update_layer(self, layer_objects):
        for layer in layer_objects:
            self.layer_comboBox.addItem(layer[0], layer[1])

    # get layer - retrieving the value of the current selected layer
    def get_layer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        return layer

    # NEW FUNCTIONS
    def loadFrontageLayer(self):
        index = self.layer_comboBox.currentIndex()
        layer = self.layer_comboBox.itemData(index)
        layer.featureAdded.connect(self.logFeatureAdded)
        print layer

    def logFeatureAdded(self, fid):
        message = str(fid)




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