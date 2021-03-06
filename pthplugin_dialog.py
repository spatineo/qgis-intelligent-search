# -*- coding: utf-8 -*-
"""
/***************************************************************************
 pthpluginDialog
                                 A QGIS plugin
 QGIS plugin utilizing the pth intelligent search api
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

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5 import QtCore, QtGui


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'pthplugin_dialog_base.ui'))


class pthpluginDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(pthpluginDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.resizeElements()
        #self.resizeEvent(self.resizeElements())

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        self.resizeElements()

    def resizeElements(self):
        self.setSearchBoxSize()
        self.setLayerTreeSize()
        self.setSearchResultSize()
        self.setAbstractBoxSize()
        self.setAbstractLabel()
        self.setSearchButton()
        self.setAddLayerButton()
        self.setServiceLabel()
        self.setSearchResultLabel()

    def setSearchBoxSize(self):
        #searchBox
        height = float(self.height()) * 0.05
        width = float(self.width()) * 0.4
        self.searchBox.resize(width, height)
        posX = int(float(self.width()) * 0.05)
        posY = int(float(self.height()) * 0.05)
        self.searchBox.move(posX, posY)

    def setSearchResultSize(self):
        #searchResult
        height = float(self.height()) * 0.35
        width = float(self.width()) * 0.4
        self.searchResult.resize(width, height)
        posX = int(float(self.width()) * 0.05)
        posY = int(float(self.height()) * 0.17)
        self.searchResult.move(posX, posY)

    def setLayerTreeSize(self):
        #layerTree
        height = float(self.height()) * 0.72
        width = float(self.width()) * 0.45
        self.layerTree.resize(width, height)
        posX = int(float(self.width()) * 0.5)
        posY = int(float(self.height()) * 0.17)
        self.layerTree.move(posX, posY)

    def setAbstractBoxSize(self):
        #abstractBox
        height = float(self.height()) * 0.4
        width = float(self.width()) * 0.4
        self.abstractBox.resize(width, height)
        posX = int(float(self.width()) * 0.05)
        posY = int(float(self.height()) * 0.55)
        self.abstractBox.move(posX, posY)

    def setAbstractLabel(self):
        #abstractLabel
        height = float(self.height()) * 0.1
        width = float(self.width()) * 0.4
        self.abstractLabel.resize(width, height)
        posX = int(float(self.width()) * 0.05)
        posY = int(float(self.height()) * 0.48)
        self.abstractLabel.move(posX, posY)

    def setSearchButton(self):
        #searchButton
        height = float(self.height()) * 0.05
        width = float(self.width()) * 0.45
        self.searchButton.resize(width, height)
        posX = int(float(self.width()) * 0.50)
        posY = int(float(self.height()) * 0.05)
        self.searchButton.move(posX, posY)

    def setAddLayerButton(self):
        #AddLayerButton
        height = float(self.height()) * 0.05
        width = float(self.width()) * 0.45
        self.AddLayerButton.resize(width, height)
        posX = int(float(self.width()) * 0.50)
        posY = int(float(self.height()) * 0.90)
        self.AddLayerButton.move(posX, posY)

    def setSearchResultLabel(self):
        #searchResultLabel
        height = float(self.height()) * 0.05
        width = float(self.width()) * 0.4
        self.searchResultLabel.resize(width, height)
        posX = int(float(self.width()) * 0.05)
        posY = int(float(self.height()) * 0.11)
        self.searchResultLabel.move(posX, posY)

    def setServiceLabel(self):
        #serviceLabel
        height = float(self.height()) * 0.05
        width = float(self.width()) * 0.4
        self.serviceLabel.resize(width, height)
        posX = int(float(self.width()) * 0.5)
        posY = int(float(self.height()) * 0.11)
        self.serviceLabel.move(posX, posY)
