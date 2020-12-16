# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ptaplugin
                                 A QGIS plugin
 QGIS plugin utilizing the pta intelligent search api
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-11-12
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Spatineo
        email                : patrick.alaspaa@spatineo.com
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
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QListWidgetItem
from qgis.server import *
from qgis.core import QgsVectorLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .ptaplugin_dialog import ptapluginDialog
import os.path
import requests
import urllib
from xml.etree import ElementTree
from owslib.wms import WebMapService
from owslib.wfs import WebFeatureService
from owslib.wmts import WebMapTileService
from .requestHandler import SearchPTA, getCapabilities, getWFSFeature, getWMSFeature, listServiceContent, LOG
from .LayerMeta import LayerMeta


class ptaplugin:
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
            'ptaplugin_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&intelligent-search-plugin')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

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
        return QCoreApplication.translate('ptaplugin', message)


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
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ptaplugin/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'pta search'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def addWFS(self, layerMeta):
        crs = getCRS()
        LOG(layerMeta.serviceIndex)
        vlayer = getWFSFeature(layerMeta, self.services[layerMeta.serviceIndex], crs)
        if vlayer.isValid:
            QgsProject.instance().addMapLayer(vlayer)

    def addWMS(self, layerMeta):
        crs = getCRS()
        rlayer = getWMSFeature(layerMeta, self.services[layerMeta.serviceIndex], crs)
        if rlayer.isValid:
            QgsProject.instance().addMapLayer(rlayer)

    def getCRS():
        crs = "EPSG:3067"
        activeLayer =  self.iface.activeLayer()
        if activeLayer:
            if activeLayer.crs().authid():
                crs = self.iface.activeLayer().crs().authid()
        return crs


    def searchApi(self):
        """Send request to pta search API and return results."""
        #getWMSFeature("", "", "")
        self.dlg.searchResult.clear()
        text = self.dlg.searchBox.text()
        if(text and text.strip()):
            #TODO: Do something with language
            hits = SearchPTA(text, "FI")
            if hits:
                self.addResults(hits)
                self.dlg.searchResult.itemClicked.connect(self.searchResultClicked)




    def addResults(self, hits):
        for hit in hits:
            for link in hit.get("downloadLinks"):
                title = self.getTitleFromHit(hit)
                if title:
                    item = QListWidgetItem()
                    item.setText(title)
                    item.setData(1, hit)
                    self.dlg.searchResult.addItem(item)

    def getTitleFromHit(self, hit):
        title = ""
        for text in hit.get("text"):
            if text.get("lang") == "FI":
                title = text.get("title")
        return title


    def searchResultClicked(self, item):
        self.dlg.abstractBox.clear()
        self.dlg.searchResult2.clear()
        self.dlg.abstractLabel.clear()
        self.services = []
        self.urls = []

        data = item.data(1)
        for text in data.get("text"):
            #TODO: Do something better with language
            lang = text.get("lang")
            if lang == "FI":
                self.dlg.abstractBox.setText(text.get("title"))
                self.dlg.abstractBox.setText(text.get("abstractText"))

        links = data.get("downloadLinks")
        if links:
            for link in links:
                url = link.get("url")
                if "?" in url:
                    url = url.split("?")[0]
                self.urls.append(url)
                self.services.append(self.getCapabilities(url))

        #self.service = getCapabilities(item.data(1))
        #Add handling for wms and wmts. Try to make code more reusable
        itemList = []
        for index, service in enumerate(self.services):
            items = listServiceContent(index, service, self.urls[index])
            itemList = itemList + items

        for item in itemList:
            self.dlg.searchResult2.addItem(item)
        self.dlg.searchResult2.itemClicked.connect(self.layerClicked)

    def getCapabilities(self, url):
        if url.endswith("wms"):
            return WebMapService(url)
        elif url.endswith("wfs"):
            return WebFeatureService(url, version='1.1.0')
        elif url.endswith("wmts"):
            return WebMapTileService(url)

    def layerClicked(self, item):
        LOG("Layer was clicked")
        LOG(str(item))
        layerMeta = item.data(1)
        serviceType = self.services[layerMeta.serviceIndex].identification.type
        if "wfs" in serviceType.lower():
            self.addWFS(layerMeta)
        elif "wms" in serviceType.lower():
            self.addWMS(layerMeta)

        #pass

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&intelligent-search-plugin'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ptapluginDialog()
            self.dlg.searchButton.clicked.connect(self.searchApi)

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass
