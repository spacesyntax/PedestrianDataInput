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



    #def closeEvent(self, event):
        #self.closingPlugin.emit()
        #event.accept()

    #update functions
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


    #add functions
    def add_Feature(self):

        # this sets style
        #plugin_path = os.path.dirname(__file__)
        #qml_path = plugin_path + "/frontagesThematic.qml"
        #input.loadNamedStyle(qml_path)

        # this sets data
        layer = self.get_layer()

        # needs to catch the last added feature signal
        layer.featureAdded.connect(self.logFeatureAdded)

        # this activates the toggle editing
        if not layer.isEditable():
            self.iface.actionToggleEditing().trigger()

        # this updates layer by adding features
        self.iface.actionAddFeature().trigger()

    def update_Feature(self):
        activity = self.get_activity()
        category = self.get_category()
        time_period = self.get_time_period()
        layer = self.get_layer()
        layer.startEditing()
        selection = layer.selectedFeatures()
        for feature in selection:
            #layer.changeAttributeValue(feature.id(), 0, 100, True)
            layer.changeAttributeValue(feature.id(), 1, str(activity), True)
            layer.changeAttributeValue(feature.id(), 2, str(category), True)
            layer.changeAttributeValue(feature.id(), 3, str(time_period), True)

        layer.commitChanges()

    def disconnect_Layer(self):

        layer = self.get_layer()
        #print layer
        if layer.isEditable():
            self.iface.actionToggleEditing().trigger()
        layer.commitChanges()
        #layer.stopEditing()



# these functions work in python console but not in plugin

    # Signal Functions to catch
    # http://gis.stackexchange.com/questions/53269/handle-add-new-feature-event-and-or-access-feature-before-commit
    # http://gis.stackexchange.com/questions/102376/how-to-find-the-id-of-the-last-added-feature-using-pyqgis
    # http://gis.stackexchange.com/questions/176686/automatically-updating-user-edited-features-in-qgis-plugin

    def logFeatureAdded(self,fid):
        QgsMessageLog.logMessage("feature added, id = " + str(fid))
        #QApplication.beep()

        # this gets layer and activity
        activity = self.get_activity()
        category = self.get_category()
        time_period = self.get_time_period()
        layer = self.get_layer()

        # this starts editing
        layer.startEditing()
        feature_count=layer.featureCount()

        # this updates the updated features
        features = layer.getFeatures()
        data = layer.dataProvider()
        layer.changeAttributeValue(fid, 0,feature_count,True)
        layer.changeAttributeValue(fid, 1,str(activity), True)
        layer.changeAttributeValue(fid, 2,str(category), True)
        layer.changeAttributeValue(fid, 3,str(time_period), True)
        print activity
        print category
        print time_period

    # QGIS direct functions
    # layer = iface.activeLayer()
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

    #def old_logFeatureAdded(self, fid):
            #message = str(fid)
            #QgsMessageLog.logMessage("feature added, id = " + str(fid))
            #print fid
            # mc = self.canvas
            # layer = self.get_layer()
            # feature_Count = layer.featureCount()
            # features = layer.getFeatures()
            # inputid = 0
            # print layer

    def logEditingStarted(self):
        QgsMessageLog.logMessage("editing started")
        QApplication.beep()

    def old_functions(self):
        print "booboo"
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

        #trying to set attributes - tests01
        #attrs = {'id': 10}
        #layer.dataProvider().changeAttributeValues({ fid : attrs })
        #for i in layer.getFeatures():
            #print i.id
        #i.setAttribute(0,1)
        #i['id'] = 10
        #layer.updateFeature(i)
        #print addedFeatures()
        #for i in addedFeatures():
            #i['id']=10
        #layer.updateFeature(i)
        # Call commit to save the changes
        #layer.commitChanges()

        #python functions on feature class
        #dir(features)
        #help(features)

        # signal functions
        #layer.featureAdded.connect(self.logFeatureAdded)
        #layer.committedFeaturesAdded.connect(self.logCommittedFeaturesAdded)
        #layer.selectionChanged.connect(self.addDataFields)

