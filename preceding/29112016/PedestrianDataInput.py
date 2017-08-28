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
import qgis



class PedestrianDataInput:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)


        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PedestrianDataInput_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PedestrianDataInput')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PedestrianDataInput')
        self.toolbar.setObjectName(u'PedestrianDataInput')

        #print "** INITIALIZING PedestrianDataInput"

        self.pluginIsActive = False
        self.dockwidget = None


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PedestrianDataInput', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/PedestrianDataInput/icon.png'

        action = self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())


    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING PedestrianDataInput"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD PedestrianDataInput"

        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PedestrianDataInput'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING PedestrianDataInput"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = PedestrianDataInputDockWidget(self.iface)



            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

            # put current layers into comboBox
            layers = QgsMapLayerRegistry.instance().mapLayers().values()
            layer_objects = []
            for layer in layers:
                if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                    layer_objects.append((layer.name(), layer))
            self.dockwidget.update_layer(layer_objects)


            # put current activities into comboBox
            activities = ["walking","Sitting","Standing","talking","Type01","Type02","Type03","Type04"]
            self.dockwidget.update_activity(activities)

            # put current categories into comboBox
            categories = ["Visitor","Tourists","Workers","Locals","Type01","Type02","Type03","Type04"]
            self.dockwidget.update_category(categories)

            # put current time periods into comboBox
            time_periods=["0700-0730","0730-0800","0800-0830","0830-0900","0900-0930","0930-1000",
                          "1000-1030","1030-1100","1100-1130","1130-1200","1200-1230","1230-1300",
                          "1300-1330","1330-1400","1400-1430","1430-1500","1500-1530","1530-1600",
                          "1600-1630","1630-1700","1700-1730","1730-1800","1800-1830","1830-1900"
                          "1900-1930","1930-2000","2000-2030","2030-2100"]
            self.dockwidget.update_time_period(time_periods)

            # run, update and stop button
            self.dockwidget.run_button.clicked.connect(self.draw_method)
            self.dockwidget.update_button.clicked.connect(self.update_method)
            self.dockwidget.stop_button.clicked.connect(self.stop_method)


    def draw_method(self):
        print "hello world - draw"
        self.dockwidget.add_Feature()

    def stop_method(self):
        print "hello world - stop"
        self.dockwidget.disconnect_Layer()

    def update_method(self):
        print "hello world - update"
        self.dockwidget.update_Feature()



